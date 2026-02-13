import os
from flask import Flask, render_template_string, jsonify, request
from scrapers import HackathonScraper
from india_scrapers import IndiaHackathonScraper
from manual_sources import get_manual_hackathons
from filters import apply_all_filters, get_statistics
from datetime import datetime, timedelta
import threading
import time
import json

app = Flask(__name__)

# Store hackathons in memory
cached_hackathons = []
last_updated = None
update_history = []
platform_stats = {}

def update_hackathons():
    """Background job to update hackathons"""
    global cached_hackathons, last_updated, update_history, platform_stats
    
    while True:
        try:
            print(f"🔄 Updating hackathons at {datetime.now()}")
            
            # Scrape all sources
            hackathons = []
            
            # International platforms
            scraper = HackathonScraper()
            hackathons.extend(scraper.get_all_hackathons())
            
            # India platforms
            india_scraper = IndiaHackathonScraper()
            hackathons.extend(india_scraper.get_all_india_hackathons())
            
            # Manual sources
            hackathons.extend(get_manual_hackathons())
            
            # Apply filters - LIVE only
            hackathons = apply_all_filters(hackathons, live_only=True)
            
            # Calculate platform statistics
            platform_stats = {}
            for hack in hackathons:
                platform = hack.get('platform', 'Unknown')
                if platform not in platform_stats:
                    platform_stats[platform] = 0
                platform_stats[platform] += 1
            
            # Store update history
            update_history.append({
                'time': datetime.now().isoformat(),
                'count': len(hackathons)
            })
            
            # Keep only last 10 updates
            if len(update_history) > 10:
                update_history = update_history[-10:]
            
            cached_hackathons = hackathons
            last_updated = datetime.now()
            
            print(f"✅ Updated: {len(hackathons)} live hackathons found")
            
        except Exception as e:
            print(f"❌ Update error: {e}")
        
        # Wait 6 hours before next update
        time.sleep(21600)

# Start background thread
update_thread = threading.Thread(target=update_hackathons, daemon=True)
update_thread.start()

