# Operation Rabbit - Play Box

A Capture The Flag (CTF) Play Box designed as part of Module IE3132 - Penetration Testing, Assignment: CTF Play Box Implementation


## Overview

This CTF follows the story of investigating Ms. Rabbit, the replacement manager to Mr. Fish O' Nile, being unable to 
log in to her company account. The challenge follows six stages with increasing 


## Team

1. Dissanayake D.M.K.H (IT24102109) - Platform architecture and network topology design. Deployment plan development
2. Fernando S.K (IT24100860) - Challenge Stages 2, 3, 5
3. Thaveesha L.H.K (IT24100368) - Challenge Stage 1, 4, 6
4. Santhilani W.M.K (IT24101240) - Testing criteria, analysis of risks and limitations of projects


## Live Playthrough (Local)

The box is designed to be deployed locally by anyone with Docker.

# bash
git clone https://github.com/KodeAspire/ctf-playbox.git
cd ctf-playbox
docker compose up -d

# Wait ~30 seconds for initialization, then open:

CTF Platform: http://localhost:8000

## Requirements

Docker Engine 24.0 or later
Docker Compose v2.0 or later
4 GB RAM minimum for the Ubuntu VM
25 GB free disk space
Linux, macOS, or Windows (with Docker Desktop)
No external dependencies or internet access is required once images are pulled.

## Quick Start

git clone <REPO_URL>
cd ctf-playbox
docker compose up -d
Navigate to http://localhost:8000 in a browser.
Click Register and create an account. You will be dropped into the first stage.

## Services

Service	Network	Purpose	Port
ctfd	ctfdnet	CTF platform	8000 (host)
db	ctfdnet	MariaDB (challenges, users, flags)	internal
cache	ctfdnet	Redis (session cache)	internal
db-seed	ctfdnet	One-shot seeder — loads seed.sql on first boot	none
stage5-linux	challnet	SSH Linux challenge container	2222 (host)
stage3-intranet	challnet	Nginx serving Stage 3 HTML pages	8080 (host)
Network Segmentation

ctfdnet — Platform services only. Contains CTFd, its database, and Redis.
challnet — Challenge services only. Contains the Stage 5 container and the Stage 3 intranet.
Containers on different Docker networks cannot reach each other by default. 

This means:

The Stage 5 challenge container cannot reach CTFd, the database, or Redis.
The Stage 3 intranet server cannot reach the platform.
Even if a player fully compromises the challenge container, they cannot pivot to the CTF platform.
Firewall

## The Ubuntu VM uses UFW to restrict inbound traffic.

bash
sudo ufw status
Expected rules:

## Port	Purpose
22/tcp	Admin SSH (optional — disable if managing via console)
8000/tcp	CTFd platform
8080/tcp	Stage 3 intranet
2222/tcp	Stage 5 SSH challenge
All other ports are denied by default.

Note on Docker and UFW: Docker manipulates iptables directly and can bypass UFW rules for published container ports. Only ports explicitly published in docker-compose.yml should be considered exposed. The rules above ensure the host's own services (SSH, etc.) remain protected.

## Challenge Progression

Six stages across six cybersecurity domains, with a shared narrative.


1	The Altered ID - Steganography -	Easy
2	The Lizard Cipher -	Cryptography -	Easy
3	Who is Lizard? - OSINT / Reconnaissance - 	Moderate
4	The Onboarding Evidence	- Digital Forensics -	Moderate
5	The Forgotten Permission - Linux / System Security	- Moderate–Hard
6	The Final Trace	- Networking	- Hard

Stages unlock sequentially. Each flag is formatted as FLAG{...}.

## Reset / Recovery

Two reset scripts are included at the repository root.

## Full platform reset

Wipes all data (users, scores, submissions) and restores the CTF from the seed.

bash
./reset-all.sh
Equivalent to:

bash
docker compose down -v
docker compose up -d
Stage 5 container reset

Rebuilds only the Stage 5 challenge container. Player scores and CTFd state are preserved.

bash
./reset-stage5.sh
Equivalent to:

bash
docker compose up -d --force-recreate --build stage5-linux
Verification

A deployment verification script is included:

bash
./verify-deployment.sh
It checks:

## Container status
CTFd reachability (HTTP)
Stage 5 SSH port availability
Stage 3 intranet port availability
Database seed status (user count)
Isolation — confirms the Stage 5 container cannot resolve ctfd
UFW rules
Directory Structure


## Manual Deployment Notes

First-time setup

The very first docker compose up -d will:

Start MariaDB and wait for it to become healthy.
Run the db-seed service, which loads seed.sql if the database is empty.
Start Redis.
Start CTFd once the seed is complete.
Build and start the Stage 5 challenge container.
Start the Stage 3 intranet server.
Total startup time on a fresh machine: 30–60 seconds.

## Stopping the box

bash
docker compose down
Stopping and clearing data

bash
docker compose down -v
The next up will re-seed from seed.sql.

## Viewing logs

bash
docker compose logs -f <service>
Example:

bash
docker compose logs -f ctfd
Troubleshooting

Port already in use

If port 8000, 8080, or 2222 is already bound on the host, either stop the conflicting service or change the published port in docker-compose.yml.

CTFd shows the setup wizard instead of challenges

The database did not seed. Check:

bash
docker compose logs db-seed
If it says "database already populated" but you expected a fresh CTF, run:

bash
docker compose down -v
docker compose up -d
Stage 5 SSH connection refused

Check that the container is running:

bash
docker compose ps
docker compose logs stage5-linux
Then retry:

bash
ssh investigator@localhost -p 2222
Uploads hang in CTFd

The CTFd service requires write access to /var/lib/ctfd/uploads inside the container. This is handled by the user: root directive in docker-compose.yml. If uploads still fail, restart the container:

bash
docker compose restart ctfd
Firewall blocking access from Kali VM

## Ensure UFW has rules for ports 8000, 8080, and 2222:

bash
sudo ufw allow 8000/tcp
sudo ufw allow 8080/tcp
sudo ufw allow 2222/tcp
Security Model

## Control	Implementation
Network isolation	Separate Docker bridge networks (ctfdnet / challnet)
Host firewall	UFW — only required ports exposed
CTFd authentication	Role-based (admin / player), public registration enabled
Flag validation	Platform-based (CTFd submissions table)
Stage 5 privilege separation	Low-privilege investigator account; escalation limited to sudo -u lizard
Evidence integrity (Stage 4)	SHA-256 hash manifest provided to players

## Acknowledgments

CTFd — CTF platform (https://github.com/CTFd/CTFd)
MariaDB — database
Redis — session cache
Nginx — static intranet server
Steghide — steganography tool (used to embed Stage 1 payload)
Wireshark — packet capture analysis (Stage 6)
Autopsy — used to generate Stage 4 forensics evidence
Challenge development and content by Group 39. Platform, architecture, and infrastructure by Member 1.




