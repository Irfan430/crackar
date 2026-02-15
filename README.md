# CRACKAR v5.0.0.1 - Advanced Multi-Vector Penetration Testing Tool

[![GitHub stars](https://img.shields.io/github/stars/yourusername/crackar?style=social)](https://github.com/yourusername/crackar)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/crackar?style=social)](https://github.com/yourusername/crackar)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/crackar)](https://github.com/yourusername/crackar)

<div align="center">
  <img src="https://raw.githubusercontent.com/yourusername/crackar/main/banner.png" alt="CRACKAR Banner"/>
</div>

**⚠️ AUTHORIZED USE ONLY** - I have explicit permission and am authorized to perform penetration testing on target systems under company Terms of Service.

# 🚀 Features
- **Multi-Vector Attacks**: HTTP Flood, UDP Flood, SYN Flood, Slowloris
- **WAF Bypass**: Intelligent payload randomization & header rotation (3+ UA profiles)
- **TOR Support**: Anonymous traffic routing (127.0.0.1:9050)
- **Real-time Stats**: Live RPS, MBPS, success rates with Rich TUI
- **Rate Limiting**: Precise RPS control (up to 5000+)
- **Thread Pool**: 1000+ concurrent workers
- **Smart Path Discovery**: 12+ common attack surfaces
- **SSL/TLS Support**: Full HTTPS compatibility

# 🛠️ Attack Modes

| Mode | Type | Description | Success Rate |
|------|------|-------------|--------------|
| `http` | Layer 7 | Application layer flood w/ WAF bypass | 80-95% |
| `udp` | Layer 4 | Volumetric UDP flood (1400B packets) | 95%+ |
| `syn` | Layer 4 | Raw TCP SYN flood | 90%+ |
| `slowloris` | Layer 7 | Application-layer DoS | 85%+ |
| `multi` | Hybrid | Random multi-vector (70/15/15) | 90%+ |

# 🔒 Bypass Techniques
3+ User-Agent Profiles (Chrome, Safari, Firefox)
Random Query Parameters (?id=123456, ?page=789)
Path Obfuscation (12+ common paths)
TOR Circuit Rotation
HTTP/2 & Keep-Alive
Rate Limiting Evasion

# 📦 Quick Installation
Clone repository
git clone https://github.com/yourusername/crackar.git
cd crackar

# Install dependencies
pip3 install -r requirements.txt
Start TOR

# 📋 Requirements
requests==2.31.0
rich==13.7.1
colorama==0.4.6
dnspython==2.6.1
urllib3>=2.6.3,<3.0

# Run pentest tool
$ python3 crackar.py

[TOR DETECTION] 127.0.0.1:9050
CONNECTED

SELECT MODE:
1: http - Application Layer (Default)
2: udp - Volumetric UDP Flood
3: syn - SYN Flood (Protocol)
4: slowloris - APDoS Slowloris
5: multi - Multi-Vector (All Methods)

Threads [1000]: 500
RPS [5000]: 2000
TARGET URL/IP: https://target.com:8080

# 📊 Live Dashboard Preview
┌────────────────────────────────────────────────────────────────┐
│ CRACKER v5.0.0.1 | MULTI MODE | LIVE STATS                     │
├────────────────────┬──────────────────┬────────────────────────┤
│ Metric             │ Value            │ Status                 │
├────────────────────┼──────────────────┼────────────────────────┤
│ LIVE RPS           │ 2,847            │ LIMIT [3,000]          │
│ LIVE MBPS          │ 24.7             │                        │
│ TOTAL REQ          │ 847,234          │                        │
│ SUCCESS            │ 742,156          │ 87.6%                  │
│ BLOCKED            │ 45,678           │                        │
│ ERRORS             │ 59,400           │                        │
│ BYTES SENT         │ 7.2GB            │                        │
│ UPTIME             │ 298s             │ PEAK: 3,124            │
│ TOR                │ ONLINE           │                        │
│ TARGET             │ https://target.com:8443 │ MODE: MULTI     │   
└────────────────────┴──────────────────┴────────────────────────┘

# 🎯 Final Report Example
┌──────────────────────────────────────────────────────────────┐
│                       ATTACK COMPLETE                        │
├──────────────────────────────────────────────────────────────┤
│ TARGET: HTTPS://target.com:8443/admin                        │
│ TOTAL REQUESTS: 1,247,892                                    │
│ AVG RPS: 4,182                                               │
│ AVG MBPS: 38.7                                               │
│ SUCCESS RATE: 89.2%                                          │
│ TOR STATUS: ONLINE                                           │
│ TOTAL BYTES: 12.4GB                                          │
└──────────────────────────────────────────────────────────────┘

# 🔒 Legal & Ethical Use
✅ Authorized penetration testing only
✅ Company Terms of Service compliance
✅ Red team exercises with permission
✅ Security research & validation

❌ Unauthorized attacks prohibited
❌ Denial of service without consent

# ⚠️ Note
## I would like to request everyone that the tool is very powerful so do not use it illegally, if you do so, then it is entirely your own responsibility, the author of the tool will not take responsibility for it.
## First connect to tor, then run the tool in the second terminal, do not run it without tor, it can be dangerous for you, your real IP address may be revealed as a result.

# For support or custom builds Contact

# Contact
Instagram:- arcane.__01
Telegram:- @cashhustle_8

# Join Now
Yotutuhe:- https://youtube.com/@cyberarcane8?si=ufFzu1ubtIzTrbHZ
Telegram Channel:- https://t.me/dealzone2888

