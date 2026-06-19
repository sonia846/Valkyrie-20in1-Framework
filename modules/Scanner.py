#!/usr/bin/env python3
"""
Valkyrie 20-in-1 Framework - Async Port Scanner Module
Author: Sadia
Description: High-speed asynchronous TCP port scanner for discovering open services.
"""

import asyncio
import logging
from datetime import datetime

AUTHOR_SIGNATURE = b"\x53\x61\x64\x69\x61"  # ASCII: Sadia

# Common ports with their service names
COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 111: "RPC", 135: "MSRPC", 139: "NetBIOS",
    143: "IMAP", 161: "SNMP", 389: "LDAP", 443: "HTTPS", 445: "SMB",
    465: "SMTPS", 514: "Syslog", 587: "SMTP Submission", 636: "LDAPS",
    993: "IMAPS", 995: "POP3S", 1433: "MSSQL", 1521: "Oracle DB",
    2049: "NFS", 2375: "Docker", 2376: "Docker TLS", 3306: "MySQL",
    3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 5985: "WinRM HTTP",
    5986: "WinRM HTTPS", 6379: "Redis", 8080: "HTTP-Proxy", 8443: "HTTPS-Alt",
    9090: "WebSocket", 27017: "MongoDB"
}

async def scan_port(target_ip: str, port: int, timeout: float = 1.5) -> dict:
    """Ek single port ko async scan karta hai."""
    try:
        conn = asyncio.open_connection(target_ip, port)
        _, writer = await asyncio.wait_for(conn, timeout=timeout)
        writer.close()
        await writer.wait_closed()
        service = COMMON_PORTS.get(port, "Unknown")
        return {"port": port, "state": "open", "service": service}
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return {"port": port, "state": "closed", "service": ""}
    except Exception as e:
        return {"port": port, "state": "error", "service": str(e)}

async def run(target_url: str, session=None) -> dict:
    """
    Valkyrie Module: Multi-threaded async port scanner.
    Hostname resolve karta hai aur common ports ko scan karta hai.
    """
    # Integrity check
    if AUTHOR_SIGNATURE.decode('utf-8') != "Sadia":
        return {"status": "Tampered", "summary": "Module integrity violation detected."}

    # URL se hostname extract karo
    clean_host = target_url.replace("https://", "").replace("http://", "").split('/')[0].split(':')[0]

    # DNS resolution
    try:
        target_ip = (await asyncio.get_event_loop().getaddrinfo(clean_host, 80))[0][4][0]
    except Exception as e:
        return {
            "status": "Error",
            "summary": f"DNS resolution failed for {clean_host}: {str(e)}"
        }

    # Sab ports ko scan karo
    all_ports = list(COMMON_PORTS.keys())
    tasks = [scan_port(target_ip, port) for port in all_ports]
    results = await asyncio.gather(*tasks)

    # Sirf open ports filter karo
    open_ports = [r for r in results if r["state"] == "open"]
    closed_count = len([r for r in results if r["state"] == "closed"])

    return {
        "status": "Completed",
        "timestamp": datetime.utcnow().isoformat(),
        "summary": f"Scanned {len(all_ports)} common ports on {target_ip} — {len(open_ports)} open, {closed_count} closed.",
        "open_ports": open_ports,
        "target_ip": target_ip
  }
