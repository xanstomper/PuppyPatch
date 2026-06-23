export class Swarm{agents:string[]=[]; add(id:string){this.agents.push(id)} status(){return this.agents.map(id=>({id,state:'idle'}))}}
