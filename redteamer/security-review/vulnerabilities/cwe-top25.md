# CWE Top 25 (2024) — Detection Signatures

## CWE-79: Cross-Site Scripting
**CVSS**: 6.1 (Medium)
**Detection**: Unescaped user input in HTML/JS/CSS context

### Per-Framework Detection
```javascript
// React
dangerouslySetInnerHTML={{__html: userContent}}  // HIGH

// Vue
v-html="userContent"  // HIGH

// Angular
[innerHTML]="userContent"  // HIGH
bypassSecurityTrustHtml(userInput)  // CRITICAL

// Django
{{ user_input|safe }}  // HIGH
mark_safe(user_input)   // HIGH

// Flask
render_template_string(user_input)  // CRITICAL (SSTI + XSS)

// Express
res.send(user_input)  // HIGH (HTML content type)
res.render(user_input)  // CRITICAL (SSTI)
```

## CWE-89: SQL Injection
**CVSS**: 9.8 (Critical)
**Detection**: String concatenation/formatting in SQL queries

## CWE-78: OS Command Injection
**CVSS**: 9.8 (Critical)
**Detection**: User input in shell commands

## CWE-20: Improper Input Validation
**CVSS**: 8.2 (High)
**Detection**: Missing type/length/range checks on inputs

## CWE-125: Out-of-Bounds Read
**CVSS**: 7.5 (High)
**Languages**: C, C++, Rust (unsafe)

## CWE-22: Path Traversal
**CVSS**: 7.5 (High)
**Detection**: User input in file paths without canonicalization

## CWE-352: Cross-Site Request Forgery
**CVSS**: 6.5 (Medium)
**Detection**: Missing CSRF token on state-changing endpoints

## CWE-434: Unrestricted File Upload
**CVSS**: 8.8 (High)
**Detection**: Missing content validation on uploads

## CWE-476: NULL Pointer Dereference
**CVSS**: 5.5 (Medium)
**Languages**: C, C++, Java, C#

## CWE-502: Deserialization of Untrusted Data
**CVSS**: 9.8 (Critical)
**Detection**: `pickle.loads()`, `readObject()`, `unserialize()`

## CWE-862: Missing Authorization
**CVSS**: 8.6 (High)
**Detection**: Endpoints without auth checks

## CWE-863: Incorrect Authorization
**CVSS**: 8.1 (High)
**Detection**: Auth check but wrong scope/role

## CWE-269: Improper Privilege Management
**CVSS**: 8.4 (High)
**Detection**: Running with excessive privileges

## CWE-295: Improper Certificate Validation
**CVSS**: 7.5 (High)
**Detection**: `verify=False`, `InsecureSkipVerify: true`

## CWE-287: Improper Authentication
**CVSS**: 9.1 (Critical)
**Detection**: Weak or missing auth on sensitive endpoints

## CWE-190: Integer Overflow
**CVSS**: 7.5 (High)
**Detection**: Arithmetic without overflow checks

## CWE-611: Improper XML External Entity (XXE)
**CVSS**: 7.5 (High)
**Detection**: XML parsers with external entities enabled

## CWE-200: Information Exposure
**CVSS**: 5.3 (Medium)
**Detection**: Stack traces, debug pages, version disclosure

## CWE-918: Server-Side Request Forgery
**CVSS**: 8.6 (High)
**Detection**: User-controlled URL fetched server-side

## CWE-362: Race Condition
**CVSS**: 7.0 (High)
**Detection**: Check-then-act patterns without locking

## CWE-787: Out-of-Bounds Write
**CVSS**: 9.8 (Critical)
**Languages**: C, C++

## CWE-400: Uncontrolled Resource Consumption
**CVSS**: 7.5 (High)
**Detection**: Missing rate limits, unbounded loops, large allocations

## CWE-611: XXE (duplicate above)
## CWE-94: Code Injection
**CVSS**: 9.8 (Critical)
**Detection**: `eval()`, `exec()`, `new Function()`, dynamic import

## CWE-77: Command Injection (see CWE-78)
## CWE-119: Buffer Overflow
**CVSS**: 9.8 (Critical)
**Languages**: C, C++
