import fs from 'node:fs';
export type ProjectInstructions = { horus?: string; agents?: string; readme?: string };
export function loadProjectInstructions(cwd = '.'): ProjectInstructions {
  const read = (file: string) => fs.existsSync(`${cwd}/${file}`) ? fs.readFileSync(`${cwd}/${file}`, 'utf8').slice(0, 12000) : undefined;
  return { horus: read('HORUS.md'), agents: read('AGENTS.md'), readme: read('README.md') };
}
