import fs from 'node:fs'; import path from 'node:path';
import { Templates, type InitOptions, type TemplateName, templateDefaults } from './templates.js';
import { writeFile, kebab } from './writer.js';

export function initProject(name:string, options:InitOptions={}){
  const root=kebab(name); const template=(options.template ?? 'coding-agent') as TemplateName; if(!Templates.includes(template)) throw new Error(`Unknown template ${template}`);
  const d=templateDefaults(template); fs.mkdirSync(root,{recursive:true});
  writeFile(root,'package.json',JSON.stringify({name:root,type:'module',scripts:{dev:'tsx src/index.ts',test:'node --import tsx --test tests/*.test.ts',eval:'tsx evals/sample.eval.ts',build:'tsc --noEmit'},dependencies:{'@aporia/horus':'latest',zod:'latest'},devDependencies:{tsx:'latest',typescript:'latest','@types/node':'latest'}},null,2));
  writeFile(root,'tsconfig.json',JSON.stringify({compilerOptions:{target:'ES2022',module:'NodeNext',moduleResolution:'NodeNext',strict:true,esModuleInterop:true,skipLibCheck:true}},null,2));
  writeFile(root,'pnpm-workspace.yaml','packages:\n  - "."\n');
  writeFile(root,'src/index.ts',`import { runTask } from './runtime.js';\nrunTask('default', { prompt: 'Audit this project safely.' }).then(console.log);\n`);
  writeFile(root,'src/runtime.ts',`import { defaultTask } from './tasks/defaultTask.js';\nexport async function runTask(name:string,input:unknown){ if(name==='default') return defaultTask(input); throw new Error('Unknown task '+name); }\n`);
  writeFile(root,'src/agents/defaultAgent.ts',`export const defaultAgent = ${JSON.stringify({id:'default-agent',name:d.agentRole,role:d.agentRole,description:`Generated ${template} agent`,system_prompt:`You are ${d.agentRole}. Work safely and verify results.`,model_route:d.modelRoute,tools:d.tools,mcp_tools:options.mcp??[],memory_scope:d.memoryPolicy,permissions:[d.permissionPolicy],max_runtime:1800,max_tokens:8000,max_cost:1,output_schema:{type:'object'},verification_policy:'run generated tests/evals',handoff_policy:'handoff to reviewer when risk is high',escalation_policy:'ask user for destructive actions'},null,2)} as const;\n`);
  writeFile(root,'src/tasks/defaultTask.ts',`import { defaultAgent } from '../agents/defaultAgent.js';\nexport async function defaultTask(input: any){ return { agent: defaultAgent.name, input, status: 'planned', verification: ['pnpm test','pnpm eval'] }; }\n`);
  writeFile(root,'src/tools/exampleTool.ts',`import { z } from 'zod';\nexport const ExampleToolInput = z.object({ text: z.string() });\nexport async function exampleTool(input: z.infer<typeof ExampleToolInput>){ const parsed=ExampleToolInput.parse(input); return { ok:true, echo: parsed.text }; }\n`);
  writeFile(root,'config/horus.config.ts',`export default ${JSON.stringify({template,provider:options.provider??'openrouter',memory:options.memory??'sqlite',deploy:options.deploy??'docker',modelRoutes:{default:'balanced'},permissions:{default:['read-only'],generated:[d.permissionPolicy]}},null,2)};\n`);
  writeFile(root,'config/agents.yaml',`default:\n  role: ${d.agentRole}\n  model_route: ${d.modelRoute}\n  tools: ${d.tools.join(',')}\n`);
  writeFile(root,'config/tasks.yaml',`default:\n  assigned_agent: default-agent\n  acceptance_criteria:\n    - produces structured result\n    - tests pass\n`);
  writeFile(root,'config/tools.yaml',`example_tool:\n  safety_level: low\n  permissions_required: [read-only]\n`);
  writeFile(root,'config/models.yaml',`default: ${options.provider??'openrouter'}:default\nprofiles: [cheap, fast, balanced, strong, long-context, local, private, review, security, creative, coding]\n`);
  writeFile(root,'config/mcp.yaml',`servers:\n${(options.mcp??['filesystem']).map(x=>`  ${x}:\n    command: mcp-${x}\n    permissions: read-only`).join('\n')}\n`);
  writeFile(root,'config/memory.yaml',`backend: ${options.memory??'sqlite'}\nscopes: [session, project, user, skills]\n`);
  writeFile(root,'config/permissions.yaml',`default: [read-only]\nrequire_approval: [destructive, deploy, secrets, admin]\n`);
  writeFile(root,'config/evals.yaml',`sample:\n  task: default\n  expected_status: planned\n`);
  writeFile(root,'tests/default.test.ts',`import test from 'node:test'; import assert from 'node:assert/strict'; import { defaultTask } from '../src/tasks/defaultTask.ts';\ntest('default task returns planned status', async()=>{ const r=await defaultTask({prompt:'x'}); assert.equal(r.status,'planned'); });\n`);
  writeFile(root,'evals/sample.eval.ts',`import { defaultTask } from '../src/tasks/defaultTask.js';\nconst r=await defaultTask({prompt:'eval'}); console.log(JSON.stringify({passed:r.status==='planned', score:r.status==='planned'?1:0}));\n`);
  writeDocs(root, template, d, options);
  writeFile(root,'.env.example','OPENROUTER_API_KEY=\nHORUS_APPROVAL_MODE=manual\n');
  writeFile(root,'.github/workflows/tests.yml','name: tests\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: pnpm/action-setup@v4\n        with: { version: 9 }\n      - uses: actions/setup-node@v4\n        with: { node-version: 22, cache: pnpm }\n      - run: pnpm install\n      - run: pnpm test\n');
  writeFile(root,'Dockerfile','FROM node:22-slim\nWORKDIR /app\nCOPY . .\nRUN corepack enable && pnpm install\nCMD ["pnpm","dev"]\n');
  writeFile(root,'docker-compose.yml','services:\n  agent:\n    build: .\n    env_file: .env\n');
  return root;
}
function writeDocs(root:string, template:string, d:any, options:InitOptions){
  writeFile(root,'README.md',`# ${root}\n\nGenerated by Horus using template \`${template}\`.\n\n## Run\n\n\`\`\`bash\npnpm install\npnpm dev\npnpm test\npnpm eval\n\`\`\`\n`);
  writeFile(root,'HORUS.md',`# HORUS.md\n\nPurpose: ${template} agent project.\nStack: TypeScript, Horus SDK, Zod.\nCommands: pnpm dev, pnpm test, pnpm eval.\nCoding style: strict TypeScript, small safe diffs.\nForbidden actions: destructive shell, secret edits, production deploy without approval.\nDeployment: ${options.deploy??'docker'}.\nUseful paths: src/agents, src/tasks, src/tools, config, evals, tests.\n`);
  for(const [file,title] of Object.entries({ 'docs/QUICKSTART.md':'Quickstart','docs/ARCHITECTURE.md':'Architecture','docs/TOOLS.md':'Tools','docs/TASKS.md':'Tasks','docs/CONFIG.md':'Config','docs/DEPLOYMENT.md':'Deployment','docs/SECURITY.md':'Security','docs/EVALS.md':'Evals'})) writeFile(root,file,`# ${title}\n\nGenerated docs for the ${template} template. This file matches generated project structure.\n`);
}
