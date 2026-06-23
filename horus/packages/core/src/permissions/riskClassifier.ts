const destructive = [/\brm\s+-rf\b/i,/Remove-Item.+-Recurse/i,/\bgit\s+push\b/i,/\bdeploy\b/i,/\bkubectl\s+delete\b/i,/\bterraform\s+apply\b/i,/\bdel\s+\/s\b/i];
export function classifyCommandRisk(command: string): 'low'|'medium'|'high'|'destructive' {
  if (destructive.some(r => r.test(command))) return 'destructive';
  if (/npm install|pnpm add|pip install|curl|wget/i.test(command)) return 'high';
  if (/test|build|lint|typecheck|git status|git diff/i.test(command)) return 'low';
  return 'medium';
}
export function redactSecrets(text: string) {
  return text.replace(/sk-[A-Za-z0-9_-]{16,}/g,'[REDACTED]').replace(/gh[pousr]_[A-Za-z0-9_]{20,}/g,'[REDACTED]');
}
export function isProtectedFile(path: string, protectedFiles = ['.env','.env.local','id_rsa','id_ed25519']) {
  return protectedFiles.some(p => path.endsWith(p) || path.includes(`/${p}`) || path.includes(`\\${p}`));
}
