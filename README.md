# Tasked

A lightweight, JSON-backed command-line task manager built with Python, [Typer](https://typer.tiangolo.com/), and [Rich](https://rich.readthedocs.io/).

Tasked stores your todos locally in a simple JSON file and provides a clean CLI for managing them with timestamps, status tracking, and formatted table output.

> Project URL: https://roadmap.sh/projects/task-tracker

---

## Features

- **7 CLI commands** &mdash; init, add, list, update, delete, mark-in-progress, mark-complete
- **Status tracking** &mdash; Todo, In Progress, Done
- **Timestamps** &mdash; `createdAt` set on creation, `updatedAt` on every modification
- **Filtered listing** &mdash; filter todos by status
- **Bulk operations** &mdash; mark all or delete all in a single command
- **Rich table output** &mdash; formatted tables via the Rich library
- **JSON persistence** &mdash; human-readable storage, no database required
- **Configurable path** &mdash; override the default database location with `--db`

---

## Requirements

- **Python 3.13+**
- **[uv](https://docs.astral.sh/uv/)** (recommended) or pip

---

## Installation

### With uv (recommended)

```bash
git clone https://github.com/LegendaryPredz/tasked.git
cd tasked
uv sync
```

This creates a virtual environment and installs all dependencies from the lockfile.

### With pip

```bash
git clone https://github.com/LegendaryPredz/tasked.git
cd tasked
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

### With direnv

If you use [direnv](https://direnv.net/), the included `.envrc` will automatically set up the environment:

```bash
cd tasked
direnv allow
```

---

## Usage

After installation, the `tasked` command is available:

```bash
tasked --help
```

You can also run it directly as a script:

```bash
python tasked.py --help
```

### Database Location

By default, todos are stored at `~/.todo/todo.json`. Override with `--db`:

```bash
tasked --db ./my-todos.json list
```

---

## Commands

### `init` &mdash; Initialize the database

Creates an empty database file. Overwrites existing contents.

```bash
tasked init
# Initialized empty database: /Users/you/.todo/todo.json
```

### `add` &mdash; Add a new todo

```bash
tasked add "Buy groceries"
# Created todo #1: Buy groceries

tasked add "Finish firmware review"
# Created todo #2: Finish firmware review
```

### `list` &mdash; List todos

List all todos:

```bash
tasked list
```

Filter by status:

```bash
tasked list --status Todo
tasked list --status "In Progress"
tasked list --status Done
```

Output is a Rich table:

```
┏━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Description            ┃ Status      ┃ Date Created         ┃ Date Updated         ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ 1  │ Buy groceries          │ Todo        │ 10-02-2026 11:46 PM  │ 10-02-2026 11:46 PM  │
│ 2  │ Finish firmware review │ In Progress │ 10-02-2026 11:47 PM  │ 10-02-2026 11:48 PM  │
└────┴────────────────────────┴─────────────┴──────────────────────┴──────────────────────┘
```

### `update` &mdash; Update a todo

Update description, status, or both:

```bash
tasked update 1 --description "Buy groceries and snacks"
tasked update 1 --status "In Progress"
tasked update 1 -d "Buy groceries and snacks" -s Done
```

| Option | Short | Description |
|--------|-------|-------------|
| `--description` | `-d` | New description |
| `--status` | `-s` | New status (`Todo`, `In Progress`, `Done`) |

### `mark-in-progress` &mdash; Mark a todo as In Progress

```bash
tasked mark-in-progress 2
# 2: Finish firmware review Marked in-progress

tasked mark-in-progress all
# Marked all todos as In Progress.
```

### `mark-complete` &mdash; Mark a todo as Done

```bash
tasked mark-complete 2
# 2: Finish firmware review Marked complete!

tasked mark-complete all
# Marked all todos as Done.
```

### `delete` &mdash; Delete todos

Delete by ID:

```bash
tasked delete 3
# Removed todo #3: Some task
```

Delete all:

```bash
tasked delete all
# Removed 3 todo(s).
```

---

## Data Model

Each todo is stored as a JSON object:

```json
{
  "id": 1,
  "desc": "Buy groceries",
  "status": "Todo",
  "createdAt": "2026-02-10T23:46:23.827272",
  "updatedAt": "2026-02-10T23:46:23.827272"
}
```

The database file is a JSON array of these objects:

```json
[
  { "id": 1, "desc": "Buy groceries", "status": "Todo", "createdAt": "...", "updatedAt": "..." },
  { "id": 2, "desc": "Review code", "status": "In Progress", "createdAt": "...", "updatedAt": "..." }
]
```

### Status Values

Status values are **case-sensitive** and must match exactly:

| Value | Meaning |
|-------|---------|
| `Todo` | Not started (default for new todos) |
| `In Progress` | Currently being worked on |
| `Done` | Completed |

---

## Project Structure

```
tasked/
├── tasked.py           # Main application (single-file CLI)
├── pyproject.toml      # Project metadata, dependencies, and tooling config
├── uv.lock             # Locked dependency versions
├── .python-version     # Python 3.13
├── .envrc              # Direnv auto-setup
├── .gitignore          # Standard Python ignores
└── dist/               # Built distributions (wheel + sdist)
```

---

## Tech Stack

| Component | Tool |
|-----------|------|
| Language | Python 3.13 |
| CLI framework | [Typer](https://typer.tiangolo.com/) |
| Table formatting | [Rich](https://rich.readthedocs.io/) |
| Package manager | [uv](https://docs.astral.sh/uv/) |
| Linter | [Ruff](https://docs.astral.sh/ruff/) |
| Data storage | JSON |

---

## Notes

- `init` overwrites the database with an empty list &mdash; use with caution.
- The `--status` help text in `list` shows lowercase values, but the actual accepted values are capitalized: `Todo`, `In Progress`, `Done`.
- IDs are auto-incremented based on the highest existing ID.

---

## License

MIT
