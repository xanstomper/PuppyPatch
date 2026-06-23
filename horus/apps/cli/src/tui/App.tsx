import React, { useEffect, useState } from 'react';
import { Box, useApp } from 'ink';
import { eventBus, loadConfig, runCodingLoop } from '@horus/core';
import { gitStatus } from '@horus/tools';
import { AppShell } from './components/AppShell.js';
import { MainTranscriptPane } from './components/MainTranscriptPane.js';
import { RightSidebar } from './components/RightSidebar.js';
import { PromptBar } from './components/PromptBar.js';
import { FooterStatus } from './components/FooterStatus.js';
import { SlashCommandMenu } from './components/SlashCommandMenu.js';
import { runSlashCommand } from './slash.js';

export function HorusApp(){
  const { exit } = useApp();
  const [lines,setLines] = useState<string[]>(['Horus Phase 1 Core MVP ready. Type a task or /help.']);
  const [input,setInput] = useState('');
  const [git,setGit] = useState('loading');
  const [model,setModel] = useState(loadConfig().model);
  useEffect(()=>{ const off = eventBus.onEvent(e=>setLines(x=>[...x, formatEvent(e)])); return () => { off(); }; },[]);
  useEffect(()=>{gitStatus({cwd:'.'}).then(r=>setGit(String(r.data ?? 'unknown'))).catch(()=>setGit('not a git repo'));},[]);
  async function submit(text:string){
    const v=text.trim(); if(!v) return; setInput(''); setLines(x=>[...x,`you: ${v}`]);
    if(v==='/quit'||v==='/exit'){exit();return;}
    if(v.startsWith('/')) return handleSlash(v);
    await runCodingLoop(v,'.');
  }
  function handleSlash(v:string){
    const [cmd,arg] = v.split(/\s+/,2);
    if(cmd==='/model' && arg){ setModel(arg); setLines(x=>[...x,`model set: ${arg}`]); return; }
    const result = runSlashCommand(v, git);
    setLines(x=>[...x,result.text]);
  }
  return <AppShell><Box flexGrow={1}><Box flexDirection="column" flexGrow={1}><MainTranscriptPane lines={lines}/><SlashCommandMenu query={input}/><PromptBar value={input} onChange={setInput} onSubmit={submit}/></Box><RightSidebar model={model} git={git}/></Box><FooterStatus/></AppShell>;
}
function formatEvent(e:any){ if(e.type==='tool') return `tool:${e.tool}:${e.action} ${e.content??''}`; if(e.type==='git') return `git:${e.action} ${e.content??''}`; if(e.type==='shell') return `shell:${e.action} ${e.content??e.exitCode??''}`; if(e.type==='file') return `file:${e.action} ${e.path??''}`; if(e.type==='agent') return `agent:${e.action} ${e.content??''}`; if(e.type==='mcp') return `mcp:${e.action} placeholder`; return `${e.type}:${e.action} ${e.content??e.message??''}`; }
export default HorusApp;
