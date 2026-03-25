# Project Internship-1

A consolidated repository for multiple security-focused Python projects.

## Projects Overview

### 1. Web Application Scanner (project1)
- **What it is**: A Flask-based web application for automated vulnerability scanning.
- **Purpose**: To crawl target websites and identify insecure forms or configurations.
- **Usage**: Run `python project1/app.py` and navigate to the local server address.
- **Directory Structure**:
  - `app.py`: Main Flask application server.
  - `requirements.txt`: Python package dependencies.
  - `scanner/crawler.py`: Logic for parsing HTML and extracting forms.
  - `scanner/vulnerability_scanner.py`: Core security analysis logic.
  - `templates/`: HTML frontend files (`index.html`, `results.html`).

### 2. Password Strength Analyzer (project2)
- **What it is**: A tool for evaluating password security and generating custom wordlists.
- **Purpose**: To help users create strong passwords and analyze potential weaknesses using entropy and feedback.
- **Usage**: Run `python "project2/Password Strength Analyzer/main.py"`. Supports `analyze` and `generate` subcommands, or interactive mode.
- **Directory Structure**:
  - `main.py`: Command-line interface entry point.
  - `analyzer.py`: Logic for password strength calculation.
  - `generator.py`: Script for generating custom wordlists based on user details.
  - `gui.py`: Graphical user interface components.

### 3. Log File Analyzer (project3)
- **What it is**: A log-based intrusion detection system (IDS).
- **Purpose**: Parses Apache and SSH logs to identify brute-force attacks, DoS patterns, and cross-reference malicious IPs.
- **Usage**: Run `python project3/log_analyzer.py`.
- **Directory Structure**:
  - `log_analyzer.py`: Main parsing and analysis script.
  - `access.log`/`auth.log`: Sample log files for testing.
  - `blacklist.txt`: Pre-defined list of malicious IP addresses.
  - `security_report.md`: Generated report summarizing the findings.
  - `request_analysis.png`: Visualization of log analysis results.
