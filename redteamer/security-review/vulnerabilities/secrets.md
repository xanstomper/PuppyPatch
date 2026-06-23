# Secrets Detection Reference — Complete Pattern Library

## Overview

This document contains all secret detection patterns used by the RedTeamer agent, including regex patterns, entropy analysis, context-aware detection, false positive reduction rules, and scanning methodology for all known secret types.

---

## PART 1: REGEX PATTERN LIBRARY

### 1.1 Cloud Provider Credentials

#### Amazon Web Services (AWS)

```regex
# AWS Access Key ID
AKIA[0-9A-Z]{16}
ASIA[0-9A-Z]{16}

# AWS Secret Access Key
(?i)aws[_-]?(secret[_-]?access[_-]?key|access[_-]?key[_-]?id|session[_-]?token)\s*[=:]\s*['"][A-Za-z0-9/+=]{20,60}['"]

# AWS Session Token (from STS)
(?i)aws[_-]?session[_-]?token\s*[=:]\s*['"][A-Za-z0-9/+=]{20,}['"]

# AWS AppSync Key
da2-[A-Za-z0-9]{26}

# AWS Marketplace Key
(?i)aws[_-]?marketplace[_-]?(key|token|secret)\s*[=:]\s*['"][A-Za-z0-9]{20,}['"]

# AWS MWS (Amazon MWS)
amzn\.mws\.[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}
```

#### Google Cloud Platform (GCP)

```regex
# GCP API Key
AIza[0-9A-Za-z\-_]{35}

# GCP Service Account (JSON key file pattern)
"type": "service_account"

# GCP OAuth Client ID
[0-9]+-[0-9a-zA-Z_]+\.apps\.googleusercontent\.com

# GCP OAuth Refresh Token
[0-9]+\/[0-9a-zA-Z\-_]+

# GCP Storage Access Token
(?i)(?:ya29|1\/[0-9a-zA-Z\-_]+)[0-9A-Za-z\-_]{30,}

# GCP Cloud SQL Credentials
(?i)gcp[_-]?(sql[_-]?password|db[_-]?password|database[_-]?password)\s*[=:]\s*['"][^'"]{8,}['"]

# GCP KMS Key Ring
(?i)projects\/[^\/]+\/locations\/[^\/]+\/keyRings\/[^\/]+\/cryptoKeys\/[^\/]+
```

#### Microsoft Azure

```regex
# Azure Subscription Key
(?i)azure[_-]?(subscription[_-]?key|api[_-]?key|management[_-]?key)\s*[=:]\s*['"][A-Za-z0-9]{32}['"]

# Azure Connection String
(?i)(AZURE_CONNECTION_STRING|azure[_-]?storage[_-]?connection[_-]?string)\s*[=:]\s*['"]DefaultEndpointsProtocol=

# Azure Storage Account Key
(?i)(AccountKey|storage[_-]?account[_-]?key)\s*[=:]\s*['"][A-Za-z0-9+/=]{86,88}['"]

# Azure SQL Connection String
(?i)Server=[^;]+;Database=[^;]+;User\s*Id=[^;]+;Password=

# Azure Service Bus Connection String
(?i)Endpoint=sb:\/\/(.+?)\.servicebus\.windows\.net\/;SharedAccessKeyName=

# Azure DevOps PAT
(?i)(azure[_-]?devops[_-]?pat|vsts[_-]?pat|azure[_-]?devops[_-]?token)\s*[=:]\s*['"][a-z0-9]{52}['"]

# Azure Container Registry Credentials
(?i)(acr[_-]?(username|password)|azure[_-]?container[_-]?registry[_-]?password)\s*[=:]\s*['"][^'"]+['"]

# Azure Functions Key
(?i)(x-functions-key|FunctionKey)\s*[:=]\s*['"][A-Za-z0-9+/=]{20,}['"]
```

#### Alibaba Cloud (Aliyun)

```regex
# Alibaba Cloud Access Key
(?i)(aliyun[_-]?(access[_-]?key|secret[_-]?key)|LTAI[0-9A-Za-z]{16,})

# Alibaba Cloud Secret
(?i)aliyun[_-]?secret\s*[=:]\s*['"][A-Za-z0-9]{30,}['"]
```

#### DigitalOcean

```regex
# DigitalOcean PAT
(?i)(dop_v1|do[_-]?personal[_-]?access[_-]?token|digitalocean[_-]?token)\s*[=:]\s*['"][0-9a-f]{64}['"]

# DigitalOcean OAuth Token
dop_v1_[0-9a-f]{64}

# DigitalOcean API Key
(?i)digitalocean[_-]?api[_-]?key\s*[=:]\s*['"][^'"]+['"]
```

