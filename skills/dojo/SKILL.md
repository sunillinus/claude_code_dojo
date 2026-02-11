---
name: dojo
description: Claude Code Dojo - Learn Claude Code through hands-on challenges. Use when the user says /dojo or wants to practice Claude Code skills.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
---

# Claude Code Dojo

An interactive learning system for mastering Claude Code through progressive challenges.

## Commands

Parse the user's input to determine which command they want:

- **help** - Show this help guide and available commands
- **start [query]** - Begin learning, or jump to a module/challenge by name or ID (e.g., `start plugin`, `start 09-001`, `start debugging`)
- **challenge <id>** - Start a specific challenge by ID (e.g., `challenge 01-001`)
- **hint** - Get a hint for the current challenge (costs XP)
- **check** - Verify if current challenge objectives are complete
- **skip** - Skip the current challenge (no XP awarded)
- **progress** - Display your stats, XP, level, and streak
- **dashboard** - Open the web dashboard for visual progress
- **list [module]** - List available challenges, optionally filtered by module
- **reset** - Reset all progress (requires confirmation)

## Session State

Read these files to understand current state:

1. **~/.claude/dojo/progress.json** - Overall progress (XP, level, completed challenges, badges)
2. **~/.claude/dojo/session.json** - Active challenge state (current challenge, hints used, actions)

If these files don't exist, initialize them with default values.

## Command Implementations

### /dojo help

Display the following help guide:

```
╔══════════════════════════════════════════════════════════════════╗
║                    🥋 CLAUDE CODE DOJO                           ║
║         Learn Claude Code through hands-on challenges            ║
╚══════════════════════════════════════════════════════════════════╝

COMMANDS
────────
  /dojo help              Show this help guide
  /dojo start [query]     Begin learning, or jump by name/ID
  /dojo challenge <id>    Start a specific challenge (e.g., 01-001)
  /dojo hint              Get a hint for current challenge (costs XP)
  /dojo check             Verify if objectives are complete
  /dojo skip              Skip current challenge (no XP awarded)
  /dojo progress          Display your stats, XP, level, and streak
  /dojo dashboard         Open the visual web dashboard
  /dojo list [module]     List challenges (optionally by module)
  /dojo reset             Reset all progress (requires confirmation)

QUICK START
───────────
  1. Run /dojo start to begin your first challenge
  2. Read the objectives and complete them naturally
  3. Run /dojo check when you think you're done
  4. Earn XP, level up, and explore any module!

MODULES (70 challenges across 16 modules)
  All modules are open - jump to whatever interests you!
  Recommended order shown, but not required.
─────────────────────────────────────────
  Phase 1: Core Skills
  📁 Fundamentals      (5)   File operations basics
  🔍 Search & Nav      (5)   Finding files and code
  📚 Git Basics        (5)   Version control essentials
  ✏️ Code Editing      (5)   Refactoring and editing
  🐛 Debugging         (4)   Finding and fixing bugs
  🧪 Testing & TDD     (5)   Write tests, TDD, coverage

  Phase 2: Optimize Workflow
  ⚙️ Project Config    (5)   CLAUDE.md and settings
  💬 Prompting         (4)   Effective communication
  🏗️ Code Generation   (4)   Scaffolding and generation
  🌐 Web Research      (4)   Docs, search, APIs

  Phase 3: Advanced Execution
  🤖 Subagents         (4)   Specialized agents
  ⏳ Background Tasks  (4)   Parallel execution
  🔄 Agentic Loops     (4)   Ralph Loop autonomy

  Phase 4: Build Tools
  🪝 Skills & Hooks    (4)   Custom commands
  🔌 MCP Integration   (3)   External tools
  📦 Plugin Dev        (5)   Build plugins

TIPS
────
  • Complete challenges without hints for bonus XP (+25%)
  • Maintain a daily streak for streak bonuses (up to +25%)
  • Use /dojo dashboard for a visual progress view
```

### /dojo start [query]

If no query is provided:
1. Read progress.json to check for active challenge in session.json
2. If active challenge exists: remind user of objectives and current progress
3. If no active challenge: find next uncompleted challenge and offer to start it
4. If all challenges complete: celebrate and show final stats!

If a query IS provided (e.g., `/dojo start plugin`, `/dojo start debugging`, `/dojo start 09-001`):
1. Read index.json to find a match. Try matching in this order:
   a. Exact challenge ID (e.g., "09-001")
   b. Module ID (e.g., "plugin-development", "debugging")
   c. Fuzzy match on module name (e.g., "plugin" matches "Plugin Development", "git" matches "Git Basics")
   d. Fuzzy match on challenge title (e.g., "first skill" matches "Create Your First Skill")
2. If a **module** is matched: start the first uncompleted challenge in that module. If all are completed, show the module as done and suggest another.
3. If a **challenge** is matched: load and start that specific challenge (same as `/dojo challenge <id>`).
4. If no match: show a helpful message listing available modules and suggest close matches.

### /dojo challenge <id>

1. Load challenge from challenges/<module>/<id>.json
2. Create/update session.json with challenge state
3. Set up workspace directory as specified in challenge setup
4. Display challenge title, description, and objectives
5. Show estimated time and XP reward
6. If the challenge has a recommended prerequisite that hasn't been completed, show a brief note like: "💡 Tip: This builds on [prerequisite module]. You can still proceed, but that module may help." Always allow the user to proceed regardless.

