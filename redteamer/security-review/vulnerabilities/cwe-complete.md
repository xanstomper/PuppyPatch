# Complete CWE Taxonomy Reference (CWE-1000 Research Concepts View)

## Overview

This document covers the full CWE-1000 Research Concepts taxonomy organized by major pillars. Each entry includes CWE-ID, description, detection patterns, and language-specific examples.

---

## PILLAR 1: Memory Safety (CWE-119 Series — Buffer Operations)

### CWE-119: Buffer Buffer Overflow
**Description**: Writing data beyond buffer bounds, overwriting adjacent memory.
**CVSS Base**: 9.8 (Critical)
**Languages**: C, C++, Assembly
**Detection**:
- `strcpy`, `sprintf`, `gets`, `scanf` without length limits
- `memcpy` with attacker-controlled size
- Array indexing without bounds check

```c
// BAD
char buf[10];
strcpy(buf, user_input);  // Overflow if input > 9 chars

// FIXED
strncpy(buf, user_input, sizeof(buf) - 1);
buf[sizeof(buf) - 1] = '\0';
```

### CWE-120: Classic Buffer Overflow
**Sub-type of CWE-119**. Standard case of copying data without bounds.
**Detection**: `strcpy`, `wcscpy`, `lstrcpy`, `strcat`, `sprintf`

### CWE-121: Stack-Based Buffer Overflow
**Description**: Overflow on stack frame (return address, saved EBP).
**Exploitation**: Overwrite return address → control EIP → ROP chain.
```c
void vuln(char *input) {
    char buf[64];
    strcpy(buf, input);  // Stack smash
}
```

### CWE-122: Heap-Based Buffer Overflow
**Description**: Overflow on heap memory region.
**Exploitation**: Corrupt chunk metadata → arbitrary write primitive.
```c
void vuln(char *input) {
    char *buf = malloc(64);
    strcpy(buf, input);  // Heap overflow
}
```

### CWE-123: Write-WHAT-Where Condition
**Description**: Attacker controls both value and target address of a write.

### CWE-124: Buffer Underwrite
**Description**: Writing before the start of a buffer.

### CWE-125: Out-of-Bounds Read
**Description**: Reading memory beyond buffer bounds → information disclosure.
**CVSS Base**: 7.5 (High)
**Languages**: C, C++, Rust (unsafe)
```c
int arr[10];
int val = arr[user_index];  // OOB read if index > 9
```

### CWE-126: Buffer Over-read
**Description**: Reading more data than the buffer contains.

### CWE-127: Buffer Under-read
**Description**: Reading before the start of a buffer.

### CWE-129: Improper Validation of Array Index
**Description**: Array index not validated.
```java
int val = arr[userInput];  // Missile if userInput < 0 or >= arr.length
```
**Fix**: Validate bounds before indexing.

### CWE-130: Improper Handling of Length Parameter
**Description**: Length from user used in memory operations without validation.

### CWE-131: Incorrect Calculation of Buffer Size
**Description**: Off-by-one or overflow in size calculation leading to undersized allocation.
```c
size_t size = n * sizeof(int);  // Integer overflow if n is large
buf = malloc(size);
```

### CWE-134: Use of Externally-Controlled Format String
**Description**: User input used as format string argument.
```c
printf(user_input);   // BAD: format string vuln
printf("%s", user_input);  // FIXED
```
**Detection regex**: `\bprintf\([^"]*[a-zA-Z]`, `\b(sprintf|fprintf|snprintf)\([^,]*[a-zA-Z]`

### CWE-135: Incorrect Calculation of Multi-Byte String Length
**Description**: Byte count vs character count mismatch with wide/multi-byte strings.

### CWE-170: Improper Null Termination
**Description**: Missing null terminator leading to OOB read.
```c
char buf[10];
strncpy(buf, input, sizeof(buf));  // No null terminator if input >= 10
buf[sizeof(buf) - 1] = '\0';       // FIXED
```

### CWE-188: Reliance on Data/Memory Layout
**Description**: Assuming specific struct packing, endianness, or alignment.

### CWE-194: Unexpected Sign Extension
**Description**: Signed to unsigned conversion causing unexpected large value.
```c
int len = get_user_len();  // Could be negative
memcpy(buf, src, len);     // len becomes huge unsigned
```

### CWE-195: Signed to Unsigned Conversion Error
**Description**: Sign bits cause unexpected values in comparisons.

### CWE-196: Unsigned to Signed Conversion Error
**Description**: Large unsigned value becomes negative signed.

### CWE-197: Numeric Truncation Error
**Description**: Integer truncated during assignment/cast.
```c
uint64_t big = 0x1FFFFFFFF;
uint32_t small = big;  // Truncated to 0xFFFFFFFF
```

### CWE-198: Use of Incorrect Byte Ordering
**Description**: Endianness mismatch in network/application data.

### CWE-242: Use of Inherently Dangerous Function
**Description**: Using `gets`, `strcpy`, `strcat`, `sprintf` without bounds.
```c
gets(buf);        // No bounds checking at all
```
**Detection regex**: `\b(gets|strcpy|strcat|sprintf|scanf|sscanf|vsprintf|wcscpy)\s*\(`

### CWE-243: Creation of chroot Jail in Wrong Working Directory
**Description**: `chroot()` without `chdir("/")` leaves escape possible.

### CWE-244: Improper Clearing of Heap Memory Before Release
**Description**: Sensitive data remains in freed heap memory.

### CWE-415: Double Free
**Description**: `free()` called twice on same pointer.
```c
free(ptr);
free(ptr);  // Double free → heap corruption
```

### CWE-416: Use After Free
**Description**: Memory used after being freed.
```c
free(ptr);
ptr->data = val;  // UAF → arbitrary code execution
```

### CWE-457: Use of Uninitialized Variable
**Description**: Variable read before being initialized.

### CWE-458: Reliance on Global Variables in Re-entrant Code
**Description**: Global state in signal handlers or multi-threaded code.

### CWE-464: Addition of Data Structure Sentinel
**Description**: Incorrect sentinel value usage.

### CWE-466: Return of Pointer Value Outside of Expected Range
**Description**: Pointer arithmetic produces address outside expected range.

### CWE-467: Use of sizeof() on a Pointer Type
**Description**: `sizeof(ptr)` when `sizeof(*ptr)` was intended.
```c
memset(buf, 0, sizeof(buf));  // sizeof(pointer) = 8, not array size
```

### CWE-468: Incorrect Pointer Scaling
**Description**: Multiplying pointer dereference by element size incorrectly.

### CWE-469: Use of Pointer Subtraction to Determine Size
**Description**: Subtracting pointers from different objects (undefined behavior).

### CWE-476: NULL Pointer Dereference
**Description**: Dereferencing a null pointer.
**Languages**: C, C++, Java, C#, Rust (unsafe)
```java
if (obj != null) {  // Missing null check
    obj.doSomething();  // NullPointerException
}
```

### CWE-478: Missing Default Case in Switch
**Description**: Switch statement missing default case.

### CWE-479: Signal Handler Use of a Non-Reentrant Function
**Description**: `printf`, `malloc` in signal handler → undefined behavior.

### CWE-480: Use of Incorrect Operator
**Description**: `=` used instead of `==`.
```c
if (x = 5) {  // Assignment, not comparison
```

### CWE-481: Assigning Instead of Comparing
**Description**: Same as CWE-480.

### CWE-482: Comparing Instead of Assigning
**Description**: `==` used where `=` was intended.

### CWE-483: Incorrect Block Delimitation
**Description**: Missing braces create unexpected control flow.
```c
if (condition)
    do_something();
    do_something_else();  // Always executes!
```

### CWE-484: Omitted Break Statement in Switch
**Description**: Fall-through in switch statement.
```c
switch(c) {
    case 'a':
        foo();  // Falls through to 'b'
    case 'b':
        bar();
}
```

### CWE-561: Dead Code
**Description**: Code that can never execute.

### CWE-562: Return of Stack Variable Address
**Description**: Function returns pointer to local variable.
```c
int *get_val() {
    int x = 5;
    return &x;  // Dangling pointer
}
```

### CWE-587: Assignment of a Fixed Address to a Pointer
**Description**: Hardcoded memory address.

### CWE-588: Attempt to Access Child of a Non-struct Pointer
**Description**: Incorrect pointer casting to access struct members.

### CWE-590: Free of Memory Not on the Heap
**Description**: `free()` on stack memory, static memory, or string literal.
```c
char buf[64];
free(buf);  // Error: not heap memory
```

### CWE-617: Reachable Assertion
**Description**: Assertion that can be triggered by attacker → DoS.

### CWE-690: Unchecked Return Value to NULL Pointer Dereference
**Description**: Not checking malloc/calloc return value.

### CWE-761: Free of Pointer not at Start of Buffer
**Description**: `free()` on pointer into middle of allocation.

### CWE-762: Mismatched Memory Management Routines
**Description**: `malloc`/`delete`, `new`/`free` — cross-CRT mismatches.

### CWE-763: Release of Invalid Pointer or Reference
**Description**: Freeing uninitialized or already-freed pointer.

### CWE-764: Multiple Locks of a Critical Resource
**Description**: Double lock causing deadlock or undefined behavior.

### CWE-765: Multiple Unlocks of a Critical Resource
**Description**: Double unlock.

### CWE-767: Access to Critical Private Variable via Public Method
**Description**: Public getter returns reference to private mutable object.

### CWE-768: Incorrect Short Circuit Evaluation
**Description**: Side effects skipped due to short-circuit evaluation.

### CWE-769: Uncontrolled File Descriptor Consumption
**Description**: Not closing file descriptors → DoS via fd exhaustion.

### CWE-770: Allocation of Resources Without Limits
**Description**: Unbounded memory allocation.

### CWE-771: Missing Reference to Active Allocated Resource
**Description**: Lost pointer to allocation → memory leak.

### CWE-772: Missing Release of Resource
**Description**: Resource leak (files, sockets, handles).

### CWE-773: Missing Reference to Active File Descriptor or Handle
**Description**: File descriptor leak.

### CWE-774: Allocation of File Descriptors or Handles Without Limits
**Description**: FD/handle exhaustion DoS.

### CWE-775: Missing Release of File Descriptor or Handle
**Description**: FD not closed after use.

