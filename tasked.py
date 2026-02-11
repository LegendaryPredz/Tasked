from __future__ import annotations

import json
from os.path import exists
import sys
from argparse import ArgumentParser
from pathlib import Path
import datetime as dt
import os
from enum import Enum
from dataclasses import dataclass

from click import Option
import typer
from rich.console import Console
from rich.table import Table

from typing import List, Dict, Annotated, Optional, Literal, NamedTuple, Any, TypeAlias, TypedDict, Union

app = typer.Typer()

console = Console()

now = dt.datetime.now()


class TaskStatus(str, Enum):
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


@dataclass()
class Todo:
    id: int
    desc: str
    status: TaskStatus
    createdAt: dt.datetime
    updatedAt: dt.datetime


Database: TypeAlias = List[Todo]

# 1. Create a JSON file
# 2. Create some data in the format of
# {
#   id: #,
#   description: "",
#   status: TaskStatus,
#   createdAt: datetime.now() only when created
#   updatedAt: datetime.now() when modified
# }


def todo_to_dict(t: Todo) -> dict:
    return {
        "id": t.id,
        "desc": t.desc,
        "status": t.status.value,
        "createdAt": t.createdAt.isoformat(),
        "updatedAt": t.updatedAt.isoformat(),
    }


def dict_to_todo(d: dict) -> Todo:
    return Todo(
        id=int(d["id"]),
        desc=str(d["desc"]),
        status=TaskStatus(d["status"]),
        createdAt=dt.datetime.fromisoformat(d["createdAt"]),
        updatedAt=dt.datetime.fromisoformat(d["updatedAt"]),
    )


# Load the database
def load_database(path: Path) -> Database:
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        if raw is None:
            return []
        if not isinstance(raw, List):
            raise ValueError("Database JSON must be a list/array of todos")
        return [dict_to_todo(item) for item in raw]
    except json.JSONDecodeError as e:
        raise typer.BadParameter(f"Invalid JSON in {path}: {e}") from e


def save_database(path: Path, db: Database) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump([todo_to_dict(t) for t in db], f, indent=2)
        f.write("\n")


def next_id(db: Database) -> int:
    return 1 if not db else max(t.id for t in db) + 1


# Create a database file
@app.command()
def init():
    """Create an empty database file (or overwrite to empty)."""
    assert STATE.db_path is not None
    STATE.db = []
    save_database(STATE.db_path, STATE.db)
    typer.echo(f"Initialized empty database: {STATE.db_path}")


# Add a todo to the database
@app.command()
def add(description: str):
    """Add a new todo."""
    assert STATE.db_path is not None
    now = dt.datetime.now()
    todo = Todo(
        id=next_id(STATE.db),
        desc=description,
        status=TaskStatus.TODO,
        createdAt=now,
        updatedAt=now,
    )

    STATE.db.append(todo)
    save_database(STATE.db_path, STATE.db)
    typer.echo(f"Created todo #{todo.id}: {todo.desc}")


# Delete a todo from the database
@app.command()
def delete(target: str):
    """Delete a todo by id or delete them all with 'all'"""
    assert STATE.db_path is not None

    if target == "all":
        count = len(STATE.db)
        STATE.db.clear()
        save_database(STATE.db_path, STATE.db)
        typer.echo(f"Revoved {count} todo(s).")
        return

    todo_id = int(target)
    removed = next((t for t in STATE.db if t.id == todo_id), None)
    if removed is None:
        typer.echo(f"No todo with id: {todo_id}")
        raise typer.Exit(code=1)

    STATE.db.remove(removed)
    save_database(STATE.db_path, STATE.db)
    typer.echo(f"Removed todo #{removed.id}: {removed.desc}")


@app.command()
def update(
    id: int,
    desc: Optional[str] = typer.Option(None, "--description", "-d", help="New Description for the task"),
    status: Optional[TaskStatus] = typer.Option(None, "--status", "-s", help="New Status for the task"),
):
    """Update the description or status of a task."""
    assert STATE.db_path is not None

    todo = next((t for t in STATE.db if t.id == id), None)
    if todo is None:
        typer.echo(f"No todo with id: {id}")
        raise typer.Exit(code=1)

    changed = False
    now = dt.datetime.now()

    if desc is not None and desc != todo.desc:
        todo.desc = desc
        changed = True

    if status is not None and status != todo.status:
        todo.status = status
        changed = True

    if changed:
        todo.updatedAt = now
        save_database(STATE.db_path, STATE.db)
        typer.echo(f"Updated todo #{todo.id}")
    else:
        typer.echo("No changes provided.")


# List todo(s) in the database.
@app.command(name="list")
def list_todos(
    status: Optional[TaskStatus] = typer.Option(
        None, "--status", "-s", help="Filter by status (todo, in-progress, done)"
    ),
):
    """List todos."""
    if not STATE.db:
        typer.echo("No todos.")
        return

    table = Table("ID", "Description", "Status", "Date Created", "Date Updated")

    todos = STATE.db if status is None else [t for t in STATE.db if t.status == status]

    if not todos:
        typer.echo(f"No todos with status: {status.value}" if status else "No todos.")

    for t in todos:
        table.add_row(
            str(t.id),
            t.desc,
            t.status.value,
            t.createdAt.strftime("%d-%m-%Y %I:%M %p"),
            t.updatedAt.strftime("%d-%m-%Y %I:%M %p"),
        )

    console.print(table)


@app.command()
def mark_in_progress(target: str):
    """Mark a todo in-progress by id."""
    assert STATE.db_path is not None

    now = dt.datetime.now()

    if target == "all":
        for t in STATE.db:
            t.status = TaskStatus.IN_PROGRESS
            t.updatedAt = now
        save_database(STATE.db_path, STATE.db)
        typer.echo(f"Marked all todos as {TaskStatus.IN_PROGRESS.value}.")
        return

    todo = Todo
    id = int(target)
    for todo in STATE.db:
        if todo.id == id:
            todo.status = TaskStatus.IN_PROGRESS
            todo.updatedAt = now
            typer.echo(f"{todo.id}: {todo.desc} Marked in-progress")

    save_database(STATE.db_path, STATE.db)


# Mark a todo as
@app.command()
def mark_complete(target: str):
    """Mark a todo complete by id."""
    assert STATE.db_path is not None

    now = dt.datetime.now()

    if target == "all":
        for t in STATE.db:
            t.status = TaskStatus.DONE
            t.updatedAt = now
        save_database(STATE.db_path, STATE.db)
        typer.echo(f"Marked all todos as {TaskStatus.DONE.value}.")
        return

    todo = Todo
    id = int(target)
    for todo in STATE.db:
        if todo.id == id:
            todo.status = TaskStatus.DONE
            todo.updatedAt = now
            typer.echo(f"{todo.id}: {todo.desc} Marked complete!")

    save_database(STATE.db_path, STATE.db)


class AppState:
    def __init__(self) -> None:
        self.db_path: Optional[Path] = None
        self.db: Database = []


STATE = AppState()


@app.callback()
def main(
    db: Path = typer.Option(
        Path.home() / ".todo" / "todo.json",
        "--db",
        help="Path to the JSON database file",
        show_default=True,
    ),
):
    """
    Tasked CLI
    Loads the database once; commands reuse it.
    """

    STATE.db_path = db
    STATE.db = load_database(db)


if __name__ == "__main__":
    app()