# Professional Dashboard HTML
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hackathon Tracker | Live Dashboard</title>
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- AOS Animation -->
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --secondary: #8b5cf6;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --dark: #1f2937;
            --light: #f3f4f6;
            --white: #ffffff;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }
        
        /* Animated Background */
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.3;
        }
        
        .bg-animation span {
            position: absolute;
            display: block;
            width: 20px;
            height: 20px;
            background: rgba(255, 255, 255, 0.2);
            animation: move 25s linear infinite;
            bottom: -150px;
        }
        
        @keyframes move {
            0% {
                transform: translateY(0) rotate(0deg);
                opacity: 1;
                border-radius: 0;
            }
            100% {
                transform: translateY(-1000px) rotate(720deg);
                opacity: 0;
                border-radius: 50%;
            }
        }
        
        /* Header */
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
            animation: slideDown 0.5s ease;
        }
        
        @keyframes slideDown {
            from {
                transform: translateY(-100%);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 15px;
            font-size: 24px;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .logo i {
            font-size: 30px;
            color: var(--primary);
        }
        
        .nav-menu {
            display: flex;
            gap: 30px;
            align-items: center;
        }
        
        .nav-link {
            color: var(--dark);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
            position: relative;
        }
        
        .nav-link:hover {
            color: var(--primary);
        }
        
        .nav-link::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background: var(--primary);
            transition: width 0.3s;
        }
        
        .nav-link:hover::after {
            width: 100%;
        }
        
        .live-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            background: var(--success);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }
        
        .live-dot {
            width: 8px;
            height: 8px;
            background: white;
            border-radius: 50%;
            animation: blink 1.5s infinite;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
        
        /* Main Container */
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px;
        }
        
        /* Stats Section */
        .stats-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }
        
        .stat-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
        }
        
        .stat-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            color: white;
            margin-bottom: 15px;
        }
        
        .stat-value {
            font-size: 32px;
            font-weight: 800;
            color: var(--dark);
            margin-bottom: 5px;
            counter-reset: stat-counter 0;
        }
        
        .stat-label {
            color: #6b7280;
            font-size: 14px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stat-change {
            position: absolute;
            top: 25px;
            right: 25px;
            background: rgba(16, 185, 129, 0.1);
            color: var(--success);
            padding: 4px 8px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
        }
        
        /* Filters Section */
        .filters-section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 40px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        
        .filters-container {
            display: flex;
            gap: 20px;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .filter-group {
            flex: 1;
            min-width: 200px;
        }
        
        .filter-label {
            display: block;
            color: var(--dark);
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .filter-input,
        .filter-select {
            width: 100%;
            padding: 10px 15px;
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            font-size: 14px;
            transition: all 0.3s;
            background: white;
        }
        
        .filter-input:focus,
        .filter-select:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        
        .search-box {
            position: relative;
        }
        
        .search-icon {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: #9ca3af;
        }
        
        /* Hackathon Grid */
        .hackathons-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        
        .hackathon-card {
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transition: all 0.3s;
            position: relative;
        }
        
        .hackathon-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        }
        
        .card-header {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            padding: 20px;
            position: relative;
        }
        
        .card-header::after {
            content: '';
            position: absolute;
            bottom: -20px;
            left: 0;
            right: 0;
            height: 40px;
            background: inherit;
            transform: skewY(-3deg);
        }
        
        .hackathon-title {
            color: white;
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 10px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        
        .hackathon-meta {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        
        .meta-tag {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            backdrop-filter: blur(10px);
        }
        
        .card-body {
            padding: 40px 20px 20px;
        }
        
        .info-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
            color: var(--dark);
            font-size: 14px;
        }
        
        .info-row i {
            width: 20px;
            color: var(--primary);
        }
        
        .prize-badge {
            background: linear-gradient(135deg, #fbbf24, #f59e0b);
            color: white;
            padding: 8px 15px;
            border-radius: 10px;
            font-weight: 600;
            margin: 15px 0;
            display: inline-block;
        }
        
        .card-footer {
            padding: 20px;
            border-top: 1px solid #e5e7eb;
            display: flex;
            gap: 10px;
        }
        
        .btn {
            flex: 1;
            padding: 12px 20px;
            border-radius: 10px;
            border: none;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            text-align: center;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
        }
        
        .btn-primary:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
        }
        
        .btn-secondary {
            background: var(--light);
            color: var(--dark);
        }
        
        .btn-secondary:hover {
            background: #e5e7eb;
        }
        
        /* Platform Chart */
        .chart-section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 40px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        
        .section-title {
            font-size: 20px;
            font-weight: 700;
            color: var(--dark);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* Loading Animation */
        .loading-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 100px 20px;
        }
        
        .loading-spinner {
            width: 60px;
            height: 60px;
            border: 4px solid rgba(255, 255, 255, 0.3);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .loading-text {
            color: white;
            margin-top: 20px;
            font-size: 18px;
            font-weight: 500;
        }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 80px 20px;
        }
        
        .empty-icon {
            font-size: 80px;
            color: #e5e7eb;
            margin-bottom: 20px;
        }
        
        .empty-title {
            font-size: 24px;
            font-weight: 700;
            color: var(--dark);
            margin-bottom: 10px;
        }
        
        .empty-text {
            color: #6b7280;
            font-size: 16px;
        }
        
        /* Footer */
        .footer {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 30px;
            margin-top: 40px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        
        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .footer-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .footer-links {
            display: flex;
            gap: 20px;
        }
        
        .footer-link {
            color: var(--dark);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .footer-link:hover {
            color: var(--primary);
        }
        
        .last-updated {
            color: #6b7280;
            font-size: 14px;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .nav-container {
                flex-direction: column;
                gap: 20px;
            }
            
            .nav-menu {
                flex-direction: column;
                width: 100%;
                gap: 15px;
            }
            
            .hackathons-grid {
                grid-template-columns: 1fr;
            }
            
            .filters-container {
                flex-direction: column;
            }
            
            .filter-group {
                width: 100%;
            }
            
            .footer-content {
                flex-direction: column;
                text-align: center;
            }
        }
        
        /* Scroll to Top Button */
        .scroll-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            z-index: 1000;
        }
        
        .scroll-top.active {
            opacity: 1;
            visibility: visible;
        }
        
        .scroll-top:hover {
            transform: scale(1.1);
        }
    </style>
</head>
<body>
    <!-- Animated Background -->
    <div class="bg-animation">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
    </div>

    <!-- Header -->
    <header class="header">
        <nav class="nav-container">
            <div class="logo">
                <i class="fas fa-rocket"></i>
                <span>Hackathon Tracker</span>
            </div>
            <div class="nav-menu">
                <a href="#" class="nav-link">Dashboard</a>
                <a href="#platforms" class="nav-link">Platforms</a>
                <a href="#stats" class="nav-link">Statistics</a>
                <a href="https://github.com/Swapnilpawar17/Hackathon-tracker" target="_blank" class="nav-link">
                    <i class="fab fa-github"></i> GitHub
                </a>
                <div class="live-indicator">
                    <div class="live-dot"></div>
                    <span>LIVE</span>
                </div>
            </div>
        </nav>
    </header>

    <!-- Main Container -->
    <div class="container">
        <!-- Stats Section -->
        <section class="stats-section" data-aos="fade-up">
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-trophy"></i>
                </div>
                <div class="stat-value" id="total-hackathons">0</div>
                <div class="stat-label">Live Hackathons</div>
                <div class="stat-change">+0 today</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-globe"></i>
                </div>
                <div class="stat-value" id="platform-count">0</div>
                <div class="stat-label">Platforms Tracked</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-users"></i>
                </div>
                <div class="stat-value" id="fresher-count">0</div>
                <div class="stat-label">Fresher Friendly</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-dollar-sign"></i>
                </div>
                <div class="stat-value" id="total-prize">0</div>
                <div class="stat-label">Total Prizes</div>
            </div>
        </section>

        <!-- Filters Section -->
        <section class="filters-section" data-aos="fade-up">
            <div class="filters-container">
                <div class="filter-group search-box">
                    <label class="filter-label">Search</label>
                    <input type="text" class="filter-input" id="search-input" placeholder="Search hackathons...">
                    <i class="fas fa-search search-icon"></i>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label">Platform</label>
                    <select class="filter-select" id="platform-filter">
                        <option value="">All Platforms</option>
                    </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label">Mode</label>
                    <select class="filter-select" id="mode-filter">
                        <option value="">All Modes</option>
                        <option value="Online">Online</option>
                        <option value="Offline">Offline</option>
                        <option value="Hybrid">Hybrid</option>
                    </select>
                </div>
                
                <div class="filter-group">
                    <label class="filter-label">Sort By</label>
                    <select class="filter-select" id="sort-filter">
                        <option value="name">Name</option>
                        <option value="platform">Platform</option>
                        <option value="prize">Prize Pool</option>
                    </select>
                </div>
            </div>
        </section>

        <!-- Platform Distribution Chart -->
        <section class="chart-section" id="platforms" data-aos="fade-up">
            <h2 class="section-title">
                <i class="fas fa-chart-pie"></i>
                Platform Distribution
            </h2>
            <canvas id="platformChart" width="400" height="100"></canvas>
        </section>

        <!-- Hackathons Grid -->
        <section id="hackathons-container">
            <div class="loading-container">
                <div class="loading-spinner"></div>
                <div class="loading-text">Loading awesome hackathons...</div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="footer" data-aos="fade-up">
            <div class="footer-content">
                <div class="footer-left">
                    <i class="fas fa-rocket" style="font-size: 24px; color: var(--primary);"></i>
                    <div>
                        <div style="font-weight: 700; color: var(--dark);">Hackathon Tracker</div>
                        <div class="last-updated" id="last-updated">Last updated: Never</div>
                    </div>
                </div>
                <div class="footer-links">
                    <a href="https://github.com/Swapnilpawar17" target="_blank" class="footer-link">
                        <i class="fab fa-github"></i> GitHub
                    </a>
                    <a href="https://www.linkedin.com/in/swapnilpawar17" target="_blank" class="footer-link">
                        <i class="fab fa-linkedin"></i> LinkedIn
                    </a>
                    <a href="#" class="footer-link">
                        <i class="fas fa-envelope"></i> Contact
                    </a>
                </div>
            </div>
        </footer>
    </div>

    <!-- Scroll to Top Button -->
    <div class="scroll-top" id="scroll-top">
        <i class="fas fa-arrow-up"></i>
    </div>

    <script>
        // Initialize AOS
        AOS.init({
            duration: 1000,
            once: true
        });

        // Global variables
        let allHackathons = [];
        let filteredHackathons = [];
        let platformChart = null;

        // Animated Counter
        function animateValue(id, start, end, duration) {
            const obj = document.getElementById(id);
            const range = end - start;
            const minTimer = 50;
            let stepTime = Math.abs(Math.floor(duration / range));
            stepTime = Math.max(stepTime, minTimer);
            const startTime = new Date().getTime();
            const endTime = startTime + duration;
            
            function run() {
                const now = new Date().getTime();
                const remaining = Math.max((endTime - now) / duration, 0);
                const value = Math.round(end - (remaining * range));
                obj.innerHTML = value;
                if (value == end) {
                    return;
                }
                setTimeout(run, stepTime);
            }
            run();
        }

        // Calculate total prize pool
        function calculateTotalPrize(hackathons) {
            let total = 0;
            hackathons.forEach(hack => {
                const prize = hack.prize_pool || '';
                // Extract numbers from prize string
                const match = prize.match(/[\d,]+/);
                if (match) {
                    const value = parseInt(match[0].replace(/,/g, ''));
                    if (!isNaN(value)) {
                        total += value;
                    }
                }
            });
            return total;
        }

        // Format number with suffix
        function formatNumber(num) {
            if (num >= 1000000) {
                return (num / 1000000).toFixed(1) + 'M';
            }
            if (num >= 1000) {
                return (num / 1000).toFixed(1) + 'K';
            }
            return num.toString();
        }

        // Fetch hackathons from API
        async function fetchHackathons() {
            try {
                const response = await fetch('/api/hackathons');
                const data = await response.json();
                
                allHackathons = data.hackathons;
                filteredHackathons = allHackathons;
                
                // Update stats with animation
                animateValue('total-hackathons', 0, data.total, 1500);
                animateValue('platform-count', 0, data.platform_count, 1500);
                animateValue('fresher-count', 0, data.fresher_count, 1500);
                
                // Calculate and display total prize
                const totalPrize = calculateTotalPrize(allHackathons);
                document.getElementById('total-prize').innerHTML = formatNumber(totalPrize);
                
                // Update platform filter
                updatePlatformFilter();
                
                // Draw platform chart
                drawPlatformChart(data.platform_stats);
                
                // Render hackathons
                renderHackathons(filteredHackathons);
                
                // Update last updated time
                document.getElementById('last-updated').textContent = 
                    `Last updated: ${new Date(data.last_updated).toLocaleString()}`;
                
            } catch (error) {
                console.error('Error fetching hackathons:', error);
                showError();
            }
        }

        // Update platform filter options
        function updatePlatformFilter() {
            const platforms = [...new Set(allHackathons.map(h => h.platform))].sort();
            const select = document.getElementById('platform-filter');
            
            // Clear existing options except first
            select.innerHTML = '<option value="">All Platforms</option>';
            
            platforms.forEach(platform => {
                const option = document.createElement('option');
                option.value = platform;
                option.textContent = platform;
                select.appendChild(option);
            });
        }

        // Draw platform distribution chart
        function drawPlatformChart(platformStats) {
            const ctx = document.getElementById('platformChart').getContext('2d');
            
            if (platformChart) {
                platformChart.destroy();
            }
            
            const labels = Object.keys(platformStats || {});
            const data = Object.values(platformStats || {});
            
            platformChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: [
                            '#6366f1',
                            '#8b5cf6',
                            '#ec4899',
                            '#f43f5e',
                            '#f59e0b',
                            '#10b981',
                            '#06b6d4',
                            '#3b82f6'
                        ],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: {
                                padding: 15,
                                font: {
                                    size: 12,
                                    weight: '500'
                                }
                            }
                        }
                    }
                }
            });
        }

        // Render hackathons grid
        function renderHackathons(hackathons) {
            const container = document.getElementById('hackathons-container');
            
            if (hackathons.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <i class="fas fa-inbox empty-icon"></i>
                        <h3 class="empty-title">No Hackathons Found</h3>
                        <p class="empty-text">Try adjusting your filters or check back later!</p>
                    </div>
                `;
                return;
            }
            
            const hackathonsHTML = hackathons.map((hack, index) => `
                <div class="hackathon-card" data-aos="fade-up" data-aos-delay="${index * 50}">
                    <div class="card-header">
                        <h3 class="hackathon-title">${hack.name}</h3>
                        <div class="hackathon-meta">
                            <span class="meta-tag">${hack.platform}</span>
                            <span class="meta-tag">${hack.mode || 'Online'}</span>
                            <span class="meta-tag">
                                <i class="fas fa-circle" style="font-size: 8px;"></i> LIVE
                            </span>
                        </div>
                    </div>
                    <div class="card-body">
                        ${hack.organizer ? `
                            <div class="info-row">
                                <i class="fas fa-building"></i>
                                <span>${hack.organizer}</span>
                            </div>
                        ` : ''}
                        
                        ${hack.fresher_friendly ? `
                            <div class="info-row">
                                <i class="fas fa-check-circle"></i>
                                <span>Fresher Friendly</span>
                            </div>
                        ` : ''}
                        
                        ${hack.prize_pool && hack.prize_pool !== 'N/A' ? `
                            <div class="prize-badge">
                                <i class="fas fa-trophy"></i> ${hack.prize_pool}
                            </div>
                        ` : ''}
                    </div>
                    <div class="card-footer">
                        ${hack.registration_link ? `
                            <a href="${hack.registration_link}" target="_blank" class="btn btn-primary">
                                <i class="fas fa-external-link-alt"></i> Register Now
                            </a>
                        ` : ''}
                        <button class="btn btn-secondary" onclick="shareHackathon('${encodeURIComponent(hack.name)}', '${encodeURIComponent(hack.registration_link || '')}')">
                            <i class="fas fa-share"></i> Share
                        </button>
                    </div>
                </div>
            `).join('');
            
            container.innerHTML = `<div class="hackathons-grid">${hackathonsHTML}</div>`;
            
            // Reinitialize AOS for new elements
            AOS.refresh();
        }

        // Filter hackathons
        function filterHackathons() {
            const searchTerm = document.getElementById('search-input').value.toLowerCase();
            const platform = document.getElementById('platform-filter').value;
            const mode = document.getElementById('mode-filter').value;
            const sortBy = document.getElementById('sort-filter').value;
            
            filteredHackathons = allHackathons.filter(hack => {
                const matchesSearch = !searchTerm || 
                    hack.name.toLowerCase().includes(searchTerm) ||
                    (hack.organizer && hack.organizer.toLowerCase().includes(searchTerm)) ||
                    hack.platform.toLowerCase().includes(searchTerm);
                
                const matchesPlatform = !platform || hack.platform === platform;
                const matchesMode = !mode || hack.mode === mode;
                
                return matchesSearch && matchesPlatform && matchesMode;
            });
            
            // Sort hackathons
            if (sortBy === 'platform') {
                filteredHackathons.sort((a, b) => a.platform.localeCompare(b.platform));
            } else if (sortBy === 'prize') {
                filteredHackathons.sort((a, b) => {
                    const prizeA = parseInt((a.prize_pool || '0').replace(/[^\d]/g, '') || '0');
                    const prizeB = parseInt((b.prize_pool || '0').replace(/[^\d]/g, '') || '0');
                    return prizeB - prizeA;
                });
            } else {
                filteredHackathons.sort((a, b) => a.name.localeCompare(b.name));
            }
            
            renderHackathons(filteredHackathons);
        }

        // Share hackathon
        function shareHackathon(name, url) {
            const text = `Check out ${decodeURIComponent(name)} on Hackathon Tracker!`;
            
            if (navigator.share) {
                navigator.share({
                    title: decodeURIComponent(name),
                    text: text,
                    url: decodeURIComponent(url)
                }).catch(err => console.log('Error sharing:', err));
            } else {
                // Fallback: Copy to clipboard
                const shareText = `${text} ${decodeURIComponent(url)}`;
                navigator.clipboard.writeText(shareText).then(() => {
                    alert('Link copied to clipboard!');
                });
            }
        }

        // Show error state
        function showError() {
            const container = document.getElementById('hackathons-container');
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-exclamation-triangle empty-icon" style="color: var(--danger);"></i>
                    <h3 class="empty-title">Oops! Something went wrong</h3>
                    <p class="empty-text">Unable to load hackathons. Please try refreshing the page.</p>
                    <button class="btn btn-primary" onclick="location.reload()">
                        <i class="fas fa-redo"></i> Refresh Page
                    </button>
                </div>
            `;
        }

        // Scroll to top functionality
        const scrollTopBtn = document.getElementById('scroll-top');
        
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                scrollTopBtn.classList.add('active');
            } else {
                scrollTopBtn.classList.remove('active');
            }
        });
        
        scrollTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        // Event listeners
        document.getElementById('search-input').addEventListener('input', filterHackathons);
        document.getElementById('platform-filter').addEventListener('change', filterHackathons);
        document.getElementById('mode-filter').addEventListener('change', filterHackathons);
        document.getElementById('sort-filter').addEventListener('change', filterHackathons);

        // Animated background elements
        const bgAnimation = document.querySelector('.bg-animation');
        for (let i = 0; i < 10; i++) {
            const span = document.createElement('span');
            span.style.left = `${Math.random() * 100}%`;
            span.style.animationDuration = `${Math.random() * 20 + 10}s`;
            span.style.animationDelay = `${Math.random() * 5}s`;
            bgAnimation.appendChild(span);
        }

        // Initialize
        fetchHackathons();
        
        // Auto refresh every 5 minutes
        setInterval(fetchHackathons, 300000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/hackathons')
def api_hackathons():
    """API endpoint for hackathons"""
    global cached_hackathons, last_updated, platform_stats
    
    if not cached_hackathons:
        # Initial load if cache is empty
        hackathons = []
        
        try:
            scraper = HackathonScraper()
            hackathons.extend(scraper.get_all_hackathons())
            
            india_scraper = IndiaHackathonScraper()
            hackathons.extend(india_scraper.get_all_india_hackathons())
            
            hackathons.extend(get_manual_hackathons())
            hackathons = apply_all_filters(hackathons, live_only=True)
            
            # Calculate platform stats
            platform_stats = {}
            for hack in hackathons:
                platform = hack.get('platform', 'Unknown')
                if platform not in platform_stats:
                    platform_stats[platform] = 0
                platform_stats[platform] += 1
            
            cached_hackathons = hackathons
            last_updated = datetime.now()
        except:
            pass
    
    # Calculate additional stats
    fresher_count = len([h for h in cached_hackathons if h.get('fresher_friendly', False)])
    
    return jsonify({
        'hackathons': cached_hackathons,
        'total': len(cached_hackathons),
        'platform_count': len(platform_stats),
        'fresher_count': fresher_count,
        'platform_stats': platform_stats,
        'last_updated': last_updated.isoformat() if last_updated else datetime.now().isoformat()
    })

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({
        'status': 'healthy',
        'hackathons_loaded': len(cached_hackathons),
        'last_updated': last_updated.isoformat() if last_updated else 'Never',
        'time': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)