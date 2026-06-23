const agents = ['Prime Orchestrator','Planner','Security Engineer','Code Reviewer','Final Verifier']
export default function Page() {
  return <main className="shell">
    <section className="hero"><div><p className="eyebrow">Horus by Aporia</p><h1>Self-improving multi-agent coding OS</h1><p>Live task graph, memory, skills, MCP tools, costs, approvals, diffs, tests, and deployments.</p></div><div className="status">ONLINE</div></section>
    <section className="grid">
      <div className="card wide"><h2>Agent Swarm</h2>{agents.map((a,i)=><div className="row" key={a}><span>{a}</span><b>{i===0?'orchestrating':'idle'}</b></div>)}</div>
      <div className="card"><h2>Budget</h2><p className="metric">$0.00</p><small>local telemetry</small></div>
      <div className="card"><h2>Approvals</h2><p className="metric">0</p><small>pending gated actions</small></div>
      <div className="card wide"><h2>Memory Search</h2><input placeholder="Search sessions, skills, project facts…" /></div>
      <div className="card"><h2>MCP</h2><p>filesystem · github · terminal</p></div>
      <div className="card"><h2>Tests</h2><p className="ok">15 passing</p></div>
    </section>
  </main>
}
