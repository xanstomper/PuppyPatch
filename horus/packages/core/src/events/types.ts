export type ModelEvent = { type: 'model'; action: 'list'|'set'|'route'|'stream'; model?: string; content?: string };
export type AgentEvent = { type: 'agent'; action: 'start'|'plan'|'done'|'error'; content?: string };
export type ToolEvent = { type: 'tool'; action: 'start'|'stdout'|'stderr'|'done'|'error'; tool: string; content?: string; ok?: boolean };
export type FileEditEvent = { type: 'file'; action: 'checkpoint'|'write'|'patch'|'diff'|'undo'|'restore'; path?: string; diff?: string; content?: string };
export type ShellEvent = { type: 'shell'; action: 'start'|'stdout'|'stderr'|'exit'; command: string; content?: string; exitCode?: number };
export type GitEvent = { type: 'git'; action: 'status'|'diff'; content: string };
export type ApprovalEvent = { type: 'approval'; action: 'request'|'approve'|'deny'; id: string; reason: string };
export type ErrorEvent = { type: 'error'; action: 'error'; message: string; stack?: string };
export type MCPEvent = { type: 'mcp'; action: 'placeholder'; content: string };
export type TaskEvent = { type: 'task'; action: 'new'|'progress'|'done'; content: string };
export type HorusEvent = ModelEvent|AgentEvent|ToolEvent|FileEditEvent|ShellEvent|GitEvent|ApprovalEvent|ErrorEvent|MCPEvent|TaskEvent;

