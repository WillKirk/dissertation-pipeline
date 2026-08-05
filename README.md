# Dissertation Pipeline

A research repository for an MSc Computer Science dissertation investigating the effectiveness of AI-assisted security scanning tools compared to traditional static analysis tools in a CI/CD pipeline context.

## Research Question

How effectively do AI-assisted security scanning tools detect predefined vulnerabilities and misconfigurations in a CI/CD pipeline compared with traditional static analysis tools?

## Overview

This repository contains a deliberately vulnerable Flask REST API built as a controlled research environment. The application contains a predefined set of fourteen security vulnerabilities across five categories and three difficulty tiers, against which four scanning tools are evaluated:

**AI-based:**
- Claude Sonnet (via Anthropic API)
- Snyk

**Traditional static analysis:**
- Semgrep
- Trivy

## Vulnerability Categories

- Exposed secrets
- Outdated dependencies with known CVEs
- Overly permissive IAM roles
- Insecure infrastructure-as-code configurations
- Injection-prone code (SQL, command, and template injection)

## Project Structure

dissertation-pipeline/
├── .github/
│ └── workflows/
│ └── security-scan.yml
├── infrastructure/
│ ├── iam-policy.json
│ └── main.tf
├── app/
│ ├── init.py
│ ├── models.py
│ ├── config.py
│ └── routes/
│ ├── auth.py
│ ├── users.py
│ ├── files.py
│ └── templates.py
├── requirements.txt
└── run.py

## Setup

```bash
# Clone the repository
git clone https://github.com/[your-username]/dissertation-pipeline.git
cd dissertation-pipeline

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Run the application
python3 run.py
```

## Important Notice

This repository contains **deliberately introduced security vulnerabilities** for research purposes. It should never be deployed to a production environment or exposed to the public internet. All vulnerabilities are documented in the ground truth reference document included in this repository.

## Academic Context

This project forms part of an MSc dissertation at the University of East London. The vulnerability set and evaluation methodology are described in full in the accompanying dissertation.