#### IBM Cloud

```regex
# IBM Cloud API Key
(?i)(ibm[_-]?cloud[_-]?api[_-]?key|bluemix[_-]?api[_-]?key)\s*[=:]\s*['"][A-Za-z0-9\-_]{40,}['"]

# IBM Cloud IAM Token
(?i)ibm[_-]?iam[_-]?token\s*[=:]\s*['"][A-Za-z0-9\-_]{100,}['"]
```

#### Oracle Cloud (OCI)

```regex
# OCI API Key Fingerprint
(?i)oci[_-]?(api[_-]?key[_-]?fingerprint|fingerprint)\s*[=:]\s*['"][0-9a-f]{2}(?::[0-9a-f]{2}){15}['"]

# OCI User OCID
ocid1\.user\.oc1\.\.[A-Za-z0-9]{50,}

# OCI Tenancy OCID
ocid1\.tenancy\.oc1\.\.[A-Za-z0-9]{50,}

# OCI Private Key Pattern
-----BEGIN RSA PRIVATE KEY-----[A-Za-z0-9+/=]{100,}-----END RSA PRIVATE KEY-----
```

### 1.2 Version Control & Development Platforms

#### GitHub

```regex
# GitHub Personal Access Token (classic)
ghp_[A-Za-z0-9]{36}

# GitHub OAuth Access Token
gho_[A-Za-z0-9]{36}

# GitHub User-to-Server Token
ghu_[A-Za-z0-9]{36}

# GitHub Server-to-Server Token
ghs_[A-Za-z0-9]{36}

# GitHub Refresh Token
ghr_[A-Za-z0-9]{36}

# GitHub Fine-Grained PAT
github_pat_[A-Za-z0-9\-_]{82,}

# GitHub App Token
ghs_[0-9a-f]{64}

# GitHub SSH Key (deploy key)
(?i)git@github\.com:|ssh-rsa AAAA[0-9A-Za-z+/]+[=]{0,3}.*github\.com

# GitHub OIDC Token
(?i)action[_-]?id[_-]?token\s*[=:]\s*['"][A-Za-z0-9\-_]{100,}['"]
```

#### GitLab

```regex
# GitLab Personal Access Token
glpat-[A-Za-z0-9\-_]{20,35}

# GitLab CI/CD Token
(?i)(gitlab[_-]?ci[_-]?(token|job[_-]?token)|CI_JOB_TOKEN)\s*[=:]\s*['"][A-Za-z0-9\-_]{20,}['"]

# GitLab OAuth Token
(?i)gitlab[_-]?oauth[_-]?token\s*[=:]\s*['"][A-Za-z0-9\-_]{20,}['"]

# GitLab Runner Token
(?i)gitlab[_-]?runner[_-]?token\s*[=:]\s*['"][A-Za-z0-9\-_]{20,}['"]
```

#### Bitbucket

```regex
# Bitbucket App Password
(?i)bitbucket[_-]?(app[_-]?password|password)\s*[=:]\s*['"][A-Za-z0-9]{32}['"]

# Bitbucket OAuth Key
(?i)bitbucket[_-]?oauth[_-]?(key|consumer[_-]?key)\s*[=:]\s*['"][A-Za-z0-9]{32}['"]

# Bitbucket OAuth Secret
(?i)bitbucket[_-]?oauth[_-]?(secret|consumer[_-]?secret)\s*[=:]\s*['"][A-Za-z0-9]{48}['"]
```

### 1.3 Communication & Collaboration

#### Slack

```regex
# Slack Bot Token
xoxb-[A-Za-z0-9\-_]{20,}

# Slack Webhook URL
https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+

# Slack User Token
xoxp-[A-Za-z0-9\-_]{20,}

# Slack App-Token
xoxe-[A-Za-z0-9\-_]{20,}

# Slack Workspace Token
xoxa-[A-Za-z0-9\-_]{20,}

# Slack Workspace Access Token
xoxr-[A-Za-z0-9\-_]{20,}
```

#### Discord

```regex
# Discord Webhook URL
https://discord(?:app)?\.com/api/webhooks/[0-9]+/[A-Za-z0-9_-]+

# Discord Bot Token
[A-Za-z0-9\-_]{24}\.[A-Za-z0-9\-_]{6}\.[A-Za-z0-9\-_]{27}
```

#### Twilio

```regex
# Twilio Account SID
AC[A-Za-z0-9]{32}

# Twilio Auth Token
(?i)twilio[_-]?auth[_-]?token\s*[=:]\s*['"][A-Za-z0-9]{32}['"]

# Twilio API Key
SK[A-Za-z0-9]{32}
```

