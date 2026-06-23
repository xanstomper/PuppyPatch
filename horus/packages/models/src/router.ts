export type ModelRef = { provider: string; model: string };
export function parseModelRef(value: string): ModelRef { const i = value.indexOf(':'); if (i < 1) throw new Error('Model must be provider:model'); return { provider: value.slice(0, i), model: value.slice(i + 1) }; }
export class ModelRouter {
  constructor(public current: string) {}
  set(model: string) { this.current = model; }
  route() { return parseModelRef(this.current); }
  listProviders() { return ['openai','openrouter','anthropic','gemini','nvidia','glm','kimi','local','custom']; }
}
