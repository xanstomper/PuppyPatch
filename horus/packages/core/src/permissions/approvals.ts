export type Approval = { id: string; reason: string; status: 'pending'|'approved'|'denied'; createdAt: number };
export class ApprovalStore {
  approvals: Approval[] = [];
  request(reason: string) { const approval = { id: crypto.randomUUID(), reason, status: 'pending' as const, createdAt: Date.now() }; this.approvals.push(approval); return approval; }
  decide(id: string, status: 'approved'|'denied') { const a = this.approvals.find(x => x.id === id); if (a) a.status = status; return a; }
}
