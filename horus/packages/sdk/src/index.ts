import { z } from 'zod';
export type DefinedAgent<T extends Record<string,unknown>=Record<string,unknown>>=T & {kind:'agent'};
export type DefinedTask<I=unknown,O=unknown>={kind:'task';name:string;agent:DefinedAgent;input:z.ZodType<I>;output:z.ZodType<O>;run?:(input:I)=>Promise<O>|O};
export type DefinedTool<I=unknown,O=unknown>={kind:'tool';name:string;description:string;input:z.ZodType<I>;output:z.ZodType<O>;safetyLevel:string;permissions:string[];handler:(input:I)=>Promise<O>|O};
export function defineAgent<T extends Record<string,unknown>>(agent:T):DefinedAgent<T>{return {...agent,kind:'agent'}}
export function defineTask<I,O>(task:Omit<DefinedTask<I,O>,'kind'>):DefinedTask<I,O>{return {...task,kind:'task'}}
export function defineTool<I,O>(tool:Omit<DefinedTool<I,O>,'kind'>):DefinedTool<I,O>{return {...tool,kind:'tool'}}
export async function runTask<I,O>(task:DefinedTask<I,O>, input:unknown):Promise<O>{const parsed=task.input.parse(input); if(task.run){const out=await task.run(parsed); return task.output.parse(out)} return task.output.parse({} as O)}
