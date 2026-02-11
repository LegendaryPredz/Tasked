# Tasked

A simple command-line task manager that keeps your to-do list organized right from your terminal. No accounts, no cloud sync, no bloat — just your tasks stored locally on your machine.

---

## Installation

```bash
pip install git+https://github.com/LegendaryPredz/Tasked.git
```

> Requires **Python 3.13+**

---

## Quick Start

```bash
# Set up your task list
tasked init

# Add some tasks
tasked add "Buy groceries"
tasked add "Finish report"

# See what's on your plate
tasked list
```

```
┏━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Description      ┃ Status ┃ Date Created         ┃ Date Updated         ┃
┡━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ 1  │ Buy groceries    │ Todo   │ 10-02-2026 11:46 PM  │ 10-02-2026 11:46 PM  │
│ 2  │ Finish report    │ Todo   │ 10-02-2026 11:47 PM  │ 10-02-2026 11:47 PM  │
└────┴─────────────────┴────────┴──────────────────────┴──────────────────────┘
```

---

## Usage

### Adding tasks

```bash
tasked add "Walk the dog"
```

### Viewing tasks

```bash
# Show all tasks
tasked list

# Show only tasks with a specific status
tasked list --status Todo
tasked list --status "In Progress"
tasked list --status Done
```

### Updating tasks

Change the description, status, or both:

```bash
tasked update 1 --description "Buy groceries and snacks"
tasked update 1 --status "In Progress"
tasked update 1 -d "Buy groceries and snacks" -s Done
```

### Marking progress

```bash
# Mark a single task as in progress
tasked mark-in-progress 2

# Mark all tasks as in progress
tasked mark-in-progress all
```

### Completing tasks

```bash
# Mark a single task as done
tasked mark-complete 1

# Mark all tasks as done
tasked mark-complete all
```

### Deleting tasks

```bash
# Delete a specific task
tasked delete 3

# Delete all tasks
tasked delete all
```

### Custom storage location

By default, tasks are stored at `~/.todo/todo.json`. You can point to a different file:

```bash
tasked --db ./work-tasks.json list
tasked --db ./work-tasks.json add "Prepare slides"
```

---

## Command Reference

| Command | What it does |
|---------|-------------|
| `tasked init` | Create a fresh task list |
| `tasked add "..."` | Add a new task |
| `tasked list` | Show all tasks (use `--status` to filter) |
| `tasked update ID` | Change a task's description (`-d`) or status (`-s`) |
| `tasked mark-in-progress ID\|all` | Set tasks to "In Progress" |
| `tasked mark-complete ID\|all` | Set tasks to "Done" |
| `tasked delete ID\|all` | Remove tasks |

Run `tasked --help` for full details on any command.

---

## Tips

- **Status values** are `Todo`, `In Progress`, and `Done` (case-sensitive).
- **`init` resets your task list** — it will overwrite any existing tasks, so use it only when starting fresh.
- **Task IDs** are assigned automatically and increment from the highest existing ID.

---

## License

MIT