### CWE-781: Improper Address Validation in IOCTL
**Description**: IOCTL handler doesn't validate user-provided addresses.

### CWE-782: Exposed IOCTL with Insufficient Access Control
**Description**: IOCTL accessible from user space without permission.

### CWE-783: Operator Precedence Logic Error
**Description**: Bitwise vs logical operator confusion.

### CWE-784: Reliance on Cookies Without Validation
**Description**: Trusting cookie values without HMAC/integrity.

### CWE-785: Use of Path Manipulation Function without Maximum-Sized Buffer
**Description**: RealPath without size argument.

### CWE-786: Access of Memory Location Before Start of Buffer
**Description**: Negative index on array/pointer.

### CWE-787: Out-of-Bounds Write
**Description**: Writing past buffer end.
**CVSS Base**: 9.8 (Critical)
```c
char buf[10];
buf[user_index] = 0;  // Write OOB if user_index >= 10 or < 0
```

### CWE-788: Access of Memory Location After End of Buffer
**Description**: Just past buffer access.

### CWE-789: Memory Allocation with Excessive Size Value
**Description**: Unvalidated size → massive allocation → DoS.

### CWE-805: Buffer Access with Incorrect Length Value
**Description**: Length mismatch in buffer operations.

### CWE-806: Buffer Access Using Size of Source Buffer
**Description**: Using source size instead of destination size.
```c
char dst[10];
strncpy(dst, src, sizeof(src));  // Should be sizeof(dst)
```

### CWE-822: Untrusted Pointer Dereference
**Description**: Dereferencing attacker-controlled pointer.

### CWE-823: Use of Out-of-Range Pointer Offset
**Description**: Pointer arithmetic results in pointer outside valid range.

### CWE-824: Access of Uninitialized Pointer
**Description**: Using possibly uninitialized pointer.

### CWE-825: Expired Pointer Dereference
**Description**: Using pointer to freed/reallocated memory.

### CWE-826: Premature Release of Resource During Acceptable Lifetime
**Description**: Resource freed while still in use by other code path.

---

## PILLAR 2: Input Validation (CWE-20, CWE-138 Series)

### CWE-20: Improper Input Validation
**Description**: Application receives data from external source but does not validate type, length, format, or range.
**CVSS Base**: 8.2 (High)
**Detection**: Missing type checks, length checks, range validation, format validation, allowlist vs denylist.
```python
# BAD: No validation
def process(data):
    db.execute(f"SELECT * FROM users WHERE id = {data}")

# FIXED: Type and range validation
def process(data):
    if not isinstance(data, int) or data < 0:
        raise ValueError("Invalid id")
    db.execute("SELECT * FROM users WHERE id = %s", (data,))
```

### CWE-21: Path Traversal (Equivalence)
**See CWE-22 series.**

### CWE-22: Path Traversal
**Description**: User input used in file path operations without canonicalization.
**CVSS Base**: 7.5 (High)
**Detection**: User input in file operations without path normalization.
```python
# BAD
filepath = os.path.join(UPLOAD_DIR, filename)
with open(filepath) as f: ...

# FIXED
real_path = os.path.realpath(os.path.join(UPLOAD_DIR, filename))
if not real_path.startswith(os.path.realpath(UPLOAD_DIR)):
    raise ValueError("Invalid path")
```
**Bypass techniques**: `../`, `..\\`, URL encoding double encoding, Unicode, null byte.

### CWE-23: Relative Path Traversal
**Description**: Path traversal using relative paths (`../`).

### CWE-24: Path Traversal (..filedir)
**Description**: Using `..` in filenames.

### CWE-25: Path Traversal (/directory/)
**Description**: Using `/` or `//` prefix.

### CWE-26: Path Traversal (dir/../filename)
**Description**: Embedded `..` segments.

### CWE-27: Path Traversal (dir/../../filename)
**Description**: Multiple `..` traversals.

### CWE-28: Path Traversal (input/./../filename)
**Description**: `.` current directory component.

### CWE-29: Path Traversal (input/\\..\\filename)
**Description**: Backslash-based path traversal on Windows.

### CWE-30: Path Traversal (dir/..\\filename)
**Description**: Mixed separator traversal.

### CWE-31: Path Traversal (dir\\..\\filename)
**Description**: Pure backslash traversal.

### CWE-32: Path Traversal (..\\..\\filename)
**Description**: Multiple backslash traversals.

### CWE-33: Path Traversal (....//....//)
**Description**: Long path traversal bypass for filters.

### CWE-34: Path Traversal (..%2f)
**Description**: URL-encoded path traversal.

### CWE-35: Path Traversal (file:)
**Description**: Using `file://` URI scheme.

### CWE-36: Absolute Path Traversal
**Description**: Using absolute paths like `/etc/passwd`, `C:\Windows\System32\`.

### CWE-37: Path Traversal (\\UNC\share)
**Description**: Windows UNC path traversal.

### CWE-38: Path Traversal (\\?\C:\)
**Description**: Windows extended-length path.

### CWE-39: Path Traversal (C:\dirname)
**Description**: Absolute Windows drive path.

### CWE-40: Path Traversal (\\UNC\)
**Description**: UNC share root traversal.

### CWE-41: Path Traversal (\\\\share\\)
**Description**: UNC root access.

### CWE-42: Path Equivalence ('filename.' trailing dot)
**Description**: Trailing dot bypass on Windows.

### CWE-43: Path Equivalence ('filename....' trailing dots)
**Description**: Multiple trailing dots.

### CWE-44: Path Equivalence ('filename' 'file name' Truncation)
**Description**: File name truncation.

### CWE-45: Path Equivalence ('file name' Multiple Internal Space)
**Description**: Multiple spaces equivalence.

### CWE-46: Path Equivalence ('filename*')
**Description**: Wildcard characters in path.

### CWE-47: Path Equivalence (' filename' leading space)
**Description**: Leading space bypass.

### CWE-48: Path Equivalence ('file name' trailing space)
**Description**: Trailing space bypass.

### CWE-49: Path Equivalence ('filename/' trailing slash)
**Description**: Trailing slash equivalence.

### CWE-50: Path Equivalence ('//multiple/leading/slash')
**Description**: Multiple leading slashes.

### CWE-51: Path Equivalence ('/./' single dot)
**Description**: Single dot directory component.

### CWE-52: Path Equivalence ('/multiple//internal/slash')
**Description**: Multiple internal slashes.

### CWE-53: Path Equivalence ('\\multiple\\internal\\backslash')
**Description**: Multiple internal backslashes.

### CWE-54: Path Equivalence ('filedir\\file')
**Description**: Mixed slash/backslash paths.

### CWE-55: Path Equivalence ('-filedir\\file')
**Description**: Leading dash in path.

### CWE-56: Path Equivalence ('filedir/*')
**Description**: Wildcard in path.

### CWE-57: Path Equivalence ('= ' at beginning of path)
**Description**: Equals sign prefix.

### CWE-58: Path Equivalence ('/proc/self/environ' — direct)
**Description**: Access to `/proc/self/environ`.

### CWE-59: Link Following (Symlink)
**Description**: Following symbolic links without validation.

### CWE-60: Path Traversal Using Alternate Encoding
**Description**: Unicode/hex/octal encoding of path characters.

### CWE-61: UNIX Symbolic Link Following
**Description**: Symlink following on Unix.

### CWE-62: UNIX Hard Link Following
**Description**: Hard link following on Unix.

### CWE-63: Windows Symlink Following
**Description**: Reparse point following.

### CWE-64: Windows Shortcut Following (.lnk)
**Description**: LNK file following.

### CWE-65: Windows Hard Link Following
**Description**: Hard link following on Windows.

### CWE-66: Improper Handling of File Names with Trailing Space
**Description**: File operations with trailing spaces.

### CWE-67: Improper Handling of Windows Device Names
**Description**: Using `CON`, `NUL`, `AUX`, `LPT1` as file names.

### CWE-68: Windows Virtual Drive Handling
**Description**: `\\127.0.0.1\C$` type paths.

### CWE-69: Improper Handling of Windows ::DATA Alternate Data Stream
**Description**: ADS access: `file.txt::$DATA`.

### CWE-70: Improper Handling of Windows ::DATA Alternate Data Stream (..)
**Description**: ADS with path traversal.

### CWE-71: Apple HFS+ File Name Encoding
**Description**: Unicode equivalence in HFS+.

### CWE-72: Improper Handling of Apple HFS+ Alternate Data Stream
**Description**: Resource fork access.

### CWE-73: External Control of File Name or Path
**Description**: User controls file name/path.

### CWE-74: Injection
**Description**: Parent class for all injection vulnerabilities.
**Detection**: Dynamic construction of interpreted language strings with user input.

### CWE-75: Failure to Sanitize Special Elements into a Different Plane (Special Element Injection)
**Description**: Third-party special element injection.

### CWE-76: Improper Neutralization of Equivalent Special Elements
**Description**: Different but equivalent special elements.

### CWE-77: Improper Neutralization of Special Elements used in a Command
**Description**: Command injection in shell.
**CVSS Base**: 9.8 (Critical)
```python
# BAD
os.system(f"ls {user_input}")

