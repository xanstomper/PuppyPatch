import { z } from 'zod';
import type { Permission, SafetyLevel, StructuredResult } from '@horus/shared';

export type ToolSpec<I=unknown,O=unknown> = { name: string; description: string; inputSchema: z.ZodType<I>; outputSchema: z.ZodType<O>; safety: SafetyLevel; permission: Permission; run: (input: I) => Promise<StructuredResult<O>> | StructuredResult<O> };
export class ToolRegistry {
  private tools = new Map<string, ToolSpec<any,any>>();
  register<I,O>(tool: ToolSpec<I,O>) { this.tools.set(tool.name, tool); return tool; }
  get(name: string) { return this.tools.get(name); }
  list() { return [...this.tools.values()].map(t => ({ name: t.name, description: t.description, safety: t.safety, permission: t.permission })); }
  async call(name: string, input: unknown) { const tool = this.get(name); if (!tool) throw new Error(`Unknown tool: ${name}`); return tool.run(tool.inputSchema.parse(input)); }
}
