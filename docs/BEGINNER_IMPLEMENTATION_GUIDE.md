# OpenDLab-Secure — Beginner Implementation & Execution Guide

Audience: complete beginner with a Windows laptop, Visual Studio Code and a GitHub account.

Goal: build, run, test and document the OpenDLab-Secure software avionics datalink integration bench first, then expand it toward network impairment, IPv6/ATN-IPS-inspired experiments, ARINC 429 hardware-in-the-loop and passive receive-only VDL2 observation.

> SAFETY / SCOPE
>
> - This is an educational laboratory simulator, not airworthy equipment.
> - Never connect experimental electronics to a real aircraft or aircraft wiring.
> - Never transmit on aviation VHF/HF/SATCOM frequencies.
> - Nmap scans in this guide are only for your own laptop / private isolated lab.
> - The ARINC 429 implementation is educational and is not a replacement for the official specification.

---

## 0. What you are building

The first working system is:

```text
Aircraft Application Simulator
        |
        | UDP 127.0.0.1:5000
        v
Datalink Router
  - validates message
  - applies source/destination/service policy
  - chooses simulated bearer
        |
        | UDP 127.0.0.1:5100
        v
Ground Station Simulator

Evidence:
  router_events.jsonl
  ground_events.jsonl
  pytest results
  packet capture (.pcap)
```

The starter router has three logical bearers:

- `VDL2_SIM`: lowest cost, normal choice for ordinary AOC messages.
- `SATCOM_SIM`: fallback choice when VDL2 is unavailable.
- `WIFI_LAB`: lowest nominal latency, chosen for high-priority ATS messages in the starter policy.

The initial bench is entirely software-based. Do not buy hardware before completing the software milestones.

---

# PART A — PREPARE THE WINDOWS / LINUX DEVELOPMENT ENVIRONMENT

## 1. Confirm Windows version

Press `Windows + R`, type:

```text
winver
```

Windows 11 is ideal. Modern Windows 10 also supports WSL2.

## 2. Install WSL2 and Ubuntu

Open **Windows PowerShell as Administrator**.

First see whether WSL already exists:

```powershell
wsl --status
```

If WSL is not installed, run:

```powershell
wsl --install
```

Restart Windows when requested.

If you want to explicitly use Ubuntu 24.04, first list available distributions:

```powershell
wsl --list --online
```

Then, if `Ubuntu-24.04` is listed:

```powershell
wsl --install -d Ubuntu-24.04
```

After installation, launch Ubuntu from the Start menu.

The first launch asks you to create:

- a Linux username
- a Linux password

The password does not display characters while you type. This is normal Linux behavior.

## 3. Verify WSL

In Ubuntu:

```bash
uname -a
cat /etc/os-release
pwd
whoami
```

You should see Linux / Ubuntu information and a home directory similar to:

```text
/home/kavitha
```

## 4. Update Ubuntu

Run:

```bash
sudo apt update
sudo apt upgrade -y
```

Enter your Linux password when requested.

## 5. Install required tools

Run:

```bash
sudo apt install -y \
  python3 \
  python3-venv \
  python3-pip \
  git \
  unzip \
  nmap \
  tcpdump \
  iproute2 \
  jq
```

Check them:

```bash
python3 --version
git --version
nmap --version | head -n 1
tcpdump --version | head -n 1
ip -V
jq --version
```

## 6. Install VS Code extensions

VS Code itself remains installed on Windows.

Open VS Code and install these Microsoft extensions:

1. **WSL**
2. **Python**

Optional later:

- Python Environments
- GitHub Pull Requests and Issues

Do not install another copy of VS Code inside Ubuntu.

---

# PART B — GET THE PROJECT INTO WSL

## 7. Create a Linux project folder

In Ubuntu:

```bash
mkdir -p ~/projects
cd ~/projects
pwd
```

Expected path:

```text
/home/<your-linux-user>/projects
```

