MikroTik Network Compliance Automation

A Python-based network security assessment tool for MikroTik RouterOS environments.

This project connects to a MikroTik router through the RouterOS API, evaluates a set of operational and security controls, calculates an assessment score, and generates both console and HTML reports.

The project is designed as a practical network automation and security assessment solution rather than a configuration-changing tool.

---

Overview

MikroTik devices are widely used in enterprise, branch-office, ISP, and infrastructure environments.

Regular security and configuration assessments can help identify:

- Unnecessary or insecure services
- Unrestricted management access
- Missing firewall protections
- DNS configuration risks
- VPN configuration status
- User/account configuration
- Network addressing and DHCP configuration
- Basic security hardening gaps

This project automates these checks through the MikroTik RouterOS API.

The assessment is read-only and does not modify router configuration.

---

Key Capabilities

- Connect to MikroTik RouterOS through the API
- Collect system and device information
- Check RouterOS services
- Evaluate management-service exposure
- Inspect firewall rules
- Check NAT configuration
- Inspect IP addressing
- Check DHCP configuration
- Evaluate DNS configuration
- Check VPN/L2TP configuration
- Inspect configured users
- Calculate an overall assessment score
- Display results in the terminal
- Generate an HTML assessment report

---

Assessment Areas

Area| Examples of Checks
System| RouterOS version, board, architecture
Services| FTP, Telnet, WWW, API, API-SSL
Management| Winbox and SSH access restrictions
Firewall| Established/related, invalid traffic, WAN protection
NAT| Masquerade configuration
IP Configuration| Configured addresses
DHCP| DHCP configuration
DNS| DNS servers and remote-request configuration
VPN| L2TP/IPsec status
Users| Configured RouterOS accounts

---

Assessment Model

Each check produces a result such as:

- PASS — expected security/configuration condition detected
- WARNING — configuration exists but requires review
- FAIL — potentially insecure or missing configuration detected

The project calculates a percentage score based on the checks performed.

Important

The score is a project-defined assessment metric.

It should not be interpreted as formal certification or proof of compliance with a specific security standard unless the checks and scoring model are explicitly mapped and validated against that standard.

---

Architecture

The current implementation intentionally keeps the assessment logic in two executable Python scripts:

                    +----------------------+
                    |   MikroTik RouterOS  |
                    +----------+-----------+
                               |
                         RouterOS API
                               |
                               v
                +--------------------------+
                |   Python Assessment      |
                |          Logic            |
                +------------+-------------+
                             |
              +--------------+--------------+
              |                             |
              v                             v
     +------------------+          +------------------+
     | Console Results  |          |   HTML Report    |
     +------------------+          +------------------+

The project currently uses the same core assessment concepts in:

Mikrotik_compliance.py
Mikrotik_compliance_HTML.py

The code has intentionally not been over-engineered into multiple modules because the current implementation is already functional and tested in a practical MikroTik environment.

---

Project Structure

Mikrotik-Network-Compliance/
│
├── Mikrotik_compliance.py
├── Mikrotik_compliance_HTML.py
├── requirements.txt
├── .gitignore
└── README.md

Main Scripts

"Mikrotik_compliance.py"

Runs the assessment and displays the results in the terminal.
Mikrotik_compliance_HTML.py"

Runs the assessment and generates a formatted HTML report.

---

Technology Stack

- Python 3
- MikroTik RouterOS API
- "librouteros"
- HTML
- Git / GitHub

Dependency:

librouteros==4.2.2

---

Requirements

- Python 3.x
- Network connectivity to the MikroTik router
- RouterOS API access
- Valid RouterOS credentials
- "librouteros"

Install the dependency:

pip install -r requirements.txt

---

Usage

Console Assessment

Run:

python Mikrotik_compliance.py

The script connects to the configured MikroTik router and evaluates the configured controls.

Results are displayed in the terminal together with the calculated assessment score.

---

HTML Assessment

Run:

python Mikrotik_compliance_HTML.py

The script performs the assessment and generates an HTML report.

The current implementation uses a Windows-based report path:

C:\NetworkAutomation\Compliance\Mikrotik_Compliance_Report.html

This path is an implementation detail of the current version and can be externalized in a future version.

---

Security and Operational Model

The tool is designed primarily for assessment and auditing.

It does not intentionally change:

- Firewall rules
- NAT rules
- IP addresses
- Services
- Users
- VPN configuration
- DNS configuration

The tool reads the current RouterOS configuration and evaluates it against the implemented assessment rules.

This makes it suitable for:

- Periodic configuration reviews
- Security assessments
- Internal IT audits
- Network documentation
- Pre-audit preparation
- Baseline comparison

---

Firewall Assessment Scope

The firewall checks include selected controls such as:

- Established/related traffic handling
- Invalid traffic handling
- WAN input protection
- WAN forward protection

These checks provide useful security indicators but do not prove that an entire firewall policy is secure.

A complete firewall security assessment should also consider:

- Rule ordering
- Allowed services
- Trusted source networks
- Inter-VLAN policies
- VPN access policies
- NAT behavior
- Logging
- Address lists
- Application requirements
- Network architecture

---

Practical Use Cases

This project can be used as a lightweight assessment tool for:

Enterprise Networks

Periodic review of MikroTik routers used in branch or office environments.

Security Audits

Automated collection of selected security-related configuration indicators.

Network Administration

Quick visibility into device configuration and security posture.

Documentation

Generate a repeatable assessment report for network infrastructure.

Network Automation Portfolio

Demonstrates practical experience with:

- Network automation
- RouterOS API
- Python
- Network security
- Configuration assessment
- Automated reporting

---

Limitations

The current version has several intentional limitations:

- Designed primarily for MikroTik RouterOS
- Single-device assessment
- Assessment rules are implemented directly in the Python scripts
- Credentials and connection parameters are currently configured in the scripts
- HTML report path is currently Windows-specific
- No external configuration file
- No centralized logging framework
- No JSON output
- No automated multi-device inventory

These limitations are candidates for future development rather than requirements for the current implementation.

---

Future Extensions

Possible future improvements include:

- External configuration using YAML/JSON
- Secure credential management
- Multi-device assessment
- Inventory-based execution
- JSON output
- CSV reporting
- Centralized logging
- Historical compliance tracking
- Configuration baseline comparison
- Custom security policies
- Mapping checks to standards such as CIS or organizational security baselines
- Automated scheduled assessments
- REST API integration
- Dashboard visualization

---

Project Context

This project is part of a broader practical network automation portfolio focused on:
Network Administration
        ↓
MikroTik / Routing / Firewall
        ↓
Python Network Automation
        ↓
Configuration Assessment
        ↓
Security Automation
        ↓
Network DevOps

The objective is to demonstrate practical engineering capabilities through real-world-oriented automation projects rather than isolated programming exercises.

---

Disclaimer

This tool provides automated configuration checks based on the rules implemented in the project.

It is not a replacement for:

- Professional security auditing
- Penetration testing
- Full firewall review
- Formal compliance certification
- Organizational risk assessment

The assessment score is specific to this project and should be interpreted within the scope of the implemented checks.

---

Author

Mohammad Ebrahimpour

Network & IT Infrastructure Specialist

Focus areas:

- Network Administration
- MikroTik
- Network Security
- Network Automation
- Python
- Infrastructure Automation
- IT Infrastructure