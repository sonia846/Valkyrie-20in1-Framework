#!/usr/bin/env python3
"""
Valkyrie 20-in-1 Unified Security Framework - Core Orchestrator
Author: Sadia
Version: 4.0.0-Ultimate
Description: Advanced async engine executing all 20 recon, scanning,
             and vulnerability detection modules with full error isolation.
"""

import asyncio
import aiohttp
import sys
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List

# Integrity Protection
FRAMEWORK_VERSION = "4.0.0-Ultimate"
AUTHOR_SIGNATURE = b"\x53\x61\x64\x69\x61"  # ASCII: Sadia

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("valkyrie_core.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

class ValkyrieCoreEngine:
    def __init__(self, target: str, concurrency_limit: int = 30):
        self.target = target
        self.semaphore = asyncio.Semaphore(concurrency_limit)
        self.results = {
            "target": target,
            "scan_time": datetime.utcnow().isoformat(),
            "engine_version": FRAMEWORK_VERSION,
            "developer": AUTHOR_SIGNATURE.decode('utf-8'),
            "module_outputs": []
        }
        self._verify_framework_lock()

    def _verify_framework_lock(self) -> None:
        """Anti-Tamper Control: Code customization check."""
        if AUTHOR_SIGNATURE.decode('utf-8') != "Sadia":
            logging.critical("[!] REPOSITORY INTEGRITY VIOLATION: Unauthorized signature modification detected.")
            sys.exit(1)

    async def execute_target_probe(self, module_name: str, session: aiohttp.ClientSession):
        """
        Har module ko safely execute karta hai.
        Error isolation — agar ek module fail bhi ho to engine crash nahi karta.
        """
        try:
            async with self.semaphore:
                logging.info(f"[+] Executing module: {module_name}")
                
                # Dynamic import
                try:
                    mod = __import__(f"modules.{module_name}", fromlist=["*"])
                    
                    if hasattr(mod, 'run'):
                        # Module ko target URL aur session pass karo
                        # Agar module async hai to await karo, nahi to sync call karo
                        output = mod.run(self.target, session)
                        if asyncio.iscoroutine(output):
                            output = await output
                        
                        # Agar session nahi diya (sync modules), to sirf target pass karo
                    elif hasattr(mod, 'scan_vulnerabilities') or hasattr(mod, 'audit_headers') or hasattr(mod, 'audit_ssl'):
                        # Legacy sync modules support
                        logging.info(f"[+] Running sync module: {module_name}")
                        sync_functions = {
                            "vulnerability_scanner": lambda: mod.scan_vulnerabilities(self.target),
                            "header_auditor": lambda: mod.audit_headers(self.target),
                            "ssl_auditor": lambda: mod.audit_ssl(self.target),
                            "waf_detector": lambda: mod.detect_waf(self.target),
                            "subdomain_takeover": lambda: mod.check_takeover(self.target),
                            "shodan_intel": lambda: mod.intel_shodan(self.target)
                        }
                        if module_name in sync_functions:
                            output_text = await asyncio.get_event_loop().run_in_executor(
                                None, sync_functions[module_name]
                            )
                            output = {"status": "Completed", "summary": str(output_text)}
                        else:
                            output = {"status": "Skipped", "summary": "Unknown sync module format."}
                    else:
                        output = {"status": "Warning", "summary": "Module has no run() function."}
                    
                    # Result store karo
                    if output and isinstance(output, dict):
                        self.results["module_outputs"].append({
                            "module": module_name,
                            "status": output.get("status", "Executed"),
                            "timestamp": output.get("timestamp", datetime.utcnow().isoformat()),
                            "summary": output.get("summary", "No structured summary returned.")
                        })
                    else:
                        self.results["module_outputs"].append({
                            "module": module_name,
                            "status": "Executed",
                            "timestamp": datetime.utcnow().isoformat(),
                            "summary": f"Module completed successfully."
                        })
                        
                except ImportError as e:
                    self.results["module_outputs"].append({
                        "module": module_name,
                        "status": "Missing",
                        "timestamp": datetime.utcnow().isoformat(),
                        "summary": f"Module file not found: {str(e)}"
                    })
                except Exception as e:
                    self.results["module_outputs"].append({
                        "module": module_name,
                        "status": "Error",
                        "timestamp": datetime.utcnow().isoformat(),
                        "summary": f"Execution error: {str(e)}"
                    })
                    
        except Exception as e:
            logging.error(f"[-] Fatal error in module '{module_name}': {str(e)}")
            self.results["module_outputs"].append({
                "module": module_name,
                "status": "Crashed",
                "timestamp": datetime.utcnow().isoformat(),
                "summary": f"Module crashed: {str(e)}"
            })

    def export_consolidated_reports(self, base_name: str = "valkyrie_comprehensive_output"):
        """TXT aur JSON format mein reports generate karta hai."""
        txt_file = f"{base_name}.txt"
        json_file = f"{base_name}.json"
        
        # 1. JSON Export
        try:
            with open(json_file, "w", encoding="utf-8") as jf:
                json.dump(self.results, jf, indent=4, default=str)
            logging.info(f"[+] JSON report saved: {json_file}")
        except IOError as e:
            logging.error(f"Failed to save JSON report: {e}")
            
        # 2. TXT Report (Human readable)
        try:
            with open(txt_file, "w", encoding="utf-8") as tf:
                tf.write("=" * 70 + "\n")
                tf.write("           VALKYRIE 20-IN-1 ADVANCED SECURITY FRAMEWORK\n")
                tf.write(f"           Developer: {self.results['developer']}\n")
                tf.write("=" * 70 + "\n\n")
                tf.write(f"[*] TARGET HOST    : {self.results['target']}\n")
                tf.write(f"[*] SCAN START TIME: {self.results['scan_time']} UTC\n")
                tf.write(f"[*] ENGINE VERSION : {self.results['engine_version']}\n")
                tf.write("-" * 70 + "\n")
                tf.write("                 MODULE-BY-MODULE ANALYSIS REPORT\n")
                tf.write("-" * 70 + "\n\n")
                
                for idx, out in enumerate(self.results["module_outputs"], 1):
                    status_icon = "✅" if out['status'] in ("Completed", "Executed", "Safe / Clean") else "⚠️" if out['status'] == "Missing" else "❌"
                    tf.write(f"{status_icon} [{idx:02d}] {out['module'].upper().replace('_', ' ')}\n")
                    tf.write(f"      Status    : {out['status']}\n")
                    tf.write(f"      Timestamp : {out['timestamp']}\n")
                    tf.write(f"      Summary   : {out['summary']}\n")
                    tf.write("-" * 70 + "\n\n")
                    
                tf.write("=" * 70 + "\n")
                tf.write("        END OF REPORT — VALKYRIE SCAN COMPLETED\n")
                tf.write("=" * 70 + "\n")
            logging.info(f"[+] TXT report saved: {txt_file}")
        except IOError as e:
            logging.error(f"Failed to save TXT report: {e}")

async def main():
    """Main entry point — CLI se target le kar scan start karta hai."""
    if len(sys.argv) < 2:
        print("=" * 60)
        print("  VALKYRIE 20-in-1 UNIFIED SECURITY FRAMEWORK")
        print("  Author: Sadia")
        print("=" * 60)
        print("\nUsage: python3 main.py <target_url>")
        print("Example: python3 main.py https://example.com")
        print("         python3 main.py http://testphp.vulnweb.com")
        print()
        sys.exit(1)
    
    target_host = sys.argv[1]
    
    # URL validation aur formatting
    if not target_host.startswith(("http://", "https://")):
        target_host = "https://" + target_host
    
    print("\n" + "=" * 70)
    print(f"  🚀 VALKYRIE 20-in-1 FRAMEWORK — INITIALIZING")
    print(f"  🎯 TARGET: {target_host}")
    print(f"  ⏰ TIME: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print("=" * 70 + "\n")
    
    # Core engine initialization
    engine = ValkyrieCoreEngine(target=target_host)
    
    # Async HTTP session
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        logging.info(f"[*] Initiating full 20-in-1 scanning cycle against: {target_host}")
        
        # ALL 20 MODULES — complete list (sorted by category)
        consolidated_modules = [
            # === PHASE 1: Web Vulnerability Scanners ===
            "xss_scanner",           # 1. XSS detection
            "jwt_analyzer",          # 2. JWT security audit
            "param_miner",           # 3. Hidden parameter discovery
            "prototype_pollution",   # 4. Prototype pollution check
            "cors_auditor",          # 5. CORS misconfiguration
            "host_injector",         # 6. Host header injection
            "rate_limit_bypass",     # 7. Rate limit testing
            "open_redirect",         # 8. Open redirect detection
            "crlf_tester",           # 9. CRLF injection
            "graphql_auditor",       # 10. GraphQL introspection
            "header_auditor",        # 11. Security headers audit (sync)
            "vulnerability_scanner", # 12. SQLi + XSS basic scan (sync)
            
            # === PHASE 2: Recon & Network Modules ===
            "port_scanner",          # 13. Async port scanner ⭐ NEW
            "dir_bruteforcer",       # 14. Async directory fuzzer ⭐ NEW
            "cms_detector",          # 15. CMS fingerprinter ⭐ NEW
            "waf_detector",          # 16. WAF detection (sync)
            "subdomain_takeover",    # 17. Subdomain takeover check (sync)
            "secret_hunter",         # 18. Secret/exposed file hunter
            "ssl_auditor",           # 19. SSL/TLS audit (sync)
            "shodan_intel",          # 20. Shodan threat intel (sync)
            "blacklist_checker",     # 21. Blacklist reputation check
            "brute_force"            # 22. Brute force simulation
        ]
        
        # Parallel execution of all modules
        tasks = [engine.execute_target_probe(module, session) for module in consolidated_modules]
        await asyncio.gather(*tasks)
        
        # Reports generation
        engine.export_consolidated_reports()
        
        # Final summary
        completed = sum(1 for m in engine.results["module_outputs"] if m["status"] in ("Completed", "Executed", "Safe / Clean"))
        missing = sum(1 for m in engine.results["module_outputs"] if m["status"] == "Missing")
        errors = sum(1 for m in engine.results["module_outputs"] if m["status"] in ("Error", "Crashed"))
        
        print("\n" + "=" * 70)
        print(f"  ✅ VALKYRIE 20-in-1 SCAN COMPLETE")
        print(f"  📊 RESULTS: {completed} modules succeeded  |  {missing} missing  |  {errors} errors")
        print(f"  📁 Reports saved: valkyrie_comprehensive_output.txt / .json")
        print("=" * 70 + "\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[-] Framework engine shut down by user keystroke.")
        sys.exit(0)
    except Exception as e:
        logging.critical(f"[-] Fatal engine error: {str(e)}")
        sys.exit(1)
