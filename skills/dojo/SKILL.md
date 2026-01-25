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
- **start** - Begin or continue your learning journey
- **challenge <id>** - Start a specific challenge (e.g., `challenge 01-001`)
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
  /dojo start             Begin or continue your learning journey
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
  4. Earn XP, level up, and unlock new modules!

MODULES (70 challenges across 16 modules)
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

### /dojo start

1. Read progress.json to check for active challenge in session.json
2. If active challenge exists: remind user of objectives and current progress
3. If no active challenge: find next uncompleted challenge and offer to start it
4. If all challenges complete: celebrate and show final stats!

### /dojo challenge <id>

1. Load challenge from challenges/<module>/<id>.json
2. Create/update session.json with challenge state
3. Set up workspace directory as specified in challenge setup
4. Display challenge title, description, and objectives
5. Show estimated time and XP reward

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
  🔒 Git Basics        [0/5] ░░░░░░░░░░░░
```

### /dojo list [module]

Show challenges with status indicators:
- ✅ Completed
- 🔄 In Progress
- ⭕ Available
- 🔒 Locked

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
    "fundamentals": { "completed": 0, "total": 5, "unlocked": true },
    "search-navigation": { "completed": 0, "total": 5, "unlocked": true },
    "git-basics": { "completed": 0, "total": 5, "unlocked": false },
    "code-editing": { "completed": 0, "total": 5, "unlocked": false },
    "debugging": { "completed": 0, "total": 4, "unlocked": false },
    "testing-tdd": { "completed": 0, "total": 5, "unlocked": false },
    "project-config": { "completed": 0, "total": 5, "unlocked": false },
    "effective-prompting": { "completed": 0, "total": 4, "unlocked": false },
    "code-generation": { "completed": 0, "total": 4, "unlocked": false },
    "web-research": { "completed": 0, "total": 4, "unlocked": false },
    "subagents": { "completed": 0, "total": 4, "unlocked": false },
    "background-tasks": { "completed": 0, "total": 4, "unlocked": false },
    "agentic-loops": { "completed": 0, "total": 4, "unlocked": false },
    "skills-hooks": { "completed": 0, "total": 4, "unlocked": false },
    "mcp-integration": { "completed": 0, "total": 3, "unlocked": false },
    "plugin-development": { "completed": 0, "total": 5, "unlocked": false }
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

## Module Unlocking

Phase 1 - Core Skills:
- Fundamentals: Always unlocked
- Search & Navigation: Always unlocked
- Git Basics: Complete 3 challenges from Fundamentals
- Code Editing: Complete Git Basics module
- Debugging: Complete Code Editing module
- Testing & TDD: Complete Debugging module

Phase 2 - Optimize Workflow:
- Project Config: Complete Testing & TDD module
- Effective Prompting: Complete Project Config module
- Code Generation: Complete Effective Prompting module
- Web Research: Complete Code Generation module

Phase 3 - Advanced Execution:
- Subagents: Complete Web Research module
- Background Tasks: Complete Subagents module
- Agentic Loops: Complete Background Tasks module

Phase 4 - Build Tools:
- Skills & Hooks: Complete Agentic Loops module
- MCP Integration: Complete Skills & Hooks module
- Plugin Development: Complete Skills & Hooks module

## Important

- Always read the challenge JSON files to understand objectives
- Use the dojo-validator subagent for checking completion
- Keep progress.json and session.json up to date
- Be encouraging and celebrate achievements!
- If user seems stuck, gently suggest using hints
