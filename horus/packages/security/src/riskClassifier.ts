const dangerous=[/rm\s+-rf/i,/Remove-Item.+-Recurse/i,/git\s+push/i,/terraform\s+apply/i,/kubectl\s+delete/i,/drop\s+database/i];
export type Risk='low'|'network'|'destructive';
export function classifyCommand(cmd:string):Risk{ if(dangerous.some(r=>r.test(cmd))) return 'destructive'; if(/npm install|pnpm add|pip install|uv add/i.test(cmd)) return 'network'; return 'low'; }
