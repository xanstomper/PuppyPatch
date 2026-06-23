import { z } from 'zod';
export const HorusConfigSchema = z.object({
  model: z.string().default('openai:gpt-4o-mini'),
  providers: z.record(z.string(), z.object({ baseUrl: z.string(), apiKeyEnv: z.string(), models: z.array(z.string()).default([]) })).default({}),
  protectedFiles: z.array(z.string()).default(['.env', '.env.local', 'id_rsa', 'id_ed25519']),
  approvalMode: z.enum(['manual','auto-safe']).default('manual')
});
export type HorusConfig = z.infer<typeof HorusConfigSchema>;
export const defaultConfig: HorusConfig = HorusConfigSchema.parse({
  model: process.env.HORUS_MODEL ?? 'openai:gpt-4o-mini',
  providers: {
    openai: { baseUrl: 'https://api.openai.com/v1', apiKeyEnv: 'OPENAI_API_KEY', models: ['gpt-4o-mini','gpt-4.1-mini'] },
    openrouter: { baseUrl: 'https://openrouter.ai/api/v1', apiKeyEnv: 'OPENROUTER_API_KEY', models: ['anthropic/claude-sonnet-4.5','openai/gpt-4o-mini'] },
    local: { baseUrl: 'http://127.0.0.1:11434/v1', apiKeyEnv: 'LOCAL_API_KEY', models: ['local-model'] }
  }
});