#### Telegram

```regex
# Telegram Bot Token
[0-9]{8,10}:[A-Za-z0-9\-_]{35}

# Telegram API Key
(?i)telegram[_-]?(bot[_-]?token|api[_-]?key)\s*[=:]\s*['"][0-9]+:[A-Za-z0-9\-_]+['"]
```

### 1.4 Payment & Fintech

#### Stripe

```regex
# Stripe Live Secret Key
(?i)sk_live_[0-9a-zA-Z]{24,}

# Stripe Live Publishable Key
(?i)pk_live_[0-9a-zA-Z]{24,}

# Stripe Test Secret Key
(?i)sk_test_[0-9a-zA-Z]{24,}

# Stripe Test Publishable Key
(?i)pk_test_[0-9a-zA-Z]{24,}

# Stripe Restricted Key
(?i)rk_live_[0-9a-zA-Z]{24,}

# Stripe Webhook Secret
whsec_[A-Za-z0-9\-_]{32,}
```

#### PayPal

```regex
# PayPal Client ID
(?i)paypal[_-]?client[_-]?id\s*[=:]\s*['"][A-Za-z0-9\-_]{80,}['"]

# PayPal Secret
(?i)paypal[_-]?secret\s*[=:]\s*['"][A-Za-z0-9\-_]{80,}['"]
```

#### Square

```regex
# Square Access Token
(?i)sq0atp-[0-9A-Za-z\-_]{22}

# Square OAuth Token
(?i)sq0csp-[0-9A-Za-z\-_]{22}
```

### 1.5 Database Connection Strings

```regex
# PostgreSQL
postgres(?:ql)?:\/\/[^:]+:[^@]+@[^:\/]+(?::\d+)?\/[^?\s]*

# MySQL
mysql:\/\/[^:]+:[^@]+@[^:\/]+(?::\d+)?\/[^?\s]*

# MongoDB
mongodb(?:\+srv)?:\/\/[^:]+:[^@]+@[^:\/]+(?::\d+)?\/[^?\s]*

# Redis
redis:\/\/[^:]+:[^@]+@[^:\/]+(?::\d+)?[\/\s]*

# RabbitMQ / AMQP
amqps?:\/\/[^:]+:[^@]+@[^:\/]+(?::\d+)?\/[^?\s]*

# Elasticsearch
https?:\/\/[^:]+:[^@]+@[^:\/]+:[0-9]+\/

# MSSQL / SQL Server
Server=[^;]+;Database=[^;]+;User\s*Id=[^;]+;Password=[^;]+

# Generic JDBC URL
jdbc:(?:mysql|postgresql|oracle|sqlserver):\/\/[^:]+:[^@]+@

# CockroachDB
cockroach(?:db)?:\/\/[^:]+:[^@]+@[^:\/]+(?::\d+)?\/[^?\s]*
```

### 1.6 Authentication Tokens & Keys

#### JSON Web Tokens (JWT)

```regex
# JWT (standard three-part JWT)
eyJ[A-Za-z0-9\-_]{10,}\.[A-Za-z0-9\-_]{10,}\.[A-Za-z0-9\-_]{10,}

# JWT with Bearer prefix
(?i)bearer\s+eyJ[A-Za-z0-9\-_]{10,}\.[A-Za-z0-9\-_]{10,}\.[A-Za-z0-9\-_]{10,}
```

#### OAuth Tokens

```regex
# OAuth 2.0 Access Token (generic)
(?i)(access_token|oauth_token)\s*[=:]\s*['"][A-Za-z0-9\-_]{20,}['"]

# OAuth 2.0 Client Secret
(?i)(client_secret)\s*[=:]\s*['"][A-Za-z0-9\-_!@#$%^&*()]{20,}['"]

# OAuth 2.0 Bearer Token (header)
(?i)authorization:\s*bearer\s+[A-Za-z0-9\-_.~+/]+=*

# Session ID
session[_-]?(id|token|key)?\s*[=:]\s*['"][A-Za-z0-9\-_]{20,}['"]

# CSRF Token
(?i)(csrf|xsrf)[_-]?token\s*[=:]\s*['"][A-Za-z0-9\-_]{16,}['"]
```

### 1.7 Private Keys & Certificates

```regex
# RSA/DSA/EC/OPENSSH Private Key
-----BEGIN (RSA|DSA|EC|OPENSSH|PGP|SSH2) PRIVATE KEY-----[A-Za-z0-9+/=\s]{100,}-----END

# SSH Public Key (authorized_keys)
ssh-(rsa|dss|ed25519)\s+AAAA[0-9A-Za-z+/]+[=]{0,3}\s+

# X.509 Certificate
-----BEGIN CERTIFICATE-----

# PGP Private Key Block
-----BEGIN PGP PRIVATE KEY BLOCK-----

# PKCS12 / PFX
(?i)(\.p12|\.pfx)\s*password\s*[=:]\s*['"][^'"]+['"]

# Java KeyStore (JKS) password
(?i)(keystore|jks)[_-]?(password|pass)\s*[=:]\s*['"][^'"]+['"]
```

