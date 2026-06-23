import { z } from 'zod';
export const HorusConfigSchema = z.object({
  models: z.object({default: z.string(), routes: z.record(z.string(), z.string()).default({})}),
  agents: z.object({maxConcurrent: z.number().min(1).max(60).default(60), defaultTimeoutMinutes: z.number().default(45)}),
  memory: z.object({sqlitePath: z.string().default('.horus/memory.db'), fts: z.boolean().default(true)}),
  mcp: z.object({servers: z.record(z.string(), z.object({command: z.string(), args: z.array(z.string()).default([]), permissions: z.string().default('read-only')})).default({})}),
  permissions: z.object({default: z.array(z.string()).default(['read-only']), requireApproval: z.array(z.string()).default(['destructive','deploy','secrets','admin'])})
});
export type HorusConfig = z.infer<typeof HorusConfigSchema>;

export const AdvancedSkillSchema = z.object({
  id: z.string(), name: z.string(), description: z.string(), trigger_conditions: z.array(z.string()), required_context: z.array(z.string()), required_tools: z.array(z.string()), required_permissions: z.array(z.string()), step_by_step_procedure: z.array(z.string()), verification_checks: z.array(z.string()), failure_modes: z.array(z.string()), recovery_steps: z.array(z.string()), examples: z.array(z.string()), anti_patterns: z.array(z.string()), compatible_models: z.array(z.string()), compatible_projects: z.array(z.string()), tags: z.array(z.string()), version: z.string(), changelog: z.array(z.string()), success_rate: z.number(), last_used: z.string().optional(), created_from_session: z.string().optional(), confidence_score: z.number()
});
export type AdvancedSkill = z.infer<typeof AdvancedSkillSchema>;

export const MemoryRecordSchema = z.object({id:z.number().optional(), ts:z.number(), layer:z.enum(['session','project','user','skill','tool','failure','semantic','fulltext','profile']), scope:z.string(), content:z.string(), summary:z.string().optional(), sourceSession:z.string().optional(), confidence:z.number().default(0.5), relevance:z.number().optional(), tags:z.array(z.string()).default([]), meta:z.record(z.string(), z.unknown()).default({})});
export type MemoryRecord = z.infer<typeof MemoryRecordSchema>;

export const UserPreferenceSchema = z.object({key:z.string(), value:z.string(), confidence:z.number(), sourceSession:z.string(), sensitive:z.boolean().default(false), updatedAt:z.number()});
export type UserPreference = z.infer<typeof UserPreferenceSchema>;

export const AutomationSchema = z.object({id:z.string(), name:z.string(), natural_language_prompt:z.string(), schedule:z.string(), timezone:z.string().default('UTC'), delivery_platform:z.string(), allowed_tools:z.array(z.string()), allowed_agents:z.array(z.string()), model_route:z.string(), budget_limit:z.number(), timeout:z.number(), permission_policy:z.string(), approval_policy:z.string(), memory_scope:z.string(), output_format:z.string(), enabled:z.boolean(), last_run:z.number().optional(), next_run:z.number().optional(), run_history:z.array(z.record(z.string(), z.unknown())).default([])});
export type AutomationSpec = z.infer<typeof AutomationSchema>;

export const TrajectoryEventSchema = z.object({id:z.string(), taskId:z.string(), ts:z.number(), kind:z.string(), prompt:z.string().optional(), model:z.string().optional(), tool:z.string().optional(), observation:z.string().optional(), patch:z.string().optional(), testResult:z.string().optional(), success:z.boolean().optional(), meta:z.record(z.string(), z.unknown()).default({})});
export type TrajectoryEvent = z.infer<typeof TrajectoryEventSchema>;
