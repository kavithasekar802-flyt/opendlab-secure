# ARINC 429 home-bench extension

Preferred low-cost direction:
- RP2040/RP2350/Pico-class microcontroller
- open-source ARINC429 proof-of-concept transceiver design
- isolated loopback TX -> RX
- USB serial/Ethernet bridge to the Linux test host

Minimum measurements:
- correct word count
- label filtering
- parity error detection
- rate selection test
- missing-word timeout
- burst/stress run
- timestamp correlation with host logs

Do not connect experimental hardware to actual aircraft wiring or avionics.
If you later obtain a commercial ARINC429 USB/Ethernet adapter, keep the same software API
so that the test procedures remain hardware-independent.