### 1.8 Infrastructure & Container Registry

```regex
# Docker Hub Access Token
(?i)docker[_-]?(hub[_-]?)?(access[_-]?token|pat)\s*[=:]\s*['"][A-Za-z0-9\-_]{30,}['"]

# Docker Compose AWS ECR
(?i)ecr[_-]?(login|password|secret)\s*[=:]\s*['"][^'"]+['"]

# Kubernetes Secret (base64 pattern)
(?i)kind:\s*Secret[\s\S]{0,500}?data:\s*\n(?:\s{2,}[A-Za-z0-9\-_]+:\s*[A-Za-z0-9+/=]{10,}\n)+

# Kubeconfig user token
users:\s*- name:.*\n\s*user:\s*\n\s*[a-z_]+:\s*[A-Za-z0-9\-_]{30,}

# Terraform Cloud Token
(?i)terraform[_-]?(cloud[_-]?)?(token|api[_-]?token)\s*[=:]\s*['"][A-Za-z0-9\-_]{40,}['"]
```

### 1.9 Package Managers & Registries

```regex
# npm Token
npm_[A-Za-z0-9\-_]{36}
//registry\.npmjs\.org/:_authToken=[A-Za-z0-9\-_]{36}

# npm Authentication Token (legacy)
(?i)_authToken\s*=\s*[A-Za-z0-9\-_]{36}

# PyPI Token
pypi-[A-Za-z0-9\-_]{40,}

# RubyGems API Key
rubygems-[0-9a-f]{48}

# NuGet API Key
(?i)nuget[_-]?api[_-]?key\s*[=:]\s*['"][A-Za-z0-9\-_]{40,}['"]

# Composer / Packagist Token
(?i)(composer|packagist)[_-]?(token|api[_-]?key)\s*[=:]\s*['"][A-Za-z0-9\-_]{40,}['"]
```

### 1.10 CI/CD & Automation

```regex
# Jenkins API Token
(?i)jenkins[_-]?api[_-]?token\s*[=:]\s*['"][A-Za-z0-9]{32}['"]

# CircleCI Token
(?i)circle[_-]?ci[_-]?(token|api[_-]?token)\s*[=:]\s*['"][A-Za-z0-9\-_]{40}['"]

# Travis CI Token
(?i)travis[_-]?ci[_-]?(token|api[_-]?token)\s*[=:]\s*['"][A-Za-z0-9\-_]{22}['"]

# GitHub Actions Token
(?i)(GITHUB_TOKEN|ACTIONS_RUNTIME_TOKEN|ACTIONS_ID_TOKEN_REQUEST_TOKEN)

# GitLab CI Token
(?i)(CI_JOB_TOKEN|CI_REGISTRY_PASSWORD|CI_DEPLOY_PASSWORD)

# Ansible Vault Password
(?i)ansible[_-]?vault[_-]?password\s*[=:]\s*['"][^'"]+['"]

# Drone CI Token
(?i)drone[_-]?(token|server[_-]?token)\s*[=:]\s*['"][A-Za-z0-9\-_]{32,}['"]
```

### 1.11 Generic Secret Patterns

```regex
# Generic API Key (variable assignment)
(?i)(api[_-]?key|apikey|secret[_-]?key|access[_-]?key)\s*[=:]\s*['"][A-Za-z0-9_\-=@#$%^&*+]{16,}['"]

# Generic Token (variable assignment)
(?i)(token|auth[_-]?token|bearer[_-]?token)\s*[=:]\s*['"][A-Za-z0-9_\-=+/]{20,}['"]

# Generic Secret (variable assignment)
(?i)(secret|private[_-]?key)\s*[=:]\s*['"][A-Za-z0-9_\-=+/@#$%^&*]{16,}['"]

# Password Variable
(?i)(password|passwd|pwd|pass)\s*[=:]\s*['"][^'"]{8,}['"]
```

### 1.12 SAAS & Third-Party Services

