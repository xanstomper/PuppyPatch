import React from 'react'; import { Text } from 'ink';
export function ToolOutputBlock({text}:{text:string}){return <Text color="green">tool: {text}</Text>}
