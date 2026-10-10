
# Stage 6: The Final Trace

**Stage ID:** STG-06  
**Domain:** Networking  
**Difficulty:** Hard

## Scenario

Previous investigation stages established that Lizard sent Rabbit's
identity information to an external recipient. Investigators must now
examine a controlled network capture to determine what happened during
the synthetic transfer.

## Objective

Analyze `challenge/rabbit_traffic.pcap` in Wireshark and identify:

- The suspicious network conversation
- The application-level transfer identifier
- The transferred filename
- The intended destination

## Required Tool

Wireshark.

## Instructions

1. Open `challenge/rabbit_traffic.pcap`.
2. Review the conversations and TCP traffic.
3. Identify the suspicious destination and service.
4. Right-click a relevant packet and select Follow > TCP Stream.
5. Inspect the application data and record the requested values.

## Safety

This capture contains synthetic, offline-generated training traffic.
It does not represent a real incident and does not require external
network access.

## Learning Objectives

- Packet-capture analysis
- TCP conversation tracing
- Application-layer inspection
- Evidence correlation