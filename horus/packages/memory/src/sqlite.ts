import Database from 'better-sqlite3'; import fs from 'node:fs'; import path from 'node:path';
export class SQLiteMemory { db:Database.Database; constructor(public file='.horus/memory.db'){fs.mkdirSync(path.dirname(file),{recursive:true}); this.db=new Database(file); this.db.exec('create table if not exists events(id integer primary key, ts integer, type text, scope text, content text, meta text); create virtual table if not exists memory_fts using fts5(content,type,scope);');}
 add(type:string,content:string,scope='session',meta:unknown={}){const info=this.db.prepare('insert into events(ts,type,scope,content,meta) values(?,?,?,?,?)').run(Date.now(),type,scope,content,JSON.stringify(meta)); this.db.prepare('insert into memory_fts(content,type,scope) values(?,?,?)').run(content,type,scope); return Number(info.lastInsertRowid)}
 search(q:string){return this.db.prepare('select rowid,content,type,scope from memory_fts where memory_fts match ? limit 20').all(q)}
 summarize(scope='session'){return this.db.prepare('select type,content from events where scope=? order by id desc limit 20').all(scope).map((r:any)=>`- ${r.type}: ${String(r.content).slice(0,160)}`).join('\n')}
}