### /dojo hint

1. Check session.json for current challenge
2. Get next unused hint level (1, 2, or 3)
3. Deduct hint XP cost from potential reward
4. Display hint and update session.json

### /dojo check

1. Use the dojo-validator subagent to check objectives
2. Parse validation results
3. If all required objectives pass:
   - Calculate XP (base + bonuses - hint penalties)
   - Update progress.json
   - Mark challenge complete
   - Check for newly earned badges
   - Offer next challenge
4. If not complete: show which objectives are pending

### /dojo progress

Display formatted stats:
```
╔══════════════════════════════════════╗
║         CLAUDE CODE DOJO             ║
╠══════════════════════════════════════╣
║  Level: 5        XP: 1,250 / 1,500   ║
║  ████████░░░░░░░░░░░░  83%           ║
╠══════════════════════════════════════╣
║  🔥 Streak: 3 days                   ║
║  ✅ Challenges: 12 / 70              ║
║  🏆 Badges: 4                        ║
╚══════════════════════════════════════╝

Modules:
  ✅ Fundamentals      [5/5] ████████████
  🔄 Search & Nav      [2/5] ████░░░░░░░░
  ⭕ Git Basics        [0/5] ░░░░░░░░░░░░
```

### /dojo list [module]

Show challenges with status indicators:
- ✅ Completed
- 🔄 In Progress
- ⭕ Available
- 💡 Available (has recommended prerequisites not yet completed - show which module is recommended)

### /dojo dashboard

1. Run: `python3 scripts/serve-dashboard.py`
2. Open browser to http://localhost:3847
3. Dashboard reads progress.json and displays visual stats

## Progress Schema

When initializing progress.json:

```json
{
  "userId": "local",
  "startedAt": "<current ISO timestamp>",
  "lastActiveAt": "<current ISO timestamp>",
  "xp": {
    "total": 0,
    "level": 1,
    "toNextLevel": 100
  },
  "streak": {
    "current": 0,
    "longest": 0,
    "lastActiveDate": null
  },
  "challenges": {},
  "modules": {
    "fundamentals": { "completed": 0, "total": 5 },
    "search-navigation": { "completed": 0, "total": 5 },
    "git-basics": { "completed": 0, "total": 5 },
    "code-editing": { "completed": 0, "total": 5 },
    "debugging": { "completed": 0, "total": 4 },
    "testing-tdd": { "completed": 0, "total": 5 },
    "project-config": { "completed": 0, "total": 5 },
    "effective-prompting": { "completed": 0, "total": 4 },
    "code-generation": { "completed": 0, "total": 4 },
    "web-research": { "completed": 0, "total": 4 },
    "subagents": { "completed": 0, "total": 4 },
    "background-tasks": { "completed": 0, "total": 4 },
    "agentic-loops": { "completed": 0, "total": 4 },
    "skills-hooks": { "completed": 0, "total": 4 },
    "mcp-integration": { "completed": 0, "total": 3 },
    "plugin-development": { "completed": 0, "total": 5 }
  },
  "skills": {},
  "badges": [],
  "stats": {
    "totalChallengesCompleted": 0,
    "totalTimeSpent": 0,
    "hintsUsedTotal": 0
  }
}
```

## XP Calculation

Base XP by difficulty:
- Beginner: 100 XP
- Intermediate: 200 XP
- Advanced: 350 XP
- Expert: 500 XP

Bonuses:
- No hints used: +25%
- Speed bonus (under half estimated time): +15%
- Streak bonus: +5% per day (max +25%)

Penalties:
- Hint level 1: -10 XP
- Hint level 2: -25 XP
- Hint level 3: -50 XP

## Level Progression

XP required for each level: `100 * level^1.5`

Level 1: 100 XP
Level 2: 283 XP
Level 3: 520 XP
Level 5: 1,118 XP
Level 10: 3,162 XP

## Module Prerequisites (Soft - Recommended, Not Required)

All modules are always available. The recommended order below helps build skills progressively, but users can jump to any module that interests them. When a user starts a challenge whose recommended prerequisite isn't complete, show a brief tip but always allow them to proceed.

Phase 1 - Core Skills:
- Fundamentals: No prerequisites
- Search & Navigation: No prerequisites
- Git Basics: Recommended after Fundamentals
- Code Editing: Recommended after Git Basics
- Debugging: Recommended after Code Editing
- Testing & TDD: Recommended after Debugging

Phase 2 - Optimize Workflow:
- Project Config: Recommended after Testing & TDD
- Effective Prompting: Recommended after Project Config
- Code Generation: Recommended after Effective Prompting
- Web Research: Recommended after Code Generation

Phase 3 - Advanced Execution:
- Subagents: Recommended after Web Research
- Background Tasks: Recommended after Subagents
- Agentic Loops: Recommended after Background Tasks

Phase 4 - Build Tools:
- Skills & Hooks: Recommended after Agentic Loops
- MCP Integration: Recommended after Skills & Hooks
- Plugin Development: Recommended after Skills & Hooks

## Important

- Always read the challenge JSON files to understand objectives
- Use the dojo-validator subagent for checking completion
- Keep progress.json and session.json up to date
- Be encouraging and celebrate achievements!
- If user seems stuck, gently suggest using hints
