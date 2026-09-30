from librouteros import connect

ROUTER_IP = "192.168.10.1"
USERNAME = "your username"
PASSWORD = "your password"

results = []


def add(category, name, status, details):
    results.append((category, name, status, details))


def disabled(value):
    return str(value).lower() == "true"


def state(rule, wanted):
    return wanted in [
        x.strip().lower()
        for x in str(rule.get("connection-state", "")).split(",")
    ]


# =========================
# Connect
# =========================

api = connect(
    ROUTER_IP,
    USERNAME,
    PASSWORD,
    port=8728
)

identity = list(
    api.path("/system/identity").select("name")
)[0].get("name", "Unknown")

resource = list(
    api.path("/system/resource").select(
        "version",
        "board-name",
        "architecture-name"
    )
)[0]

print("=" * 60)
print("MikroTik Network Compliance Checker")
print("=" * 60)
print(f"Device       : {identity}")
print(f"RouterOS     : {resource.get('version', 'Unknown')}")
print(f"Board        : {resource.get('board-name', 'Unknown')}")
print(f"Architecture : {resource.get('architecture-name', 'Unknown')}")
print()


# =========================
# Services
# =========================


services = list(
    api.path("/ip/service").select(
        "name",
        "port",
        "disabled",
        "address"
    )
)

for service in services:

    name = service.get("name", "")

    if name in {
        "ftp",
        "telnet",
        "www",
        "api-ssl"
    }:

        if disabled(service.get("disabled")):

            add(
                "Services",
                name,
                "PASS",
                "Service is disabled."
            )

        else:

            add(
                "Services",
                name,
                "FAIL",
                "Unnecessary service is enabled."
            )

    elif name == "api":

        address = str(
            service.get("address", "")
        ).strip()

        restricted = (
            address
            and address not in {
                "0.0.0.0/0",
                "0.0.0.0"
            }
        )

        if disabled(service.get("disabled")):

            add(
                "Services",
                name,
                "PASS",
                "API service is disabled."
            )

        elif restricted:

            add(
                "Services",
                name,
                "PASS",
                f"API enabled for automation and restricted to: {address}"
            )

        else:

            add(
                "Services",
                name,
                "FAIL",
                "API is enabled without address restriction."
            )
# =========================
# Management Services
# =========================

for name in ("winbox", "ssh"):

    service = next(
        (
            x for x in services
            if x.get("name") == name
        ),
        None
    )

    if not service:

        add(
            "Management",
            name,
            "WARNING",
            "Service not found."
        )

        continue

    address = str(
        service.get("address", "")
    ).strip()

    restricted = (
        address
        and address not in {
            "0.0.0.0/0",
            "0.0.0.0"
        }
    )

    if restricted:

        add(
            "Management",
            name,
            "PASS",
            f"Access restricted to: {address}"
        )

    else:

        add(
            "Management",
            name,
            "WARNING",
            "Management service is not restricted by address."
        )


# =========================
# Firewall
# =========================

rules = list(
    api.path("/ip/firewall/filter").select(
        "chain",
        "action",
        "protocol",
        "dst-port",
        "src-address",
        "in-interface",
        "comment",
        "disabled",
        "connection-state"
    )
)

active = [
    rule for rule in rules
    if not disabled(rule.get("disabled"))
]

add(
    "Firewall",
    "Active Rules",
    "PASS" if active else "FAIL",
    f"{len(active)} active firewall rules found."
)


# Established / Related

established_related = any(
    rule.get("action") == "accept"
    and state(rule, "established")
    and state(rule, "related")
    for rule in active
)

add(
    "Firewall",
    "Established/Related",
    "PASS" if established_related else "WARNING",
    "Established/related accept rule detected."
    if established_related
    else
    "Established/related accept rule not detected."
)


# Invalid Traffic

invalid_drop = any(
    rule.get("action") == "drop"
    and state(rule, "invalid")
    for rule in active
)

add(
    "Firewall",
    "Invalid Traffic",
    "PASS" if invalid_drop else "WARNING",
    "Invalid traffic drop rule detected."
    if invalid_drop
    else
    "Invalid traffic drop rule not detected."
)


# WAN Input
wan_input_drop = any(
    rule.get("chain") == "input"
    and rule.get("action") == "drop"
    and rule.get("in-interface") == "ether1"
    for rule in active
)

