import React from 'react'; import { Box, Text } from 'ink';
export function ContextMeter(){return <Text color="gray">context 0%</Text>}
export function MCPStatusPanel(){return <Text color="cyan">MCP placeholder — Phase 2 planned</Text>}
export function AgentStatusPanel(){return <Text color="green">agent: single runtime</Text>}
export function TodoPanel(){return <Text>todos: current task only</Text>}
export function RightSidebar({model,git}:{model:string;git:string}){return <Box flexDirection="column" width={36} borderStyle="single" borderColor="gray" paddingX={1}><Text color="yellow">model</Text><Text>{model}</Text><Text color="yellow">git</Text><Text>{git || 'clean/unknown'}</Text><ContextMeter/><MCPStatusPanel/><AgentStatusPanel/><TodoPanel/></Box>}

