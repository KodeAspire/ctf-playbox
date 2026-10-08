# Stage 1: The Altered ID

| Field | Details |
|-------|---------|
| **Stage ID** | STG-01 |
| **Domain** | Steganography |
| **Difficulty** | Easy |
| **Author** | IT24100368 Thaveesha L.H.K |

## Scenario

Ms. Fluffy Rabbit, a newly onboarded employee at Nile Technologies, 
cannot access her account after a suspicious credential change. 

Support Services approved the credential change based on an ID photo 
submitted by someone claiming to be Ms. Rabbit. Security believes the 
photo was modified and contains hidden information.

You are the investigator assigned to examine the ID photo.

## Objective

Download the provided ID card image and discover the hidden message 
embedded within it. The hidden message will provide a clue for the 
next stage.

## Files Provided

- `rabbit_id.jpg` - The suspicious ID card photo

## Tools You May Need

- `exiftool` - To inspect image metadata
- `steghide` - To detect and extract hidden data
- `binwalk` - To detect embedded files (alternative)
- `strings` - To find readable strings (alternative)

## Hints

1. Inspect the file before assuming it is an ordinary photograph.
2. Look for tools designed to detect hidden data in files.
3. The password for extraction is related to the scenario — try "rabbit".

## Flag Format

`FLAG{...}`

## Learning Outcome

After completing this stage, you should be able to:
- Inspect file metadata using ExifTool
- Detect steganographic content in images
- Extract hidden payloads using Steghide
