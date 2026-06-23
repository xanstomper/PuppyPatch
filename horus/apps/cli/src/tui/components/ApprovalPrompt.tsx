import React from 'react'; import { Text } from 'ink';
export function ApprovalPrompt({reason}:{reason:string}){return <Text color="yellow">approval required: {reason}</Text>}
