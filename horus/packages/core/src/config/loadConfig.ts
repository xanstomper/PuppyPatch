import fs from 'node:fs';
import { HorusConfigSchema, defaultConfig, type HorusConfig } from './schema.js';

export function loadConfig(path = 'horus.config.json'): HorusConfig {
  if (!fs.existsSync(path)) return defaultConfig;
  const raw = JSON.parse(fs.readFileSync(path, 'utf8'));
  return HorusConfigSchema.parse({ ...defaultConfig, ...raw });
}
export function saveConfig(config: HorusConfig, path = 'horus.config.json') {
  fs.writeFileSync(path, JSON.stringify(config, null, 2));
}
