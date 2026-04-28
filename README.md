# modbus-security-bridge

## Overview
A security bridge that inspects Modbus TCP packets and blocks unauthorized commands in OT networks.

## Environment
- Windows11 machine
- VirtualBox
- Kali Linux
- GRFICSv3 (Industrial Control System Simulator)

## Network Architecture (Attack Demonstration)
192.168.95.0/24

Kali Linux (192.168.95.100) ─-attack-→ ChemicalPlant (192.168.95.10 ~ 192.168.95.13)

PLC (192.168.95.2)

 ↕
 
ChemicalPlant (192.168.95.10 ~ 192.168.95.13)

## Attack Demonstration
Executed `attack_demonstration.py` from Kali Linux using FC6 (Write Single Register) to send abnormal values (0 and 65535) at high speed, causing the chemical plant process to fail.

## Network Architecture (Bridge Setup)
192.168.95.0/24

PLC (192.168.95.2)

 ↕
 
Kali Linux - Security Bridge (192.168.95.100)

 ↕
 
ChemicalPlant (192.168.95.10 ~ 192.168.95.13)

ARP spoofing was used to place Kali Linux inline between the PLC and Chemical Plant.
Confirmed that Modbus traffic passes through Kali Linux using Wireshark.

## IP Forwarding Verification
To confirm that Kali Linux is properly placed inline, 
IP forwarding was tested in two states.

- `pcap/arpspoof_ip_forward_0.pcapng` : IP forwarding disabled.
  Modbus traffic between PLC and Chemical Plant was interrupted,
  confirming that traffic passes through Kali Linux.

- `pcap/arpspoof_ip_forward_1.pcapng` : IP forwarding enabled.
  Modbus traffic was successfully forwarded through Kali Linux.

## Blocking Rules
- FC6 (Write Single Register) with abnormal values
- FC16 (Write Multiple Registers) with abnormal values
- Any Modbus write command from unauthorized IP

## Status
Security bridge implementation is in progress.

## References
- GRFICS: https://github.com/mrideout/GRFICSv3
- 福田 敏博, 「現場で役立つOTの仕組みとセキュリティ 演習で学ぶ! わかる! リスク分析と対策」, 翔泳社, 2021
