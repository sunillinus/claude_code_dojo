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
- **start [query]** - Begin learning, or jump to a module/challenge by name or ID (e.g., `start plugin`, `start 16-001`, `start debugging`)
- **hint** - Get a hint for the current challenge (costs XP)
- **check** - Verify if current challenge objectives are complete
- **skip** - Skip the current challenge (no XP awarded)
- **progress** - Display your stats, XP, level, and streak
- **dashboard** - Open the web dashboard for visual progress
- **details <id|module>** - Preview a challenge or module without starting it
- **list [module]** - List available challenges, optionally filtered by module
- **quiz [module]** - Take a quiz to test your Claude Code knowledge
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
  /dojo hint              Get a hint for current challenge (costs XP)
  /dojo check             Verify if objectives are complete
  /dojo skip              Skip current challenge (no XP awarded)
  /dojo progress          Display your stats, XP, level, and streak
  /dojo details <id>      Preview a challenge (teaches, exercise, objectives)
  /dojo details <module>  Preview a module overview
  /dojo dashboard         Open the visual web dashboard
  /dojo list [module]     List challenges (optionally by module)
  /dojo quiz              Diagnostic quiz (15 questions, 1 per module)
  /dojo quiz <module>     Module quiz (5 questions for one topic)
  /dojo reset             Reset all progress (requires confirmation)

QUICK START
───────────
  1. Run /dojo start to begin your first challenge
  2. Read the objectives and complete them naturally
  3. Run /dojo check when you think you're done
  4. Earn XP, level up, and explore any module!

MODULES (71 challenges across 16 modules)
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
  💬 Prompting         (5)   Effective communication
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

QUIZ MODE
─────────
  Take quizzes to test your Claude Code knowledge!
  • /dojo quiz         Full diagnostic (1 question per module)
  • /dojo quiz <name>  Deep dive into one module (5 questions)
  Score 100% on a module quiz to earn the Quiz Ace badge!

TIPS
────
  • Complete challenges without hints for bonus XP (+25%)
  • Maintain a daily streak for streak bonuses (up to +25%)
  • Use /dojo dashboard for a visual progress view
  • Run /dojo quiz to find which modules to study
```

### /dojo start [query]

If no query is provided:
1. Read progress.json to check for active challenge in session.json
2. If active challenge exists: remind user of objectives and current progress
3. If no active challenge: find next uncompleted challenge and offer to start it
4. If all challenges complete: celebrate and show final stats!

If a query IS provided (e.g., `/dojo start plugin`, `/dojo start debugging`, `/dojo start 16-001`):
1. Read index.json to find a match. Try matching in this order:
   a. Exact challenge ID (e.g., "16-001")
   b. Module ID (e.g., "plugin-development", "debugging")
   c. Fuzzy match on module name (e.g., "plugin" matches "Plugin Development", "git" matches "Git Basics")
   d. Fuzzy match on challenge title (e.g., "first skill" matches "Create Your First Skill")
2. If a **module** is matched: start the first uncompleted challenge in that module. If all are completed, show the module as done and suggest another.
3. If a **challenge** is matched: load and start that challenge using the steps below.
4. If no match: show a helpful message listing available modules and suggest close matches.

**Starting a challenge** (used whenever a specific challenge is identified — by ID, module match, or next-uncompleted):
1. Load challenge from challenges/<module>/<id>.json
2. Create/update session.json with challenge state
3. Set up workspace directory as specified in challenge setup
4. Display challenge title, description, and objectives
5. Show estimated time and XP reward
6. If the challenge has a recommended prerequisite that hasn't been completed, show a brief note like: "💡 Tip: This builds on [prerequisite module]. You can still proceed, but that module may help." Always allow the user to proceed regardless.

### /dojo details <id | module>

Preview a challenge or module without starting it. Shows what the lesson teaches, what the exercise involves, and what objectives must be met. No workspace setup, no session state changes — purely informational.

**If argument matches a challenge ID (e.g., "13-002"):**

1. Load challenge JSON from challenges/<module>/<id>.json (use index.json to find the module directory — the challenge ID prefix maps to the directory number, e.g. "13-002" → "13-agentic-loops/002-*.json")
2. Display a header box:
```
╔══════════════════════════════════════════════════════════════════╗
║  13-002: Crafting Completion Promises                            ║
║  Module: Agentic Loops  •  Intermediate  •  225 XP  •  ~15 min  ║
╚══════════════════════════════════════════════════════════════════╝
```
3. **TEACHES section**: Read the challenge's `description` field. Extract the teaching content (everything before the exercise/task section, typically before "## Your Exercise" or "## Your Task" or similar). Summarize as 3-6 bullet points covering the key concepts taught.
```
TEACHES
───────
  - Bullet point summarizing key concept 1
  - Bullet point summarizing key concept 2
  ...
