from datetime import datetime, timedelta

def filter_live_hackathons(hackathons):
    """
    Filter to show ONLY LIVE hackathons
    Remove all upcoming and closed ones
    """
    live_hackathons = []
    
    for hack in hackathons:
        status = hack.get('status', '').lower()
        
        # Only keep if status is explicitly LIVE
        if status in ['live', 'open', 'active', 'ongoing', 'coding']:
            hack['status'] = 'Live'  # Standardize to 'Live'
            live_hackathons.append(hack)
        # Skip upcoming and closed
        elif status in ['upcoming', 'closed', 'ended', 'finished', 'completed', 'before']:
            continue
        # If no status, check platform defaults
        elif not status:
            # These platforms usually have live content
            if hack.get('platform') in ['GitHub', 'Unstop']:
                hack['status'] = 'Live'
                live_hackathons.append(hack)
            else:
                # Skip if unknown status
                continue
    
    return live_hackathons

def filter_upcoming_hackathons(hackathons):
    """Get only upcoming hackathons"""
    return [h for h in hackathons if h.get('status', '').lower() in ['upcoming', 'before']]

def filter_fresher_friendly(hackathons):
    """Filter only fresher-friendly hackathons"""
    return [h for h in hackathons if h.get('fresher_friendly', True)]

def filter_by_platform(hackathons, platforms):
    """Filter hackathons by specific platforms"""
    if not platforms:
        return hackathons
    return [h for h in hackathons if h.get('platform', '') in platforms]

def filter_by_mode(hackathons, mode):
    """Filter hackathons by mode (Online/Offline/Hybrid)"""
    if not mode:
        return hackathons
    return [h for h in hackathons if h.get('mode', '').lower() == mode.lower()]

def remove_duplicates(hackathons):
    """Remove duplicate hackathons based on name and link"""
    seen = set()
    unique = []
    
    for hack in hackathons:
        # Create unique key
        key = f"{hack.get('name', '')}||{hack.get('registration_link', '')}"
        if key not in seen:
            seen.add(key)
            unique.append(hack)
    
    return unique

def sort_hackathons(hackathons, sort_by='name'):
    """Sort hackathons by specified field"""
    if sort_by == 'platform':
        return sorted(hackathons, key=lambda x: x.get('platform', ''))
    elif sort_by == 'status':
        return sorted(hackathons, key=lambda x: x.get('status', ''))
    elif sort_by == 'prize':
        return sorted(hackathons, key=lambda x: x.get('prize_pool', ''), reverse=True)
    else:
        return sorted(hackathons, key=lambda x: x.get('name', ''))

def apply_all_filters(hackathons, live_only=True, fresher_only=False, remove_dupes=True):
    """Apply all filters at once"""
    filtered = hackathons
    
    # First remove duplicates
    if remove_dupes:
        filtered = remove_duplicates(filtered)
    
    # Then filter by status (LIVE only)
    if live_only:
        filtered = filter_live_hackathons(filtered)
    
    # Then filter by fresher friendly
    if fresher_only:
        filtered = filter_fresher_friendly(filtered)
    
    # Sort by platform for better organization
    filtered = sort_hackathons(filtered, sort_by='platform')
    
    return filtered

def get_statistics(hackathons):
    """Get statistics about hackathons"""
    stats = {
        'total': len(hackathons),
        'live': len([h for h in hackathons if h.get('status', '').lower() == 'live']),
        'upcoming': len([h for h in hackathons if h.get('status', '').lower() == 'upcoming']),
        'platforms': len(set(h.get('platform', '') for h in hackathons)),
        'fresher_friendly': len([h for h in hackathons if h.get('fresher_friendly', False)]),
        'online': len([h for h in hackathons if h.get('mode', '').lower() == 'online']),
        'offline': len([h for h in hackathons if h.get('mode', '').lower() == 'offline']),
        'hybrid': len([h for h in hackathons if h.get('mode', '').lower() == 'hybrid'])
    }
    
    # Platform breakdown
    platform_counts = {}
    for hack in hackathons:
        platform = hack.get('platform', 'Unknown')
        platform_counts[platform] = platform_counts.get(platform, 0) + 1
    
    stats['by_platform'] = platform_counts
    
    return stats