
from pathlib import Path
import hashlib
import json

from scapy.all import Ether, IP, TCP, Raw
from scapy.utils import PcapWriter


# --------------------------------------------------
# Stage 6: The Final Trace
# Creates a synthetic, offline network capture.
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
CHALLENGE = ROOT / "challenge"

CAPTURE = CHALLENGE / "rabbit_traffic.pcap"
MANIFEST = CHALLENGE / "capture_manifest.json"

# Documentation-only IP addresses; no real traffic is sent.
CLIENT_IP = "10.10.6.25"
PORTAL_IP = "192.0.2.20"
DEST_IP = "203.0.113.66"

CLIENT_MAC = "02:00:00:00:06:25"
PORTAL_MAC = "02:00:00:00:06:20"
DEST_MAC = "02:00:00:00:06:66"

TRANSFER_ID = "XFER-6F2A-ONB2048"
FILENAME = "rabbit_id.jpg"
RECIPIENT = "fish@badcomp.com"


def make_packet(src_mac, dst_mac, src_ip, dst_ip,
                sport, dport, flags, seq, ack,
                timestamp, payload=b""):
    """Create one synthetic Ethernet/TCP packet."""

    packet = (
        Ether(src=src_mac, dst=dst_mac)
        / IP(src=src_ip, dst=dst_ip)
        / TCP(
            sport=sport,
            dport=dport,
            flags=flags,
            seq=seq,
            ack=ack
        )
    )

    if payload:
        packet = packet / Raw(load=payload)

    packet.time = float(timestamp)
    return packet


def add_tcp_session(writer, server_ip, server_mac,
                    client_port, server_port,
                    host, request, response, start_time):
    """Write a small synthetic TCP session to the PCAP."""

    client_seq = 1000
    server_seq = 7000

    request_bytes = request.encode("ascii")
    response_bytes = response.encode("ascii")

    packets = [
        # 1. Client starts TCP connection
        make_packet(
            CLIENT_MAC, server_mac,
            CLIENT_IP, server_ip,
            client_port, server_port,
            "S", client_seq, 0,
            start_time
        ),

        # 2. Server responds
        make_packet(
            server_mac, CLIENT_MAC,
            server_ip, CLIENT_IP,
            server_port, client_port,
            "SA", server_seq, client_seq + 1,
            start_time + 0.01
        ),

        # 3. Client acknowledges
        make_packet(
            CLIENT_MAC, server_mac,
            CLIENT_IP, server_ip,
            client_port, server_port,
            "A", client_seq + 1, server_seq + 1,
            start_time + 0.02
        ),

        # 4. Client sends HTTP-like request
        make_packet(
            CLIENT_MAC, server_mac,
            CLIENT_IP, server_ip,
            client_port, server_port,
            "PA", client_seq + 1, server_seq + 1,
            start_time + 0.03, request_bytes
        ),

        # 5. Server returns a response
        make_packet(
            server_mac, CLIENT_MAC,
            server_ip, CLIENT_IP,
            server_port, client_port,
            "PA", server_seq + 1,
            client_seq + 1 + len(request_bytes),
            start_time + 0.04, response_bytes
        ),

        # 6. Server closes the connection
        make_packet(
            server_mac, CLIENT_MAC,
            server_ip, CLIENT_IP,
            server_port, client_port,
            "FA", server_seq + 1 + len(response_bytes),
            client_seq + 1 + len(request_bytes),
            start_time + 0.05
        ),

        # 7. Client acknowledges server's FIN
        make_packet(
            CLIENT_MAC, server_mac,
            CLIENT_IP, server_ip,
            client_port, server_port,
            "A",
            client_seq + 1 + len(request_bytes),
            server_seq + 2 + len(response_bytes),
            start_time + 0.06
        ),
    ]

    for packet in packets:
        writer.write(packet)


def main():
    CHALLENGE.mkdir(parents=True, exist_ok=True)

    # Remove any old output so the new file is generated cleanly.
    if CAPTURE.exists():
        CAPTURE.unlink()

    # Session 1: Ordinary onboarding status request.
    normal_request = (
        "GET /status HTTP/1.1\r\n"
        "Host: onboarding.internal\r\n"
        "User-Agent: CTF-Client/1.0\r\n"
        "Connection: close\r\n"
        "\r\n"
    )

    normal_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Content-Length: 2\r\n"
        "Connection: close\r\n"
        "\r\n"
        "OK"
    )

    # Session 2: Suspicious synthetic file-transfer request.
    body = FILENAME
    suspicious_request = (
        "POST /synthetic-transfer HTTP/1.1\r\n"
        f"Host: {DEST_IP}:{8088}\r\n"
        "User-Agent: CTF-Client/1.0\r\n"
        f"X-Transfer-ID: {TRANSFER_ID}\r\n"
        f"X-Recipient: {RECIPIENT}\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{body}"
    )

    suspicious_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Content-Length: 15\r\n"
        "Connection: close\r\n"
        "\r\n"
        "Transfer logged"
    )

    # Use classic PCAP format with Ethernet link-layer packets.
    writer = PcapWriter(
        str(CAPTURE),
        linktype=1,
        sync=True
    )

    try:
        add_tcp_session(
            writer=writer,
            server_ip=PORTAL_IP,
            server_mac=PORTAL_MAC,
            client_port=49160,
            server_port=8080,
            host="onboarding.internal",
            request=normal_request,
            response=normal_response,
            start_time=1785575700.0
        )

        add_tcp_session(
            writer=writer,
            server_ip=DEST_IP,
            server_mac=DEST_MAC,
            client_port=49161,
            server_port=8088,
            host=DEST_IP,
            request=suspicious_request,
            response=suspicious_response,
            start_time=1785576000.0
        )
    finally:
        writer.close()

    # Verify the output exists and is not empty.
    if not CAPTURE.exists() or CAPTURE.stat().st_size == 0:
        raise RuntimeError("Capture generation failed: file is empty.")

    # Generate a SHA-256 manifest.
    digest = hashlib.sha256(CAPTURE.read_bytes()).hexdigest()

    manifest_data = {
        "file": CAPTURE.name,
        "format": "classic PCAP",
        "sha256": digest,
        "purpose": (
            "Synthetic offline CTF network traffic. "
            "Contains a normal session and a simulated transfer session."
        )
    }

    MANIFEST.write_text(
        json.dumps(manifest_data, indent=4),
        encoding="utf-8"
    )

    print(f"[+] Created: {CAPTURE}")
    print(f"[+] Size: {CAPTURE.stat().st_size} bytes")
    print(f"[+] SHA-256: {digest}")
    print("[PASS] Normal traffic session included")
    print("[PASS] Synthetic transfer session included")
    print("[PASS] Capture file is not empty")
    print("[SUCCESS] Stage 6 capture generated.")


if __name__ == "__main__":
    main()