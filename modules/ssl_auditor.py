import socket
import ssl
from datetime import datetime

def audit_ssl(hostname):
    print(f"\n[+] Auditing SSL/TLS Configuration for: {hostname}")
    context = ssl.create_default_context()
    
    try:
        # Resolving hostname to IP
        formatted_host = hostname.replace("https://", "").replace("http://", "").split('/')[0]
        
        with socket.create_connection((formatted_host, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=formatted_host) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                version = ssock.version()
                
                print(f"  [-] TLS/SSL Version In Use: {version}")
                print(f"  [-] Cipher Suite: {cipher[0]} ({cipher[1]} bits)")
                
                # Expiry Date Calculation
                expire_date_str = cert.get('notAfter')
                if expire_date_str:
                    expire_date = datetime.strptime(expire_date_str, '%b %d %H:%M:%S %Y %Z')
                    days_left = (expire_date - datetime.utcnow()).days
                    print(f"  [-] Certificate Expires On: {expire_date} ({days_left} days left)")
                    
                    if days_left < 30:
                        print("  [!] WARNING: Certificate is expiring soon!")
                
                # Basic Vulnerability Check (Weak Protocol Detection)
                if "TLSv1" in version or "SSL" in version:
                    print("  [!] VULNERABILITY ALERT: Server accepts outdated/weak TLS/SSL protocols!")
                else:
                    print("  [✓] Protocol Security: Modern TLS Protocol detected.")
                    
                return f"Host: {formatted_host}\nVersion: {version}\nCipher: {cipher[0]}\nDays Left: {days_left}\n"

    except Exception as e:
        print(f"  [X] SSL Audit Failed: {str(e)}")
        return f"SSL Audit Failed for {hostname}: {str(e)}\n"
      
