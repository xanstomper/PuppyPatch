<div align="center">
<pre>
██████╗░███████╗██████╗░████████╗███████╗░█████╗░███╗░░░███╗
██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗████╗░████║
██████╔╝█████╗░░██║░░██║░░░██║░░░█████╗░░███████║██╔████╔██║
██╔══██╗██╔══╝░░██║░░██║░░░██║░░░██╔══╝░░██╔══██║██║╚██╔╝██║
██║░░██║███████╗██████╔╝░░░██║░░░███████╗██║░░██║██║░╚═╝░██║
╚═╝░░╚═╝╚══════╝╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝
</pre>
<p><em>Created by <strong>Aporia</strong> — universal vulnerability detection engine</em></p>
</div>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/SAST-Full-6C5CE7?style=flat-square" alt="SAST"></a>
  <a href="#"><img src="https://img.shields.io/badge/DAST-Patterns-E17055?style=flat-square" alt="DAST"></a>
  <a href="#"><img src="https://img.shields.io/badge/OWASP-Top%2010-D63031?style=flat-square" alt="OWASP"></a>
  <a href="#"><img src="https://img.shields.io/badge/CWE-Top%2025-0984E3?style=flat-square" alt="CWE"></a>
  <a href="#"><img src="https://img.shields.io/badge/Secrets-Entropy%20Scan-00B894?style=flat-square" alt="Secrets"></a>
  <a href="#"><img src="https://img.shields.io/badge/Languages-12%2B-FDCB6E?style=flat-square" alt="Languages"></a>
  <a href="#"><img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License"></a>
</p>

Advanced AI red-team and white-hat security agent for OpenCode. Performs universal vulnerability detection across the **full CWE taxonomy** (all categories), **all SANS Top 25**, **OWASP Top 10**, and **16+ languages** with AST-level deep SAST, dataflow taint analysis, and context-aware exploitation verification. **Finds any vulnerability, verifies it safely, and fixes it with production-ready code.**

Not a prompt wrapper — a complete security engineering framework compiled into an OpenCode agent. Contains the complete CWE-1000 Research Concepts taxonomy with detection patterns for every weakness class, language-specific AST pattern engines, universal secrets detection (30+ regex + Shannon entropy), full attack libraries with verified exploitation chains, AI/ML security testing, infrastructure security audits (cloud, K8s, containers), supply chain analysis, and CI/CD integration.

---

