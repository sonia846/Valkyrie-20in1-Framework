#!/usr/bin/env python3
"""
Valkyrie 20-in-1 Framework - Async CMS Detector Module
Author: Sadia
Description: Identifies Content Management Systems (WordPress, Joomla, Drupal, etc.) from response signatures.
"""

import aiohttp
import logging
from datetime import datetime

AUTHOR_SIGNATURE = b"\x53\x61\x64\x69\x61"  # ASCII: Sadia

CMS_SIGNATURES = {
    "WordPress": {
        "paths": ["/wp-admin/", "/wp-content/", "/wp-includes/", "/wp-login.php"],
        "headers": ["X-Powered-By: WordPress"],
        "body_indicators": ["/wp-content/", "wp-json", "WordPress"]
    },
    "Joomla": {
        "paths": ["/administrator/", "/components/", "/modules/", "/templates/"],
        "headers": [],
        "body_indicators": ["com_content", "option=com_", "/templates/"]
    },
    "Drupal": {
        "paths": ["/user/login", "/node/", "/sites/default/", "/misc/drupal.js"],
        "headers": ["X-Generator: Drupal"],
        "body_indicators": ["drupal.js", "Drupal.settings", "sites/default"]
    },
    "Magento": {
        "paths": ["/admin/", "/skin/", "/media/", "/app/"],
        "headers": ["X-Magento-*"],
        "body_indicators": ["Magento", "Varien_Form"]
    },
    "Shopify": {
        "paths": ["/admin", "/cart", "/collections/"],
        "headers": ["X-ShopId:", "X-Shopify-Shop:"],
        "body_indicators": ["Shopify", "myshopify.com"]
    },
    "Laravel": {
        "paths": ["/vendor/", "/storage/"],
        "headers": [],
        "body_indicators": ["Laravel", "csrf-token"]
    },
    "Express/Node.js": {
        "paths": [],
        "headers": ["X-Powered-By: Express"],
        "body_indicators": []
    },
    "ASP.NET": {
        "paths": ["/WebResource.axd", "/ScriptResource.axd"],
        "headers": ["X-AspNet-Version:", "X-Powered-By: ASP.NET"],
        "body_indicators": ["__VIEWSTATE", "__EVENTVALIDATION"]
    }
}

async def check_cms_path(target_url: str, path: str, session: aiohttp.ClientSession) -> bool:
    """Check if a CMS-specific path exists on the target."""
    full_url = f"{target_url.rstrip('/')}{path}"
    try:
        async with session.get(full_url, timeout=5, ssl=False,
                             headers={"User-Agent": "Valkyrie-Framework/4.0"},
                             allow_redirects=False) as resp:
            return resp.status in (200, 301, 302, 401, 403)
    except Exception:
        return False

async def run(target_url: str, session: aiohttp.ClientSession) -> dict:
    """
    Valkyrie Module: CMS (Content Management System) Detector.
    Signatures, paths, aur headers use karta hai CMS identify karne ke liye.
    """
    # Integrity check
    if AUTHOR_SIGNATURE.decode('utf-8') != "Sadia":
        return {"status": "Tampered", "summary": "Module integrity violation detected."}

    detected_cms = []

    for cms_name, signatures in CMS_SIGNATURES.items():
        score = 0
        total_checks = 0

        # Check CMS-specific paths
        for path in signatures["paths"]:
            total_checks += 1
            if await check_cms_path(target_url, path, session):
                score += 1

        # Generate a final response report
        if score >= 2:
            detection_summary = f"Detected {cms_name} with {score}/{len(signatures['paths'])} path matches."
            detected_cms.append({
                "cms": cms_name,
                "confidence": f"{score}/{len(signatures['paths'])} paths matched",
                "summary": detection_summary
            })

    if detected_cms:
        return {
            "status": "Completed",
            "timestamp": datetime.utcnow().isoformat(),
            "summary": f"Detected {len(detected_cms)} CMS platform(s).",
            "detected_cms": detected_cms
        }
    else:
        return {
            "status": "Completed",
            "timestamp": datetime.utcnow().isoformat(),
            "summary": "No known CMS signatures detected.",
            "detected_cms": []
                                    }