```regex
# Heroku API Key
(?i)heroku[_-]?(api[_-]?key|token)\s*[=:]\s*['"][A-Za-z0-9\-_]{40,}['"]

# Firebase Admin SDK
(?i)firebase[_-]?(admin[_-]?sdk|private[_-]?key|database[_-]?url)\s*[=:]\s*['"][^'"]+['"]

# Firebase Cloud Messaging Key
(?i)(FCM_SERVER_KEY|firebase[_-]?cloud[_-]?messaging[_-]?key)\s*[=:]\s*['"][A-Za-z0-9\-_:]{100,}['"]

# SendGrid API Key
(?i)(sendgrid[_-]?api[_-]?key|SENDGRID_API_KEY)\s*[=:]\s*['"]SG\.[A-Za-z0-9\-_]{60,}['"]

# Mailgun API Key
(?i)(mailgun[_-]?api[_-]?key|MAILGUN_API_KEY)\s*[=:]\s*['"]key-[A-Za-z0-9]{32}['"]

# Mailchimp API Key
(?i)(mailchimp[_-]?api[_-]?key|MAILCHIMP_API_KEY)\s*[=:]\s*['"][A-Za-z0-9]{32}-us[0-9]{1,2}['"]

# New Relic API Key
(?i)(new[_-]?relic[_-]?api[_-]?key|NEW_RELIC_LICENSE_KEY)\s*[=:]\s*['"][A-Za-z0-9\-_]{40,}['"]

# Datadog API Key
(?i)(datadog[_-]?(api[_-]?key|app[_-]?key)|DD_API_KEY|DD_APP_KEY)\s*[=:]\s*['"][A-Za-z0-9]{32}['"]

# Datadog API Key (raw)
DATADOG_API_KEY=[A-Za-z0-9]{32}
DATADOG_APP_KEY=[A-Za-z0-9]{40}

# PagerDuty API Token
(?i)(pagerduty[_-]?api[_-]?token|PAGERDUTY_API_TOKEN)\s*[=:]\s*['"][A-Za-z0-9\-_]{20,}['"]

# Sentry DSN
https://[A-Za-z0-9]{32}@[^\/]+/[0-9]+
(?i)sentry[_-]?auth[_-]?token\s*[=:]\s*['"][A-Za-z0-9]{64}['"]

# Rollbar Token
(?i)rollbar[_-]?(access[_-]?token|post[_-]?server[_-]?token)\s*[=:]\s*['"][A-Za-z0-9]{32}['"]

# Sumo Logic Token
(?i)sumo[_-]?logic[_-]?(access[_-]?id|access[_-]?key|token)\s*[=:]\s*['"][A-Za-z0-9\-_]{20,}['"]

# Cloudflare API Key
(?i)cloudflare[_-]?(api[_-]?key|token|zone[_-]?id)\s*[=:]\s*['"][A-Za-z0-9\-_]{30,}['"]

# Fastly API Token
(?i)fastly[_-]?api[_-]?token\s*[=:]\s*['"][A-Za-z0-9\-_]{30,}['"]

# Akamai Credentials
(?i)akamai[_-]?(host|access[_-]?token|client[_-]?token|client[_-]?secret)\s*[=:]\s*['"][A-Za-z0-9\-_]+['"]

# Shopify Secret / Token
(?i)shopify[_-]?(secret[_-]?key|api[_-]?key|password|access[_-]?token)\s*[=:]\s*['"][A-Za-z0-9\-_]{30,}['"]

# Shopify API Token (raw)
shpat_[A-Za-z0-9\-_]{32}

# HubSpot API Key
(?i)hubspot[_-]?api[_-]?key\s*[=:]\s*['"][A-Za-z0-9\-_]{40,}['"]

# Auth0 Credentials
(?i)auth0[_-]?(domain|client[_-]?id|client[_-]?secret|management[_-]?api[_-]?token)\s*[=:]\s*['"][A-Za-z0-9\-_.]{10,}['"]

# Snowflake Credentials
(?i)snowflake[_-]?(account|user|password|warehouse|database|schema|private[_-]?key)\s*[=:]\s*['"][^'"]+['"]

# Confluent / Kafka Cloud
(?i)(confluent|kafka)[_-]?(api[_-]?key|api[_-]?secret|bootstrap[_-]?server)\s*[=:]\s*['"][A-Za-z0-9\-_]{16,}['"]

# Grafana API Key
(?i)grafana[_-]?api[_-]?key\s*[=:]\s*['"][A-Za-z0-9\-_]{40,}['"]

# SonarQube Token
(?i)sonarqube[_-]?token\s*[=:]\s*['"][A-Za-z0-9]{40}['"]

# Artifactory Credentials
(?i)artifactory[_-]?(user|password|api[_-]?key|token)\s*[=:]\s*['"][A-Za-z0-9\-_]{10,}['"]

# HashiCorp Vault Token
(?i)vault[_-]?(token|addr|auth[_-]?method|namespace)\s*[=:]\s*['"][A-Za-z0-9\-_.]{10,}['"]

# Vault Token
s\.[A-Za-z0-9\-_]{24,}

# Consul Token
(?i)consul[_-]?(token|acl[_-]?token|http[_-]?token)\s*[=:]\s*['"][A-Za-z0-9\-_]{20,}['"]

# Okta API Token
(?i)okta[_-]?api[_-]?token\s*[=:]\s*['"][A-Za-z0-9\-_]{40,}['"]

# OpenStack Credentials
(?i)OS_[A-Z_]+=(?:['"][^'"]+['"]|[A-Za-z0-9\-_]+)

# Zendesk API Token
(?i)zendesk[_-]?api[_-]?token\s*[=:]\s*['"][A-Za-z0-9\-_]{40,}['"]
```

