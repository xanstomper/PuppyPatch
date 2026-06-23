import { execa } from 'execa';
import { z } from 'zod';
export const SearchFilesInput = z.object({ query: z.string(), cwd: z.string().default('.') });
export async function searchFiles(input: z.infer<typeof SearchFilesInput>) {
  const cmd = process.platform === 'win32' ? 'rg.exe' : 'rg';
  const r = await execa(cmd, [input.query, '.'], { cwd: input.cwd, reject: false });
  return { ok: r.exitCode === 0 || r.exitCode === 1, data: r.stdout };
}
