const secrets=[/sk-[A-Za-z0-9_-]{16,}/g,/gh[pousr]_[A-Za-z0-9_]{20,}/g,/AKIA[0-9A-Z]{16}/g];
export function redact(input:string){return secrets.reduce((s,r)=>s.replace(r,'[REDACTED]'), input)}