```
4. **EXERCISE section**: Extract the exercise/task portion from the description (typically after "## Your Exercise" or "## Your Task"). Summarize the concrete task in 2-4 sentences. If the exercise lists specific items (TODOs, files to create, steps), list them.
```
EXERCISE
────────
  Concise summary of what the user needs to do...

  Specific items if applicable:
  - item 1
  - item 2
```
5. **OBJECTIVES section**: List all required objective descriptions from the `objectives` array. Show the count.
```
OBJECTIVES (N required)
───────────────────────
  - objective description 1
  - objective description 2
```
6. **BONUS section**: List bonus objective descriptions with total bonus XP from `bonusObjectives` array. Omit this section entirely if there are no bonus objectives.
```
BONUS (+XX XP)
──────────────
  - bonus objective description 1
  - bonus objective description 2
```
7. **SKILLS line**: Show the `skills` array as comma-separated tags.
```
SKILLS: skill-1, skill-2, skill-3
```
8. **Footer**: `Run /dojo start <id> to start!`

**If argument matches a module name (fuzzy match, same logic as /dojo start):**

1. Load index.json, find matching module using fuzzy matching (e.g., "agentic" matches "Agentic Loops (Ralph Loop)", "plugin" matches "Plugin Development")
2. Read ~/.claude/dojo/progress.json for completion status
3. Display a header box:
```
╔══════════════════════════════════════════════════════════════════╗
║  AGENTIC LOOPS (Ralph Loop)                                      ║
║  4 challenges  •  0/4 completed  •  1,050 total XP               ║
╚══════════════════════════════════════════════════════════════════╝
```
4. List all challenges in the module with: ID, title, difficulty, XP. Mark completed challenges with ✅.
```
  13-001  Your First Ralph Loop           Intermediate  200 XP
  13-002  Crafting Completion Promises     Intermediate  225 XP  ✅
  13-003  Multi-Phase Loops               Advanced      275 XP
  13-004  Complex Iterative Task          Advanced      350 XP
```
5. Footer: `Run /dojo details <first-incomplete-challenge-id> for challenge details.`

**If argument matches neither:** Show a helpful error message listing available modules and suggest close matches.

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
║  ✅ Challenges: 12 / 71              ║
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

### /dojo quiz [module]

The quiz system tests Claude Code knowledge with multiple-choice questions.

**Two modes:**
- **Diagnostic** (`/dojo quiz` with no argument): 15 questions, 1 randomly selected from each module (git-basics excluded). Identifies strengths and weaknesses across all Claude Code topics.
- **Module quiz** (`/dojo quiz <module>`): 5 questions for a specific module. Deeper assessment. Supports fuzzy module name matching (same logic as `/dojo start`).

**Steps:**

1. **Load questions**: Read `quizzes/questions.json` from the plugin root directory (use `${CLAUDE_PLUGIN_ROOT}/quizzes/questions.json` or the relative path from the dojo project).

2. **Select questions**:
   - Diagnostic mode: Pick 1 random question from each of the 15 modules (all modules except git-basics).
   - Module mode: Use all 5 questions for the matched module.

3. **Present questions** as formatted text:

For diagnostic mode:
```
╔══════════════════════════════════════════════════════════╗
║              CLAUDE CODE DOJO - DIAGNOSTIC QUIZ          ║
║           Test your Claude Code knowledge!                ║
╠══════════════════════════════════════════════════════════╣

Q1. [Fundamentals] What tool does Claude Code use to create
    new files?
    A) Edit tool
    B) Write tool
    C) Bash echo command
    D) Create tool
    E) Touch tool

Q2. [Search & Nav] Which tool finds files by name patterns?
    A) Grep tool
    B) Bash find command
    C) Glob tool
    D) Read tool
    E) Search tool

... (15 questions total)

╚══════════════════════════════════════════════════════════╝

Type your answers as a single string (e.g., "BCADEBCADEBCADEB"):
```

For module mode:
```
╔══════════════════════════════════════════════════════════╗
║         CLAUDE CODE DOJO - MODULE QUIZ                   ║
║         Topic: Fundamentals                               ║
╠══════════════════════════════════════════════════════════╣

