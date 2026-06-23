import { defineConfig } from 'vitest/config';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
const root = dirname(fileURLToPath(import.meta.url));
export default defineConfig({
  resolve: { alias: {
    '@horus/shared': resolve(root, 'packages/shared/src/index.ts'),
    '@horus/core': resolve(root, 'packages/core/src/index.ts'),
    '@horus/models': resolve(root, 'packages/models/src/index.ts'),
    '@horus/tools': resolve(root, 'packages/tools/src/index.ts')
  }},
  test: { include: ['tests/**/*.test.ts'] }
});
