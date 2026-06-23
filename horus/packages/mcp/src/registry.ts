export type MCPServerConfig={name:string;command:string;args:string[];permissions:string};
export class MCPRegistry{servers=new Map<string,MCPServerConfig>(); add(s:MCPServerConfig){this.servers.set(s.name,s)} list(){return [...this.servers.values()]} health(name:string){const s=this.servers.get(name); return {name,configured:!!s,permissions:s?.permissions}}}
