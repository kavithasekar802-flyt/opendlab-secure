# Passive ACARS / VDL2 receive-only extension

Goal: learn how real air/ground datalink traffic is structured and instrumented without
transmitting anything.

Candidate toolchain:
- receive-only RTL-SDR-class device
- dumpvdl2
- libacars
- acarsdec
- Wireshark / JSON processing

Portfolio outputs:
- receiver setup notes
- decoder health metrics
- protocol-stack diagram
- sanitized screenshots of decoded structure
- comparison between observed protocol layering and OpenDLab abstractions

Privacy:
Avoid publishing message content that can identify crew, passengers, operational details or
other nonessential sensitive information. Prefer protocol metadata and sanitized examples.
