# MikroTik Network Compliance Automation

A Python-based MikroTik RouterOS configuration and security assessment tool.

This project connects to a MikroTik router through the RouterOS API, collects selected operational and security-related configuration data, evaluates implemented controls, calculates an indicative assessment score, and produces console and HTML reports.

The project was developed and tested against real MikroTik equipment in a practical network environment. The published repository contains only sanitized example connection parameters and does not include production credentials, MAC addresses, or infrastructure-identifying configuration.

> The assessment is read-only: the tool does not intentionally modify the router configuration.

---

## What It Does

The tool automates a focused set of configuration and security checks useful during periodic network reviews and internal assessments.

It checks areas such as:

- RouterOS version, board, and architecture
- RouterOS service exposure
- Winbox and SSH management access restrictions
- Firewall rule presence and selected protection controls
- NAT masquerade configuration
- Active IP addressing
- DHCP server configuration
- DNS configuration and remote DNS requests
- L2TP/IPsec server status
- RouterOS user accounts
- PASS / WARNING / FAIL results
- Indicative assessment score
- HTML assessment reporting

---

## Assessment Scope

| Area | Examples of Checks |
|---|---|
| System | RouterOS version, board, architecture |
| Services | FTP, Telnet, WWW, API, API-SSL |
| Management | Winbox and SSH access restrictions |
| Firewall | Established/related, invalid traffic, WAN input/forward protection |
| NAT | Masquerade configuration |
| IP Configuration | Active IP addresses |
| DHCP | Active DHCP servers |
| DNS | DNS servers and remote-request configuration |
| VPN | L2TP/IPsec status |
| Users | Active RouterOS accounts |

The checks are intentionally focused. This project is not intended to replace a complete firewall review, penetration test, formal security audit, or compliance certification.

---

## Assessment Model

Each implemented check returns one of:

- PASS - expected configuration or security condition detected
- WARNING - condition requires review or is outside the expected baseline
- FAIL - potentially insecure or missing condition detected

The current score is an indicative project-defined metric calculated from the checks performed:

`PASS checks / Total checks * 100

All checks currently have equal weight.

The score is not a weighted risk score and must not be interpreted as proof of compliance with a security standard.

Formal compliance mapping would require explicitly defined controls, weighting, evidence requirements, and validation against the target standard or organizational baseline.


---

Architecture

+----------------------+
|   MikroTik RouterOS  |
+----------+-----------+
           |
      RouterOS API
           |
           v
+--------------------------+
| Python Assessment Logic  |
+------------+-------------+
             |
       +-----+-----+
       |           |
       v           v
+-------------+ +-------------+
|   Console   | | HTML Report |
|   Results   | |             |
+-------------+ +-------------+

The current implementation intentionally keeps the assessment logic in two executable scripts:

Mikrotik_compliance.py

Console-based assessment.

Mikrotik_compliance_HTML.py

Assessment with HTML report generation.

This keeps the project focused while demonstrating:

RouterOS API integration

Python network automation

Security-oriented configuration assessment

Automated reporting



---

Project Structure

MikroTik-Network-Compliance/
|
+-- Mikrotik_compliance.py
+-- Mikrotik_compliance_HTML.py
+-- requirements.txt
+-- .gitignore
+-- README.md


---

Technology Stack

Python 3

MikroTik RouterOS API

librouteros 4.2.2

HTML

Git / GitHub


Dependency:

librouteros==4.2.2


---

Requirements

Python 3.x

Network connectivity to the target MikroTik router

RouterOS API access

Valid RouterOS credentials

librouteros


Install dependencies:

pip install -r requirements.txt


---

Configuration

The current implementation keeps connection parameters directly in the Python scripts.

The published repository uses placeholders:

ROUTER_IP = "192.168.10.1"
USERNAME = "your username"
PASSWORD = "your password"

The IP address above is an example private address and is not a production device address.

For a production-oriented implementation, credentials should be externalized through secure credential management rather than committed to source code.


---

Usage

Console Assessment

Run:

python Mikrotik_compliance.py

The script connects to the configured MikroTik router, performs the implemented checks, and displays the results and assessment score in the terminal.

HTML Assessment

Run:

python Mikrotik_compliance_HTML.py

The script performs the assessment and generates an HTML report.

The current implementation writes the report to:

C:\NetworkAutomation\Compliance\Mikrotik_Compliance_Report.html

The report path is currently Windows-specific and can be externalized in a future version.


---

Security and Operational Model

The assessment is read-only and does not intentionally change:

Firewall rules

NAT rules

IP addresses

RouterOS services

Users

VPN configuration

DNS configuration


The tool reads selected RouterOS configuration and evaluates it against the rules implemented in the project.

This makes it useful for:

Periodic configuration reviews

Internal IT security assessments

Network administration

Pre-audit preparation

Configuration documentation

Repeatable baseline checks



---

Firewall Assessment Scope

The firewall checks currently cover selected indicators including:

Established/related traffic handling

Invalid traffic handling

WAN input protection

WAN forward protection

Presence of active firewall rules


These checks provide useful indicators but do not establish that an entire firewall policy is secure.

A broader firewall assessment may also need to consider:

Rule ordering

Allowed services and ports

Trusted source networks

Inter-VLAN policies

VPN access policies

NAT behavior

Logging

Address lists

Application requirements

Overall network architecture



---

Practical Use Cases

Enterprise and Branch Networks

Periodic review of MikroTik routers used in office and branch environments.

Internal Security Assessments

Automated collection of selected configuration and security indicators.

Network Administration

Fast visibility into important device configuration areas.

Documentation

Generate a repeatable assessment report for network infrastructure.

Network Automation Portfolio

Demonstrates practical experience with:

Python network automation

RouterOS API

MikroTik administration

Network security

Configuration assessment

Automated reporting



---

Limitations

The current version intentionally has a limited scope:

MikroTik RouterOS focused

Single-device assessment

Assessment rules are implemented directly in the Python scripts

Connection parameters are currently configured in the scripts

HTML report path is Windows-specific

No external inventory

No JSON output

No centralized logging framework

No automated multi-device execution


These are known boundaries of the current implementation.


---

Future Extensions

Potential next-stage improvements include:

External YAML/JSON configuration

Secure credential management

Multi-device assessment

Inventory-based execution

JSON and CSV output

Centralized logging

Historical assessment tracking

Configuration baseline comparison

Custom security policies

Mapping selected checks to CIS or organizational security baselines

Scheduled assessments

REST API integration

Dashboard visualization



---

Project Context

This project is part of a broader practical network automation portfolio:

Network Administration
        |
        v
MikroTik / Routing / Firewall
        |
        v
Python Network Automation
        |
        v
Configuration Assessment
        |
        v
Security Automation
        |
        v
Network DevOps

The portfolio focuses on practical, business-oriented automation projects built around real network administration and infrastructure scenarios.


---

Disclaimer

This tool performs automated checks based on the rules implemented in the project.

It is not a replacement for:

Professional security auditing

Penetration testing

Full firewall review

Formal compliance certification

Organizational risk assessment


The assessment score is specific to the implemented checks and should be interpreted only within that scope.


---

Author

Mohammad Ebrahimpour

Network & IT Infrastructure Specialist

Focus areas:

Network Administration

MikroTik

Network Security

Network Automation

Python

Infrastructure Automation

IT Infrastructure
