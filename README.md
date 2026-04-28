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
Kali Linux (192.168.95.100)

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

## Blocking Rules
- FC6 (Write Single Register) with abnormal values
- FC16 (Write Multiple Registers) with abnormal values
- Any Modbus write command from unauthorized IP

## Status
Security bridge implementation is in progress.

## References
- GRFICS: https://github.com/mrideout/GRFICSv3
- 福田 敏博, 「現場で役立つOTの仕組みとセキュリティ 演習で学ぶ! わかる! リスク分析と対策」, 翔泳社, 2021
