export type SessionCheckpoint = {id:string; timestamp:number; files:string[]; note:string};
export class SessionState { transcript:string[]=[]; checkpoints:SessionCheckpoint[]=[]; add(line:string){this.transcript.push(line)} checkpoint(note:string, files:string[]=[]){const cp={id:crypto.randomUUID(),timestamp:Date.now(),files,note}; this.checkpoints.push(cp); return cp;} }
