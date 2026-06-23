import React from 'react'; import { Text } from 'ink';
export function Badge({children,color='cyan'}:{children:React.ReactNode;color?:string}){return <Text color={color}>[{children}]</Text>}
