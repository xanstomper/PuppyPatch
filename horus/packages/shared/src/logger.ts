export type LogLevel = 'debug'|'info'|'warn'|'error';
export function log(level: LogLevel, message: string, meta?: unknown) {
  if (process.env.HORUS_LOG === 'silent') return;
  console.error(`[${level}] ${message}`, meta ?? '');
}
