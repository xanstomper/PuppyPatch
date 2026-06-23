# Python Security Detection Patterns
# These are the signals the agent searches for when auditing Python code.

## SQL Injection
PATTERNS_SQLI = {
    "f-string in query": r'f["\'].*SELECT.*\{.*\}.*FROM',
    "string concat in query": r'("|\').*\bSELECT\b.*("|\')\s*\+',
    "modulo in query": r'("|\').*\bSELECT\b.*("|\')\s*\%',
    "raw execute": r'\.execute\(f["\']',
    "raw cursor": r'cursor\.execute\(.*\+',
}

## Command Injection
PATTERNS_CMD_INJ = {
    "os.system": r'os\.system\(.*input',
    "subprocess shell": r'subprocess\.(call|Popen|run)\(.*shell\s*=\s*True',
    "eval": r'eval\(.*input',
    "exec": r'exec\(.*input',
    "popen shell": r'Popen\(.*shell\s*=\s*True',
}

## Path Traversal
PATTERNS_PATH_TRAV = {
    "open with user input": r'open\(.*input',
    "send file user input": r'send_file\(.*input',
    "file open concat": r'open\(.*\+.*input',
}

## Insecure Deserialization
PATTERNS_DESERIAL = {
    "pickle loads": r'pickle\.loads\(',
    "yaml load": r'yaml\.load\(',
    "shelve open": r'shelve\.open\(',
}

## Hardcoded Secrets
PATTERNS_SECRETS = {
    "secret key": r'SECRET_KEY\s*=\s*["\'][a-zA-Z0-9!@#$%^&*()_+-=]{10,}["\']',
    "api key": r'(API_KEY|api_key)\s*=\s*["\'][a-zA-Z0-9]{16,}["\']',
    "password": r'PASSWORD\s*=\s*["\'][^"\']{6,}["\']',
}

## Weak Cryptography
PATTERNS_CRYPTO = {
    "md5": r'md5\(',
    "sha1": r'sha1\(',
    "ECB mode": r'AES\.MODE_ECB',
    "DES": r'DES\.new\(',
    "random for crypto": r'import random',
    "verify false": r'verify\s*=\s*False',
}

## Template Injection (SSTI)
PATTERNS_SSTI = {
    "render_template_string": r'render_template_string\(.*input',
    "string template": r'Template\(.*input',
    "jinja2 from string": r'from_string\(.*input',
}

## Django-Specific
PATTERNS_DJANGO = {
    "all fields": r'fields\s*=\s*["\']__all__["\']',
    "raw sql": r'\.raw\(".*%s?"\s*%',
    "debug true": r'DEBUG\s*=\s*True',
    "mark safe": r'mark_safe\(',
}

## Flask-Specific
PATTERNS_FLASK = {
    "debug true": r'app\.run\(.*debug\s*=\s*True',
    "secret hardcoded": r'app\.secret_key\s*=\s*["\'][^"\']+["\']',
    "cors all": r'allow_origins\s*=\s*\["\*"\]',
}
