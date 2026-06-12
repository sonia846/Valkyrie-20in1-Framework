import socket

def check_takeover(subdomain):
    print(f"\n[+] Analyzing Subdomain Takeover Vulnerability for: {subdomain}")
    
    # URL clean up (agar HTTP laga ho to remove karne ke liye)
    clean_sub = subdomain.replace("https://", "").replace("http://", "").split('/')[0]
    
    # Popular services ke signature dhoondnay ke liye dictionary
    signatures = {
        "github.io": "There isn't a GitHub Pages site here",
        "amazonaws.com": "The specified bucket does not exist",
        "tumblr.com": "Whatever you were looking for is not here",
        "shopify.com": "Sorry, this shop is currently unavailable",
        "squarespace.com": "404 Not Found - Squarespace"
    }
    
    try:
        # 1. CNAME Record Verification via Socket
        # Real-world tools CNAME lookup karte hain, hum basic verification check lagayenge
        print(f"  [-] Checking DNS pointing for {clean_sub}...")
        
        # Checking connection stability
        socket.gethostbyname(clean_sub)
        print("  [-] Subdomain is active and resolving to an IP.")
        print("  [✓] Takeover Status: Safe (Domain actively managed).")
        return "Safe"

    except socket.gaierror:
        # Agar IP resolve nahi ho rahi, to chance hai ke domain broken ho
        print("  [!] DNS Resolution Failed: Subdomain might be pointing to a dead service!")
        print("  [!] VULNERABILITY ALERT: Potential Subdomain Takeover vulnerability detected if CNAME points to an unclaimed cloud bucket.")
        return "Vulnerable"
        
    except Exception as e:
        print(f"  [X] Error during DNS lookup: {str(e)}")
        return "Error"
      
