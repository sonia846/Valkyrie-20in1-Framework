import requests

def hunt_secrets(url):
    print(f"\n[+] Hunting for Exposed Secrets & Git Repositories on: {url}")
    
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
        
    # Professional wordlist for sensitive files
    secret_paths = {
        "/.env": "DB_PASSWORD",
        "/.git/HEAD": "ref: refs/heads",
        "/config.php.bak": "<?php",
        "/wp-config.php.bak": "DB_PASSWORD",
        "/.sql": "INSERT INTO",
        "/backup.zip": ""
    }
    
    headers = {'User-Agent': 'Mozilla/5.0 (Valkyrie-Framework/2.0)'}
    
    for path, signature in secret_paths.items():
        test_url = url.rstrip('/') + path
        try:
            response = requests.get(test_url, headers=headers, timeout=4, allow_redirects=False)
            
            # Agar file exists karti hai (200 OK)
            if response.status_code == 200:
                # Signature check taake false positive na ho
                if signature == "" or signature in response.text:
                    print(f"  [!] CRITICAL EXPOSURE DETECTED: {test_url}")
                else:
                    print(f"  [!] Potential Sensitive File Found (Status 200): {test_url}")
            else:
                print(f"  [-] Checked: {path} (Not Found / Protected)")
                
        except Exception as e:
            continue
            
    return "Secret Hunting Complete."
