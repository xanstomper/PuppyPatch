import type { ModelRef } from '../router.js';

export type ModelProvider = { name: string; baseUrl: string; apiKeyEnv: string; model: string; status(): ProviderStatus; call(prompt: string): Promise<string> };
export type ProviderStatus = { mode: 'mock'|'real'; provider: string; model: string; ready: boolean; warning?: string };

export class OpenAICompatibleProvider implements ModelProvider {
  constructor(public name: string, public baseUrl: string, public apiKeyEnv: string, public model: string) {}
  status(): ProviderStatus {
    if (process.env.HORUS_MOCK_MODEL !== '0') return { mode: 'mock', provider: this.name, model: this.model, ready: true };
    const key = process.env[this.apiKeyEnv];
    if (!key) return { mode: 'mock', provider: this.name, model: this.model, ready: true, warning: `Missing ${this.apiKeyEnv}; falling back to mock model` };
    if (!this.baseUrl) return { mode: 'mock', provider: this.name, model: this.model, ready: true, warning: `Missing base URL for ${this.name}; falling back to mock model` };
    return { mode: 'real', provider: this.name, model: this.model, ready: true };
  }
  async call(prompt: string) {
    const status = this.status();
    if (status.mode === 'mock') {
      return `${status.warning ? `Warning: ${status.warning}\n` : ''}Mock model response:\n- received task: ${prompt.slice(0, 160)}\n- inspect repository\n- use safe tools\n- checkpoint before edits\n- verify when command is detected\n- report results`;
    }
    const key = process.env[this.apiKeyEnv]!;
    const res = await fetch(`${this.baseUrl.replace(/\/$/,'')}/chat/completions`, { method: 'POST', headers: { 'content-type': 'application/json', authorization: `Bearer ${key}` }, body: JSON.stringify({ model: this.model, messages: [{ role: 'user', content: prompt }] }) });
    if (!res.ok) return `Warning: provider call failed (${res.status}); falling back to mock model\nMock model response:\n- inspect repository\n- use safe tools\n- report results`;
    const json: any = await res.json();
    return json.choices?.[0]?.message?.content ?? '';
  }
}
export function providerFromRef(ref: ModelRef) { const base: Record<string,string> = { openai: 'https://api.openai.com/v1', openrouter: 'https://openrouter.ai/api/v1', local: 'http://127.0.0.1:11434/v1' }; const env: Record<string,string> = { openai: 'OPENAI_API_KEY', openrouter: 'OPENROUTER_API_KEY', local: 'LOCAL_API_KEY' }; return new OpenAICompatibleProvider(ref.provider, process.env[`HORUS_${ref.provider.toUpperCase()}_BASE_URL`] ?? base[ref.provider] ?? '', env[ref.provider] ?? `${ref.provider.toUpperCase()}_API_KEY`, ref.model); }