# FIXED
subprocess.run(["ls", user_input])  # Array form avoids shell
```

### CWE-78: OS Command Injection
**Description**: User input in OS command.
**CVSS Base**: 9.8 (Critical)
**Detection regex**:
```regex
(os\.system|subprocess\.(call|Popen|run)|exec|popen)\(.*[uU]ser|input|param|arg
```

### CWE-79: Cross-Site Scripting
**Description**: Injection of client-side scripts.
**CVSS Base**: 6.1 (Medium)
**Types**: Reflected, Stored, DOM-based
**Detection patterns by framework**:

**React**:
```javascript
dangerouslySetInnerHTML={{__html: userContent}}  // HIGH
```

**Vue**:
```javascript
v-html="userContent"  // HIGH
```

**Angular**:
```typescript
[innerHTML]="userContent"  // HIGH
bypassSecurityTrustHtml(input)  // CRITICAL
```

**Django**:
```python
{{ user_input|safe }}  // HIGH
mark_safe(user_input)  // HIGH
```

**Flask/Jinja2**:
```python
render_template_string(user_input)  // CRITICAL (SSTI + XSS)
{{ user_input|safe }}  // HIGH
```

**Express**:
```javascript
res.send(user_input)  // HIGH
res.render(user_input)  // CRITICAL (SSTI)
```

### CWE-80: XSS (Basic)
**Description**: Basic XSS in HTML body context.

### CWE-81: XSS (Using Script)
**Description**: Script tag injection.

### CWE-82: XSS (Using IMG Tag)
**Description**: `<img src=x onerror=alert(1)>`.

### CWE-83: XSS (Using Attribute)
**Description**: Attribute injection `<div class="PAYLOAD">`.

### CWE-84: XSS (Using Alternate Encoding)
**Description**: Unicode/numeric entity encoding bypass.

### CWE-85: XSS (Using Thesaurus)
**Description**: Synonym-based JavaScript event handler bypass.

### CWE-86: XSS (Using MIME Type Mismatch)
**Description**: `.html` vs `text/html` vs `application/xhtml+xml` tricks.

### CWE-87: XSS (Using Alternate Syntax of Script)
**Description**: Using `<script>` variant syntax.

### CWE-88: Argument Injection or Modification
**Description**: Injection into command arguments.
```bash
curl --user-agent "Mozilla/5.0" $url  # If url contains --user-agent, it overrides
```

### CWE-89: SQL Injection
**Description**: User input in SQL queries.
**CVSS Base**: 9.8 (Critical)

**Detection by language**:

**Python (Django)**:
```python
User.objects.raw(f"SELECT * FROM users WHERE id = {user_input}")  // BAD
User.objects.filter(id=user_input)                                // FIXED (ORM)
```

**Python (SQLAlchemy)**:
```python
session.execute(text(f"SELECT * FROM users WHERE id = {user_input}"))  // BAD
session.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_input})  // FIXED
```

**Node (Sequelize)**:
```javascript
sequelize.query(`SELECT * FROM users WHERE id = ${userInput}`)  // BAD
sequelize.query("SELECT * FROM users WHERE id = ?", {replacements: [userInput]})  // FIXED
```

**Java (JDBC)**:
```java
Statement stmt = conn.createStatement();
stmt.executeQuery("SELECT * FROM users WHERE id = " + userInput);  // BAD

PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
pstmt.setString(1, userInput);  // FIXED
```

**C# (ADO.NET)**:
```csharp
SqlCommand cmd = new SqlCommand($"SELECT * FROM users WHERE id = {userInput}", conn);  // BAD
SqlCommand cmd = new SqlCommand("SELECT * FROM users WHERE id = @id", conn);
cmd.Parameters.AddWithValue("@id", userInput);  // FIXED
```

**Go**:
```go
db.Query(fmt.Sprintf("SELECT * FROM users WHERE id = %s", userInput))  // BAD
db.Query("SELECT * FROM users WHERE id = $1", userInput)  // FIXED
```

**Ruby (ActiveRecord)**:
```ruby
User.where("id = '#{user_input}'")  // BAD
User.where("id = ?", user_input)    // FIXED
User.find_by(id: user_input)        // FIXED (ORM hash)
```

**PHP (PDO)**:
```php
$stmt = $pdo->query("SELECT * FROM users WHERE id = " . $userInput);  // BAD
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = :id");
$stmt->execute(['id' => $userInput]);  // FIXED
```

### CWE-90: LDAP Injection
**Description**: User input in LDAP queries.
```java
String filter = "(uid=" + userInput + ")";  // BAD
DirContext ctx = new InitialDirContext(env);
NamingEnumeration<?> results = ctx.search("dc=example,dc=com", filter, null);
```

### CWE-91: XML Injection (XPath Injection)
**Description**: Injection into XPath queries.
```python
# BAD
query = f"//user[name='{username}' and pass='{password}']"
# FIXED
from lxml import etree
expr = etree.XPath(f"//user[name=$name and pass=$pass]")
result = expr(root, name=username, pass=password)
```

### CWE-92: DEPRECATED (XSS via Content-Type)

### CWE-93: Improper Neutralization of CRLF Sequences (HTTP Response Splitting)
**Description**: Injecting CRLF into HTTP response headers.
```python
# BAD
response.headers["Location"] = user_input
# If user_input = "\r\n\r\n<html>evil</html>" — response splitting
```

### CWE-94: Code Injection
**Description**: Injection of executable code.
**CVSS Base**: 9.8 (Critical)

```python
# BAD
eval(user_input)
exec(user_input)

# BAD (PHP)
eval($userInput);
assert($userInput);

# BAD (JS)
eval(userInput);
new Function(userInput);
```

### CWE-95: Eval Injection
**Description**: eval() with user input.

### CWE-96: Static Code Injection
**Description**: Injection into static files.

### CWE-97: Server-Side Include (SSI) Injection
**Description**: Injecting `<!--#exec cmd="..." -->`.

### CWE-98: PHP Remote File Inclusion
**Description**: `include($userInput)`, `require($userInput)`.
```php
include($_GET['page'] . '.php');  // If page=../../../etc/passwd%00
```

### CWE-99: Control of Resource Identifiers
**Description**: User-controlled resource identifier.

### CWE-100: DEPRECATED

### CWE-102: Struts: Duplicate Validation Forms
### CWE-103: Struts: Incomplete validate() Method
### CWE-104: Struts: Action Form not populated with enough validation
### CWE-105: Struts: Form does not include reset() method
### CWE-106: Struts: Plug-in Framework not in use
### CWE-107: Struts: Action form without validate
### CWE-108: Struts: Unvalidated Action Form
### CWE-109: Struts: Validator turned off
### CWE-110: Struts: Validator without form field
### CWE-111: Direct Use of Unsafe JNI
**Description**: Unsafe native method invocation from Java.

### CWE-112: Missing XML Validation
**Description**: XML input not validated against schema.

### CWE-113: Improper Neutralization of CRLF Sequences in HTTP Headers
**Description**: Header injection via CRLF.

### CWE-114: Process Control
**Description**: User-controlled process execution.

### CWE-115: Misinterpretation of Input
**Description**: Input misinterpreted by different parsers.

### CWE-116: Improper Encoding or Escaping of Output
**Description**: XSS via improper output encoding.

### CWE-117: Improper Output Neutralization for Logs
**Description**: Log injection (log forging).

### CWE-118: DEPRECATED (Resource Injection)

### CWE-120: See Memory Safety above.
### CWE-121: See Memory Safety above.
### CWE-122: See Memory Safety above.

### CWE-123: Write-WHAT-Where

### CWE-124: Buffer Underwrite

### CWE-125: Out-of-Bounds Read

### CWE-126: Buffer Over-read

### CWE-127: Buffer Under-read

### CWE-128: Wrap-around Error
**Description**: Wraparound in buffer size calculation.

### CWE-129: Improper Validation of Array Index

### CWE-130: Improper Handling of Length Parameter

### CWE-131: Incorrect Calculation of Buffer Size

### CWE-132: DEPRECATED
### CWE-133: DEPRECATED
### CWE-134: Use of Externally-Controlled Format String

### CWE-135: Incorrect Calculation of Multi-Byte String Length

### CWE-138: Improper Sanitization of Special Elements
**Description**: Parent of CWE-139 through CWE-150 — special element injection.

### CWE-140: Improper Neutralization of Delimiters
### CWE-141: Improper Neutralization of Parameter Delimiters
### CWE-142: Improper Neutralization of Value Delimiters
### CWE-143: Improper Neutralization of Record Delimiters
### CWE-144: Improper Neutralization of Line Delimiters
### CWE-145: Improper Neutralization of Section Delimiters
### CWE-146: Improper Neutralization of Expression/Command Delimiters
### CWE-147: Improper Neutralization of Input Terminators
### CWE-148: Improper Neutralization of Input Leaders
### CWE-149: Improper Neutralization of Quoting Syntax
### CWE-150: Improper Neutralization of Escape, Meta, or Control Sequences

### CWE-157: Failure to Neutralize Multiple Encoding
**Description**: Double decoding bypass.

### CWE-158: Null Byte Injection
```php
include($_GET['file'] . ".php");  // file=../../../etc/passwd%00 → bypasses .php append
```

### CWE-159: Improper Neutralization of Multiple Special Elements
### CWE-160: Improper Neutralization of Whitespace
### CWE-161: Improper Neutralization of Multiple Trailing Special Elements
### CWE-162: Improper Neutralization of Trailing Special Elements
### CWE-163: Improper Neutralization of Multiple Leading Special Elements
### CWE-164: Improper Neutralization of Leading Special Elements
### CWE-165: Improper Neutralization of Multiple Internal Special Elements
### CWE-166: Improper Neutralization of Special Elements with Specific Name

### CWE-167: Improper Handling of Additional Special Element
### CWE-168: Improper Handling of Inconsistent Special Elements
### CWE-169: DEPRECATED

### CWE-170: Improper Null Termination
**Description**: Missing null terminator.
```c
strncpy(dst, src, sizeof(dst));  // Not null-terminated if src >= sizeof(dst)
```

### CWE-172: Encoding Error
### CWE-173: Bad Handling of US-ASCII Escape Character
### CWE-174: Double Decoding of the Same Data
### CWE-175: Improper Handling of Mixed Encoding
### CWE-176: Improper Handling of Unicode Encoding
### CWE-177: Improper Handling of URL Encoding (Hex Encoding)
### CWE-178: Improper Handling of Case Sensitivity
### CWE-179: Incorrect Behavior Order: Validate Before Canonicalize
### CWE-180: Incorrect Behavior Order: Canonicalize Before Validate

### CWE-181: Incorrect Behavior Order: Validate Before Filter
### CWE-182: Collapse of Data into Unsafe Value
### CWE-183: Allowlist vs Denylist
**Description**: Denylist approach misses new/malformed attacks.
```python
# BAD: Denylist
bad_chars = ["<", ">", "'", "\""]
if any(c in input for c in bad_chars):
    reject()

# FIXED: Allowlist
import re
if not re.match(r"^[a-zA-Z0-9_\-]+$", input):
    reject()
```

### CWE-184: Incomplete Denylist
### CWE-185: Incorrect Regular Expression
### CWE-186: Overly Restrictive Regular Expression
### CWE-187: Partial String Comparison
### CWE-188: Reliance on Data/Memory Layout

### CWE-190: Integer Overflow or Wraparound
**Description**: Arithmetic result exceeds data type capacity.
**CVSS Base**: 7.5 (High)
```c
uint16_t a = 65535;
uint16_t b = 1;
uint16_t c = a + b;  // Wraps to 0
```

