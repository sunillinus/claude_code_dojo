# Claude Code Dojo

Learn Claude Code through hands-on challenges with progress tracking and gamification.

## Installation

```bash
cd /Users/sunil/vibe_code/claude_code_dojo
claude plugins add . --scope user
```

## Usage

Start Claude Code and use the `/dojo` command:

```bash
claude

> /dojo                    # Show available commands
> /dojo start              # Begin or continue learning
> /dojo challenge 01-001   # Start a specific challenge
> /dojo hint               # Get a hint (costs XP)
> /dojo check              # Verify completion
> /dojo progress           # Show your stats
> /dojo dashboard          # Open web dashboard
```

## Curriculum

### Phase 1: Core Coding Skills

| # | Module | Challenges | Description |
|---|--------|------------|-------------|
| 1 | Fundamentals | 5 | File creation, reading, editing |
| 2 | Search & Navigation | 5 | Finding files and code |
| 3 | Git Basics | 5 | Version control essentials |
| 4 | Code Editing | 5 | Refactoring and modifications |
| 5 | Debugging | 4 | Finding and fixing bugs |
| 6 | Testing & TDD | 5 | Write tests, TDD, coverage |

### Phase 2: Optimize Your Workflow

| # | Module | Challenges | Description |
|---|--------|------------|-------------|
| 7 | Project Configuration | 5 | CLAUDE.md and settings |
| 8 | Effective Prompting | 4 | Better communication with Claude |
| 9 | Code Generation | 4 | Scaffolding and generation |
| 10 | Web Research | 4 | Docs, search, API research |

### Phase 3: Advanced Execution

| # | Module | Challenges | Description |
|---|--------|------------|-------------|
| 11 | Subagents | 4 | Specialized agent delegation |
| 12 | Background Tasks | 4 | Parallel and async execution |
| 13 | Agentic Loops | 4 | Ralph Loop for autonomous work |

### Phase 4: Build Your Own Tools

| # | Module | Challenges | Description |
|---|--------|------------|-------------|
| 14 | Skills & Hooks | 4 | Custom commands and automation |
| 15 | MCP Integration | 3 | External tool connections |
| 16 | Plugin Development | 5 | Build and publish plugins |

**Total: 16 modules, 70 challenges**

## Gamification

- **XP System**: Earn XP for completing challenges
- **Levels**: Progress through levels as you gain XP
- **Streaks**: Maintain daily streaks for bonus XP
- **Badges**: Unlock achievements for milestones
- **Skill Tree**: Track mastery of different skill areas

## Progress Storage

Progress is stored in `~/.claude/dojo/`:
- `progress.json` - Overall progress and stats
- `session.json` - Current challenge state

## Development

### Directory Structure

```
claude_code_dojo/
├── .claude-plugin/plugin.json   # Plugin manifest
├── skills/dojo/SKILL.md         # Main skill
├── agents/dojo-validator.md     # Validation subagent
├── hooks/track-progress.py      # Progress tracking hook
├── challenges/                  # Challenge definitions
├── dashboard/                   # Web dashboard
└── scripts/                     # Utility scripts
```

### Adding Challenges

1. Create JSON file in `challenges/<module>/<id>.json`
2. Add entry to `challenges/index.json`
3. Follow the challenge schema (see existing challenges)

## License

MIT
