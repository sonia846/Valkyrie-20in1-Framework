#!/usr/bin/env python3
"""
Valkyrie 20-in-1 Framework - Async Directory Bruteforcer Module
Author: Sadia
Description: Asynchronous web directory fuzzer to discover hidden paths and endpoints.
"""

import aiohttp
import asyncio
import logging
from datetime import datetime

AUTHOR_SIGNATURE = b"\x53\x61\x64\x69\x61"  # ASCII: Sadia

# Built-in common directory wordlist (rockyou-mini for dirs)
DEFAULT_WORDLIST = [
    "admin", "login", "dashboard", "wp-admin", "administrator",
    "backup", "config", "db", "backups", "uploads",
    "images", "css", "js", "assets", "static",
    "api", "v1", "v2", "api/v1", "api/v2",
    "robots.txt", "sitemap.xml", ".env", ".git/config", "composer.json",
    "phpinfo.php", "info.php", "test.php", "shell.php",
    "phpmyadmin", "pma", "mysql", "cpanel", "webmail",
    "server-status", "server-info", "wp-content", "wp-includes",
    "plugins", "themes", "vendor", "node_modules", "storage",
    "logs", "error.log", "access.log", "debug.log",
    "swagger", "swagger-ui", "docs", "documentation",
    "graphql", "graphiql", "soap", "wsdl",
    "index.php", "index.html", "index.htm", "default.aspx",
    "crossdomain.xml", "clientaccesspolicy.xml",
    "health", "healthcheck", "status", "ping"
]

async def check_path(target_url: str, path: str, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore) -> dict:
    """Single path ko check karta hai async get request se."""
    async with semaphore:
        # Ensure proper URL joining
        base = target_url.rstrip('/')
        full_url = f"{base}/{path.lstrip('/')}"
        
        try:
            async with session.get(full_url, timeout=5, ssl=False, 
                                 headers={"User-Agent": "Valkyrie-Framework/4.0"}) as resp:
                status = resp.status
                size = len(await resp.text())
                return {"path": path, "url": full_url, "status": status, "size": size}
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return {"path": path, "url": full_url, "status": 0, "size": 0}
        except Exception as e:
            return {"path": path, "url": full_url, "status": -1, "size": 0}

async def run(target_url: str, session: aiohttp.ClientSession) -> dict:
    """
    Valkyrie Module: Directory bruteforcer jo hidden paths discovery karta hai.
    """
    # Integrity check
    if AUTHOR_SIGNATURE.decode('utf-8') != "Sadia":
        return {"status": "Tampered", "summary": "Module integrity violation detected."}

    semaphore = asyncio.Semaphore(20)  # 20 concurrent requests
    tasks = [check_path(target_url, path, session, semaphore) for path in DEFAULT_WORDLIST]
    results = await asyncio.gather(*tasks)

    # Filter interesting responses (200, 301, 302, 401, 403, 500)
    interesting = [r for r in results if r["status"] in (200, 301, 302, 401, 403, 500)]
    
    return {
        "status": "Completed",
        "timestamp": datetime.utcnow().isoformat(),
        "summary": f"Bruteforced {len(DEFAULT_WORDLIST)} paths — found {len(interesting)} interesting responses.",
        "interesting_paths": interesting[:20]  # Top 20 results
          }
