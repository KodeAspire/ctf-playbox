import paramiko

host = "localhost"
port = 2222
user = "investigator"
password = "investigator123"

print("[*] Connecting to Stage 5 container...")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port=port, username=user, password=password)

print("[+] Connected as investigator")

def run(cmd):
    stdin, stdout, stderr = client.exec_command(cmd)
    return stdout.read().decode() + stderr.read().decode()

print("\n[*] Investigating Lizard's account...")
print(run("sudo -u lizard find / -group legacy_proj -type f 2>/dev/null"))

print("[*] Reading protected evidence...")
print(run("sudo -u lizard cat /srv/onboarding_evidence/rabbit_id.txt"))

client.close()
print("[+] Done")