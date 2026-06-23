import type { MemoryRecord } from '@horus/shared';
import { SQLiteMemory } from './sqlite.js';

export class LayeredMemory extends SQLiteMemory {
  writeRecord(record: Omit<MemoryRecord,'id'>){ return this.add(record.layer, record.content, record.scope, record); }
  inspect(id:number){ return this.db.prepare('select * from events where id=?').get(id); }
  delete(id:number){ return this.db.prepare('delete from events where id=?').run(id); }
  edit(id:number, content:string){ return this.db.prepare('update events set content=? where id=?').run(content,id); }
  hybridSearch(query:string, opts:{scope?:string; layer?:string; since?:number; limit?:number}={}){ const rows=this.search(query) as any[]; return rows.filter(r=>(!opts.scope||r.scope===opts.scope)&&(!opts.layer||r.type===opts.layer)).slice(0,opts.limit??20).map((r,i)=>({...r,relevance:1/(i+1),confidence:0.75,reason:`matched exact/fts query: ${query}`})); }
  failurePatterns(){ return this.db.prepare("select content,count(*) as count from events where type='failure' group by content order by count desc limit 20").all(); }
}
