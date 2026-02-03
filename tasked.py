import json
import sys
from argparse import ArgumentParser
from pathlib import Path
import datetime
import os

import typer

from typing import List, Dict, Annotated, Optional, Literal, NamedTuple, Any, TypeAlias, TypedDict, Union

app = typer.Typer()

TaskStatus: TypeAlias = Literal["Done", "In-Progress", "Todo"]


class Todo(NamedTuple):
    id: int
    desc: str
    status: TaskStatus
    createdAt: datetime.datetime
    updatedAt: datetime.datetime


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


@app.command()
def init(self, json_file: str):
    self.json_file = json_file
    filepath = self.json_file + ".json"
    if not os.path.exists(filepath):
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)
        except Exception as e:
            print(f"Failed to create {filepath}: {e}")
    else:
        print(f"{filepath} already exists!")


def load_database(json_file: str):
    if json_file.endswith(".json"):
        try:
            with open(json_file, "w") as file:
                data = json.load(file)
                print(f"Opened {json_file} successfully")
        except FileNotFoundError:
            print(f"Error: The file '{json_file}' was not found. Please check the file path.")


def save_database():
    pass


@app.command()
def add(filename: str, description: str):
    filename = filename + ".json"
    database = load_database(filename)
    if database:
        try:
            todo = Todo
            todo.id = 1
            todo.desc = description
            todo.status = "Todo"
            todo.createdAt = datetime.datetime.now()
            todo.updatedAt = datetime.datetime.now()
            json.dump(todo, database, indent=4)
            print(f"Created todo successfully!")
        except Exception as e:
            print(f"Failed to create the todo: {e}")


@app.command()
def delete():
    pass


@app.command()
def list():
    pass


@app.command()
def mark_complete():
    pass


@app.command()
def main(name: str):
    typer.secho(f"Welcome here {name}", fg=typer.colors.MAGENTA)


if __name__ == "__main__":
    app()