Keep the repository in the Linux filesystem, not under `/mnt/c`, because Linux development tools perform better against Linux filesystem files.

## 8. Download the corrected OpenDLab-Secure ZIP

Download the corrected project ZIP from ChatGPT into your normal Windows Downloads folder.

To make copying easy, from Ubuntu run:

```bash
cd ~/projects
explorer.exe .
```

Windows File Explorer opens the WSL `projects` folder.

Drag the downloaded ZIP from Windows Downloads into this folder.

Return to Ubuntu and run:

```bash
ls -lh
```

You should see:

```text
opendlab-kavitha-airbus-datalink-corrected.zip
```

## 9. Extract it

```bash
unzip opendlab-kavitha-airbus-datalink-corrected.zip
cd opendlab-kavitha-airbus-datalink
```

Verify the structure:

```bash
find . -maxdepth 2 -type f | sort
```

Important directories:

```text
src/        Python bench code
tests/      automated tests
configs/    sample lab configurations
docs/       test strategy / traceability / roadmap
scripts/    packet capture / Nmap / netem helpers
hardware/   future hardware notes
artifacts/  generated test evidence
```

## 10. Open the Linux project in VS Code

From the project root:

```bash
code .
```

VS Code should reopen showing a WSL indicator in the lower-left corner.

If `code` is not found:

1. Open VS Code normally in Windows.
2. Press `Ctrl+Shift+P`.
3. Run `WSL: Connect to WSL`.
4. Select **File > Open Folder**.
5. Open `/home/<linux-user>/projects/opendlab-kavitha-airbus-datalink`.

---

# PART C — CREATE THE PYTHON ENVIRONMENT

## 11. Create a virtual environment

In the VS Code terminal or Ubuntu terminal, from the project root:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Your prompt should begin with something like:

```text
(.venv)
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install project dependencies:

```bash
python -m pip install -r requirements.txt
```

Check:

```bash
python --version
python -m pip list
```

You should see at least `pytest` and `PyYAML`.

## 12. Select the venv in VS Code

Press:

```text
Ctrl+Shift+P
```

Select:

```text
Python: Select Interpreter
```

Choose the interpreter ending in:

```text
.venv/bin/python
```

---

# PART D — UNDERSTAND THE STARTER BEFORE RUNNING IT

## 13. Open the important source files

Read these in this order:

```text
src/common.py
src/aircraft_app.py
src/security_policy.py
src/datalink_router.py
src/ground_station.py
src/arinc429.py
src/config_control.py
```

Do not try to memorize them.

Understand only this flow initially:

```text
aircraft_app.py
     sends JSON UDP message
          |
          v
datalink_router.py
     checks security_policy.py
     chooses logical bearer
     logs router event
          |
          v
ground_station.py
     receives message
     logs ground event