---

## PART 2: ENTROPY-BASED DETECTION

### 2.1 Shannon Entropy Calculation

```python
import math
import re

def shannon_entropy(s: str) -> float:
    """Calculate Shannon entropy in bits per character.
    Higher entropy = more random-looking string.
    """
    if not s:
        return 0.0
    s = s.strip()
    if len(s) < 8:
        return 0.0
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    entropy = -sum((f / len(s)) * math.log2(f / len(s)) for f in freq.values())
    return entropy

def is_high_entropy_string(s: str, threshold: float = 4.5) -> bool:
    """Determine if a string looks like a secret based on entropy."""
    if len(s) < 14:
        return False
    return shannon_entropy(s) >= threshold
```

### 2.2 Context-Aware Entropy Detection

```python
CONTEXT_KEYWORDS = {
    "high_confidence": [
        "api_key", "apikey", "secret", "token", "password", "passwd",
        "credentials", "auth", "bearer", "jwt", "access_key", "secret_key",
        "private_key", "ssh_key", "pem", "certificate", "connection_string",
    ],
    "medium_confidence": [
        "key", "pass", "pwd", "login", "token", "client_secret",
        "client_id", "consumer_key", "consumer_secret", "signing_key",
        "encryption_key", "master_key", "admin", "db_password",
    ],
    "low_confidence": [
        "hash", "salt", "iv", "nonce", "signature", "hmac",
        "fingerprint", "thumbprint", "credential",
    ],
}

def entropy_with_context(line: str, threshold: float = 4.2) -> list:
    """Detect secrets using entropy + context analysis."""
    results = []
    assignments = re.findall(
        r'''([\'\"]?)([A-Za-z_][A-Za-z0-9_]*)\1\s*[=:]\s*([\'\"])([^\'\"]{8,})\3''',
        line
    )
    for match in assignments:
        var_name = match[1].lower()
        value = match[3]
        ent = shannon_entropy(value)
        confidence = "low"
        for kw in CONTEXT_KEYWORDS["high_confidence"]:
            if kw in var_name:
                confidence = "high"
                break
        if confidence == "low":
            for kw in CONTEXT_KEYWORDS["medium_confidence"]:
                if kw in var_name:
                    confidence = "medium"
                    break
        thresh = 4.0 if confidence == "high" else 4.5 if confidence == "medium" else 5.0
        if ent >= thresh:
            results.append({
                "variable": match[1],
                "value_preview": value[:8] + "...",
                "entropy": round(ent, 2),
                "confidence": confidence,
                "line": line.strip(),
            })
    return results
```

### 2.3 Entropy Thresholds by Secret Type

| Secret Type | Min Length | Min Entropy | Notes |
|---|---|---|---|
| API Keys | 16 | 4.5 | High ASCII randomness |
| JWT Tokens | 20 | 5.0 | Base64url, high entropy |
| AWS Keys | 20 | 5.5 | Mixed case + digits |
| Private Keys | 100 | 5.8 | Base64, very high entropy |
| Passwords | 8 | 3.5 | Lower entropy possible |
| Connection Strings | 20 | 4.0 | Structured but mixed |
| OAuth Tokens | 20 | 4.8 | Random alphanumeric |
| Session IDs | 16 | 4.2 | Moderate entropy |

### 2.4 Multi-Factor Secret Detection (N-Gram + Entropy)

