import requests

def detect_waf(url):
    print(f"\n[+] Identifying Web Application Firewall (WAF) for: {url}")
    
    # URL formatting
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
        
    # Standard security testing headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Cybersecurity-Auditor/2.0'
    }
    
    # Malicious-looking but harmless payload to trigger a WAF block safely
    waf_payload = "/?etc/passwd=../..//etc/passwd><script>alert(1)</script>"
    test_url = url + waf_payload

    try:
        response = requests.get(test_url, headers=headers, timeout=5)
        server_header = response.headers.get("Server", "").lower()
        
        # 1. Inspection via HTTP Status Code & Server Headers
        if response.status_code in [403, 406, 501, 999]:
            print(f"  [!] Traffic Blocked/Challenged (Status Code: {response.status_code})")
            
            if "cloudflare" in server_header or "cf-ray" in response.headers:
                print("  [✓] WAF Detected: Cloudflare Protection System")
                return "Cloudflare"
            elif "cloudfront" in server_header or "x-amz-cf-id" in response.headers:
                print("  [✓] WAF Detected: AWS CloudFront / AWS WAF")
                return "AWS WAF"
            elif "sucuri" in server_header or "x-sucuri-id" in response.headers:
                print("  [✓] WAF Detected: Sucuri CloudProxy")
                return "Sucuri"
            elif "akamai" in server_header:
                print("  [✓] WAF Detected: Akamai Edge Protection")
                return "Akamai"
            else:
                print("  [✓] WAF Detected: Generic/Unknown Firewall Rule Triggered.")
                return "Generic WAF"
        else:
            # 2. Check if Server Header explicitly reveals WAF even on clean request
            if "cloudflare" in server_header:
                print("  [✓] WAF Detected: Cloudflare (Passive Detection)")
                return "Cloudflare"
            else:
                print("  [-] No WAF detected. The server responded normally to raw payloads.")
                return "None"

    except Exception as e:
        print(f"  [X] Connection Error while checking WAF: {str(e)}")
        return "Error"
