import { z } from 'zod';
export const SkillSchema=z.object({name:z.string(),description:z.string(),triggerConditions:z.array(z.string()).default([]),requiredTools:z.array(z.string()).default([]),steps:z.array(z.string()).default([]),examples:z.array(z.string()).default([]),failureModes:z.array(z.string()).default([]),verificationChecks:z.array(z.string()).default([]),lastUsed:z.string().optional(),successRate:z.number().default(0),owner:z.string().default('Aporia'),version:z.string().default('0.1.0'),changelog:z.array(z.string()).default([])});
export type Skill=z.infer<typeof SkillSchema>;
