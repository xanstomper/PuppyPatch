import type { AgentContract } from '@horus/shared';
export class Orchestrator{tasks:AgentContract[]=[]; constructor(public max=60){} spawn(c:AgentContract){if(this.tasks.length>=this.max)throw new Error('agent limit reached'); this.tasks.push(c); return c} list(){return this.tasks}}
