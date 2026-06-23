import { z } from 'zod';
import { ToolRegistry } from './registry.js';
import { readFile, writeFile, listFiles, ReadFileInput, WriteFileInput, ListFilesInput } from './filesystem.js';
import { runCommand, RunCommandInput } from './shell.js';
import { gitStatus, gitDiff, GitInput } from './git.js';
import { searchFiles, SearchFilesInput } from './search.js';
import { patchFile, PatchFileInput, createCheckpoint, restoreCheckpoint, undoLastPatch, diffLastPatch } from './edit.js';
import { createRedTeamTools } from './redteam.js';

export function createMvpToolRegistry() {
  const r = new ToolRegistry();
  r.register({ name: 'read_file', description: 'Read a UTF-8 file', inputSchema: ReadFileInput, outputSchema: z.any(), safety: 'low', permission: 'read-only', run: readFile });
  r.register({ name: 'write_file', description: 'Write a file with checkpoint', inputSchema: WriteFileInput, outputSchema: z.any(), safety: 'medium', permission: 'safe-write', run: writeFile });
  r.register({ name: 'patch_file', description: 'Patch a file with checkpoint', inputSchema: PatchFileInput, outputSchema: z.any(), safety: 'medium', permission: 'repo-write', run: patchFile });
  r.register({ name: 'list_files', description: 'List directory entries', inputSchema: ListFilesInput, outputSchema: z.any(), safety: 'low', permission: 'read-only', run: listFiles });
  r.register({ name: 'search_files', description: 'Search files with ripgrep', inputSchema: SearchFilesInput, outputSchema: z.any(), safety: 'low', permission: 'read-only', run: searchFiles });
  r.register({ name: 'run_command', description: 'Run a safe shell command', inputSchema: RunCommandInput, outputSchema: z.any(), safety: 'high', permission: 'command-exec', run: runCommand });
  r.register({ name: 'git_status', description: 'Show git status', inputSchema: GitInput, outputSchema: z.any(), safety: 'low', permission: 'read-only', run: gitStatus });
  r.register({ name: 'git_diff', description: 'Show git diff', inputSchema: GitInput, outputSchema: z.any(), safety: 'low', permission: 'read-only', run: gitDiff });
  r.register({ name: 'create_checkpoint', description: 'Create file checkpoint', inputSchema: z.object({ path: z.string(), note: z.string().optional() }), outputSchema: z.any(), safety: 'low', permission: 'read-only', run: createCheckpoint });
  r.register({ name: 'restore_checkpoint', description: 'Restore checkpoint by id', inputSchema: z.object({ id: z.string() }), outputSchema: z.any(), safety: 'medium', permission: 'safe-write', run: restoreCheckpoint });
  r.register({ name: 'undo_last_patch', description: 'Undo last file patch', inputSchema: z.object({}).default({}), outputSchema: z.any(), safety: 'medium', permission: 'safe-write', run: () => undoLastPatch() });
  r.register({ name: 'diff_last_patch', description: 'Show last patch diff', inputSchema: z.object({}).default({}), outputSchema: z.any(), safety: 'low', permission: 'read-only', run: () => diffLastPatch() });
  for (const tool of createRedTeamTools()) { r.register(tool); }
  return r;
}
export * from './registry.js';
export * from './filesystem.js';
export * from './shell.js';
export * from './git.js';
export * from './search.js';
export * from './edit.js';
export * from './redteam.js';