```

The files under `configs/` currently act mainly as lab configuration/reference material; the starter's core routing/security values are still represented directly in Python code. Wiring all runtime policy into YAML is a later improvement task.

---

# PART E — RUN AUTOMATED REGRESSION TESTS

## 14. Run all tests

Make sure the venv is active:

```bash
source .venv/bin/activate
```

Then:

```bash
python -m pytest -q
```

Expected result:

```text
.........                                                                [100%]
9 passed
```

If you do not get `9 passed`, stop here and fix the problem before attempting the live bench.

## 15. Run tests verbosely

```bash
python -m pytest -v
```

Read each test name.

They currently validate:

- valid ARINC 429 pack/unpack
- ARINC parity corruption detection
- configuration drift detection
- normal bearer choice
- bearer failover policy
- high-priority low-latency choice
- valid security-policy message
- unauthorized source rejection
- unauthorized service rejection

## 16. Understand what “9 passed” proves

It proves the tested software functions passed those automated checks.

It does **not** prove:

- certified avionics compliance
- real VDL2 performance
- real SATCOM performance
- a complete Airbus ATSU implementation
- airworthiness

Always keep that distinction in your portfolio.

---

# PART F — RUN YOUR FIRST LIVE INTEGRATION TEST

You will now use three VS Code terminals.

## 17. Clear old evidence

In Terminal 1:

```bash
cd ~/projects/opendlab-kavitha-airbus-datalink
source .venv/bin/activate
rm -f artifacts/router_events.jsonl artifacts/ground_events.jsonl
```

## 18. Start the ground station

Terminal 1:

```bash
python -u -m src.ground_station
```

Expected:

```text
[GROUND] listening on udp://127.0.0.1:5100
```

Leave this running.

## 19. Start the datalink router

Open Terminal 2.

```bash
cd ~/projects/opendlab-kavitha-airbus-datalink
source .venv/bin/activate
python -u -m src.datalink_router
```

Expected start:

```text
[ROUTER] aircraft input udp://127.0.0.1:5000
[ROUTER] bearer health: ...
```

Leave this running.

## 20. Start the aircraft application

Open Terminal 3.

```bash
cd ~/projects/opendlab-kavitha-airbus-datalink
source .venv/bin/activate
python -u -m src.aircraft_app
```

It sends ten messages.

Expected aircraft output resembles:

```text
[AIRCRAFT] sent <uuid> AOC prio=5
[AIRCRAFT] sent <uuid> AOC prio=5
[AIRCRAFT] sent <uuid> ATS prio=1
...
```

## 21. Observe router behavior

Normal AOC messages should normally use:

```text
VDL2_SIM
```

High-priority ATS messages should use the lowest-latency healthy path in the starter policy:

```text
WIFI_LAB
```

This is intentional educational policy behavior.

## 22. Observe ground behavior

The ground terminal should receive ten messages.

Examples:

```text
[GROUND] bearer=VDL2_SIM id=<uuid> service=AOC
[GROUND] bearer=WIFI_LAB id=<uuid> service=ATS
```

## 23. Stop long-running processes

In router and ground terminals, press:

```text
Ctrl+C
```

Do not close VS Code until you have inspected evidence.

---

# PART G — INSPECT THE GENERATED TEST EVIDENCE

## 24. Count events

```bash
wc -l artifacts/router_events.jsonl artifacts/ground_events.jsonl
```

For the normal ten-message run you should see:

```text
10 artifacts/router_events.jsonl
10 artifacts/ground_events.jsonl
```

## 25. Pretty-print one router record

```bash
tail -n 1 artifacts/router_events.jsonl | jq .
```

Look for:

```text
event
bearer
message.msg_id
message.service
message.priority
message.payload
```

## 26. Pretty-print one ground record

```bash
tail -n 1 artifacts/ground_events.jsonl | jq .
```

The `msg_id` gives you a correlation key across aircraft/router/ground evidence.

---

# PART H — CAPTURE NETWORK TRAFFIC

## 27. Install Wireshark on Windows

Install the stable Windows x64 release from the official Wireshark site.

You can keep Wireshark on Windows and use `tcpdump` inside WSL to generate the packet file.

## 28. Start a packet capture

Run ground and router again as in the previous test.

Open Terminal 4:

```bash
cd ~/projects/opendlab-kavitha-airbus-datalink
sudo tcpdump -i lo -nn 'udp port 5000 or udp port 5100' -w artifacts/DL-NOM-001.pcap
```

Leave it running.

## 29. Generate traffic

Terminal 3:

```bash
python -u -m src.aircraft_app
```

After the ten messages finish, return to Terminal 4 and press:

```text
Ctrl+C
```

## 30. Verify the PCAP without Wireshark

```bash
tcpdump -nn -r artifacts/DL-NOM-001.pcap | head -n 20
```

You should see UDP traffic involving ports 5000 and 5100.

## 31. Open the capture in Windows Wireshark

```bash
explorer.exe artifacts
```

Double-click `DL-NOM-001.pcap`.

Useful Wireshark display filter:

```text
udp.port == 5000 || udp.port == 5100
```

Inspect packet timestamps and payload sizes.

---

# PART I — EXECUTE FORMAL TEST DL-NOM-001

## 32. Create a test evidence folder

```bash
mkdir -p artifacts/campaign_001/DL-NOM-001
```

After the run:

```bash
cp artifacts/router_events.jsonl artifacts/campaign_001/DL-NOM-001/
cp artifacts/ground_events.jsonl artifacts/campaign_001/DL-NOM-001/
cp artifacts/DL-NOM-001.pcap artifacts/campaign_001/DL-NOM-001/
```

Create a result file:

```bash
code artifacts/campaign_001/DL-NOM-001/result.md
```

Use this template:

```markdown
# DL-NOM-001 — Nominal Datalink Message Flow