add(
    "Firewall",
    "WAN Input Protection",
    "PASS" if wan_input_drop else "WARNING",
    "WAN input drop rule detected."
    if wan_input_drop
    else
    "WAN input drop rule not detected."
)


# WAN Forward

wan_forward_drop = any(
    rule.get("chain") == "forward"
    and rule.get("action") == "drop"
    and rule.get("in-interface") == "ether1"
    for rule in active
)

add(
    "Firewall",
    "WAN Forward Protection",
    "PASS" if wan_forward_drop else "WARNING",
    "WAN forward drop rule detected."
    if wan_forward_drop
    else
    "WAN forward drop rule not detected."
)


# =========================
# NAT
# =========================

nat = list(
    api.path("/ip/firewall/nat").select(
        "chain",
        "action",
        "out-interface",
        "src-address",
        "disabled"
    )
)

active_nat = [
    rule for rule in nat
    if not disabled(rule.get("disabled"))
]

masquerade = any(
    rule.get("chain") == "srcnat"
    and rule.get("action") == "masquerade"
    for rule in active_nat
)

add(
    "NAT",
    "Masquerade",
    "PASS" if masquerade else "WARNING",
    "Masquerade rule detected."
    if masquerade
    else
    "Masquerade rule not detected."
)


# =========================
# IP Addresses
# =========================

ips = list(
    api.path("/ip/address").select(
        "address",
        "interface",
        "disabled"
    )
)

active_ips = [
    item for item in ips
    if not disabled(item.get("disabled"))
]

add(
    "Network",
    "IP Addresses",
    "PASS" if active_ips else "FAIL",
    f"{len(active_ips)} active IP addresses found."
)


# =========================
# DHCP
# =========================

dhcp = list(
    api.path("/ip/dhcp-server").select(
        "name",
        "interface",
        "disabled"
    )
)

active_dhcp = [
    item for item in dhcp
    if not disabled(item.get("disabled"))
]

add(
    "DHCP",
    "DHCP Servers",
    "PASS" if active_dhcp else "WARNING",
    f"{len(active_dhcp)} active DHCP server(s) found."
    if active_dhcp
    else
    "No active DHCP server found."
)


# =========================
# DNS
# =========================

dns_data = list(
    api.path("/ip/dns").select(
        "servers",
        "allow-remote-requests"
    )
)

if dns_data:

    dns = dns_data[0]

    servers = str(
        dns.get("servers", "")
    ).strip()

    remote = str(
        dns.get("allow-remote-requests", "")
    ).lower()

    add(
        "DNS",
        "DNS Servers",
        "PASS" if servers else "WARNING",
        f"DNS servers: {servers}"
        if servers
        else
        "No DNS servers configured."
    )

    add(
        "DNS",
        "Remote DNS Requests",
        "PASS" if remote == "false" else "WARNING",
        "Remote DNS requests are disabled."
        if remote == "false"
        else
        "Remote DNS requests are enabled."
    )


# =========================
# VPN
# =========================

l2tp = list(
    api.path(
        "/interface/l2tp-server/server"
    ).select(
        "enabled",
        "use-ipsec",
        "default-profile"
    )
)

if l2tp:

    vpn = l2tp[0]

    vpn_enabled = (
        str(vpn.get("enabled", "")).lower()
        == "true"
    )

    vpn_ipsec = (
        str(vpn.get("use-ipsec", "")).lower()
        == "true"
    )

    add(
        "VPN",
        "L2TP Server",
        "PASS" if vpn_enabled else "WARNING",
        "L2TP server is enabled."
        if vpn_enabled
        else
        "L2TP server is disabled."
    )

    if vpn_enabled:

        add(
            "VPN",
            "IPsec",
            "PASS" if vpn_ipsec else "WARNING",
            "L2TP is configured to use IPsec."
            if vpn_ipsec
            else
            "L2TP is enabled without IPsec."
        )

else:

    add(
        "VPN",
        "L2TP Server",
        "WARNING",
        "L2TP server configuration not found."
    )
# =========================
# Users
# =========================

users = list(
    api.path("/user").select(
        "name",
        "group",
        "disabled"
    )
)

active_users = [
    user for user in users
    if not disabled(user.get("disabled"))
]