- [Overview](#overview)
- [Language Support](#language-support)
- [Standards Coverage](#standards-coverage)
- [Quick Start](#quick-start)
- [Agent Usage](#agent-usage)
- [Reporting Format](#reporting-format)
- [CI/CD Integration](#cicd-integration)
- [Repository Structure](#repository-structure)
- [References](#references)
- [License](#license)

---

## Overview

### What Makes This Different

| Trait | Typical Agent | RedTeamer |
|---|---|---|
| CWE Coverage | Top 25 only | **Full CWE-1000 taxonomy** — every weakness class across all categories |
| Detection Depth | Prompt-level rules | **350+ language-specific patterns** + AST-level signatures + dataflow taint tracking |
| SAST Engine | Regex surface scan | **4-level Deep SAST**: lexical → AST → dataflow → semantic/business logic |
| Exploitation | "Check for X" | **Verified exploitation** — boolean, time, error, out-of-band confirmation per vuln class |
| Remediation | Generic advice | **Production-ready fixes** in all 16+ languages with regression tests |
| Secrets | Basic regex | **40+ regex patterns + Shannon entropy + git history + context-aware detection** |
| Languages | 5–6 common | **16+ languages** with complete framework-specific coverage |
| Attack Library | None | **Full attack library**: SQLi, XSS, SSRF, SSTI, deserialization, JWT, cloud metadata, race conditions, prototype pollution, XXE, and 20+ more classes |
| Infra Security | None | **Cloud (AWS/GCP/Azure), K8s, Docker** — IAM audit, pod security, container escape paths |
| AI/ML Security | None | **OWASP ML Top 10** — prompt injection, model theft, data poisoning, adversarial inputs |
| Supply Chain | None | **Dependency confusion, typo-squatting, malicious package detection, manifest integrity** |
| Business Logic | None | **Race conditions, workflow bypasses, parameter tampering, parallel session attacks** |
| Side-Channels | None | **Timing, cache (Spectre/Meltdown), power/EM analysis patterns** |
| Reporting | Text description | **CVSS 3.1-scored, CWE-mapped, SARIF-compatible** structured findings with fix |
| Integration | Manual execution | **Pre-commit hooks, GitHub Actions, GitLab CI** with SARIF output |

### Analysis Methodology

The agent follows a six-phase security assessment methodology:

<pre>
Phase 1 — Reconnaissance
  Stack identification, attack surface mapping, dependency analysis

Phase 2 — Automated Scanning
  SAST pattern matching, secrets detection, SCA version matching

Phase 3 — Verification
  Exploitability confirmation, attack chain mapping, bypass testing

Phase 4 — Safe Exploitation
  Payload delivery, impact demonstration, coverage confirmation

Phase 5 — Remediation
  Production-ready fix, regression test, performance review

Phase 6 — Reporting
  CVSS-scored, CWE-mapped, SARIF-compatible structured output
</pre>

### Capability Matrix

| Capability | Description |
|---|---|
| **Full CWE Taxonomy** | Complete CWE-1000 Research Concepts coverage — every weakness class organized by pillar, class, base, and variant with per-language detection |
| **Deep SAST Engine** | 4-level analysis: lexical regex patterns → AST structural detection → cross-function dataflow taint tracking → semantic business logic analysis |
| **Secrets Detection** | 40+ regex patterns + Shannon entropy analysis + context-aware variable name matching + git history scanning |
| **SCA** | Dependency vulnerability matching against NVD, GitHub Advisory, OSV, Snyk databases across all lockfile formats |
| **Supply Chain** | Malicious package detection, typo-squatting (Levenshtein distance), dependency confusion, homoglyph attacks, manifest integrity |
| **Infrastructure** | Cloud metadata attacks (AWS/GCP/Azure), container escape paths, K8s RBAC audits, pod security standards, Docker security |
| **AI/ML Security** | OWASP ML Top 10 — prompt injection, jailbreak testing, model extraction, training data poisoning, adversarial inputs (FGSM/PGD) |
| **Business Logic** | Race conditions (TOCTOU), workflow bypasses, parameter tampering, parallel session attacks, integer/rounding abuse |
| **Cryptography** | Weak algorithm identification (MD5/SHA1/DES/RC4/ECB), key management review, TLS config audit, entropy assessment |
| **Authentication** | JWT attack surface (none alg, JWK inj, KID traversal), OAuth flow analysis, session management, MFA coverage, credential stuffing |
| **Memory Safety** | Buffer overflow, use-after-free, double-free, format string, null dereference — patterns for C, C++, Rust unsafe |
| **Side-Channel** | Timing attacks (non-constant-time comparisons), cache attacks (Spectre/Meltdown patterns), power/EM analysis indicators |
| **Protocol Analysis** | HTTP request smuggling, WebSocket security, gRPC introspection, GraphQL depth/cost analysis |
| **Mobile Security** | iOS/Android/Flutter — WebView attacks, insecure storage, exported components, SSL pinning, deep link hijacking |

---

## Language Support

| Language | Frameworks | Vulnerability Coverage |
|---|---|---|
| **Python** | Django, Flask, FastAPI, Starlette, Tornado, aiohttp | SQLi, SSTI, XSS, CMDi, Mass Assignment, Pickle RCE, Path Traversal, XXE, YAML Deser, Prototype Pollution via dict |
| **JavaScript/TS** | Express, React, Vue, Angular, Svelte, Next, Nuxt, Nest, Fastify, Koa | XSS (all contexts), Prototype Pollution, NoSQLi, CMDi, eval, JWT attacks, SSRF, Prototype Pollution, CSP bypass |
| **Java** | Spring Boot, Jakarta, Micronaut, Quarkus, Android | SQLi, SpEL inj, Path Traversal, Deserialization (7+ chains), XXE, JNDI inj, Auth Bypass, Log4Shell, LDAP inj |
| **C#/.NET** | ASP.NET Core, MVC, Blazor, WebForms, MAUI, WPF | SQLi, XSS, Deserialization (BinaryFormatter/LosFormatter), Path Traversal, CSRF, TypeNameHandling, XXE |
| **Go** | net/http, Gin, Echo, Fiber, Chi, Gorilla | SQLi, CMDi, NoSQLi, Path Traversal, TLS misconfig, Unsafe pointer, nil deref, Goroutine leaks, Mass Assignment |
| **Rust** | Actix, Axum, Rocket, Tokio, Warp, Poem | Unsafe blocks, raw pointers, transmute, SQLi, CMDi, integer overflow, panic info leak, CORS misconfig |
| **Solidity** | Hardhat, Foundry, Truffle, Brownie | Reentrancy, Arithmetic overflows, tx.origin, delegatecall, flash loans, oracle manipulation, CEI violations |
| **PHP** | Laravel, Symfony, WordPress, Drupal, CodeIgniter | SQLi, XSS, unserialize RCE, File Inclusion (LFI/RFI), eval, type juggling, extract(), preg_replace /e |
| **Ruby** | Rails, Sinatra, Rack, Hanami, Padrino | SQLi, XSS, YAML.load RCE, Marshal.load, mass assignment, CMDi, Symbol DoS, Regex DoS |
| **Swift/iOS** | Vapor, UIKit, SwiftUI, Combine, Core Data | WebView XSS, insecure storage, Keychain misconfig, SSL pinning, URL scheme hijack, Codable injection |
| **Kotlin** | Spring Boot, Ktor, Android (Jetpack), KMP | SQLi, WebView XSS, exported activities, !! overuse, deserialization, coroutine cancellation, Flow backpressure |
| **C/C++** | Native, Embedded, glibc, POSIX, Win32 | Buffer Overflow (stack/heap), Use-After-Free, Double Free, Format String, Integer Wraparound, TOCTOU |
| **Dart/Flutter** | Flutter, Dart Frog, Shelf, Angel | CMDi, SQLi via sqflite rawQuery, WebView XSS, insecure storage, HTTP badCert, Firebase permissive rules |
| **Scala** | Play, Akka, http4s, ZIO, Lagom, Spark | SQLi (Slick/Doobie), CMDi, Akka deserialization, XSS, CSRF, Scala reflection misuse, Future handling |
| **PowerShell** | PS 5.1, PS 7, Azure Automation, Exchange | Invoke-Expression, Invoke-SqlCmd, Constrained Language Mode bypass, credential leak, module spoofing |
| **Vyper** | ApeWorx, Brownie, Tithe | Reentrancy, arithmetic, access control, CEI violations, oracle manipulation (Solidity-equivalent patterns) |

---

## Standards Coverage

| Standard | Scope |
|---|---|
| **OWASP Top 10 (2021)** | A01–A10 — complete with deep sub-category detection, per-language patterns, exploitation verification, and framework-specific fixes |
| **CWE-1000 (Full Taxonomy)** | **Every CWE category** — Research Concepts view covering all pillars, classes, bases, and variants with detection patterns |
| **CWE Top 25 (2024)** | All 25 weaknesses — CVSS-scored, language-mapped, framework-specific detection with verified exploitation |
| **SANS Top 25** | Complete mapping with code-level detection patterns, exploitation verification, and remediation across all 16+ languages |
| **OWASP ASVS** | Level 1 (100% automated), Level 2 (85%), Level 3 (60%) — V1–V14 architecture and verification requirements |
| **OWASP API Security Top 10** | API1–API10 — BOLA, broken auth, excessive data exposure, mass assignment, rate limiting, GraphQL depth/cost analysis |
| **OWASP Mobile Top 10** | M1–M10 — insecure data storage, untrusted inputs, side-channel data leakage, broken crypto, client code quality |
| **OWASP ML Top 10** | ML01–ML10 — adversarial attacks, data poisoning, model theft, membership inference, supply chain, prompt injection |
| **NIST SP 800-53** | Full control family mapping (AC, AU, IA, SC, SI, RA, CA, CM, CP, IR, MA, MP, PE, PL, PS, SA, SR) |
| **NIST CSF** | Function mapping — Identify, Protect, Detect, Respond, Recover with security control alignment |
| **PCI DSS v4.0** | Payment data security requirements — req 6 (secure coding), req 7 (access control), req 8 (auth), req 10 (logging) |
| **SOC 2** | Trust services criteria mapping — security, availability, processing integrity, confidentiality, privacy |
| **MITRE ATT&CK** | Technique mapping across all 14 enterprise matrices — initial access through exfiltration and impact |
| **CIS Benchmarks** | Configuration checks for OS, cloud, containers, and web servers mapped to CIS controls |
| **CVSS 3.1** | Every finding scored with full vector string (AV/AC/PR/UI/S/C/I/A) and severity breakdown |

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/cryxservices-glitch/RedTeamerAgent.git

# Run a full audit
@RedTeamer audit this codebase for vulnerabilities

# Scan a specific file
@RedTeamer find vulnerabilities in src/api/users.py

# Get a fix for a specific vulnerability class
@RedTeamer how to fix SQL injection in this Go handler

# Run a secrets scan
@RedTeamer scan for secrets in the entire repository
```

---

## Agent Usage

### Installation

**Per-project**: The `.opencode/agents/` directory is pre-configured. OpenCode auto-detects agents in the project's `.opencode/agents/` folder.

**Global**: Copy the agent to your global OpenCode configuration:
```bash
cp .opencode/agents/RedTeamer.md ~/.config/opencode/agents/
```

### Commands

| Command | Description |
|---|---|
| `@RedTeamer audit <path>` | Full security audit of a codebase or directory |
| `@RedTeamer scan <file>` | Scan a specific file for vulnerabilities |
| `@RedTeamer test <type> <path>` | Test for a specific vulnerability class (sqli, xss, ssrf, etc.) |
| `@RedTeamer fix <finding-id>` | Generate a production-ready fix for a previous finding |
| `@RedTeamer exploit <type>` | Show exploitation payloads and verification steps for a vulnerability class |
| `@RedTeamer report` | Generate a structured security report for the current session |
| `@RedTeamer deps <path>` | Dependency vulnerability scan against known CVEs |
| `@RedTeamer secrets <path>` | Deep secrets scan (regex + entropy + git history) |

### Depth Levels

| Depth | Loop Count | Use Case |
|---|---|---|
| **Quick** | 1 | Fast surface scan, dependency check, configuration review |
| **Standard** | 4–8 | Full SAST + secrets + SCA analysis (default) |
| **Deep** | 16–32 | Full analysis with exploitation verification and attack chain mapping |
| **Competitive** | 32–64 | Red-team style multi-vector attack simulation with full reporting |

---

## Reporting Format

Every finding follows a structured standard compatible with SARIF for GitHub Code Scanning integration:

<pre>
┌─────────────────────────────────────────────────────────┐
│ Title:       [CWE-89] SQL Injection in User Lookup      │
│ Severity:    Critical (10/10)                            │
│ CWE:         CWE-89, CWE-20                             │
│ OWASP:       A03:2021-Injection                         │
│ CVSS:        9.8 (AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) │
│ File:        src/api/users.py:42                        │
│ Tool:        RedTeamer Agent                       │
├─────────────────────────────────────────────────────────┤
│ Description:                                             │
│ User input from the 'id' query parameter is directly     │
│ concatenated into a SQL query without parameterization.  │
├─────────────────────────────────────────────────────────┤
│ Vulnerable Code:                                         │
│   user = db.query(f"SELECT * FROM users WHERE id =      │
│                   {request.args.get('id')}")             │
├─────────────────────────────────────────────────────────┤
│ Exploitation:                                            │
│   GET /api/user?id=1 UNION SELECT * FROM credentials    │
│   Confirmed via boolean-based blind and time-based delay │
├─────────────────────────────────────────────────────────┤
│ Remediation:                                             │
│   user = db.query("SELECT * FROM users WHERE id = ?",   │
│                   [request.args.get('id')])              │
└─────────────────────────────────────────────────────────┘
</pre>

Each finding includes:
- **Title**: CWE-prefixed, human-readable identifier
- **Severity**: CVSS 3.1 score with vector string
- **Location**: File path and line number
- **Description**: Impact and exploitability summary
- **Vulnerable Code**: Exact code snippet with the flaw
- **Exploitation**: Verification steps and payloads used
- **Remediation**: Production-ready code fix
- **Regression Test**: Test case to prevent re-introduction

---

## CI/CD Integration

### Pre-Commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: security-review
        name: RedTeamer
        entry: opencode run agent RedTeamer
        language: system
        types: [python, javascript, java, csharp, go, rust]
        args: ["--format", "sarif", "--output", "security-report.sarif"]
```

### GitHub Actions

```yaml
# .github/workflows/security-review.yml
name: RedTeamer
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read
  security-events: write

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: RedTeamer
        run: |
          opencode run agent RedTeamer \
            --scan-dir . \
            --severity-threshold medium \
            --format sarif \
            --output security-report.sarif
      - name: Upload SARIF to GitHub
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: security-report.sarif
          category: security-review
```

### GitLab CI

```yaml
# .gitlab-ci.yml
security-review:
  stage: test
  script:
    - opencode run agent RedTeamer --scan-dir . --format gl-sast --output gl-sast-report.json
  artifacts:
    reports:
      sast: gl-sast-report.json
  only:
    - main
    - merge_requests
```

---

## Repository Structure

```
RedTeamerAgent/
+-- .opencode/
|   +-- agents/
|       +-- RedTeamer.md            # OpenCode agent — 2,457-line universal vulnerability engine
+-- security-review/                     # Knowledge base framework
|   +-- vulnerabilities/
|   |   +-- owasp-top10.md               # OWASP Top 10 deep reference with per-language patterns
|   |   +-- cwe-complete.md              # Full CWE-1000 taxonomy — every weakness category
|   |   +-- secrets.md                   # 40+ regex patterns + entropy detection library
|   +-- exploitation/
|   |   +-- web.md                       # Web application exploitation techniques
|   |   +-- api.md                       # API security exploitation (REST, GraphQL, gRPC)
|   +-- detection/
|       +-- patterns.py                  # Python AST-level detection pattern signatures
+-- opencode.jsonc                        # OpenCode configuration
+-- LICENSE
+-- README.md                             # This file (you are here)
```

### Core Agent File
The agent definition at `.opencode/agents/RedTeamer.md` is the **complete security analysis framework** — 2,457 lines covering:
- Complete CWE taxonomy (CWE-1000 Research Concepts view)
- All SANS Top 25 with detection patterns
- 4-level Deep SAST engine (lexical → AST → dataflow → semantic)
- 16+ languages with per-framework patterns (Python/Django/Flask/FastAPI, JS/Express/React/Vue/Angular/Svelte, Java/Spring, C#/ASP.NET, Go, Rust, Solidity, PHP, Ruby, Swift, Kotlin, C/C++, Dart/Flutter, Scala, PowerShell, Vyper)
- Universal secrets detection (40+ regex + Shannon entropy)
- Complete attack library with verified exploitation chains
- Infrastructure security (AWS/GCP/Azure/K8s/Docker)
- AI/ML security (OWASP ML Top 10)
- Supply chain security (dependency confusion, typo-squatting)
- Business logic and side-channel vulnerability analysis
- Full remediation framework with production-ready fixes
- CI/CD integration templates (pre-commit, GitHub Actions, GitLab CI)

---

## References

### Standards & Frameworks

| Standard | Link |
|---|---|
| OWASP Top 10 (2021) | [owasp.org/Top10](https://owasp.org/Top10/) |
| CWE-1000 Research Concepts | [cwe.mitre.org/data/definitions/1000.html](https://cwe.mitre.org/data/definitions/1000.html) |
| CWE Top 25 (2024) | [cwe.mitre.org/top25](https://cwe.mitre.org/top25/) |
| OWASP ASVS | [owasp.org/ASVS](https://owasp.org/ASVS/) |
| OWASP API Security Top 10 | [owasp.org/API-Security](https://owasp.org/API-Security/) |
| OWASP ML Top 10 | [owasp.org/www-project-machine-learning-security-top-10](https://owasp.org/www-project-machine-learning-security-top-10/) |
| OWASP Mobile Top 10 | [owasp.org/Mobile-Top-10](https://owasp.org/Mobile-Top-10/) |
| NIST SP 800-53 | [csrc.nist.gov](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final) |
| NIST CSF | [nist.gov/cyberframework](https://www.nist.gov/cyberframework) |
| MITRE ATT&CK | [attack.mitre.org](https://attack.mitre.org/) |
| CIS Benchmarks | [cisecurity.org/cis-benchmarks](https://www.cisecurity.org/cis-benchmarks/) |
| CVSS 3.1 | [first.org/cvss](https://www.first.org/cvss/v3-1/) |
| OWASP Testing Guide | [owasp.org/wstg](https://owasp.org/wstg/) |

### Open Source Security Tools

| Tool | Purpose | Link |
|---|---|---|
| **Semgrep** | SAST rule engine — agent generates custom rules | [semgrep.dev](https://semgrep.dev/) |
| **CodeQL** | Semantic code analysis — agent fills language gaps | [codeql.github.com](https://codeql.github.com/) |
| **OWASP ZAP** | DAST / web app scanning — agent guides spider/scanner | [zaproxy.org](https://www.zaproxy.org/) |
| **Trivy** | Container, FS, and dependency scanning | [github.com/aquasecurity/trivy](https://github.com/aquasecurity/trivy) |
| **Nuclei** | Vulnerability template scanner — agent writes custom templates | [github.com/projectdiscovery/nuclei](https://github.com/projectdiscovery/nuclei) |
| **Gitleaks** | Secrets scanning — agent adds entropy + context analysis | [github.com/gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) |
| **TruffleHog** | Deep secrets discovery — agent adds per-language patterns | [github.com/trufflesecurity/trufflehog](https://github.com/trufflesecurity/trufflehog) |
| **Checkov** | IaC security scanning — agent adds context analysis | [github.com/bridgecrewio/checkov](https://github.com/bridgecrewio/checkov) |
| **Bearer** | SAST + privacy scanning — agent adds exploitation verification | [github.com/Bearer/bearer](https://github.com/Bearer/bearer) |
| **Falco** | Runtime security — agent recommends detection rules | [falco.org](https://falco.org/) |
| **Kube-bench** | Kubernetes CIS benchmark — agent interprets results | [github.com/aquasecurity/kube-bench](https://github.com/aquasecurity/kube-bench) |
| **ClamAV** | Malware scanning for uploaded files | [clamav.net](https://www.clamav.net/) |

### Training & Certification

| Resource | Link |
|---|---|
| PortSwigger Web Security Academy | [portswigger.net/web-security](https://portswigger.net/web-security) |
| OWASP Web Security Testing Guide | [owasp.org/wstg](https://owasp.org/wstg/) |
| Hack The Box | [hackthebox.com](https://www.hackthebox.com/) |
| PentesterLab | [pentesterlab.com](https://pentesterlab.com/) |
| SANS (GPEN, GWAPT, GXPN) | [sans.org](https://www.sans.org/) |
| Offensive Security (OSCP, OSED, OSEP) | [offensive-security.com](https://www.offensive-security.com/) |
| Certified Red Team Professional (CRTP) | [alteredsecurity.com](https://www.alteredsecurity.com/) |

---

## License

MIT — Copyright (c) 2026 Aporia

*"Every vulnerability is a fix waiting to be written."*

---

**RedTeamer** — Universal Vulnerability Detection Engine  
Created by **Aporia** — Full CWE Taxonomy | Deep SAST | 16+ Languages | AI/ML Security | Infrastructure Security | Supply Chain Security