### CWE-191: Integer Underflow (Wrap or Wraparound)
```c
uint16_t a = 0;
uint16_t b = 1;
uint16_t c = a - b;  // Wraps to 65535
```

### CWE-192: Integer Coercion Error
### CWE-193: Off-by-one Error
```c
char buf[10];
for (int i = 0; i <= 10; i++) buf[i] = 0;  // buf[10] is OOB
```

### CWE-194: Unexpected Sign Extension
### CWE-195: Signed to Unsigned Conversion Error
### CWE-196: Unsigned to Signed Conversion Error
### CWE-197: Numeric Truncation Error

### CWE-198: Use of Incorrect Byte Ordering (Endianness)
### CWE-199: Information Management (Parent)

---

## PILLAR 3: Authentication (CWE-287 Series)

### CWE-287: Improper Authentication
**Description**: When an actor claims to have a given identity, the software does not prove or insufficiently proves that the identity is correct.
**CVSS Base**: 9.1 (Critical)
**Detection**:
- Missing authentication on sensitive endpoints
- Weak password policy
- No MFA for sensitive operations
- Session fixation
- Weak password recovery

### CWE-288: Authentication Bypass Using Alternate Path or Channel
```http
GET /admin HTTP/1.1
Host: example.com
```
vs
```http
GET /ADMIN HTTP/1.1
Host: example.com
```
Case-sensitivity bypasses.

### CWE-289: Authentication Bypass by Alternate Name
### CWE-290: Authentication Bypass by Spoofing
**Description**: IP spoofing, X-Forwarded-For trust.

### CWE-291: Reliance on IP Address for Authentication
**Description**: Trusting source IP for authentication.

### CWE-292: DEPRECATED

### CWE-293: Using Referer Header for Authentication
**Description**: Trusting `Referer` header as auth proof.

### CWE-294: Authentication Bypass by Capture-Replay
**Description**: Replay attack on authentication.

### CWE-295: Improper Certificate Validation
**Description**: TLS certificate validation disabled.
**CVSS Base**: 7.5 (High)
**Detection**: `verify=False`, `verify: false`, `InsecureSkipVerify: true`, `ssl._create_unverified_context()`
```python
# BAD
requests.get(url, verify=False)

# FIXED
requests.get(url, verify="/path/to/ca-bundle.crt")

# BAD (Go)
httpClient := &http.Client{
    Transport: &http.Transport{
        TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
    },
}
```

### CWE-296: Improper Following of Certificate Chain of Trust
### CWE-297: Improper Validation of Host-specific Certificate Data
### CWE-298: Improper Validation of Certificate Expiration
### CWE-299: Improper Check for Certificate Revocation
### CWE-300: Channel Accessible by Non-Endpoint (Man-in-the-Middle)
### CWE-301: Reflection Attack in Authentication Protocol
### CWE-302: Authentication Bypass by Assumed-Immutable Data
**Description**: Trusting hidden fields, cookies, or headers.

### CWE-303: Incorrect Implementation of Authentication Algorithm
### CWE-304: Missing Critical Step in Authentication
### CWE-305: Authentication Bypass by Primary Weakness
### CWE-306: Missing Authentication for Critical Function
**Description**: No auth required for sensitive function.
```python
@app.route("/api/admin/delete_user")
def delete_user():  # No @login_required
    ...
```

### CWE-307: Improper Restriction of Excessive Authentication Attempts
**Description**: No rate limiting on login.
**Detection**: Login endpoint without attempt tracking.
```python
# BAD
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = authenticate(username, password)
    # No attempt counting!

# FIXED
from flask_limiter import Limiter
limiter = Limiter(key_func=lambda: request.remote_addr)
@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    ...
```

### CWE-308: Use of Single-factor Authentication
**Description**: No MFA for sensitive operations.

### CWE-309: Use of Password System for Primary Authentication
### CWE-310: Cryptographic Issues (Parent)
### CWE-311: Missing Encryption of Sensitive Data
### CWE-312: Cleartext Storage of Sensitive Data
```python
# BAD
with open("passwords.txt", "w") as f:
    f.write(password)

# FIXED
from hashlib import pbkdf2_hmac
import secrets
salt = secrets.token_hex(16)
hash = pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
store(hash, salt)
```

### CWE-313: Cleartext Storage in a File or on Disk
### CWE-314: Cleartext Storage in the Registry
### CWE-315: Cleartext Storage of Sensitive Information in a Cookie
### CWE-316: Cleartext Storage of Sensitive Information in Memory
### CWE-317: Cleartext Storage of Sensitive Information in GUI
### CWE-318: Cleartext Storage of Sensitive Information in Executable
### CWE-319: Cleartext Transmission of Sensitive Information
**Description**: Sensitive data sent over unencrypted channel (HTTP, not HTTPS).

### CWE-320: Key Management Errors (Parent)
### CWE-321: Use of Hard-coded Cryptographic Key
```python
# BAD
key = "this-is-a-fixed-key-1234"

# FIXED
key = os.environ.get("ENCRYPTION_KEY")
```

### CWE-322: Key Exchange Without Entity Authentication
### CWE-323: Reusing a Nonce, Key Pair in Encryption
### CWE-324: Use of a Key Past its Expiration Date
### CWE-325: Missing Cryptographic Step
### CWE-326: Inadequate Encryption Strength
**Description**: Weak key size (RSA < 2048, AES-56/64, DES).
```python
# BAD
from Crypto.PublicKey import RSA
key = RSA.generate(1024)  // < 2048

# FIXED
key = RSA.generate(4096)
```

### CWE-327: Use of a Broken or Risky Cryptographic Algorithm
**Description**: MD5, SHA-1, DES, RC4, ECB mode.
```python
# BAD
import hashlib
hashlib.md5(data).hexdigest()

# FIXED
hashlib.sha256(data).hexdigest()
```

### CWE-328: Use of Weak Hash
**Description**: Non-cryptographic hashes for security (CRC32, non-crypto PRNG).
```python
# BAD
import random
token = random.randint(0, 1000000)

# FIXED
import secrets
token = secrets.token_hex(32)
```

### CWE-329: Not Using a Random IV with CBC Mode
### CWE-330: Use of Insufficiently Random Values
```python
# BAD
import random
key = random.getrandbits(128)

# FIXED
import secrets
key = secrets.token_bytes(16)
```

### CWE-331: Insufficient Entropy
### CWE-332: Insufficient Entropy in PRNG
### CWE-333: Failure to Handle Insufficient Entropy in TRNG
### CWE-334: Small Space of Random Values
### CWE-335: Incorrect Usage of Seeds in Pseudo-Random Number Generator
### CWE-336: Same Seed in Pseudo-Random Number Generator
### CWE-337: Predictable Seed in Pseudo-Random Number Generator
### CWE-338: Use of Cryptographically Weak Pseudo-Random Number Generator
### CWE-339: Small Seed Space in PRNG
### CWE-340: Predictability Problems (Parent)
### CWE-341: Predictable from Observable State
### CWE-342: Predictable Exact Value from Previous Values
### CWE-343: Predictable Value Range
### CWE-344: Use of Invariant Value in Dynamically Changing Context
### CWE-345: Insufficient Verification of Data Authenticity
### CWE-346: Origin Validation Error
### CWE-347: Improper Verification of Cryptographic Signature
### CWE-348: Use of Less Trusted Source
### CWE-349: Acceptance of Extraneous Untrusted Data With Trusted Data
### CWE-350: Reliance on Reverse DNS Resolution for Security
### CWE-351: Insufficient W3C DTD Validation
### CWE-352: Cross-Site Request Forgery (CSRF)
**Description**: Attacker induces victim to perform unintended state-changing request.
**CVSS Base**: 6.5 (Medium)
**Detection**: State-changing endpoint without CSRF token or SameSite cookie.
```python
# BAD
@app.route("/transfer", methods=["POST"])
def transfer():
    amount = request.form["amount"]
    transfer_money(amount)

# FIXED
@app.route("/transfer", methods=["POST"])
@csrf.protect
def transfer():
    amount = request.form["amount"]
    transfer_money(amount)
```

### CWE-353: Missing Support for Integrity Check
### CWE-354: Improper Validation of Integrity Check Value
### CWE-355: User Authentication Permissions (Parent)
### CWE-356: Product UI does not warn user of unsafe actions
### CWE-357: Insufficient UI Warning of Dangerous Operations

---

## PILLAR 4: Authorization (CWE-285 Series)

### CWE-285: Improper Authorization
**Description**: Access control check is missing or incorrect.
**Detection**: Endpoints without role/permission checks.

### CWE-286: Incorrect User Management
### CWE-352: CSRF (See above — CSRF is both auth and authz issue)

### CWE-359: Exposure of Private Information (Privacy)
### CWE-360: Trust of System Event Data
### CWE-361: 7PK (Seven Pernicious Kingdoms) Parent

### CWE-362: Race Condition (Concurrent Execution)
**Description**: Time-of-check-time-of-use (TOCTOU) or concurrent execution flaw.
**CVSS Base**: 7.0 (High)
```python
# BAD — TOCTOU
if os.path.exists(filename):
    with open(filename) as f:  // File may have been replaced
        data = f.read()

# BAD — Non-atomic check-then-act
if balance >= amount:
    balance -= amount  // Another thread may have deducted

# FIXED
import threading
lock = threading.Lock()
with lock:
    if balance >= amount:
        balance -= amount
```

### CWE-363: Race Condition (Signal Handler)
### CWE-364: Signal Handler Race Condition
### CWE-365: Race Condition in Switch
### CWE-366: Race Condition within a Thread
### CWE-367: TOCTOU Race Condition
```c
// BAD — TOCTOU (file system)
if (access("file", W_OK) == 0) {
    fd = open("file", O_WRONLY);  // File could have been replaced with symlink
}
```

### CWE-368: Context Switching Race Condition
### CWE-369: Divide By Zero
### CWE-370: Missing Check for Certificate Revocation after Initial Check
### CWE-371: State Issues (Parent)
### CWE-372: Incomplete Internal State Distinction
### CWE-373: DEPRECATED
### CWE-374: Passing Mutable Objects to an Untrusted Method
### CWE-375: Returning a Mutable Object to an Untrusted Caller
### CWE-376: DEPRECATED
### CWE-377: Insecure Temporary File
```python
import tempfile
# BAD
tmp = "/tmp/myapp/tmp.txt"
with open(tmp, "w") as f:  // Predictable, race-able
    f.write(data)

# FIXED
with tempfile.NamedTemporaryFile(delete=False) as f:
    f.write(data)
```

