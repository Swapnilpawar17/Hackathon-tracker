def get_manual_hackathons():
    """
    Manually curated LIVE hackathons - Updated February 2025
    Only includes hackathons that are currently accepting registrations
    """
    return [
        {
            'name': 'Google Solution Challenge 2025',
            'platform': 'Other',
            'organizer': 'Google Developer Student Clubs',
            'mode': 'Online',
            'registration_link': 'https://developers.google.com/community/gdsc-solution-challenge',
            'prize_pool': '$3,000 + Mentorship + Swag',
            'fresher_friendly': True,
            'status': 'Live',  # Registration open till March 2025
        },
        {
            'name': 'Microsoft Imagine Cup 2025',
            'platform': 'Other',
            'organizer': 'Microsoft',
            'mode': 'Online',
            'registration_link': 'https://imaginecup.microsoft.com/',
            'prize_pool': '$100,000 + Azure Credits + Mentorship',
            'fresher_friendly': True,
            'status': 'Live',  # Registration open
        },
        {
            'name': 'AWS DeepRacer Student League 2025',
            'platform': 'Other',
            'organizer': 'Amazon Web Services',
            'mode': 'Online',
            'registration_link': 'https://aws.amazon.com/deepracer/student/',
            'prize_pool': 'Scholarships + AWS Credits + Devices',
            'fresher_friendly': True,
            'status': 'Live',  # Open for registration
        },
        {
            'name': 'Flipkart GRiD 6.0',
            'platform': 'Other',
            'organizer': 'Flipkart',
            'mode': 'Online',
            'registration_link': 'https://unstop.com/hackathons/flipkart-grid',
            'prize_pool': '₹50,00,000 + PPO Opportunities',
            'fresher_friendly': True,
            'status': 'Live',  # Currently accepting registrations
        },
        {
            'name': 'Smart India Hackathon 2025',
            'platform': 'Other',
            'organizer': 'Government of India',
            'mode': 'Hybrid',
            'registration_link': 'https://www.sih.gov.in/',
            'prize_pool': '₹1,00,000 per winning team',
            'fresher_friendly': True,
            'status': 'Live',  # Internal hackathon registrations open
        },
        {
            'name': 'GitHub Campus Expert Program',
            'platform': 'GitHub',
            'organizer': 'GitHub Education',
            'mode': 'Online',
            'registration_link': 'https://education.github.com/experts',
            'prize_pool': 'Training + Swag + Conference Tickets',
            'fresher_friendly': True,
            'status': 'Live',  # Always open
        },
        {
            'name': 'Google Kickstart 2025',
            'platform': 'Other',
            'organizer': 'Google',
            'mode': 'Online',
            'registration_link': 'https://codingcompetitions.withgoogle.com/kickstart',
            'prize_pool': 'Google Interview Opportunity',
            'fresher_friendly': True,
            'status': 'Live',  # Registration open for rounds
        },
        {
            'name': 'Meta Hacker Cup 2025',
            'platform': 'Other',
            'organizer': 'Meta (Facebook)',
            'mode': 'Online',
            'registration_link': 'https://www.facebook.com/codingcompetitions/hacker-cup',
            'prize_pool': '$20,000 + Medals',
            'fresher_friendly': True,
            'status': 'Live',  # Qualification round open
        },
        {
            'name': 'Red Bull Basement 2025',
            'platform': 'Other',
            'organizer': 'Red Bull',
            'mode': 'Hybrid',
            'registration_link': 'https://www.redbull.com/basement',
            'prize_pool': 'Global Summit + Mentorship',
            'fresher_friendly': True,
            'status': 'Live',  # Applications open
        },
        {
            'name': 'NASA Space Apps Challenge 2025',
            'platform': 'Other',
            'organizer': 'NASA',
            'mode': 'Hybrid',
            'registration_link': 'https://www.spaceappschallenge.org/',
            'prize_pool': 'NASA Invitation + Global Recognition',
            'fresher_friendly': True,
            'status': 'Live',  # Registration for local events open
        }
    ]

def get_upcoming_hackathons():
    """
    Upcoming hackathons (NOT YET LIVE - Don't include these in LIVE filter)
    Keep for reference only
    """
    return [
        {
            'name': 'HackMIT 2025',
            'platform': 'MLH',
            'organizer': 'MIT',
            'mode': 'Hybrid',
            'registration_link': 'https://hackmit.org/',
            'fresher_friendly': True,
            'status': 'Upcoming',  # Opens in August 2025
        },
        {
            'name': 'ETHIndia 2025',
            'platform': 'Devfolio',
            'organizer': 'ETHIndia',
            'mode': 'Hybrid',
            'registration_link': 'https://ethindia.co/',
            'prize_pool': '$50,000+',
            'fresher_friendly': True,
            'status': 'Upcoming',  # Opens in October 2025
        },
        {
            'name': 'PennApps 2025',
            'platform': 'MLH',
            'organizer': 'University of Pennsylvania',
            'mode': 'Hybrid',
            'registration_link': 'https://pennapps.com/',
            'fresher_friendly': True,
            'status': 'Upcoming',  # Opens in Fall 2025
        }
    ]

# For the main scraper, only use get_manual_hackathons() which returns LIVE hackathons