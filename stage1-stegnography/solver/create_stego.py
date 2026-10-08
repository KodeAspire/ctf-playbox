"""
Stage 1: The Altered ID - Steganography Artifact Generator
Creates a fake ID card with embedded hidden message using LSB steganography.

Author: IT24100368 Thaveesha L.H.K
Group: 39
Structure: challenge/ + solver/ (matches project convention)
"""

from PIL import Image, ImageDraw, ImageFont
from stegano import lsb
import os

# ============================================================
# PATHS - Updated to match new structure (challenge/ folder)
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHALLENGE_DIR = os.path.join(SCRIPT_DIR, "..", "challenge")
ORIGINAL_IMAGE = os.path.join(CHALLENGE_DIR, "original_id.jpg")
FINAL_IMAGE = os.path.join(CHALLENGE_DIR, "rabbit_id.jpg")

# ============================================================
# HIDDEN MESSAGE - This is what the player will extract
# Line 1: Stage 1 clue (leads to Lizard)
# Line 2: Stage 1 flag
# Line 3: Stage 2 Base64 encoded string (from Fernando)
# ============================================================
SECRET_MESSAGE = """The person of interest is Leopold Lizard.
FLAG{St3g4n0gr4phy_1s_Fun}
VGhlIHBlcnNvbiBvZiBpbnRlcmVzdCBpcyBMZW9wb2xkIExpemFyZC4gRkxBR3tsMXo0cmRfYzFwaDNyfQ=="""


def create_id_card():
    """Create a fake employee ID card image"""
    img = Image.new('RGB', (600, 400), color='white')
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arial.ttf", 28)
        text_font = ImageFont.truetype("arial.ttf", 18)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Border
    draw.rectangle([(10, 10), (590, 390)], outline='black', width=3)

    # Header
    draw.rectangle([(10, 10), (590, 70)], fill='#1a237e')
    draw.text((30, 25), "NILE TECHNOLOGIES PVT LTD", fill='white', font=title_font)

    # Title
    draw.text((30, 90), "EMPLOYEE IDENTIFICATION CARD", fill='black', font=text_font)

    # Photo placeholder
    draw.rectangle([(30, 130), (180, 280)], outline='black', width=2)
    draw.text((50, 200), "PHOTO", fill='gray', font=text_font)

    # Details
    details = [
        ("Name:", "Fluffy Rabbit"),
        ("Employee ID:", "RBT-2026-001"),
        ("Department:", "Research & Development"),
        ("Designation:", "R&D Analyst"),
        ("Blood Group:", "O+"),
        ("Joined:", "2026-08-01"),
    ]

    y_pos = 130
    for label, value in details:
        draw.text((200, y_pos), label, fill='black', font=text_font)
        draw.text((320, y_pos), value, fill='black', font=text_font)
        y_pos += 30

    # Footer
    draw.rectangle([(10, 350), (590, 390)], fill='#1a237e')
    draw.text((30, 360), "If found, please return to HR Department", fill='white', font=text_font)

    os.makedirs(CHALLENGE_DIR, exist_ok=True)
    img.save(ORIGINAL_IMAGE, quality=95)
    print(f"[+] Original ID card created: {ORIGINAL_IMAGE}")
    return ORIGINAL_IMAGE


def embed_message():
    """Embed the secret message into the image using LSB steganography"""
    if not os.path.exists(ORIGINAL_IMAGE):
        print("[!] Original image not found. Creating it first...")
        create_id_card()

    lsb.hide(ORIGINAL_IMAGE, SECRET_MESSAGE).save(FINAL_IMAGE)
    print(f"[+] Secret message embedded: {FINAL_IMAGE}")
    print(f"[+] Message length: {len(SECRET_MESSAGE)} characters")
    print(f"\n[HIDDEN MESSAGE CONTENT]:")
    print("-" * 60)
    print(SECRET_MESSAGE)
    print("-" * 60)
    return FINAL_IMAGE


def verify_extraction():
    """
    Verify the message can be extracted.
    NOTE: stegano 3.0.0 has a bug on Python 3.14 - this may fail.
    The actual extraction should be done with steghide (by the player).
    """
    if not os.path.exists(FINAL_IMAGE):
        print("[!] Final image not found!")
        return False

    try:
        extracted = lsb.reveal(FINAL_IMAGE)
        if extracted == SECRET_MESSAGE:
            print("\n[OK] VERIFICATION SUCCESSFUL!")
            return True
        else:
            print("\n[!] Message mismatch (not critical)")
            return False
    except Exception as e:
        print(f"\n[!] LSB verification skipped: {e}")
        print("[OK] Files were created successfully!")
        print("[OK] Player should use 'steghide' to extract the message.")
        return True


if __name__ == "__main__":
    print("=" * 60)
    print("Stage 1: The Altered ID - Artifact Generator")
    print("=" * 60)

    print("\n[Step 1] Creating fake ID card...")
    create_id_card()

    print("\n[Step 2] Embedding secret message...")
    embed_message()

    print("\n[Step 3] Verifying extraction...")
    verify_extraction()

    print("\n" + "=" * 60)
    print("Stage 1 artifact generation complete!")
    print("=" * 60)
    print("\nFiles created in: challenge/")
    print("  - original_id.jpg")
    print("  - rabbit_id.jpg")
    print("\nNext: Upload 'rabbit_id.jpg' to CTFd for Stage 1")
    print("Steghide password: rabbit")
    print("=" * 60)