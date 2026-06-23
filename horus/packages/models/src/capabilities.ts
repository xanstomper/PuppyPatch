export type ModelCapabilities = { contextWindow: number; toolCalling: boolean; jsonMode: boolean; vision: boolean };
export function detectCapabilities(model: string): ModelCapabilities {
  const m = model.toLowerCase();
  return { contextWindow: m.includes('gemini') ? 1_000_000 : m.includes('claude') ? 200_000 : 128_000, toolCalling: true, jsonMode: true, vision: m.includes('vision') || m.includes('gpt-4o') || m.includes('gemini') };
}