### CWE-378: Creation of Temporary File with Insecure Permissions
### CWE-379: Creation of Temporary File in Directory with Insecure Permissions

### CWE-380: DEPRECATED

### CWE-381: DEPRECATED

### CWE-382: J2EE Bad Practices: Use of System.exit()
### CWE-383: J2EE Bad Practices: Direct Use of Threads
### CWE-384: Session Fixation
**Description**: Attacker forces a known session ID on victim.
```python
# BAD
# No session regeneration after login

# FIXED
session.regenerate()  # Generate new session ID on login
```

### CWE-385: Covert Timing Channel
### CWE-386: Symbolic Name not Mapping to Correct Object
### CWE-387: Signal Handling (Parent)
### CWE-388: Error Handling (Parent)
### CWE-389: Error Conditions, Return Values, Status Codes (Parent)
### CWE-390: Detection of Error Condition Without Action
### CWE-391: Unchecked Error Condition
### CWE-392: Missing Report of Error Condition
### CWE-393: Return of Wrong Status Code
### CWE-394: Unexpected Status Code or Return Value
### CWE-395: Use of NullPointerException in Catch Block
### CWE-396: Declaration of Catch for Generic Exception
### CWE-397: Declaration of Throws for Generic Exception
### CWE-398: Code Quality (Parent)
### CWE-399: Resource Management (Parent)

---

## PILLAR 5: Resource Management (CWE-400 Series)

### CWE-400: Uncontrolled Resource Consumption
**Description**: Application does not properly control allocation/maintenance of resources.
**CVSS Base**: 7.5 (High)
**Detection**:
- No rate limiting
- Unbounded loops
- Large allocations from user input
- No resource pooling

```python
# BAD — Unbounded resource consumption
@app.route("/download")
def download():
    data = request.files["file"].read()  // No size limit
    return Response(data)

# FIXED
@app.route("/download")
def download():
    data = request.files["file"].read(1024 * 1024)  // Limit to 1MB
    return Response(data)
```

### CWE-401: Missing Release of Memory After Effective Lifetime
**Description**: Memory leak.
```c
char *buf = malloc(1024);
// Never free(buf)
```

### CWE-402: Transfer of Resources between Realms (Parent)
### CWE-403: Exposure of File Descriptor to Unintended Control Sphere
### CWE-404: Improper Resource Shutdown or Release
### CWE-405: Asymmetric Resource Consumption (Amplification)
**Description**: Low effort request causes high effort server response.
```http
GET /api/search?q=a HTTP/1.1
# Server does intensive search — amplification attack
```

### CWE-406: Insufficient Control of Network Message Volume
### CWE-407: Algorithmic Complexity
**Description**: Algorithmic complexity attack (ReDoS, hash collision).
```python
# BAD — ReDoS
import re
pattern = re.compile(r"^(a+)+$")
pattern.match("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa!")  // Catastrophic backtracking

# FIXED
pattern = re.compile(r"^a+$")
```

### CWE-408: Incorrect Behavior Order: Early Amplification
### CWE-409: Improper Handling of Highly Compressed Data
**Description**: Zip bomb / decompression bomb.

### CWE-410: Insufficient Resource Pool
### CWE-412: Unrestricted Externally Accessible Lock
### CWE-413: Improper Resource Locking
### CWE-414: Missing Lock Check
### CWE-415: Double Free
### CWE-416: Use After Free

### CWE-420: Unprotected Alternate Channel
### CWE-421: Race Condition During Access to Alternate Channel
### CWE-422: Unprotected Windows Messaging Channel
### CWE-423: DEPRECATED
### CWE-424: Improper Protection of Alternate Path
### CWE-425: Direct Request (Forced Browsing)
**Description**: Direct access to resource without proper navigation.

### CWE-426: Untrusted Search Path
**Description**: Loading libraries from user-controlled path.

### CWE-427: Uncontrolled Search Path Element
```c
// BAD: Load from current directory
LoadLibrary("evil.dll");  // Could load from attacker's location
```

### CWE-428: Unquoted Search Path
```cmd
C:\Program Files\MyApp\app.exe  // If unquoted, space causes search for "C:\Program"
```

### CWE-430: Deployment of Wrong Handler
### CWE-431: Missing Handler
### CWE-432: Dangerous Signal Handler not Disabled During Sensitive Operations
### CWE-433: Unparsed Raw Data Written to Output
### CWE-434: Unrestricted Upload of File with Dangerous Type
**Description**: File upload without content-type validation.
**CVSS Base**: 8.8 (High)
```python
# BAD
file = request.files["file"]
filename = file.filename
file.save(f"uploads/{filename}")  // Any file type accepted

# FIXED
ALLOWED_EXTENSIONS = {"png", "jpg", "gif"}
ext = filename.rsplit(".", 1)[1].lower()
if ext in ALLOWED_EXTENSIONS:
    file.save(f"uploads/{filename}")
```

### CWE-435: Improper Interaction with Multiple Versions of Same Resource
### CWE-436: Interpretation Conflict (Parent)
### CWE-437: Incomplete Model of Endpoint Features
### CWE-438: Behavioral Change in New Version or Environment
### CWE-439: Behavioral Change in New Version
### CWE-440: Expected Behavior Violation
### CWE-441: Unintended Proxy or Intermediary
### CWE-442: Web Vulnerabilities (Parent)
### CWE-443: DEPRECATED
### CWE-444: Inconsistent Interpretation of HTTP Requests
**Description**: HTTP request smuggling.
```http
POST / HTTP/1.1
Host: example.com
Content-Length: 13
Transfer-Encoding: chunked

0

GET /admin HTTP/1.1
```

### CWE-445: User Interface Errors (Parent)
### CWE-446: UI Discrepancy for Security Feature
### CWE-447: Implementation of Unimplemented Feature
### CWE-448: Obsolete Feature
### CWE-449: The UI Performs Wrong Action
### CWE-450: Multiple Interpretations of UI Input
### CWE-451: User Interface Misrepresentation of Critical Information
### CWE-452: Initialization and Cleanup Errors (Parent)
### CWE-453: Incomplete Default Configuration
### CWE-454: External Initialization of Trusted Variables
### CWE-455: Non-Unique Designation for Complete Entity
### CWE-456: Missing Initialization of a Variable
### CWE-457: Use of Uninitialized Variable
### CWE-458: Reliance on Global Variables in Re-entrant Code
### CWE-459: Incomplete Cleanup
### CWE-460: Improper Cleanup on Thrown Exception
### CWE-461: Missing Data Deletion
### CWE-462: Duplicate Key in Associative List
### CWE-463: Deletion of Data Structure Sentinel
### CWE-464: Addition of Data Structure Sentinel
### CWE-465: Pointer Issues (Parent)
### CWE-466: Return of Pointer Value Outside of Expected Range
### CWE-467: Use of sizeof() on a Pointer Type
### CWE-468: Incorrect Pointer Scaling
### CWE-469: Use of Pointer Subtraction to Determine Size

---

## PILLAR 6: Code Quality (CWE-398 Series)

### CWE-398: Code Quality
**Description**: Parent for code quality issues that don't fit other categories.

### CWE-399: Resource Management (See Resource Management)
### CWE-400: Resource Consumption (See Resource Management)

### CWE-401 through CWE-469: See Resource Management

### CWE-470: Use of External-Defined Resource (Third-party risk)
### CWE-471: Modification of Assumed-Immutable Data
### CWE-472: External Control of Assumed-Immutable Web Parameter
### CWE-473: PHP External Variable Modification
### CWE-474: Insufficient Data Validation on Input
### CWE-475: Undefined Behavior for Input to API
### CWE-476: NULL Pointer Dereference (See Memory Safety)
### CWE-477: Use of Obsolete Functions
```c
// BAD: Use obsolete function
gets(buffer);
// FIXED
fgets(buffer, sizeof(buffer), stdin);
```

### CWE-478: Missing Default Case in Switch
### CWE-479: Signal Handler Use of Non-Reentrant Function
### CWE-480: Use of Incorrect Operator
### CWE-481: Assigning Instead of Comparing
### CWE-482: Comparing Instead of Assigning
### CWE-483: Incorrect Block Delimitation
### CWE-484: Omitted Break Statement in Switch
### CWE-485: Insufficient Encapsulation
### CWE-486: Comparison of Classes by Name
### CWE-487: Reliance on Package-level Scope
### CWE-488: Exposure of Data Element to Wrong Session
### CWE-489: Active Debug Code in Production
```python
# BAD
DEBUG = True

# Or
if __name__ == "__main__":
    app.run(debug=True)  # In production!
```

### CWE-490: Mobile Device Issues (Parent)
### CWE-491: Public cloneable() Method Without Final
### CWE-492: Use of Inner Class Containing Sensitive Data
### CWE-493: Critical Public Variable Without Immutable Wrapper
### CWE-494: Download of Code Without Integrity Check
**Description**: Loading scripts from CDN without SRI.
```html
<!-- BAD -->
<script src="https://cdn.example.com/lib.js"></script>

<!-- FIXED -->
<script src="https://cdn.example.com/lib.js"
        integrity="sha384-abc123..."
        crossorigin="anonymous"></script>
```

### CWE-495: Private Data Structure Exposed Through Public Method
### CWE-496: Public Data Assignable to Private Array-Typed Field
### CWE-497: Exposure of Sensitive System Information
### CWE-498: Cloneable Class Containing Sensitive Information
### CWE-499: Serializable Class Containing Sensitive Information

### CWE-500: Public Static Field Not Marked Final
### CWE-501: Trust Boundary Violation
### CWE-502: Deserialization of Untrusted Data
**Description**: Deserializing untrusted data.
**CVSS Base**: 9.8 (Critical)

**Per language dangerous functions**:
| Language | Dangerous | Safe Alternatives |
|---|---|---|
| Python | `pickle.loads()` | `json.loads()` |
| Java | `ObjectInputStream.readObject()` | JSON/XML with validation |
| .NET | `BinaryFormatter.Deserialize()` | `DataContractSerializer` |
| PHP | `unserialize()` | `json_decode()` |
| Ruby | `Marshal.load()` | `JSON.parse()` |
| Node | `node-serialize` | `JSON.parse()` |

