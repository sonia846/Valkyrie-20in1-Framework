import json
from datetime import datetime

def generate_report(target, scan_results):
    print(f"\n[+] Activating Executive Technical Reporting Engine...")
    print(f"  [-] Compiling vulnerability logs for: {target}")
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"Valkyrie_Report_{timestamp}.txt"
    
    try:
        with open(report_filename, "w") as report:
            report.write("="*60 + "\n")
            report.write("       VALKYRIE VULNERABILITY AUDIT REPORT (PRO)     \n")
            report.write("="*60 + "\n")
            report.write(f"[-] Target Domain : {target}\n")
            report.write(f"[-] Scan Timestamp: {datetime.now()}\n")
            report.write(f"[-] Framework     : Valkyrie Security Suite v2.0\n")
            report.write("="*60 + "\n\n")
            
            report.write("[+] MODULE EXECUTION SUMMARY:\n")
            for module_name, status in scan_results.items():
                report.write(f"    • {module_name}: {status}\n")
                
            report.write("\n" + "="*60 + "\n")
            report.write("END OF EXECUTIVE REPORT - CONFIDENTIAL DATA\n")
            report.write("="*60 + "\n")
            
        print(f"  [✓] Technical Plain Text File (.txt) Compiled successfully!")
        print(f"  [✓] Executive Report Saved As: {report_filename}")
        return report_filename

    except Exception as e:
        print(f"  [X] Failed to write report file: {str(e)}")
        return None
