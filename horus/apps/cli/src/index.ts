#!/usr/bin/env node
import React from 'react';
import { render } from 'ink';
import { Command } from 'commander';
import { HorusApp } from './tui/App.js';
import { loadConfig, saveConfig } from '@horus/core';
import { ModelRouter } from '@horus/models';

const program = new Command();
program.name('horus').description('Horus Core MVP terminal coding agent').version('0.3.0');
const launch = () => { render(React.createElement(HorusApp)); };
program.action(launch);
program.command('tui').description('Launch Horus React Ink TUI').action(launch);
program.command('doctor').description('Validate environment').action(() => { const cfg = loadConfig(); console.log('Horus doctor OK'); console.log(`model=${cfg.model}`); console.log(`node=${process.version}`); });
const model = program.command('model');
model.command('list').action(() => console.table(new ModelRouter(loadConfig().model).listProviders().map(provider => ({ provider }))));
model.command('set').argument('<model>').action((model) => { const cfg = loadConfig(); cfg.model = model; saveConfig(cfg); console.log(`model set: ${model}`); });
program.parse();