```python
# BAD
import pickle
data = pickle.loads(user_input)  // RCE possible

# FIXED
import json
data = json.loads(user_input)
```

### CWE-503: Web Application Vulnerabilities (Parent)
### CWE-504: Regular Expression Denial of Service (ReDoS)
**Detection**: Look for patterns with nested quantifiers like `(a+)+`, `(a|aa)+`, `(.*)*`.
```python
# BAD — Catastrophic backtracking
pattern = r"^([a-z]+)+$"
# For input "aaaaaaaaaaaaaaaaaaaaaaaaaaaaa!" — exponential time

# FIXED
pattern = r"^[a-z]+$"
```

### CWE-505: Intentionally Invisible/Indistinguishable Backdoor
### CWE-506: Embedded Malicious Code
### CWE-507: Trojan Horse
### CWE-508: Non-Replicating Malicious Code
### CWE-509: Replicating Malicious Code (Virus/Worm)
### CWE-510: Trapdoor
### CWE-511: Logic/Time Bomb
### CWE-512: Spyware
### CWE-513: Intentionally Introduced Weakness (Parent)
### CWE-514: Covert Channel
### CWE-515: Covert Storage Channel
### CWE-516: Covert Timing Channel
### CWE-517: Covert Encoding Channel
### CWE-518: DEPRECATED
### CWE-519: DEPRECATED
### CWE-520: DEPRECATED
### CWE-521: Weak Password Requirements
```python
# BAD
if len(password) >= 4:  // Too short!

# FIXED
if (len(password) >= 12 and
    any(c.isupper() for c in password) and
    any(c.islower() for c in password) and
    any(c.isdigit() for c in password) and
    any(not c.isalnum() for c in password)):
```

### CWE-522: Insufficiently Protected Credentials
### CWE-523: Unprotected Transport of Credentials
### CWE-524: Use of Cache Containing Sensitive Information
### CWE-525: Use of Web Browser Cache Containing Sensitive Info
### CWE-526: Information Exposure Through Environmental Variables
### CWE-527: Exposure of Version-Control Repository
### CWE-528: Exposure of Core Dump to Unauthorized Sphere
### CWE-529: Exposure of Access Control List Files
### CWE-530: Exposure of Backup File to Unauthorized Sphere
### CWE-531: Inclusion of Sensitive Information in Test Code
### CWE-532: Insertion of Sensitive Information Into Log File
```python
import logging
# BAD
logging.error(f"Login failed for user {username} with password {password}")

# FIXED
logging.error(f"Login failed for user {username}")
```

### CWE-533: Information Exposure Through Server Log Files
### CWE-534: Information Exposure Through Debug Log Files
### CWE-535: Information Exposure Through Shell Error Message
### CWE-536: Information Exposure Through Servlet Error Messages
### CWE-537: Information Exposure Through Java Runtime Messages
### CWE-538: File and Directory Information Exposure
### CWE-539: Information Exposure Through Persistent Cookies
### CWE-540: Information Exposure Through Source Code
### CWE-541: Information Exposure Through Include Source Code
### CWE-542: Information Exposure Through Cleanup Log Files
### CWE-543: Use of Singleton Pattern Without Synchronization
### CWE-544: Missing Standardized Process for Continuous Improvement
### CWE-545: Use of Dynamic Class Loading and Instantiation
### CWE-546: Suspicious Comment
```python
// BAD
# TODO: FIX THIS LATER — INSECURE DO NOT DEPLOY
# HACK: bypassing auth for testing
```

### CWE-547: Use of Hard-coded, Security-relevant Constants
### CWE-548: Exposure of Information Through Directory Listing
**Detection**: Web server with directory listing enabled.

### CWE-549: Missing Password Field Masking
### CWE-550: Information Exposure Through Server Error Messages
### CWE-551: Incorrect Behavior Order: Authorization Before Parsing
### CWE-552: Files or Directories Accessible to External Parties
### CWE-553: DEPRECATED
### CWE-554: ASP.NET Misconfiguration (Parent)
### CWE-555: J2EE Misconfiguration (Parent)
### CWE-556: ASP.NET Misconfiguration: Use of Identity Impersonation
### CWE-557: Concurrency Issues (Parent)
### CWE-558: Use of getlogin() in Multithreaded Application
### CWE-559: SQL Injection (see CWE-89)
### CWE-560: Use of umask() with chmod-style Argument
### CWE-561: Dead Code
### CWE-562: Return of Stack Variable Address
### CWE-563: Assignment to Variable Without Use
### CWE-564: SQL Injection (see CWE-89)
### CWE-565: Reliance on Cookies Without Validation and Integrity
### CWE-566: Authorization Bypass Through User-Controlled SQL Primary Key
### CWE-567: Unsynchronized Access to Shared Data
### CWE-568: Finalize() Method Without super.finalize()
### CWE-569: Expression Issues (Parent)
### CWE-570: Expression is Always False
### CWE-571: Expression is Always True
### CWE-572: Call to Thread run() Instead of start()
### CWE-573: Improper Following of Specification by Caller
### CWE-574: EJB Bad Practices (Parent)
### CWE-575: EJB Bad Practices: Use of AWT Swing
### CWE-576: EJB Bad Practices: Use of Java I/O
### CWE-577: EJB Bad Practices: Use of Sockets
### CWE-578: EJB Bad Practices: Use of Class Loader
### CWE-579: J2EE Bad Practices: Non-Serializable Object Stored in Session
### CWE-580: clone() Method Without finalize()
### CWE-581: Object Model Violation
### CWE-582: Array Declared Public, Final, and Static
### CWE-583: finalize() Method Declared Public
### CWE-584: Return Inside Finally Block
### CWE-585: Empty Synchronized Block
### CWE-586: Explicit Call to Finalize()
### CWE-587: Assignment of a Fixed Address to a Pointer
### CWE-588: Attempt to Access Child of a Non-struct Pointer
### CWE-589: Call to Non-ubiquitous API
### CWE-590: Free of Memory Not on the Heap
### CWE-591: Sensitive Data Storage in Improperly Locked Memory
### CWE-592: Authentication Bypass Using OpenID Connect (Parent)
### CWE-593: Authentication Bypass via OpenID Connect
### CWE-594: J2EE Bad Practices: Non-serializable Object Stored in Session
### CWE-595: Comparison of Object References Instead of Object Contents
### CWE-596: DEPRECATED
### CWE-597: Use of Wrong Operator in String Comparison
```java
// BAD
if (str1 == str2)  // Compares references, not content

// FIXED
if (str1.equals(str2))
```

### CWE-598: Information Exposure Through Query Strings
### CWE-599: Missing Validation of OpenSSL Symmetric Key
### CWE-600: Uncaught Exception in Servlet
### CWE-601: Open Redirect
**Description**: User-controlled URL in redirect.
```python
# BAD
@app.route("/redirect")
def redirect():
    url = request.args.get("url")
    return redirect(url)

# FIXED
ALLOWED_DOMAINS = ["example.com"]
@app.route("/redirect")
def redirect():
    url = request.args.get("url")
    parsed = urlparse(url)
    if parsed.netloc not in ALLOWED_DOMAINS:
        return redirect("/")
    return redirect(url)
```

### CWE-602: Client-Side Enforcement of Server-Side Security
**Description**: Security logic in client-side JavaScript that can be bypassed.

### CWE-603: Use of Client-Side Authentication
### CWE-604: Deprecated (Authentication)
### CWE-605: Multiple Binds to the Same Port
### CWE-606: Unchecked Input for Loop Condition
```python
# BAD
for i in range(int(user_input)):  // Can loop forever
    process(data)

# FIXED
MAX_ITERATIONS = 1000
count = min(int(user_input), MAX_ITERATIONS)
for i in range(count):
    process(data)
```

### CWE-607: Public Static Final Field References Mutable Object
### CWE-608: Struts: Non-private Field in ActionForm
### CWE-609: Double-Checked Locking
```java
// BAD
if (instance == null) {
    synchronized (Singleton.class) {
        if (instance == null) {
            instance = new Singleton();  // May see partially constructed object
        }
    }
}

// FIXED
private static volatile Singleton instance;
```

### CWE-610: Externally Controlled Reference to a Resource
### CWE-611: Improper Restriction of XML External Entity Reference
**Description**: XXE — XML parser loads external entities.
**CVSS Base**: 7.5 (High)
```python
# BAD
from lxml import etree
tree = etree.parse(user_input)  // XXE enabled by default

# FIXED
parser = etree.XMLParser(resolve_entities=False, no_network=True)
tree = etree.parse(user_input, parser)

# BAD (Java)
DocumentBuilder db = DocumentBuilderFactory.newInstance().newDocumentBuilder();
Document doc = db.parse(inputStream);

# FIXED (Java)
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
```

### CWE-612: Information Exposure Through Indexing of Sensitive Data
### CWE-613: Insufficient Session Expiration
**Description**: Sessions that don't expire, no absolute timeout.

### CWE-614: Sensitive Cookie in HTTPS Session Without Secure Attribute
```http
Set-Cookie: session=abc123; Path=/   # Missing Secure flag
Set-Cookie: session=abc123; Secure; HttpOnly; SameSite=Lax  # FIXED
```

### CWE-615: Information Exposure Through Comments
### CWE-616: Incomplete Identification of Uploaded File Components
### CWE-617: Reachable Assertion
### CWE-618: Exposed Unsafe ActiveX Control
### CWE-619: Storable and Recoverable State (Parent)
### CWE-620: Unverified Password Change
### CWE-621: Variable Extraction Errors (Parent)
### CWE-622: Improper Validation of Function Hook Arguments
### CWE-623: Unsafe ActiveX Control Marked Safe For Scripting
### CWE-624: Executable Regular Expression Error
### CWE-625: Permissive Regular Expression
### CWE-626: Null Byte Interaction Error
### CWE-627: Dynamic Variable Evaluation
### CWE-628: Function Call with Incorrectly Specified Arguments
### CWE-629: Weak Mapping (Parent)
### CWE-630: Weak Mapping for Overly Broad Authority
### CWE-631: Resource-specific Loop (Parent)
### CWE-632: Weak Password Recovery Mechanism
### CWE-633: Weak Password Recovery Mechanism for Forgotten Password
### CWE-634: Weak Password Recovery Mechanism for OTP
### CWE-635: Weak Password Recovery Mechanism for Token
### CWE-636: Not Failing Securely
### CWE-637: Unnecessary Complexity in Protection Mechanism
### CWE-638: Not Using Complete Mediation
### CWE-639: Authorization Bypass Through User-Controlled Key
**Description**: Insecure Direct Object Reference (IDOR).
```python
# BAD
@app.route("/api/invoice/<invoice_id>")
def get_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)  // No ownership check
    return invoice.to_dict()

# FIXED
@app.route("/api/invoice/<invoice_id>")
@login_required
def get_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if invoice.user_id != current_user.id:
        return {"error": "Forbidden"}, 403
    return invoice.to_dict()
```

