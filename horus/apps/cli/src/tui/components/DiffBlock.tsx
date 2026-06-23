import React from 'react'; import { Text } from 'ink';
export function DiffBlock({diff}:{diff:string}){return <Text color="cyan">{diff || 'no diff'}</Text>}
