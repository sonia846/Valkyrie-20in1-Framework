import socket
import requests

def intel_shodan(hostname):
    print(f"\n[+] Gathering Shodan Threat Intelligence for: {hostname}")
    
    try:
        # Hostname ko IP address mein convert karna
        formatted_host = hostname.replace("https://", "").replace("http://", "").split('/')[0]
        target_ip = socket.gethostbyname(formatted_host)
        print(f"  [-] Resolved IP: {target_ip}")
        
        # Shodan Internet DB API Request (No API Key Required)
        url = f"https://internetdb.shodan.io/{target_ip}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # 1. Open Ports
            ports = data.get("ports", [])
            print(f"  [-] Open Ports Found: {ports}")
            
            # 2. Server Hostnames
            hostnames = data.get("hostnames", [])
            print(f"  [-] Associated Hostnames: {hostnames}")
            
            # 3. CPES (Software Fingerprinting)
            cpes = data.get("cpes", [])
            if cpes:
                print(f"  [-] Detected Software/Technologies:")
                for cpe in cpes[:5]: # Top 5 show karein
                    print(f"      • {cpe}")
            
            # 4. Vulnerabilities (CVEs) - Yeh sabse main part hai
            vulns = data.get("vulns", [])
            if vulns:
                print(f"\n  [!] VULNERABILITIES DETECTED ({len(vulns)} CVEs):")
                for vuln in vulns[:10]: # Top 10 CVEs display karein
                    print(f"      • {vuln} -> https://nvd.nist.gov/vuln/detail/{vuln}")
            else:
                print("\n  [✓] No public CVEs found on Shodan for this IP.")
                
            return f"IP: {target_ip}\nPorts: {ports}\nVulns: {len(vulns)}"
            
        elif response.status_code == 404:
            print("  [-] No data available in Shodan database for this IP.")
            return "No Shodan Data Found."
        else:
            print(f"  [X] API Error: Status Code {response.status_code}")
            return "Shodan API Error."

    except socket.gaierror:
        print("  [X] Could not resolve hostname. Check the domain name.")
        return "Resolution Failed."
    except Exception as e:
        print(f"  [X] Error: {str(e)}")
        return f"Error: {str(e)}"
      
