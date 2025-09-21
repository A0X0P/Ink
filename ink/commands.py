"""The sub command file """

import json
import os
from time import time
from datetime import datetime
from typing import Any
import click

NOTE_FILE = os.path.expanduser("~/.notes.json")

def load() -> list[dict[str, Any]]:
    """Load the notes from file."""

    if not os.path.exists(NOTE_FILE):
        return []
    with open(NOTE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save(notes: list[dict[str, Any]]) -> None:
    """Save notes to file."""

    folder = os.path.dirname(NOTE_FILE)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(NOTE_FILE, "w", encoding="utf-8") as file:
        json.dump(notes, file, indent=2)


@click.command()
@click.argument("title")
@click.option("--content", prompt=True, help="Content of the note")
@click.option("--tags", help="Comma-separated list of tags")
def add(title: str, content: str, tags: str) -> None:
    """Create a new note."""

    notes = load()
    note_data = {
        "name": f"{title}.txt",
        "content": content,
        "id": int(time()),
        "tags": tags.split(",") if tags else [],
        "timestamp": datetime.now().isoformat(),
    }
    notes.append(note_data)
    save(notes)
    click.echo(f"Note '{title}' added!")

@click.command(name="lst")
def lst() -> None:
    """List all notes."""

    notes = load()
    if not notes:
        click.echo("No notes found.")
        return
    for note in notes:
        click.echo(
            f"[{note['id']}] {note['timestamp']}" \
                 f" {note['tags']} - {note['name']} : {note['content'][:50]}"
        )

@click.command()
@click.argument("note_id", type=int)
def view(note_id: int) -> None:
    """View a note by ID."""

    notes = load()
    for note in notes:
        if note['id'] == note_id:
            click.echo(f"\n[{note['id']}] {note['timestamp']}\n{note['content']}\n")
            return
    click.echo("Note not found.")

@click.command()
@click.argument("note_id", type=int)
def delete(note_id: int) -> None:
    """Delete a note by ID."""

    notes = load()
    new_notes = [note for note in notes if note['id'] != note_id]
    if len(new_notes) == len(notes):
        click.echo("Note not found.")
        return
    save(new_notes)
    click.echo("Note deleted.")

@click.command()
@click.argument("keyword")
def search(keyword: str) -> None:
    """Search for notes by keyword."""
    notes = load()
    results = [note for note in notes if keyword.lower() in note["content"].lower()]
    if not results:
        click.echo("No matching notes found.")
        return
    for note in results:
        click.echo(
            f"[{note['id']}] {note['timestamp']} - {note['name']} : {note['content'][:50]}"
        )