```python
def ngram_entropy(s: str, n: int = 3) -> float:
    """Calculate entropy based on character n-grams.
    Better at distinguishing random strings from natural language.
    """
    if len(s) < n:
        return 0.0
    ngrams = {}
    for i in range(len(s) - n + 1):
        gram = s[i:i+n]
        ngrams[gram] = ngrams.get(gram, 0) + 1
    total = len(s) - n + 1
    return -sum((c / total) * math.log2(c / total) for c in ngrams.values())

def is_likely_secret(s: str) -> bool:
    """Multi-factor secret detection."""
    checks = {
        "length_ok": len(s) >= 14,
        "high_entropy": shannon_entropy(s) >= 4.2,
        "high_ngram": ngram_entropy(s) >= 4.5,
        "has_digits": bool(re.search(r'\d', s)),
        "has_mixed_case": bool(re.search(r'[a-z]', s)) and bool(re.search(r'[A-Z]', s)),
        "has_special": bool(re.search(r'[^a-zA-Z0-9]', s)),
        "no_natural_words": not bool(re.search(
            r'(?i)\b(?:the|and|for|are|but|not|you|all|can|had|her|was|one|our|out)\b', s
        )),
    }
    score = sum(1 for v in checks.values() if v)
    return score >= 4
```

---

## PART 3: FALSE POSITIVE REDUCTION

### 3.1 Context Validation Rules

```python
class FalsePositiveReduction:
    """Rules to reduce false positives in secret detection."""

    @staticmethod
    def is_false_positive(line: str, value: str) -> bool:
        checks = [
            FalsePositiveReduction._is_documentation(line),
            FalsePositiveReduction._is_test_or_mock(line),
            FalsePositiveReduction._is_version_hash(line),
            FalsePositiveReduction._is_url_or_path(line),
            FalsePositiveReduction._is_commit_hash(line),
            FalsePositiveReduction._is_known_non_secret(line, value),
            FalsePositiveReduction._is_example_code(line),
            FalsePositiveReduction._is_image_data(value),
        ]
        return any(checks)

    @staticmethod
    def _is_documentation(line: str) -> bool:
        pats = [
            r'(?i)#\s*(TODO|FIXME|HACK|XXX|NOTE|EXAMPLE|DEMO)',
            r'(?i)(docs?|documentation|example|sample|tutorial|guide)',
            r'(?i)(replace|placeholder|your[_-]?(key|token|secret))',
        ]
        return any(re.search(p, line) for p in pats)

    @staticmethod
    def _is_test_or_mock(line: str) -> bool:
        pats = [
            r'(?i)(test|mock|fake|dummy|stub|sample)[_-]?(key|token|secret|password)',
            r'(?i)(test_?key|test_?token|test_?password|test_?secret)',
            r'(?i)example\.com|example\.org|example\.net',
            r'(?i)000000|123456|abcdef|password|qwerty',
        ]
        return any(re.search(p, line) for p in pats)

    @staticmethod
    def _is_version_hash(line: str) -> bool:
        pats = [
            r'[0-9a-f]{40}\s',  # git commit hash
            r'[0-9a-f]{32}\s',  # MD5
            r'[0-9a-f]{64}\s',  # SHA-256
            r'version\s*=\s*[\'"][0-9]+\.[0-9]+\.[0-9]+',
        ]
        return any(re.search(p, line) for p in pats)

    @staticmethod
    def _is_url_or_path(line: str) -> bool:
        return bool(re.search(r'https?://[^\s]+|/\w+/\w+/\w+', line))

    @staticmethod
    def _is_commit_hash(line: str) -> bool:
        return bool(re.match(r'^[0-9a-f]{7,40}$', line.strip()))

    @staticmethod
    def _is_known_non_secret(line: str, value: str) -> bool:
        common = [
            "example", "test", "demo", "sample", "placeholder", "changeme",
            "your-api-key-here", "your-token-here", "your-secret-here",
            "REPLACE_ME", "TODO", "FIXME", "XXXXX",
        ]
        return value.lower().strip() in common

    @staticmethod
    def _is_example_code(line: str) -> bool:
        pats = [
            r'(?i)#\s*(Example|e\.g\.|for example|such as)',
            r'(?i)(https?://)?(example|your[_-]?(domain|org|com))',
            r'(?i)\.\.\.\s*$',
        ]
        return any(re.search(p, line) for p in pats)

    @staticmethod
    def _is_image_data(value: str) -> bool:
        prefixes = ['iVBOR', '/9j/', 'R0lGOD', 'AAAB', 'AAAA']
        return any(value.strip().startswith(p) for p in prefixes)
```

### 3.2 Whitelist Management

```python
class SecretWhitelist:
    """Manage whitelisted values to prevent recurring false positives."""

    def __init__(self, whitelist_file: str = None):
        self.exact_matches: set = set()
        self.patterns: list = []
        if whitelist_file:
            self.load(whitelist_file)

    def add_exact(self, value: str):
        self.exact_matches.add(value)

    def add_pattern(self, pattern: str):
        self.patterns.append(re.compile(pattern))

    def is_whitelisted(self, value: str, context: str = "") -> bool:
        if value in self.exact_matches:
            return True
        return any(p.search(context) for p in self.patterns)

    def load(self, filepath: str):
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    self.add_exact(line)
```