Q1. What tool does Claude Code use to create new files?
    A) Edit tool
    B) Write tool
    C) Bash echo command
    D) Create tool
    E) Touch tool

... (5 questions total)

╚══════════════════════════════════════════════════════════╝

Type your answers as a single string (e.g., "BCADE"):
```

4. **Wait for user response**: The user types a compact answer string like "BACDEBACDEBACDE" (one letter per question, A-E). Accept both upper and lower case.

5. **Grade the quiz**: Compare each answer letter to the correct answer from the question data. Track which questions were correct/incorrect.

6. **Display results**:

For diagnostic mode:
```
╔══════════════════════════════════════════════════════════╗
║                    QUIZ RESULTS                          ║
╠══════════════════════════════════════════════════════════╣
║  Score: 10/15 (67%)                                      ║
╠══════════════════════════════════════════════════════════╣

MODULE RESULTS:
  ✅ Fundamentals          ✅ Search & Nav
  ❌ Code Editing          ✅ Debugging
  ✅ Testing & TDD         ❌ Project Config
  ✅ Prompting             ✅ Code Generation
  ✅ Web Research          ❌ Subagents
  ✅ Background Tasks      ❌ Agentic Loops
  ✅ Skills & Hooks        ❌ MCP Integration
  ✅ Plugin Dev

WRONG ANSWERS:
  Q3. [Code Editing] You answered A, correct is C
      → The Edit tool uses old_string/new_string replacement,
        not line numbers. It requires reading the file first.
  ... (show explanation for each wrong answer)

RECOMMENDED MODULES:
  Start with these to fill knowledge gaps:
  1. Code Editing (Module 04)
  2. Project Config (Module 10)
  ... (list all failed modules with their module directory numbers)
```

For module mode:
```
╔══════════════════════════════════════════════════════════╗
║                    QUIZ RESULTS                          ║
║              Module: Fundamentals                        ║
╠══════════════════════════════════════════════════════════╣
║  Score: 4/5 (80%)                                        ║
╠══════════════════════════════════════════════════════════╣

  Q1. ✅  Q2. ✅  Q3. ❌  Q4. ✅  Q5. ✅

WRONG ANSWERS:
  Q3. You answered A, correct is C
      → [explanation from question data]

XP EARNED: +30 XP
```

7. **Before/after comparison**: Read progress.json for previous quiz attempts. If a previous attempt exists for the same quiz type, show improvement:
```
IMPROVEMENT: 10/15 → 13/15 (+3) since your last attempt!
```
Or if score decreased:
```
Previous score: 13/15 → Current: 10/15 (-3). Keep studying!
```

8. **Save results to progress.json**: Add results under the `quizzes` key.

For diagnostic quiz, append to `quizzes.diagnostic` array:
```json
{
  "takenAt": "<ISO timestamp>",
  "answers": { "fundamentals": "B", "search-navigation": "C", ... },
  "scores": { "fundamentals": true, "search-navigation": true, ... },
  "totalCorrect": 10,
  "totalQuestions": 15,
  "questionsUsed": { "fundamentals": "fund-2", "search-navigation": "search-4", ... }
}
```

For module quiz, append to `quizzes.modules.<moduleId>` array:
```json
{
  "takenAt": "<ISO timestamp>",
  "correct": 4,
  "total": 5,
  "answers": ["B", "C", "A", "D", "B"],
  "results": [true, true, false, true, true]
}
```

Initialize `quizzes` key if it doesn't exist: `{ "diagnostic": [], "modules": {} }`.

9. **XP for module quizzes** (diagnostic quizzes award no XP):
   - 5/5 correct: +50 XP
   - 4/5 correct: +30 XP
   - 3/5 correct: +15 XP
   - Below 3/5: No XP (encourage studying)

   Apply XP using the same level progression formula as challenges. Update xp.total, recalculate level and toNextLevel.

10. **Badge: quiz-ace**: If a module quiz scores 5/5 (100%), check if the user already has the `quiz-ace` badge. If not, award it and announce:
```
🏆 NEW BADGE: Quiz Ace - Score 100% on a module quiz!
```

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
    "effective-prompting": { "completed": 0, "total": 5 },
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
  "quizzes": {
    "diagnostic": [],
    "modules": {}
  },
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
