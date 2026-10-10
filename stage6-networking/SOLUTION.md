
# Stage 6 Solution — The Final Trace

## Expected Findings

- Transfer identifier: XFER-6F2A-ONB2048
- Transferred filename: rabbit_id.jpg
- Recipient: fish@badcomp.com
- Synthetic destination IP: 203.0.113.66
- Synthetic destination TCP port: 8088

## Investigation

1. Open rabbit_traffic.pcapng in Wireshark.
2. Inspect Statistics > Conversations > TCP.
3. Locate the connection from 10.10.6.25 to 203.0.113.66.
4. Filter with:

   ip.addr == 203.0.113.66 && tcp.port == 8088

5. Select a packet from that connection.
6. Choose Follow > TCP Stream.
7. Inspect the synthetic request for X-Transfer-ID, X-Recipient,
   and the transferred filename.

## Conclusion

The synthetic capture represents a transfer of rabbit_id.jpg
associated with XFER-6F2A-ONB2048 and the intended recipient
fish@badcomp.com.

All addresses and application data are fictional training evidence.