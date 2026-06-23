import React from 'react'; import { Box, Text } from 'ink'; import TextInput from 'ink-text-input';
export function PromptBar({value,onChange,onSubmit}:{value:string;onChange:(v:string)=>void;onSubmit:(v:string)=>void}){return <Box borderStyle="single" borderColor="gray" paddingX={1}><Text color="cyan">horus › </Text><TextInput value={value} onChange={onChange} onSubmit={onSubmit}/></Box>}
