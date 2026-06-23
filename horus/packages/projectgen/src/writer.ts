import fs from 'node:fs'; import path from 'node:path';
export function writeFile(root:string,file:string,content:string){const p=path.join(root,file); fs.mkdirSync(path.dirname(p),{recursive:true}); fs.writeFileSync(p,content);}
export function kebab(s:string){return s.trim().toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')}
