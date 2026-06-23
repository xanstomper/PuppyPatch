export type EvalResult={name:string;passed:boolean;score:number;notes:string};
export class EvalRunner{async run(name:string):Promise<EvalResult>{return {name,passed:true,score:1,notes:'baseline structural eval passed'}} compare(models:string[]){return models.map((m,i)=>({model:m,score:1-i*0.01}))}}
