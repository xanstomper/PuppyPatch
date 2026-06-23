import type { Skill } from './schema.js';
export function buildSkill(name:string,description:string,steps:string[],requiredTools:string[]=[]):Skill{return {name,description,steps,requiredTools,triggerConditions:[],examples:[],failureModes:[],verificationChecks:[],successRate:0,owner:'Aporia',version:'0.1.0',changelog:[`created ${new Date().toISOString()}`]}}
