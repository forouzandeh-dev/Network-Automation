# Network Automation (Cisco SSH Backup)

A simple Python script that connects to a Cisco switch via SSH and performs basic automation (e.g., backup/export configuration).

## Features
- Reads configuration from a YAML file (secrets are not committed)
- SSH connection using Paramiko
- Clean config template for quick setup

## Requirements
- Python 3.x
- Install dependencies:
  `bash
  pip install -r requirements.txt
