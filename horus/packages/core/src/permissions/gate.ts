import type { Permission, SafetyLevel } from '@horus/shared';
export type ApprovalDecision = {allowed:boolean; reason:string; requiresApproval:boolean};
export class PermissionGate {
  constructor(private granted: string[]) {}
  check(required: Permission | string, safety: SafetyLevel = 'low'): ApprovalDecision {
    if (!this.granted.includes(required) && !this.granted.includes('admin')) return {allowed:false, reason:`missing permission: ${required}`, requiresApproval:false};
    if (['high','destructive','deploy','secrets'].includes(safety)) return {allowed:false, reason:`approval required for ${safety}`, requiresApproval:true};
    return {allowed:true, reason:'allowed', requiresApproval:false};
  }
}
