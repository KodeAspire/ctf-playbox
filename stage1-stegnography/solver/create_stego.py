
"""
Stage 1: The Altered ID - Steganography Artifact Generator

Creates an employee ID image and embeds a hidden message using Steghide.

Author: IT24100368 Thaveesha L.H.K
Group: 39

Required tools:
- Python 3
- Pillow
- Steghide

Player extraction password: rabbit
"""

from PIL import Image, ImageDraw, ImageFont
import os
import shutil
import subprocess
import tempfile

# ============================================================
# PATHS - Updated to match new structure (challenge/ folder)
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHALLENGE_DIR = os.path.abspath(
    os.path.join(SCRIPT_DIR, "..", "challenge")
)

ORIGINAL_IMAGE = os.path.join(CHALLENGE_DIR, "original_id.jpg")
FINAL_IMAGE = os.path.join(CHALLENGE_DIR, "rabbit_id.jpg")

PASSWORD = "rabbit"

# ============================================================
# HIDDEN MESSAGE - This is what the player will extract
# Line 1: Stage 1 clue (leads to Lizard)
# Line 2: Stage 1 flag
# Line 3: Stage 2 Base64 encoded string 
# ============================================================
SECRET_MESSAGE = (
    "The person of interest is Leopold Lizard.\n"
    "FLAG{St3g4n0gr4phy_1s_Fun}\n"
    "VGhlIHBlcnNvbiBvZiBpbnRlcmVzdCBpcyBMZW9wb2xkIExpemFyZC4g"
    "RkxBR3tsMXo0cmRfYzFwaDNyfQ=="
)


def create_id_card():
    """Create the original employee ID card image."""

    os.makedirs(CHALLENGE_DIR, exist_ok=True)

    img = Image.new("RGB", (600, 400), color="white")
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arial.ttf", 28)
        text_font = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Border
    draw.rectangle(
        [(10, 10), (590, 390)],
        outline="black",
        width=3
    )

    # Header
    draw.rectangle(
        [(10, 10), (590, 70)],
        fill="#1a237e"
    )
    draw.text(
        (30, 25),
        "NILE TECHNOLOGIES PVT LTD",
        fill="white",
        font=title_font
    )

    # Title
    draw.text(
        (30, 90),
        "EMPLOYEE IDENTIFICATION CARD",
        fill="black",
        font=text_font
    )

    # Photo placeholder
    draw.rectangle(
        [(30, 130), (180, 280)],
        outline="black",
        width=2
    )
    draw.text(
        (50, 200),
        "PHOTO",
        fill="gray",
        font=text_font
    )

    # Employee details
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
        draw.text(
            (200, y_pos),
            label,
            fill="black",
            font=text_font
        )
        draw.text(
            (320, y_pos),
            value,
            fill="black",
            font=text_font
        )
        y_pos += 30

    # Footer
    draw.rectangle(
        [(10, 350), (590, 390)],
        fill="#1a237e"
    )
    draw.text(
        (30, 360),
        "If found, please return to HR Department",
        fill="white",
        font=text_font
    )

    img.save(ORIGINAL_IMAGE, format="JPEG", quality=95)

    print(f"[+] Original ID card created: {ORIGINAL_IMAGE}")
    return ORIGINAL_IMAGE


def embed_message():
    """Embed the secret message into the ID image using Steghide."""

    if shutil.which("steghide") is None:
        raise RuntimeError(
            "Steghide is not installed or is not available in PATH."
        )

    if not os.path.exists(ORIGINAL_IMAGE):
        print("[!] Original image not found. Creating it...")
        create_id_card()

    # Create a temporary payload file in the solver directory.
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".txt",
            prefix="stage1_payload_",
            dir=SCRIPT_DIR,
            delete=False
        ) as temp_file:
            temp_file.write(SECRET_MESSAGE)
            temp_path = temp_file.name

        # Generate the final steganographic image.
        command = [
            "steghide",
            "embed",
            "-cf", ORIGINAL_IMAGE,
            "-ef", temp_path,
            "-sf", FINAL_IMAGE,
            "-p", PASSWORD,
            "-f"
        ]

        subprocess.run(command, check=True)

        print(f"[+] Hidden message embedded: {FINAL_IMAGE}")
        return FINAL_IMAGE

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def verify_extraction():
    """Verify the payload can be extracted using the expected password."""

    if not os.path.exists(FINAL_IMAGE):
        print("[!] Final image not found.")
        return False

    extracted_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".txt",
            prefix="stage1_verify_",
            dir=SCRIPT_DIR,
            delete=False
        ) as temp_file:
            extracted_path = temp_file.name

        command = [
            "steghide",
            "extract",
            "-sf", FINAL_IMAGE,
            "-p", PASSWORD,
            "-xf", extracted_path,
            "-f"
        ]

        subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        with open(extracted_path, "r", encoding="utf-8") as file:
            extracted_message = file.read()

        if extracted_message == SECRET_MESSAGE:
            print("[OK] Steghide extraction verification successful!")
            print("[OK] The extracted payload matches the expected message.")
            return True

        print("[!] Verification failed: extracted content differs.")
        return False

    except (subprocess.CalledProcessError, OSError) as error:
        print(f"[!] Extraction verification failed: {error}")
        return False

    finally:
        if extracted_path and os.path.exists(extracted_path):
            os.remove(extracted_path)


def main():
    """Generate and verify the Stage 1 challenge."""

    print("=" * 60)
    print("Stage 1: The Altered ID")
    print("Steghide Artifact Generator")
    print("=" * 60)

    try:
        print("\n[Step 1] Checking the original image...")
        if not os.path.exists(ORIGINAL_IMAGE):
            create_id_card()
        else:
            print(f"[+] Using existing image: {ORIGINAL_IMAGE}")

        print("\n[Step 2] Embedding hidden message with Steghide...")
        embed_message()

        print("\n[Step 3] Verifying extraction...")
        if not verify_extraction():
            print("[ERROR] Challenge verification failed.")
            raise SystemExit(1)

        print("\n" + "=" * 60)
        print("[SUCCESS] Stage 1 challenge generated and verified.")
        print(f"Player image: {FINAL_IMAGE}")
        print("Extraction password: rabbit")
        print("=" * 60)

    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"\n[ERROR] {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()