add(
    "Users",
    "RouterOS Users",
    "PASS" if active_users else "WARNING",
    f"{len(active_users)} active user(s) found."
    if active_users
    else
    "No active RouterOS users found."
)


# =========================
# Results
# =========================

print()
print("=" * 60)
print("COMPLIANCE RESULTS")
print("=" * 60)

for category, name, status, details in results:

    print(
        f"[{status}] "
        f"{category} | {name}"
    )

    print(
        f"    {details}"
    )


# =========================
# Summary
# =========================

passed = sum(
    1
    for item in results
    if item[2] == "PASS"
)

warnings = sum(
    1
    for item in results
    if item[2] == "WARNING"
)

failed = sum(
    1
    for item in results
    if item[2] == "FAIL"
)

total = len(results)

score = (
    round(passed / total * 100)
    if total
    else 0
)

print()
print("=" * 60)
print("COMPLIANCE SUMMARY")
print("=" * 60)

print(f"PASS    : {passed}")
print(f"WARNING : {warnings}")
print(f"FAIL    : {failed}")
print(f"TOTAL   : {total}")
print(f"SCORE   : {score}%")

print("=" * 60)
print("Compliance check completed.")
print("=" * 60)

# =========================
# HTML Report
# =========================

from html import escape
from datetime import datetime
from pathlib import Path

report_file = Path(r"C:\NetworkAutomation\Compliance\Mikrotik_Compliance_Report.html")

rows = []

for category, name, status, details in results:
    if status == "PASS":
        css = "pass"
    elif status == "WARNING":
        css = "warning"
    else:
        css = "fail"

    rows.append(
        "<tr>"
        "<td>" + escape(str(category)) + "</td>"
        "<td>" + escape(str(name)) + "</td>"
        "<td class='" + css + "'>" + escape(str(status)) + "</td>"
        "<td>" + escape(str(details)) + "</td>"
        "</tr>"
    )

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>MikroTik Compliance Report</title>
<style>
body {
    font-family: Arial, sans-serif;
    background: #f4f6f8;
    margin: 0;
    padding: 30px;
    color: #222;
}
.container {
    max-width: 1100px;
    margin: auto;
}
.header {
    background: #17212b;
    color: white;
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 20px;
}
.cards {
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    flex: 1;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,.08);
}
.number {
    font-size: 28px;
    font-weight: bold;
}
table {
    width: 100%;
    border-collapse: collapse;
    background: white;
}
th {
    background: #263746;
    color: white;
    padding: 12px;
    text-align: left;
}
td {
    padding: 11px;
    border-bottom: 1px solid #eee;
}
.pass {
    color: #16803c;
    font-weight: bold;
}
.warning {
    color: #b26a00;
    font-weight: bold;
}
.fail {
    color: #c62828;
    font-weight: bold;
}
.footer {
    margin-top: 20px;
    color: #666;
    font-size: 13px;
}
</style>
</head>
<body>
<div class="container">

<div class="header">
<h1>MikroTik Network Compliance Report</h1>
<p><b>Device:</b> """ + escape(str(identity)) + """</p>
<p><b>RouterOS:</b> """ + escape(str(resource.get("version", "Unknown"))) + """</p>
<p><b>Board:</b> """ + escape(str(resource.get("board-name", "Unknown"))) + """</p>
<p><b>Architecture:</b> """ + escape(str(resource.get("architecture-name", "Unknown"))) + """</p>
</div>

<div class="cards">
<div class="card">
<div>Score</div>
<div class="number">""" + str(score) + """%</div>
</div>
<div class="card">
<div>PASS</div>
<div class="number pass">""" + str(passed) + """</div>
</div>
<div class="card">
<div>WARNING</div>
<div class="number warning">""" + str(warnings) + """</div>
</div>
<div class="card">
<div>FAIL</div>
<div class="number fail">""" + str(failed) + """</div>
</div>
</div>

<table>
<tr>
<th>Category</th>
<th>Check</th>
<th>Status</th>
<th>Details</th>
</tr>
""" + "".join(rows) + """
</table>

<div class="footer">
Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
</div>

</div>
</body>
</html>
"""

report_file.write_text(html, encoding="utf-8")

print()
print("HTML REPORT")
print("=" * 60)
print(f"Report saved to: {report_file}")
print("=" * 60)
