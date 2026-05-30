from datetime import datetime, timedelta
from backend.models import Ticket, Rep, ChannelEnum, StatusEnum, PriorityEnum


def get_mock_tickets() -> list[Ticket]:
    base_time = datetime.now()

    return [
        # ── Pre-processed: urgent escalation ─────────────────────────────────
        Ticket(
            id="TKT-004",
            subject="COMPLETELY UNACCEPTABLE SERVICE - 3rd attempt to contact",
            body=(
                "This is my THIRD attempt to contact your company about this matter. "
                "I have sent two previous emails that have been completely ignored. "
                "I purchased the Thrudark Stealth Hardshell jacket six weeks ago for "
                "£380 and the waterproofing has already failed entirely. The jacket soaks "
                "through in light rain. For a brand that prides itself on military-grade "
                "quality, this is absolutely disgraceful. I expect a full refund or "
                "replacement IMMEDIATELY. If I don't hear back today I will be escalating "
                "this to Trading Standards and posting my experience across all social "
                "media platforms.\n\nFurious,\nRobert Thornton"
            ),
            customer_name="Robert Thornton",
            customer_email="r.thornton@business.co.uk",
            channel=ChannelEnum.email,
            created_at=base_time - timedelta(hours=1),
            status=StatusEnum.open,
            priority=PriorityEnum.urgent,
            category="complaint",
            assigned_to="rep1",
            escalation_flag=True,
            escalation_reason=(
                "Customer explicitly states this is their third contact attempt with no "
                "response. Threatening Trading Standards referral and public social media "
                "posts. Warranty failure on a £380 product. Requires immediate response."
            ),
            draft_reply=(
                "Dear Robert,\n\n"
                "I want to personally apologise for the experience you've had — both with "
                "the jacket's performance and with our response time. Three unanswered "
                "contacts is not the standard we hold ourselves to, and I understand "
                "completely why you're frustrated.\n\n"
                "The waterproofing failure you've described on a six-week-old Stealth "
                "Hardshell is not acceptable. Our garments are built to perform in the "
                "conditions our heritage demands, and yours has clearly fallen short of "
                "that. We will make this right.\n\n"
                "I'm raising a priority replacement order for you immediately. You'll "
                "receive a prepaid returns label by email within the hour, and your "
                "replacement jacket will be dispatched on an overnight courier the moment "
                "we receive the return — or sooner if you'd prefer us to send first.\n\n"
                "I'll be personally monitoring this case to ensure it is resolved to your "
                "satisfaction. Please reply directly to this email if you have any "
                "questions in the meantime.\n\n"
                "The Thrudark Customer Experience Team"
            ),
        ),
        # ── Pre-processed: high priority missing parcel ───────────────────────
        Ticket(
            id="TKT-007",
            subject="Parcel hasn't arrived - shows delivered but nothing received",
            body=(
                "Good morning,\n\nMy order TD-52107 was marked as delivered three days "
                "ago but I haven't received anything. I was home all day on the supposed "
                "delivery date. There's no parcel in my building's post room either and "
                "none of my neighbours have taken it in. The courier's tracking just says "
                "'delivered - signed for' but I definitely didn't sign for anything. "
                "I'm quite worried about this - it was over £200 of gear. Can you help "
                "track this down?\n\nThanks,\nJames"
            ),
            customer_name="James Okafor",
            customer_email="j.okafor@techcorp.io",
            channel=ChannelEnum.ticket,
            created_at=base_time - timedelta(hours=3),
            status=StatusEnum.in_progress,
            priority=PriorityEnum.high,
            category="shipping_issue",
            assigned_to="rep1",
            escalation_flag=False,
            draft_reply=(
                "Dear James,\n\n"
                "Thank you for getting in touch. I'm sorry to hear your order hasn't "
                "reached you — a 'delivered' scan with no parcel in hand is a frustrating "
                "situation, and we'll get to the bottom of it.\n\n"
                "I've raised an investigation with our courier on order TD-52107. They "
                "are required to provide GPS delivery confirmation and a photo of the "
                "signature within 24 hours. I'll share their response with you the "
                "moment I have it.\n\n"
                "In the meantime, I want to reassure you: if the courier cannot "
                "satisfactorily confirm delivery to you personally, we will dispatch a "
                "replacement order at no cost. You shouldn't be out of pocket because "
                "of a courier error.\n\n"
                "I'll be in touch by tomorrow morning at the latest with an update.\n\n"
                "The Thrudark Customer Experience Team"
            ),
        ),
        # ── Pre-processed: high priority wrong item ───────────────────────────
        Ticket(
            id="TKT-011",
            subject="Wrong item sent in my order",
            body=(
                "Hi,\n\nI received my order TD-51876 today but it contains the wrong "
                "item. I ordered the Aegis Softshell in Olive/Medium but received a "
                "Recon Fleece in Black/Large. I'm guessing there's been a packing error. "
                "I need the correct item as soon as possible as I have a trip in "
                "two weeks. What's the quickest way to resolve this? Happy to send "
                "the wrong item back.\n\nThanks,\nBen"
            ),
            customer_name="Ben Ashworth",
            customer_email="ben.ashworth@outlook.com",
            channel=ChannelEnum.ticket,
            created_at=base_time - timedelta(hours=4),
            status=StatusEnum.open,
            priority=PriorityEnum.high,
            category="return_exchange",
            assigned_to="rep1",
            escalation_flag=False,
            draft_reply=(
                "Dear Ben,\n\n"
                "Thank you for letting us know — that's clearly a packing error on our "
                "end and I apologise for the inconvenience. With a trip in two weeks, "
                "I want to get the right kit to you as quickly as possible.\n\n"
                "I've reserved the Aegis Softshell in Olive/Medium and will dispatch it "
                "on a next-day courier today. You'll receive a tracking notification "
                "by this evening.\n\n"
                "For the Recon Fleece, I'll include a prepaid returns label in a "
                "follow-up email — please just drop it back whenever is convenient, "
                "there's no rush on your end.\n\n"
                "Enjoy the trip.\n\n"
                "The Thrudark Customer Experience Team"
            ),
        ),
        # ── Pre-processed: high priority warranty ─────────────────────────────
        Ticket(
            id="TKT-005",
            subject="Zip broken after only 2 months of use",
            body=(
                "Hi,\n\nI've had my Thrudark Recon Midlayer for about two months now "
                "and the main zip has stopped working properly. The zip slides but the "
                "teeth don't engage properly and it keeps coming undone. I've used this "
                "jacket on maybe 8-10 occasions. I wouldn't normally expect this kind "
                "of failure on premium outdoor gear. Is this covered under warranty? "
                "Order reference: TD-47883.\n\nRegards,\nSophie"
            ),
            customer_name="Sophie Laurent",
            customer_email="sophie.l@gmail.com",
            channel=ChannelEnum.ticket,
            created_at=base_time - timedelta(hours=14),
            status=StatusEnum.open,
            priority=PriorityEnum.high,
            category="warranty",
            assigned_to="rep1",
            escalation_flag=False,
            draft_reply=(
                "Dear Sophie,\n\n"
                "Thank you for getting in touch, and I'm sorry to hear about the zip "
                "issue on your Recon Midlayer. A zip failure after eight to ten wears "
                "is not the standard we expect, and this is absolutely covered under "
                "our warranty.\n\n"
                "To assess the fault, could you send two or three clear photos of the "
                "zip and teeth to this email address? Once we've confirmed the defect, "
                "we'll arrange a free repair or direct replacement — whichever is "
                "quicker for you.\n\n"
                "Given order reference TD-47883, the jacket is well within the warranty "
                "window and you won't need to do anything else beyond sending those "
                "photos.\n\n"
                "The Thrudark Customer Experience Team"
            ),
        ),
        # ── Pre-processed: high priority order cancellation ───────────────────
        Ticket(
            id="TKT-009",
            subject="Order cancelled without explanation - extremely disappointed",
            body=(
                "I placed an order four days ago (TD-53812) and just received an email "
                "saying it's been cancelled. No reason was given. I was planning to give "
                "this as a birthday gift and the birthday is next week. I've tried calling "
                "but can't get through. This is incredibly poor customer service for a "
                "premium brand. I want to know why my order was cancelled and I want it "
                "reinstated or an explanation given immediately. Very disappointed in "
                "Thrudark.\n\nAngrily,\nHenry"
            ),
            customer_name="Henry Blackwood",
            customer_email="h.blackwood@email.com",
            channel=ChannelEnum.ticket,
            created_at=base_time - timedelta(hours=6),
            status=StatusEnum.open,
            priority=PriorityEnum.high,
            category="complaint",
            assigned_to="rep1",
            escalation_flag=True,
            escalation_reason=(
                "Order cancelled without explanation ahead of a time-sensitive birthday "
                "gift. Customer unable to reach support by phone. High risk of churn and "
                "reputational damage if not resolved before the birthday date."
            ),
            draft_reply=(
                "Dear Henry,\n\n"
                "I completely understand your frustration, and I apologise that your "
                "order was cancelled without any explanation — that's not acceptable, "
                "particularly when you have a deadline to meet.\n\n"
                "I've looked into order TD-53812. It appears the cancellation was "
                "triggered by an automated payment security flag, which can occasionally "
                "catch legitimate orders. Your payment has not been taken.\n\n"
                "I've manually cleared the flag and can reinstate your order right now "
                "with priority dispatch to ensure delivery before the birthday — please "
                "just confirm your delivery address in reply and I'll get it moving "
                "within the hour.\n\n"
                "Again, I apologise for the stress this has caused. We'll get it sorted.\n\n"
                "The Thrudark Customer Experience Team"
            ),
        ),
        # ── Pre-processed: medium order status ────────────────────────────────
        Ticket(
            id="TKT-001",
            subject="Where is my order? It's been 10 days",
            body=(
                "Hi,\n\nI placed an order for the Thrudark Aegis Softshell jacket "
                "10 days ago (order #TD-48291) and it still hasn't arrived. The tracking "
                "number shows it left the warehouse but hasn't updated since. I need this "
                "for a hiking trip in Scotland next weekend. Can you please investigate?\n\n"
                "Thanks,\nMarcus"
            ),
            customer_name="Marcus Webb",
            customer_email="marcus.webb@email.com",
            channel=ChannelEnum.email,
            created_at=base_time - timedelta(hours=2),
            status=StatusEnum.open,
            priority=PriorityEnum.high,
            category="order_status",
            assigned_to="rep1",
            escalation_flag=False,
            draft_reply=(
                "Dear Marcus,\n\n"
                "Thank you for reaching out. Ten days with a stalled tracking update "
                "is frustrating, especially with a trip on the horizon — I'll get "
                "on this straight away.\n\n"
                "I've contacted our courier to request a trace on order TD-48291. "
                "In parallel, I've put a replacement Aegis Softshell on reserve so "
                "that if the investigation isn't resolved within 24 hours, I can "
                "dispatch it immediately on an overnight service to ensure it reaches "
                "you ahead of your Scotland trip.\n\n"
                "I'll update you by tomorrow morning with either a confirmed delivery "
                "window or confirmation that the replacement is on its way.\n\n"
                "The Thrudark Customer Experience Team"
            ),
        ),
        # ── Pre-processed: medium return/exchange ─────────────────────────────
        Ticket(
            id="TKT-002",
            subject="Want to return my jacket - wrong size",
            body=(
                "Hello,\n\nI ordered the Thrudark Recon Fleece in size Large but it runs "
                "quite small and doesn't fit properly. I'd like to return it and exchange "
                "for an XL. The item is unused and still has all original tags attached. "
                "Order number: TD-51034. What's the process for this?\n\nBest,\nPriya"
            ),
            customer_name="Priya Sharma",
            customer_email="priya.sharma@outlook.com",
            channel=ChannelEnum.ticket,
            created_at=base_time - timedelta(hours=5),
            status=StatusEnum.in_progress,
            priority=PriorityEnum.medium,
            category="return_exchange",
            assigned_to="rep1",
            escalation_flag=False,
            draft_reply=(
                "Dear Priya,\n\n"
                "Not a problem at all — sizing exchanges are straightforward with us. "
                "The Recon Fleece does run slightly narrow in the body so you're not "
                "alone in going up a size.\n\n"
                "I've checked stock and the XL is available. I'll reserve one for you "
                "now. Please use the prepaid returns label attached to this email to "
                "send back the Large — once our warehouse scans it in, the XL will "
                "ship the same day.\n\n"
                "Typical turnaround is three to four working days from us receiving "
                "the return. If you'd prefer we send the XL immediately and you return "
                "the Large within 14 days, just say the word and I'll arrange that.\n\n"
                "The Thrudark Customer Experience Team"
            ),
        ),
        # ── Pre-processed: medium product query ───────────────────────────────
        Ticket(
            id="TKT-003",
            subject="Which base layer is best for Scottish winter mountaineering?",
            body=(
                "Hi there,\n\nI'm planning a winter mountaineering trip to the Cairngorms "
                "in January and I'm looking for a base layer that can handle serious cold "
                "and wet conditions. I'll be doing multi-day expeditions with heavy packs. "
                "Which Thrudark base layer would you recommend? I run warm normally but "
                "these will be challenging conditions. Budget isn't a concern - I want "
                "the best.\n\nCheers,\nDuncan"
            ),
            customer_name="Duncan MacPherson",
            customer_email="d.macpherson@highland.net",
            channel=ChannelEnum.email,
            created_at=base_time - timedelta(hours=8),
            status=StatusEnum.open,
            priority=PriorityEnum.medium,
            category="product_query",
            assigned_to="rep2",
            escalation_flag=False,
            draft_reply=(
                "Dear Duncan,\n\n"
                "The Cairngorms in January — excellent choice of testing ground. "
                "For the conditions you're describing, here's our honest recommendation.\n\n"
                "The Recon Merino Heavyweight is your best base layer for multi-day "
                "winter expeditions. At 260gsm, it provides serious thermal output "
                "while managing moisture effectively during hard efforts. Because you "
                "run warm, you'll benefit from its moisture-wicking capability on the "
                "ascent without losing warmth on exposed ridges.\n\n"
                "Paired with the Vanguard Midlayer and the Stealth Hardshell, you'll "
                "have a system that has been tested in conditions as demanding as "
                "anything the Cairngorms will throw at you in January.\n\n"
                "If you want to discuss the full layering system before ordering, "
                "I'm happy to go into more detail — just reply here.\n\n"
                "The Thrudark Customer Experience Team"
            ),
        ),
        # ── Pre-processed: resolved positive feedback ─────────────────────────
        Ticket(
            id="TKT-006",
            subject="Just wanted to say - best outdoor gear I've ever owned",
            body=(
                "Hi Thrudark team,\n\nI just wanted to drop you a note to say how "
                "impressed I am with my recent purchases. I bought the Aegis jacket and "
                "Vanguard trousers three months ago and they've been absolutely brilliant. "
                "Used them in some genuinely horrible conditions on the Brecon Beacons "
                "and they performed flawlessly. The build quality is exceptional and you "
                "can tell real thought has gone into the design. I've already recommended "
                "Thrudark to several friends in my hiking group. Keep up the excellent "
                "work!\n\nBest wishes,\nCaroline"
            ),
            customer_name="Caroline Hughes",
            customer_email="caroline.h@webmail.com",
            channel=ChannelEnum.email,
            created_at=base_time - timedelta(hours=20),
            status=StatusEnum.resolved,
            priority=PriorityEnum.low,
            category="feedback",
            assigned_to="rep2",
            escalation_flag=False,
            draft_reply=(
                "Dear Caroline,\n\n"
                "Thank you — messages like yours mean a great deal to the whole team. "
                "The Brecon Beacons in genuinely horrible conditions is exactly the "
                "proving ground our kit is built for, and it's good to hear the Aegis "
                "and Vanguard delivered.\n\n"
                "We'll pass your feedback on to the design team — they take direct "
                "field reports seriously and your comments will be read.\n\n"
                "Thank you for recommending us to your group, and we look forward to "
                "equipping you on the next one.\n\n"
                "The Thrudark Customer Experience Team"
            ),
        ),
        # ── Pre-processed: medium sizing query ────────────────────────────────
        Ticket(
            id="TKT-010",
            subject="Sizing question - between sizes on the Vanguard jacket",
            body=(
                "Hello,\n\nI'm trying to decide between Medium and Large for the Vanguard "
                "hardshell jacket. I'm 5'11\", 80kg, with a 40\" chest. I'll be wearing "
                "it over a midlayer and base layer for winter use. I prefer a more "
                "athletic fit but obviously need room for layering. What would you "
                "recommend? Also, does the cut allow for good arm movement when climbing "
                "or scrambling?\n\nMany thanks,\nAlicia"
            ),
            customer_name="Alicia Torres",
            customer_email="alicia.torres@gmail.com",
            channel=ChannelEnum.email,
            created_at=base_time - timedelta(hours=45),
            status=StatusEnum.open,
            priority=PriorityEnum.medium,
            category="product_query",
            assigned_to="rep2",
            escalation_flag=False,
            draft_reply=(
                "Dear Alicia,\n\n"
                "At 5'11\", 80kg with a 40\" chest and planning to layer underneath, "
                "I'd recommend the Large without hesitation.\n\n"
                "The Vanguard is cut with an athletic profile, so the Large will sit "
                "close to the body rather than boxy — you won't lose the fit you're "
                "after. The Medium would be limiting once you add a midlayer, "
                "particularly across the shoulders and chest, and would restrict arm "
                "movement on technical terrain.\n\n"
                "On mobility: the Vanguard uses articulated patterning specifically "
                "for climbing and scrambling applications. The Large will give you "
                "full range of motion with arms overhead — this was a design priority "
                "from the beginning.\n\n"
                "If for any reason the fit isn't right when it arrives, our exchange "
                "process is simple and free.\n\n"
                "The Thrudark Customer Experience Team"
            ),
        ),
        # ── Pre-processed: low positive feedback ─────────────────────────────
        Ticket(
            id="TKT-012",
            subject="Absolutely love the new Operator series - incredible kit",
            body=(
                "Just had to write in about the new Operator series. I served for 12 "
                "years and I've used military-issued kit in some genuinely tough conditions. "
                "The Thrudark Operator jacket is hands down the best piece of civilian "
                "outdoor kit I've ever worn - it feels like the real thing but actually "
                "better in several ways. The pocket configuration is brilliant. Just "
                "ordered a second one in different colour. You should be very proud "
                "of what you've built here. Proper kit for proper people.\n\nWith "
                "respect,\nSergeant (Ret.) Tom Gallagher"
            ),
            customer_name="Tom Gallagher",
            customer_email="t.gallagher@veterans.org.uk",
            channel=ChannelEnum.email,
            created_at=base_time - timedelta(hours=48),
            status=StatusEnum.resolved,
            priority=PriorityEnum.low,
            category="feedback",
            assigned_to="rep2",
            escalation_flag=False,
            draft_reply=(
                "Dear Tom,\n\n"
                "That means a great deal — genuinely. The founders' background is the "
                "reason this company exists, and hearing from someone with your "
                "experience that the Operator jacket stands up to that standard is "
                "exactly the validation we build toward.\n\n"
                "We'll make sure your feedback reaches the product team directly. "
                "Thank you for your service, and for trusting us with your kit.\n\n"
                "The Thrudark Customer Experience Team"
            ),
        ),
        # ── Unprocessed: awaiting AI ──────────────────────────────────────────
        Ticket(
            id="TKT-008",
            subject="Are the Stealth trousers suitable for cycling as well as hiking?",
            body=(
                "Hi,\n\nI'm looking at the Thrudark Stealth trousers and wondering if "
                "they'd work well for both cycling commuting and weekend hiking. I need "
                "something versatile that looks reasonably smart but can handle getting "
                "wet on the bike. I cycle about 8 miles each way in all weathers. Do "
                "you have any customers who use them this way? Also, are the pockets "
                "secure enough for a phone while cycling?\n\nCheers,\nNatasha"
            ),
            customer_name="Natasha Brennan",
            customer_email="natasha.b@personalmail.com",
            channel=ChannelEnum.email,
            created_at=base_time - timedelta(hours=30),
            status=StatusEnum.open,
        ),
    ]


def get_mock_reps() -> list[Rep]:
    return [
        Rep(
            id="rep1",
            name="Sarah",
            email="sarah@thrudark.com",
        ),
        Rep(
            id="rep2",
            name="James",
            email="james@thrudark.com",
        ),
    ]