## Objective
Verify that valid aircraft messages are accepted by the datalink router and received by the ground endpoint.

## Preconditions
- OpenDLab-Secure commit: <git SHA>
- VDL2_SIM healthy
- SATCOM_SIM healthy
- WIFI_LAB healthy
- Ground station running
- Router running

## Procedure
1. Clear previous logs.
2. Start ground station.
3. Start router.
4. Start packet capture.
5. Run aircraft application.
6. Stop packet capture.
7. Stop router and ground station.
8. Count router and ground events.

## Expected Result
- 10 valid aircraft messages generated.
- 10 router forward events.
- 10 ground receive events.
- AOC uses VDL2_SIM under normal policy.
- high-priority ATS uses WIFI_LAB under current starter policy.

## Actual Result
<record actual result>

## Verdict
PASS / FAIL

## Evidence
- router_events.jsonl
- ground_events.jsonl
- DL-NOM-001.pcap

## Observations
<notes>
```

This documentation step is as important as running the code.

---

# PART J — EXECUTE BEARER FAILOVER TEST DL-FAIL-002

## 33. Stop the normal router if it is running

Press `Ctrl+C`.

## 34. Restart with VDL2 disabled

```bash
VDL2_HEALTH=0 python -u -m src.datalink_router
```

Now normal AOC messages should move from `VDL2_SIM` to `SATCOM_SIM`.

High-priority ATS messages may still choose `WIFI_LAB`, because the current priority policy selects the lowest-latency healthy bearer.

## 35. Force all traffic to SATCOM for a simple demonstration

Stop the router and run:

```bash
VDL2_HEALTH=0 WIFI_HEALTH=0 python -u -m src.datalink_router
```

Run the aircraft application again:

```bash
python -u -m src.aircraft_app
```

Every accepted message should now be forwarded via:

```text
SATCOM_SIM
```

Record this as a separate failover demonstration.

## 36. Restore normal behavior

Stop the router and launch it normally:

```bash
python -u -m src.datalink_router
```

The environment flags disappear because they were applied only to the previous command.

---

# PART K — EXECUTE SECURITY NEGATIVE TEST SEC-002

## 37. Start ground and normal router

Keep them running.

## 38. Send an unauthorized source message

Open another terminal and run:

```bash
python - <<'PY'
import json
import socket

