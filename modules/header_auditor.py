import requests

def audit_headers(url):
    print(f"\n[+] Auditing HTTP Security Headers & CORS Config for: {url}")
    
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    # Yeh hain woh main security headers jo har bade server par hona zaroori hain
    security_headers = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Valkyrie-Framework/2.0)'}
        response = requests.get(url, headers=headers, timeout=5)
        server_headers = response.headers

        print("\n  [-] Analyzing Security Headers:")
        missing_count = 0
        
        for header in security_headers:
            if header in server_headers:
                print(f"  [✓] {header}: Present (Good Security)")
            else:
                print(f"  [!] MISSING: {header} is not set!")
                missing_count += 1

        # CORS (Cross-Origin Resource Sharing) Misconfiguration Check
        print("\n  [-] Checking CORS Misconfiguration:")
        cors_header = server_headers.get("Access-Control-Allow-Origin", "")
        
        if cors_header == "*":
            print("  [!] VULNERABILITY ALERT: Wildcard '*' detected in CORS header! Data leak possible.")
        elif cors_header:
            print(f"  [✓] CORS Configured for: {cors_header}")
        else:
            print("  [-] CORS Header: Not explicitly exposed publicly (Standard).")

        if missing_count > 3:
            print("\n  [!] AUDIT RESULT: Server hardening required. Multiple security headers are missing.")
        else:
            print("\n  [✓] AUDIT RESULT: Server has decent security header configuration.")

        return "Audit Complete."

    except Exception as e:
        print(f"  [X] Connection Error during Header Audit: {str(e)}")
        return "Failed"