---

## PART 4: SCANNING METHODOLOGY

### 4.1 File Priority Matrix

| Priority | File Types | Scan Strategy |
|---|---|---|
| Critical | `.env`, `.env.*`, `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks`, `credentials`, `.netrc` | Regex + entropy, full content |
| High | `*.py`, `*.js`, `*.ts`, `*.java`, `*.cs`, `*.go`, `*.rs`, `*.rb`, `*.php`, `*.swift`, `*.kt` | Regex + entropy on string literals |
| High | `requirements.txt`, `package.json`, `Cargo.toml`, `go.mod`, `Gemfile`, `Pipfile` | Dependency token patterns |
| High | `*.yaml`, `*.yml` (K8s, Docker, CI/CD) | Infrastructure credentials |
| Medium | `*.json`, `*.xml`, `*.config`, `*.ini`, `*.cfg`, `*.conf`, `*.properties` | Config credentials |
| Medium | `*.md`, `*.rst`, `*.txt` | Documentation leaks |
| Medium | Dockerfile, docker-compose* | Build secrets |
| Low | `*.log`, `*.sql`, `*.csv` | Historical data |

### 4.2 Git History Scanning

```bash
# Scan all commits in git history
git log --all --full-history --diff-filter=A -- '*.env' '*.pem' '*.key'

# Search entire git history for a specific pattern
git rev-list --all | xargs git grep 'AKIA[0-9A-Z]\{16\}'

# Full git history secret scan (all branches, all tags)
git log --all --full-history -p -- '*.py' '*.js' '*.ts' '*.env' | grep -E '(api.key|secret|password|token)\s*[:=]'

# Check blob contents that are no longer in HEAD
git fsck --lost-found | grep blob | while read -r line; do
    hash=$(echo "$line" | awk '{print $3}')
    git show "$hash" | grep -q 'AKIA' && echo "Secret in lost blob: $hash"
done
```

### 4.3 Prevention Patterns & Best Practices

```python
# Environment Variables (GOOD)
import os
API_KEY = os.environ.get("STRIPE_SECRET_KEY")
if not API_KEY:
    raise RuntimeError("STRIPE_SECRET_KEY not set")

# Secrets Manager (BETTER)
# from vault import get_secret
# API_KEY = get_secret("stripe/live/api_key")

# Cloud Secret Store (BEST)
# AWS: boto3.client('secretsmanager').get_secret_value(SecretId='prod/stripe')
# GCP: google.cloud.secretmanager.SecretManagerServiceClient()
# Azure: azure.identity.DefaultAzureCredential()

# .gitignore rules for secrets
cat >> .gitignore << 'EOF'
.env
.env.*
*.pem
*.key
*.p12
*.pfx
*.jks
credentials
*.cred
secrets/
EOF
```

---

## PATTERN INDEX (Summary Table)

| # | Category | Patterns | Severity |
|---|---|---|---|
| 1 | AWS | 8 patterns | CRITICAL |
| 2 | GCP | 7 patterns | CRITICAL |
| 3 | Azure | 8 patterns | CRITICAL |
| 4 | Alibaba Cloud | 2 patterns | HIGH |
| 5 | DigitalOcean | 3 patterns | HIGH |
| 6 | IBM Cloud | 2 patterns | HIGH |
| 7 | Oracle Cloud | 4 patterns | HIGH |
| 8 | GitHub | 9 patterns | HIGH |
| 9 | GitLab | 4 patterns | HIGH |
| 10 | Bitbucket | 3 patterns | HIGH |
| 11 | Slack | 6 patterns | HIGH |
| 12 | Discord | 2 patterns | HIGH |
| 13 | Twilio | 3 patterns | HIGH |
| 14 | Telegram | 2 patterns | MEDIUM |
| 15 | Stripe | 6 patterns | CRITICAL |
| 16 | PayPal | 2 patterns | CRITICAL |
| 17 | Square | 2 patterns | HIGH |
| 18 | Database Connections | 10 patterns | CRITICAL |
| 19 | JWT/OAuth | 6 patterns | HIGH |
| 20 | Private Keys | 6 patterns | CRITICAL |
| 21 | Docker/K8s/Terraform | 6 patterns | HIGH |
| 22 | Package Managers | 5 patterns | HIGH |
| 23 | CI/CD | 10 patterns | HIGH |
| 24 | Generic Secrets | 4 patterns | MEDIUM |
| 25 | SAAS Services | 25+ patterns | MEDIUM-HIGH |

Total: 25+ categories, 130+ regex patterns for secret detection.
