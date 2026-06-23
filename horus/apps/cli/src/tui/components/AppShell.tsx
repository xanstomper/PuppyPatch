import React from 'react'; import { Box, Text } from 'ink';
export function AppShell({children}:{children:React.ReactNode}){return <Box flexDirection="column" height="100%" borderStyle="round" borderColor="gray" paddingX={1}><Text color="yellow">◉ HORUS</Text>{children}</Box>}
