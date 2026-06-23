import React from 'react'; import { Box, Text } from 'ink';
export function MainTranscriptPane({lines}:{lines:string[]}){return <Box flexDirection="column" flexGrow={1} borderStyle="single" borderColor="gray" paddingX={1}>{lines.slice(-24).map((l,i)=><Text key={i} color={l.startsWith('tool')?'green':l.startsWith('error')?'red':'white'}>{l}</Text>)}</Box>}
