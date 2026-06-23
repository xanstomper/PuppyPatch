import fs from 'node:fs';
import { HorusConfigSchema } from '@horus/shared';
export function validateConfig(path='horus.json'){ if(!fs.existsSync(path)) return {ok:true,source:'defaults'}; const data=JSON.parse(fs.readFileSync(path,'utf8')); return {ok:true,config:HorusConfigSchema.parse(data)}; }
export function explainConfig(){return ['CLI flags','environment variables','project config','user config','default config'];}
export function printConfig(){return JSON.stringify(validateConfig(),null,2)}
