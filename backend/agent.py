import os
import json
from anthropic import Anthropic
from backend.models import Ticket, AgentResult, CategoryEnum, PriorityEnum

SYSTEM_PROMPT = """You are the AI backbone of Thrudark's customer experience platform.

Thrudark is a UK high-performance outerwear brand with special forces heritage. Every
piece of kit is built to perform in the harshest conditions. Our customers range from
military veterans and professional guides to serious amateur mountaineers and outdoor
enthusiasts who demand the best.

Brand voice: Professional, direct, trusted. Replies should be confident and warm —
never fluffy or corporate. Action-oriented. We back our kit and our customers.

Your job is to process incoming customer tickets by:
1. Classifying the ticket into the correct category
2. Assessing priority based on urgency and customer sentiment
3. Detecting if the ticket needs escalation to a senior rep
4. Drafting a reply in the Thrudark voice
5. Assigning to the appropriate rep

Work through all steps systematically using the tools provided."""

TOOLS = [
    {
        "name": "classify_ticket",
        "description": "Classify the ticket into the appropriate category",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": [
                        "order_status", "return_exchange", "product_query",
                        "complaint", "feedback", "warranty", "shipping_issue", "other"
                    ],
                    "description": "The category that best fits this ticket"
                },
                "reasoning": {
                    "type": "string",
                    "description": "Brief explanation of why this category was chosen"
                }
            },
            "required": ["category", "reasoning"]
        }
    },
    {
        "name": "assess_priority",
        "description": "Assess the priority level of this ticket",
        "input_schema": {
            "type": "object",
            "properties": {
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "urgent"],
                    "description": "Priority level: urgent=escalation/furious customer/missing order >7 days, high=returns/shipping/warranty, medium=product questions/sizing, low=feedback/positive reviews"
                },
                "reasoning": {
                    "type": "string",
                    "description": "Brief explanation of the priority assessment"
                }
            },
            "required": ["priority", "reasoning"]
        }
    },
    {
        "name": "detect_escalation",
        "description": "Determine if this ticket requires escalation to a senior rep or management",
        "input_schema": {
            "type": "object",
            "properties": {
                "escalation_flag": {
                    "type": "boolean",
                    "description": "True if this ticket should be escalated"
                },
                "escalation_reason": {
                    "type": "string",
                    "description": "If escalation_flag is true, explain why. Otherwise null or empty string."
                }
            },
            "required": ["escalation_flag", "escalation_reason"]
        }
    },
    {
        "name": "assign_to_rep",
        "description": "Assign the ticket to the appropriate customer service rep",
        "input_schema": {
            "type": "object",
            "properties": {
                "rep_id": {
                    "type": "string",
                    "description": "rep1 (Sarah) handles orders/shipping. rep2 (James) handles product queries. Complaints/escalations go to whoever has fewer active tickets — if unknown, assign to rep1."
                },
                "reasoning": {
                    "type": "string",
                    "description": "Brief explanation of the assignment"
                }
            },
            "required": ["rep_id", "reasoning"]
        }
    },
    {
        "name": "draft_reply",
        "description": "Draft a customer reply in the Thrudark brand voice",
        "input_schema": {
            "type": "object",
            "properties": {
                "reply": {
                    "type": "string",
                    "description": "The draft reply. 150-250 words. Address the customer by first name. Reference Thrudark's commitment to quality and service. Give a concrete next step. Sign off as 'The Thrudark Customer Experience Team'. Tone: professional, direct, warm but not fluffy, action-oriented."
                },
                "confidence_score": {
                    "type": "number",
                    "description": "Confidence in the draft reply quality, 0.0 to 1.0"
                }
            },
            "required": ["reply", "confidence_score"]
        }
    }
]


def process_ticket(ticket: Ticket, rep_active_counts: dict[str, int]) -> AgentResult:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY is not set. Please add it to your .env file or environment."
        )

    client = Anthropic(api_key=api_key)

    rep_context = (
        f"Current rep workloads — Sarah (rep1): {rep_active_counts.get('rep1', 0)} active tickets, "
        f"James (rep2): {rep_active_counts.get('rep2', 0)} active tickets."
    )

    user_message = (
        f"Process this customer ticket:\n\n"
        f"Subject: {ticket.subject}\n\n"
        f"Message:\n{ticket.body}\n\n"
        f"Channel: {ticket.channel.value}\n"
        f"Customer: {ticket.customer_name} ({ticket.customer_email})\n\n"
        f"{rep_context}\n\n"
        f"Use all available tools to classify, assess priority, check for escalation, "
        f"assign to a rep, and draft a reply."
    )

    messages = [{"role": "user", "content": user_message}]

    # Agentic loop — keep going until no more tool calls
    collected = {
        "category": None,
        "priority": None,
        "escalation_flag": False,
        "escalation_reason": None,
        "assigned_to": None,
        "draft_reply": None,
        "confidence_score": 0.8,
    }

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        # Collect any tool calls from this response
        tool_calls_made = []
        for block in response.content:
            if block.type == "tool_use":
                tool_calls_made.append(block)
                _apply_tool_result(collected, block.name, block.input)

        # If no tool calls or stop_reason is end_turn, we're done
        if not tool_calls_made or response.stop_reason == "end_turn":
            break

        # Build tool results and continue the conversation
        tool_results = [
            {
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": json.dumps({"status": "ok", "input": tc.input}),
            }
            for tc in tool_calls_made
        ]

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

        # If stop_reason is end_turn after adding results, break
        if response.stop_reason == "end_turn":
            break

    # Fallbacks if agent missed any step
    if not collected["category"]:
        collected["category"] = "other"
    if not collected["priority"]:
        collected["priority"] = "medium"
    if not collected["draft_reply"]:
        collected["draft_reply"] = "Thank you for contacting Thrudark. We have received your message and will be in touch shortly."

    return AgentResult(
        ticket_id=ticket.id,
        category=CategoryEnum(collected["category"]),
        priority=PriorityEnum(collected["priority"]),
        assigned_to=collected["assigned_to"],
        escalation_flag=collected["escalation_flag"],
        escalation_reason=collected["escalation_reason"],
        draft_reply=collected["draft_reply"],
        confidence_score=collected["confidence_score"],
    )


def _apply_tool_result(collected: dict, tool_name: str, tool_input: dict) -> None:
    if tool_name == "classify_ticket":
        collected["category"] = tool_input.get("category")
    elif tool_name == "assess_priority":
        collected["priority"] = tool_input.get("priority")
    elif tool_name == "detect_escalation":
        collected["escalation_flag"] = tool_input.get("escalation_flag", False)
        reason = tool_input.get("escalation_reason", "")
        collected["escalation_reason"] = reason if reason else None
    elif tool_name == "assign_to_rep":
        collected["assigned_to"] = tool_input.get("rep_id")
    elif tool_name == "draft_reply":
        collected["draft_reply"] = tool_input.get("reply")
        collected["confidence_score"] = tool_input.get("confidence_score", 0.8)
