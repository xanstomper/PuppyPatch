export type StructuredResult<T=unknown> = { ok: boolean; data?: T; error?: string; code?: string };
export type SafetyLevel = 'low'|'medium'|'high'|'destructive';
export type Permission = 'read-only'|'safe-write'|'repo-write'|'command-exec'|'network'|'destructive'|'admin';
export const SlashCommands = ['/new','/reset','/model','/diff','/undo','/doctor','/status','/help'] as const;
export type SlashCommand = typeof SlashCommands[number];