msg = {
    "msg_id": "SEC-002-DEMO",
    "source": "UNKNOWN_NODE",
    "destination": "GROUND_SIM",
    "service": "ATS",
    "priority": 1,
    "payload": {"text": "UNAUTHORIZED_TEST"},
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(json.dumps(msg).encode("utf-8"), ("127.0.0.1", 5000))
print("Unauthorized test message sent")
PY
```

Expected router output:

```text
[ROUTER] SECURITY REJECT source_not_whitelisted
```

The ground station should **not** receive that message.

## 39. Verify the security event

```bash
tail -n 5 artifacts/router_events.jsonl | jq .
```

Look for:

```text
"event": "security_reject"
"reason": "source_not_whitelisted"
"msg_id": "SEC-002-DEMO"
```

This is an important portfolio demonstration because it converts source/destination whitelisting experience into a controlled test case.

---

# PART L — EXECUTE SECURITY NEGATIVE TEST SEC-003

## 40. Send an unauthorized service

```bash
python - <<'PY'
import json
import socket

msg = {
    "msg_id": "SEC-003-DEMO",
    "source": "ACFT_SIM",
    "destination": "GROUND_SIM",
    "service": "DEBUG_ADMIN",
    "priority": 5,
    "payload": {"text": "UNAUTHORIZED_SERVICE_TEST"},
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(json.dumps(msg).encode("utf-8"), ("127.0.0.1", 5000))
print("Unauthorized-service test message sent")
PY
```

Expected:

```text
[ROUTER] SECURITY REJECT service_not_authorized
```

Again, the ground system must not receive the message.

---

# PART M — ARINC 429 SOFTWARE DEMONSTRATION

## 41. Run the existing automated ARINC tests

```bash
python -m pytest tests/test_arinc429.py -v
```

Expected:

```text
2 passed
```

## 42. Inspect a valid educational word manually

```bash
python - <<'PY'
from src.arinc429 import pack_word, unpack_word

word = pack_word(label=0o203, data=12345, sdi=1, ssm=0)
print("Packed word (hex):", hex(word))
print("Decoded:", unpack_word(word))
PY
```

Confirm:

```text
parity_valid: True
```

## 43. Inject a parity fault

```bash
python - <<'PY'
from src.arinc429 import pack_word, unpack_word

word = pack_word(label=0o203, data=12345, sdi=1, ssm=0)
corrupted = word ^ (1 << 12)

print("Good:", unpack_word(word))
print("Corrupted:", unpack_word(corrupted))
PY
```

Expected:

```text
Good ... parity_valid: True
Corrupted ... parity_valid: False
```

Document this as `A429-PAR-006`.

---

# PART N — CONFIGURATION BASELINE / DRIFT DEMONSTRATION

## 44. Run the automated drift test

```bash
python -m pytest tests/test_config_control.py -v
```

Expected:

```text
1 passed
```

## 45. Create a real project baseline manifest

From the project root:

```bash
python - <<'PY'
from src.config_control import make_manifest, save_manifest

files = [
    "configs/bearers.yaml",
    "configs/security_policy.yaml",
    "configs/flight_profile.yaml",
]

manifest = make_manifest(files)
save_manifest(manifest, "artifacts/config_baseline.json")
print(manifest)
PY
```

View it:

```bash
cat artifacts/config_baseline.json | jq .
```

## 46. Check the baseline

```bash
python - <<'PY'
import json
from src.config_control import compare_manifest

with open("artifacts/config_baseline.json", encoding="utf-8") as f:
    expected = json.load(f)

print(compare_manifest(expected))
PY
```

Expected values are all:

```text
OK
```

## 47. Demonstrate drift safely

First create a backup:

```bash
cp configs/bearers.yaml /tmp/bearers.yaml.backup
```

Temporarily edit one value in `configs/bearers.yaml` with VS Code, save it, then rerun the comparison.

Expected:

```text
configs/bearers.yaml: DRIFT
```

Restore immediately:

```bash
cp /tmp/bearers.yaml.backup configs/bearers.yaml
```

Run the comparison again and verify `OK`.

Do not commit the intentionally modified configuration.

---

# PART O — OWNED-LAB SERVICE INVENTORY WITH NMAP

## 48. Run only against your own local system

Start the router and ground station.

Then:

```bash
./scripts/lab_inventory.sh 127.0.0.1
```

The result is saved as:

```text
artifacts/nmap_inventory.txt
```

View it:

```bash
cat artifacts/nmap_inventory.txt
```

Note: UDP services may require different scan options and privileges; this basic inventory is primarily a disciplined demonstration of local service discovery. Never point this script at Airbus, airlines, airports, suppliers or systems that you do not own or have explicit authorization to test.

---

# PART P — VERSION CONTROL WITH GIT

## 49. Configure your Git identity

Use the name you want on GitHub commits:

```bash
git config --global user.name "Kavitha Sekar"
git config --global user.email "YOUR_GITHUB_EMAIL"
```

Check:

```bash
git config --global --list
```

## 50. Initialize the repository

From project root:

```bash
git init -b main
```

Check ignored files:

```bash
git status
```

Do not commit:

```text
.venv/
__pycache__/
raw private captures containing sensitive real-world data
passwords
API tokens
credentials
```

## 51. Make the first commit

```bash
git add .
git status
git commit -m "Initial OpenDLab-Secure avionics datalink test bench"
```

Get the commit SHA:

```bash
git rev-parse HEAD
```

Use this SHA in test reports to tie evidence to exact software.

---

# PART Q — PUBLISH TO GITHUB

## 52. Recommended beginner path: GitHub CLI

Install GitHub CLI:

```bash
sudo apt install -y gh
```

Authenticate:

```bash
gh auth login
```

Choose:

```text
GitHub.com
HTTPS
Login with a web browser
```

Follow the device/browser instructions.

Check authentication:

```bash
gh auth status
```

## 53. Create the public repository and push

From the project root:

```bash
gh repo create opendlab-secure \
  --public \
  --source=. \
  --remote=origin \
  --push
```

Open it:

```bash
gh repo view --web
```

If you do not want the project public while learning, replace `--public` with `--private`, then make it public only after sanitizing and completing the portfolio evidence.

## 54. Normal future Git workflow

After each meaningful milestone:

```bash
git status
git add .
git commit -m "Describe the engineering change"
git push
```

Use engineering-quality commit messages, for example:

```text
Add unauthorized source rejection test
Add configuration baseline verification
Document DL-NOM-001 test evidence
Add ARINC parity negative test
```

---

# PART R — CREATE A PROFESSIONAL TEST CAMPAIGN

## 55. Use test IDs consistently

Start with:

```text
DL-NOM-001   nominal flow
DL-FAIL-002  bearer failure/failover
DL-LAT-003   latency injection
DL-LOSS-004  packet loss
DL-CORR-005  corrupted/malformed input
A429-PAR-006 parity error
A429-LBL-007 label validation
IPS-BGP-008  IPv6 routing failure
QOS-009      service priority
SEC-010      unauthorized input
```

## 56. Every test should contain

```text
Test ID
Requirement ID
Objective
Configuration / Git SHA
Preconditions
Inputs / stimulus
Procedure
Expected result
Actual result
Verdict
Evidence paths
Anomalies
Engineering conclusion
```

## 57. Maintain traceability

Update:

```text
docs/TRACEABILITY.md
```

Each requirement should map to at least one verification method/test.

## 58. Maintain anomaly records

Create:

```text
docs/anomalies/
```

For each real failure, create something such as:

```text
ANOM-001.md
```

Include:

```text
Observation
Reproducibility
Git SHA/configuration
Functional impact
Security impact
Severity
Evidence
Probable cause
Correction
Retest
Final disposition
```

Do not hide failed tests. A well-documented defect and retest is valuable evidence of test-engineering skill.

---

# PART S — LEVEL 2: NETWORK IMPAIRMENT WITH LINUX NETEM

Do this only after the software-only bench is reliable.

The supplied `scripts/netem_example.sh` expects a disposable Linux interface such as a veth interface. Do **not** blindly apply netem to your primary network interface.

The current starter logically models bearers inside Python. A proper physical Linux impairment topology is the next engineering increment.

## 59. First learn the commands without changing the project

Display current interfaces:

```bash
ip addr
```

Display queue disciplines:

```bash
tc qdisc show
```

Read the script:

```bash
cat scripts/netem_example.sh
```

It contains profiles for:

```text
vdl2
satcom
wifi
```

## 60. Create an isolated veth pair for practice

```bash
sudo ip link add veth-test-a type veth peer name veth-test-b
sudo ip addr add 10.250.0.1/24 dev veth-test-a
sudo ip addr add 10.250.0.2/24 dev veth-test-b
sudo ip link set veth-test-a up
sudo ip link set veth-test-b up
```

Verify:

```bash
ip addr show veth-test-a
ip addr show veth-test-b
```

## 61. Apply a simulated VDL2 profile

```bash
sudo ./scripts/netem_example.sh veth-test-a vdl2
```

Inspect:

```bash
tc qdisc show dev veth-test-a
```

Remove it after the experiment:

```bash
sudo tc qdisc del dev veth-test-a root
```

Delete the practice pair:

```bash
sudo ip link del veth-test-a
```

## 62. Engineering increment required for end-to-end impairment

Before routing OpenDLab traffic through veth/netns interfaces, refactor the Python programs so IP addresses and ports are configurable via environment variables rather than fixed to `127.0.0.1`.

Recommended future variables:

```text
AIRCRAFT_BIND_HOST
AIRCRAFT_PORT
GROUND_HOST
GROUND_PORT
ROUTER_HOST
ROUTER_PORT
```

Add automated tests before changing the networking topology.

Then create a separate ground network namespace and route the router-to-ground traffic across a veth pair where netem can be applied safely.

Treat this as a separate GitHub milestone; do not modify everything at once.

---

# PART T — LEVEL 3: IPV6 / ATN-IPS-INSPIRED LAB

This is not an implementation of certified ATN/IPS. It is an IPv6/routing learning environment inspired by the networking concepts relevant to future aeronautical communications.

## 63. First verify IPv6 in WSL

```bash
ip -6 addr
ip -6 route
```

## 64. Install FRRouting later

Do this only after you understand namespaces and veth links.

Depending on the chosen FRR packaging method, install FRR and build three isolated logical routing domains:

```text
Aircraft network
Service-provider network
Ground/ANSP-like network
```

Your engineering objective is to measure:

```text
initial connectivity
route availability
route withdrawal
convergence time
packet loss during convergence
restored connectivity
```

Keep the terminology `ATN/IPS-inspired IPv6 lab` in the portfolio unless you implement the actual required standards in accordance with authoritative specifications.

---

# PART U — LEVEL 4: ARINC 429 HARDWARE-IN-THE-LOOP

Do not begin here. Finish the software bench first.

## 65. Hardware objective

Build an **isolated bench loopback** only:

```text
Laptop Python test controller
       |
       | USB
       v
RP2040 / RP2350 / Pico-class board
       |
       v
ARINC-429 educational TX circuit
       |
       | isolated bench pair
       v
ARINC-429 educational RX circuit
       |
       v
Microcontroller -> laptop evidence
```

## 66. Skills to demonstrate

Measure and test:

```text
word count
label
SDI
SSM
data field
odd parity
unexpected label
missing word timeout
error injection
repeatability
```

## 67. Safety boundary

Never attach the prototype to:

```text
real aircraft
aircraft harness
certified LRU
airport infrastructure
operational avionics
```

Keep all TX/RX activity inside your isolated bench loopback.

Use the open-source ARINC-429 proof-of-concept only as a learning reference and obey its license. Do not represent it as a certified design.

---

# PART V — LEVEL 5: PASSIVE VDL2 OBSERVATION

This stage is optional.

## 68. Receive only

Use SDR only in receive mode.

Never build or configure a transmitter for aviation frequencies.

A candidate future chain is:

```text
receive-only SDR
   -> dumpvdl2
   -> libacars
   -> sanitized protocol observations
```

Focus portfolio evidence on protocol structure, receiver/decoder health and sanitized metadata rather than publishing operationally sensitive message content.

---

# PART W — LEVEL 6: FLIGHTGEAR INTEGRATION

## 69. Install the stable FlightGear release

Install FlightGear on Windows.

Do not start by writing an interface immediately.

First learn to:

```text
launch FlightGear
load an aircraft
read latitude
read longitude
read altitude
observe phase of flight
```

## 70. Define the intended integration

Future OpenDLab flight-profile adapter should translate simulator state to something such as:

```json
{
  "phase": "CRUISE",
  "latitude": 43.6,
  "longitude": 1.44,
  "altitude_ft": 35000
}
```

Then let the test application use phase-of-flight as stimulus for communication policy tests.

Again, keep this as a later GitHub milestone after the core bench is stable.

---

# PART X — WHAT TO COMPLETE BEFORE PUTTING THE PROJECT ON THE CV

Do not claim unfinished work as completed.

Before using strong completed-project wording, aim for:

```text
[ ] 9/9 automated starter tests pass
[ ] live aircraft -> router -> ground run demonstrated
[ ] nominal PCAP captured
[ ] failover demonstrated
[ ] unauthorized-source negative test demonstrated
[ ] unauthorized-service negative test demonstrated
[ ] ARINC parity test demonstrated
[ ] configuration drift demonstrated
[ ] at least 20-25 documented test cases
[ ] requirements-to-test traceability updated
[ ] at least one genuine anomaly + root-cause + retest documented
[ ] GitHub repository sanitized
[ ] architecture diagram published
[ ] 5-10 page engineering test report created
[ ] 3-5 minute demonstration video recorded
[ ] v1.0-test-campaign GitHub release tagged
```

Until a hardware step is actually completed, describe it as `planned` or `in development`.

---

# PART Y — RECOMMENDED FIRST FIVE SESSIONS

## Session 1

Only do:

```text
WSL
Ubuntu
VS Code WSL
Python venv
pip install
9 pytest tests
```

Do not proceed until all nine tests pass.

## Session 2

Only do:

```text
ground station
router
aircraft app
JSON logs
```

Goal: understand the data path.

## Session 3

Do:

```text
tcpdump
PCAP
Wireshark
DL-NOM-001 report
```

Goal: learn instrumentation and evidence.

## Session 4

Do:

```text
VDL2 failure
SATCOM fallback
unauthorized source
unauthorized service
```

Goal: degraded and negative testing.

## Session 5

Do:

```text
ARINC parity
configuration baseline
configuration drift
Git commit
GitHub publish
```

Goal: create the first portfolio milestone.

---

# PART Z — COMMON BEGINNER PROBLEMS

## `python: command not found`

Activate the venv and use:

```bash
source .venv/bin/activate
python --version
```

If necessary, use `python3` for system Python commands.

## `No module named src`

Run the programs from the **project root** using module syntax:

```bash
python -m src.ground_station
python -m src.datalink_router
python -m src.aircraft_app
```

Do not use:

```bash
python src/ground_station.py
```

for this project layout.

## `Address already in use`

A previous router or ground process may still be running.

Check:

```bash
ss -lunp | grep -E ':5000|:5100'
```

Stop the previous terminal with `Ctrl+C`.

## `Permission denied` when running a shell script

Run:

```bash
chmod +x scripts/*.sh
```

Then try again.

## `tcpdump: permission denied`

Use:

```bash
sudo tcpdump ...
```

## VS Code opens Windows rather than WSL

Look at the lower-left corner.

Reconnect using:

```text
Ctrl+Shift+P -> WSL: Connect to WSL
```

Then open the Linux project folder.

## Tests pass but live router fails

Check that you are using the corrected project ZIP and that `src/datalink_router.py` contains:

```python
from src.security_policy import authorize_message
```

## Git tries to commit `.venv`

Verify `.gitignore` contains:

```text
.venv/
```

Then:

```bash
git status
```

before every commit.

---

# Final milestone definition

Your first credible portfolio release should demonstrate that you can:

1. understand an interface architecture;
2. configure a repeatable test environment;
3. execute automated and manual integration tests;
4. inject failure and invalid input;
5. collect objective evidence;
6. correlate packet and application logs;
7. classify and document observations;
8. maintain configuration traceability;
9. use Git/GitHub to control changes;
10. explain limitations without overclaiming certification or aircraft experience.

That engineering discipline is the real purpose of OpenDLab-Secure.