### CWE-640: Weak Password Recovery Mechanism
### CWE-641: Information Exposure Through Files
### CWE-642: Information Exposure Through External Cookie
### CWE-643: XPath Injection
### CWE-644: Improper Neutralization of Server-Side Includes
### CWE-645: Insufficient Anti-Automation
### CWE-646: Reliance on File Name for Authorization
### CWE-647: DEPRECATED
### CWE-648: DEPRECATED
### CWE-649: Reliance on Obfuscation or Encryption of Security-Relevant Inputs
### CWE-650: Trusting HTTP Permission Methods
### CWE-651: Information Exposure Through WSDL File
### CWE-652: XQuery Injection
### CWE-653: Insufficient Compartmentalization
### CWE-654: Reliance on a Single Factor in Security Decision
### CWE-655: Insufficient Psychological Acceptability
### CWE-656: Reliance on Security Through Obscurity
### CWE-657: Violation of Secure Design Principles
### CWE-658: Security of System Software (Parent)
### CWE-659: Weaknesses in Software Development Process (Parent)
### CWE-660: Operation on Resource in Wrong Phase
### CWE-661: Insufficient Design (Parent)
### CWE-662: Improper Synchronization
### CWE-663: Use of Non-Atomic Operation on Shared Resource
### CWE-664: Improper Control of a Resource Through its Lifetime
### CWE-665: Improper Initialization
### CWE-666: Operation on Resource in Wrong Phase of Lifetime
### CWE-667: Improper Locking
### CWE-668: Exposure of Resource to Wrong Sphere
### CWE-669: Incorrect Resource Transfer Between Spheres
### CWE-670: Always-Incorrect Control Flow Implementation
### CWE-671: Lack of Administrator Control Over Security
### CWE-672: Operation on a Resource After Expiration or Release
### CWE-673: External Influence of Security Decision
### CWE-674: Uncontrolled Recursion
```python
# BAD — No recursion depth limit
def recurse():
    recurse()

# FIXED
import sys
sys.setrecursionlimit(1000)
def recurse(depth=0):
    if depth > 900:
        return
    recurse(depth + 1)
```

### CWE-675: Duplicate Operations on Resource
### CWE-676: Use of Potentially Dangerous Function
### CWE-677: DEPRECATED
### CWE-678: DEPRECATED
### CWE-679: DEPRECATED
### CWE-680: Integer Overflow to Buffer Overflow
### CWE-681: Incorrect Conversion between Numeric Types
### CWE-682: Incorrect Calculation
### CWE-683: Function Call With Incorrect Order of Arguments
### CWE-684: Incorrect Provision of Authentication
### CWE-685: Function Call With Incorrect Number of Arguments
### CWE-686: Function Call With Incorrect Argument Type
### CWE-687: Function Call With Incorrectly Specified Argument Value
### CWE-688: Function Call With Incorrect Variable or Reference as Argument
### CWE-689: Permission Race Condition During Resource Copy
### CWE-690: Unchecked Return Value to NULL Pointer Dereference
### CWE-691: Insufficient Control Flow Management
### CWE-692: Improper Denylist
### CWE-693: Protection Mechanism Failure
### CWE-694: Use of Multiple Resources with Duplicate Identifier
### CWE-695: Use of Low-Level Functionality
### CWE-696: Incorrect Behavior Order
### CWE-697: Incorrect Comparison
### CWE-698: Insufficient Transparency
### CWE-699: Software Development (Parent)
### CWE-700: Seven Pernicious Kingdoms (Parent)
### CWE-701: Weaknesses Addressed by the SEI CERT C Coding Standard
### CWE-702: Weaknesses Addressed by the SEI CERT C++ Coding Standard
### CWE-703: Improper Check for Unusual or Exceptional Conditions
### CWE-704: Incorrect Type Conversion or Cast
### CWE-705: Incorrect Control Flow Scoping
### CWE-706: Use of Incorrectly-Resolved Name or Reference
### CWE-707: Improper Neutralization (Parent — all injection)
### CWE-708: Not Using a Trustworthy Hypervisor
### CWE-709: Local Execution of Code (Parent)
### CWE-710: Improper Adherence to Coding Standards
### CWE-711: Deprecated (OWASP Top 10)

---

## ADDITIONAL INFRASTRUCTURE & CLOUD CWEs

### CWE-1104: Use of Unmaintained Third-Party Components
**Description**: Using dependencies with no active maintenance or known vulnerabilities.

### CWE-1105: Insufficient Encapsulation of Machine-Readable Output
### CWE-1106: Insufficient Use of Symmetric Key
### CWE-1107: Insufficient Isolation of Symmetric Key
### CWE-1108: Excessive Data Exposure
### CWE-1109: Use of Same Key for Different Purposes
### CWE-1110: Incomplete Design Documentation
### CWE-1111: Incomplete I/O Coverage
### CWE-1112: Incomplete Error Handling Over Weaknesses
### CWE-1113: Incomplete Ordering of Independent Operations
### CWE-1114: Inappropriate Use of Prescriptive Force
### CWE-1115: Source Code Element Not Standardized
### CWE-1116: Inaccurate Comments
### CWE-1117: Insufficient Documentation
### CWE-1118: Insufficient Documented Errors
### CWE-1119: Excessive Use of Unconditional Branching
### CWE-1120: Excessive Code Complexity
### CWE-1121: Excessive McCabe Cyclomatic Complexity
### CWE-1122: Excessive Halstead Complexity
### CWE-1123: Excessive Use of Self-Modifying Code
### CWE-1124: Excessive Use of Indirection
### CWE-1125: Excessive Attack Surface
### CWE-1126: Declaration of Variable with Unnecessarily Wide Scope
### CWE-1127: Compilation with Insufficient Warnings
### CWE-1128: Non-Production Code Issues
### CWE-1129: Hardcoded Physical Constants
### CWE-1130: Insufficiently Control of Network Message Volume
### CWE-1131: Insufficient Design
### CWE-1132: Insufficient Distinction Between Sensitive Data
### CWE-1133: Insufficient Session ID Randomness
### CWE-1134: Improperly Restricted Session ID
### CWE-1135: Session ID as HTTP Referer
### CWE-1136: Insufficient Entropy in Session Identifier
### CWE-1137: Session ID as URL Parameter
### CWE-1138: Improperly Restricted External Interaction
### CWE-1139: Insufficient Anti-Replay Capability
### CWE-1140: Insufficient Entropy in Hardware
### CWE-1141: Insufficient Entropy in PRNG
### CWE-1142: Insufficient Entropy in TRNG
### CWE-1143: Use of Uninitialized Resource
### CWE-1144: Sensitive Information Embedded in Reusable Code
### CWE-1145: Improper Control of Document Type Definition
### CWE-1146: Improper Control of SOAP Input
### CWE-1147: Excessive Granularity of Access Control
### CWE-1148: Exposure of Resource Through Incorrect Permissions
### CWE-1149: Information Exposure Through Temporary Files
### CWE-1150: Insufficient Resource Pool
### CWE-1151: Insufficient Human Verifiability
### CWE-1152: Multiple Interpretations of Configuration Data
### CWE-1153: Incomplete Proof of Possession
### CWE-1154: Persistence of Stored Data After Reset
### CWE-1155: Inadequate Policy Enforcement
### CWE-1156: Ineffective Access Control
### CWE-1157: Ineffective Logging
### CWE-1158: Ineffective Audit Trail
### CWE-1159: Ineffective Encryption Algorithm
### CWE-1160: Ineffective Key Management
### CWE-1161: Ineffective Certificate Validation
### CWE-1162: Ineffective Input Validation
### CWE-1163: Ineffective Output Encoding
### CWE-1164: Irrelevant Security Features
### CWE-1165: Inadequate System Throughput
### CWE-1166: Inadequate Error Handling
### CWE-1167: Inadequate Concurrency Management
### CWE-1168: Inadequate Synchronization
### CWE-1169: Inadequate Resource Management
### CWE-1170: Inadequate Architectural Consideration
### CWE-1171: Inadequate Design Validation
### CWE-1172: Inadequate Consideration of Platform Independence
### CWE-1173: Inadequate Consideration of Internationalization
### CWE-1174: Inadequate Consideration of Testing
### CWE-1175: Inadequate Consideration of Performance
### CWE-1176: Inadequate Consideration of Security
### CWE-1177: Inadequate Consideration of Usability
### CWE-1178: Inadequate Consideration of Configuration
### CWE-1179: Inadequate Consideration of External Interfaces
### CWE-1180: Inadequate Consideration of Data Integrity
### CWE-1181: Inadequate Consideration of Availability
### CWE-1182: Inadequate Consideration of Maintainability
### CWE-1183: Inadequate Consideration of Portability
### CWE-1184: Inadequate Consideration of Scalability
### CWE-1185: Inadequate Consideration of Reliability
### CWE-1186: Inadequate Consideration of Interoperability
### CWE-1187: Inadequate Consideration of Reusability
### CWE-1188: Inadequate Consideration of Security of Third-Party Components
### CWE-1189: Inadequate Consideration of Security of Supply Chain
### CWE-1190: Inadequate Consideration of Security of Deployment
### CWE-1191: Inadequate Consideration of Security of Interfaces
### CWE-1192: Inadequate Consideration of Security of Data
### CWE-1193: Inadequate Consideration of Security of Processes
### CWE-1194: Inadequate Consideration of Security of Users
### CWE-1195: Inadequate Consideration of Security of Administration
### CWE-1196: Inadequate Consideration of Security of Third Party

