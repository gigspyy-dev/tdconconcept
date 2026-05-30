from datetime import datetime, timedelta
from backend.models import Ticket, Rep, ChannelEnum, StatusEnum, PriorityEnum


def get_mock_tickets() -> list[Ticket]:
    base_time = datetime.now()

    return [
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
        ),
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
            status=StatusEnum.open,
        ),
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
        ),
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
        ),
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
        ),
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
            status=StatusEnum.open,
        ),
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
            status=StatusEnum.open,
        ),
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
        ),
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
        ),
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
        ),
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
