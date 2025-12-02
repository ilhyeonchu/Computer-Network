import subprocess
import sys

def run_cmd(container, cmd):
    return subprocess.run(['docker','exec',container,'vtysh','-c',cmd], capture_output=True,text=True).stdout.strip()

def generate_report(container):
    print(f"### Report for {container} ###\n")
    
    print(">> show ip route")
    print(run_cmd(container,'show ip route'))
    print("\n>> show ip rip")
    print(run_cmd(container, 'show ip rip'))
    print("\n>> show running-config")
    print(run_cmd(container,'show running-config'))

if __name__=="__main__":
    if len(sys.argv) !=2:
        print("Usage: ./report.py <router_name>")
        sys.exit(1)
    generate_report(sys.argv[1])