---

## CLOUD, CONTAINER, AND INFRASTRUCTURE CWEs

### CWE-1240: Use of Cryptographically Weak Pseudo-Random Number Generator in Blockchain
### CWE-1241: Use of Predictable Seeds in Blockchain
### CWE-1242: Inclusion of Sensible Information in Smart Contract
### CWE-1243: Sensitive Data Exposure in Smart Contract Events
### CWE-1244: Unprotected Storage of Credentials in Smart Contract
### CWE-1245: Insufficient Access Control in Smart Contract
### CWE-1246: Improper Input Validation in Smart Contract
### CWE-1247: Improper Handling of Reentrancy
**Description**: Reentrancy attack in smart contracts (DAO hack).

### CWE-1248: Insecure Randomness in Smart Contracts
### CWE-1249: Improper Validation of Block Gas Limit in Smart Contract
### CWE-1250: Improperly Controlled Modification of Dynamically-Identified Variables
### CWE-1251: Insufficient Authenticity of Public Key
### CWE-1252: Insufficient Entropy in Public Key Infrastructure
### CWE-1253: Improper Type of Key in Asymmetric Cryptographic Operation
### CWE-1254: Incorrect Selection of Primitive in Cryptographic Operation
### CWE-1255: Incorrect Use of Well-Known Name for Cryptographic Function
### CWE-1256: Improper Restriction of Security Token
### CWE-1257: Improper Verification of Token Origin
### CWE-1258: Improper Restriction of Security Token Replacement
### CWE-1259: Improper Restriction of Security Token Assignment
### CWE-1260: Improper Handling of Overlap Between Protected Domains
### CWE-1261: Improper Restriction of OTP Use
### CWE-1262: Improper Restriction of OTP Validity Period
### CWE-1263: Improper Restriction of OTP Delivery Channel
### CWE-1264: Improper Restriction of OTP Generation
### CWE-1265: Improper Restriction of OTP Reuse
### CWE-1266: Improper Restriction of OTP Lifetime
### CWE-1267: Improper Restriction of OTP Sharing
### CWE-1268: Insufficient Exchange of Keys
### CWE-1269: Improper Restriction of Security Token Issuance
### CWE-1270: Generation of Incorrect Security Tokens
### CWE-1271: Uninitialized Value in Memory Mapped I/O
### CWE-1272: Insufficient Entropy in DNS
### CWE-1273: Device Identity Issues in IoT
### CWE-1274: Insufficient Entropy in Bluetooth
### CWE-1275: Insufficient Entropy in USB
### CWE-1276: Insufficient Entropy in Network
### CWE-1277: Insufficient Entropy in Firmware
### CWE-1278: Insufficient Entropy in Embedded Systems
### CWE-1279: Cryptographic Operations without Entropy
### CWE-1280: Access Control Bypass Due to Shared Ownership
### CWE-1281: DOS via Complex Expression
### CWE-1282: Insufficient Entropy in WebSocket
### CWE-1283: Insufficient Entropy in MQTT
### CWE-1284: Improper Validation of Specified Quantity in Input
### CWE-1285: Improper Validation of Specified Index in Input
### CWE-1286: Improper Validation of Syntactic Correctness of Input
### CWE-1287: Improper Validation of Specified Type of Input
### CWE-1288: Improper Validation of Consistency within Input
### CWE-1289: Improper Validation of Unsafe Equivalence in Input
### CWE-1290: Improper Decoding of Input
### CWE-1291: Improper Handling of Unchecked Input
### CWE-1292: Insufficiently Protected Field
### CWE-1293: Insufficient Granularity of Access Control
### CWE-1294: Insecure Storage of Access Control Lists
### CWE-1295: Debug Messages Revealing Unnecessary Information
### CWE-1296: Incorrect Chaining of Security Checks
### CWE-1297: Unprotected Confidential Information on Mobile Device
### CWE-1298: Insufficient Entropy in Logical Operations
### CWE-1299: Missing Validation in OpenSSL
### CWE-1300: Insufficient Entropy in Physical Access
### CWE-1301: Insufficient Entropy in Biometrics
### CWE-1302: Missing Security Identifier
### CWE-1303: Non-Constant Time String Comparison
**Description**: Timing attack via non-constant-time comparison.
```python
# BAD — Timing side channel
if user_input == secret_key:  // Comparison takes longer on partial match

# FIXED
import hmac
if hmac.compare_digest(user_input, secret_key):  // Constant time
```

### CWE-1304: Improperly Preserved Consistency of Shared Resource
### CWE-1305: Violation of Memory Area
### CWE-1306: Reliance on Mode of Access for Authorization
### CWE-1307: Insufficient Entropy in RPDE
### CWE-1308: Insufficient Entropy in Semiconductor
### CWE-1309: Insufficient Entropy in Hardware Design
### CWE-1310: Insufficient Entropy in PCB
### CWE-1311: Improper Vetting of Parameters
### CWE-1312: Missing Protection for Multi-Factor Authentication
### CWE-1313: Hardware Security Issues
### CWE-1314: Missing Write Protection in Hardware
### CWE-1315: Improper Setting of Bus Protection
### CWE-1316: Missing Protection Against Hardware Reverse Engineering
### CWE-1317: Missing Protection Against Hardware Fuzzing
### CWE-1318: Missing Protection Against Hardware Physical Attack
### CWE-1319: Missing Protection Against Hardware Side Channel
### CWE-1320: Missing Protection Against Hardware Replay Attack
### CWE-1321: Improperly Controlled Modification of Object Prototype
**Description**: Prototype pollution in JavaScript.
```javascript
// BAD — Prototype pollution
function merge(target, source) {
    for (let key in source) {
        if (typeof source[key] === 'object' && source[key] !== null) {
            merge(target[key], source[key]);
        } else {
            target[key] = source[key];
        }
    }
}

// Attacker can change Object.prototype
merge({}, JSON.parse('{"__proto__": {"isAdmin": true}}'));
// Now every object has isAdmin: true
```

### CWE-1322: Missing Protection Against Memory Safety in Hardware
### CWE-1323: Missing Protection Against DMA Attack
### CWE-1324: Missing Protection Against Cache Side Channel
### CWE-1325: Missing Protection Against Row Hammer
### CWE-1326: Missing Protection Against Voltage Fault Injection
### CWE-1327: Missing Protection Against Clock Glitch
### CWE-1328: Missing Protection Against Power Analysis
### CWE-1329: Missing Protection Against Electromagnetic Analysis
### CWE-1330: Missing Protection Against Acoustic Analysis
### CWE-1331: Missing Protection Against Timing Side Channel
### CWE-1332: Missing Protection Against Fault Injection
### CWE-1333: Inefficient Regular Expression Complexity
**Description**: ReDoS — regular expression with exponential worst-case time.

---

## SANS TOP 25 COVERAGE MAP

All SANS Top 25 CWEs are covered above. Quick reference:

| SANS Rank | CWE | Name |
|---|---|---|
| 1 | CWE-79 | XSS |
| 2 | CWE-89 | SQL Injection |
| 3 | CWE-120 | Buffer Overflow |
| 4 | CWE-22 | Path Traversal |
| 5 | CWE-78 | OS Command Injection |
| 6 | CWE-190 | Integer Overflow |
| 7 | CWE-287 | Authentication Issues |
| 8 | CWE-862 | Missing Authorization |
| 9 | CWE-476 | NULL Pointer Dereference |
| 10 | CWE-434 | Unrestricted Upload |
| 11 | CWE-352 | CSRF |
| 12 | CWE-611 | XXE |
| 13 | CWE-502 | Deserialization |
| 14 | CWE-200 | Information Exposure |
| 15 | CWE-307 | Excessive Auth Attempts |
| 16 | CWE-285 | Improper Authorization |
| 17 | CWE-918 | SSRF |
| 18 | CWE-362 | Race Condition |
| 19 | CWE-209 | Info Exposure Through Error Messages |
| 20 | CWE-295 | Certificate Validation |
| 21 | CWE-787 | OOB Write |
| 22 | CWE-125 | OOB Read |
| 23 | CWE-119 | Buffer Overflow (General) |
| 24 | CWE-732 | Incorrect Permission Assignment |
| 25 | CWE-770 | Resource Exhaustion |

Each CWE listed above has a dedicated section with detection patterns and examples in this document.

---

## DETECTION REGEX SYNTHESIS

Common regex patterns for CWE detection across languages:

```regex
# Format string (CWE-134)
\b(printf|sprintf|fprintf|snprintf|vprintf|vsprintf|vwprintf)\s*\(\s*[^",)]

# Command injection (CWE-78)
\b(exec|system|popen|subprocess\.\w+|Runtime\.getRuntime\(\)\.exec|ProcessBuilder|ShellExecute|WinExec)\s*\(

# SQL injection (CWE-89)
\.execute\(.*["`].*(SELECT|INSERT|UPDATE|DELETE).*\{.*\}.*["`]
\.query\(.*["`].*(SELECT|INSERT|UPDATE|DELETE).*["`]\s*\+|%|\$|format\(

# Path traversal (CWE-22)
\b(open|file|read|write|delete|unlink|send_file|File\.ReadAllText|Path\.Combine)\s*\(.*\b(user|input|param|arg|name|path)

# Deserialization (CWE-502)
\b(pickle\.loads|yaml\.load|shelve\.open|ObjectInputStream\.readObject|BinaryFormatter\.Deserialize|unserialize|Marshal\.load|node-serialize)

# XXE (CWE-611)
\b(loadXML|XMLReader|SimpleXMLElement|DocumentBuilder|SAXParser)\s*\(.*\b(input|stream|data|xml|doc)

# CSRF (CWE-352)
# Missing CSRF protection — check for POST/PUT/DELETE without anti-forgery token

# Open Redirect (CWE-601)
\b(redirect|sendRedirect|Location|header\s*\(.*Location)\s*\(.*\b(user|input|param|arg|url|return)

# Code Injection (CWE-94)
\b(eval|exec|assert|create_function|call_user_func|call_user_func_array|include\s*\()\s*\(.*\b(user|input|param|arg|get|post|request|query)
```

This reference covers all major CWEs in the CWE-1000 taxonomy organized by the Research Concepts view, with detection patterns, code examples, and exploit techniques.
