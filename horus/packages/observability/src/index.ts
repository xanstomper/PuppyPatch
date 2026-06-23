import fs from 'node:fs'; import path from 'node:path'; import type { HorusEvent } from '@horus/shared';
export class JSONLObserver{constructor(public file='.horus/events.jsonl'){fs.mkdirSync(path.dirname(file),{recursive:true})} write(e:HorusEvent){fs.appendFileSync(this.file,JSON.stringify({...e,ts:Date.now()})+'\n')}}
export class Metrics{modelCalls=0;toolCalls=0;failures=0;approvals=0;tokens=0;cost=0; snapshot(){return {...this}}}
