import sys
import typer
from typing import List
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from todo_manager import TodoManager


# Create console with force_terminal and force unicode to handle Windows legacy console compatibility
console = Console(force_terminal=True, force_interactive=True)
app = typer.Typer()


def show_menu():
    """Display the main menu options."""
    menu_text = """
[bold blue]=========================================[/bold blue]
[bold blue]          TODO MANAGER MENU              [/bold blue]
[bold blue]=========================================[/bold blue]
[bold blue][/bold blue] [1] Add New Task                       [bold blue][/bold blue]
[bold blue][/bold blue] [2] View All Tasks (Table)             [bold blue][/bold blue]
[bold blue][/bold blue] [3] Update Task                        [bold blue][/bold blue]
[bold blue][/bold blue] [4] Complete Task                      [bold blue][/bold blue]
[bold blue][/bold blue] [5] Delete Task                        [bold blue][/bold blue]
[bold blue][/bold blue] [6] Search/Filter                      [bold blue][/bold blue]
[bold blue][/bold blue] [0] Exit                               [bold blue][/bold blue]
[bold blue]=========================================[/bold blue]
"""
    # Ensure menu_text is always a string and handle potential type issues
    menu_text = str(menu_text)
    console.print(Panel(menu_text, title="[bold green]Welcome to Todo Manager[/bold green]", border_style="cyan"))


def handle_add_task(manager: TodoManager):
    """Handle adding a new task."""
    console.print("\n[bold yellow]Adding New Task[/bold yellow]")

    task = Prompt.ask("[blue]Enter task title[/blue]")
    description = Prompt.ask("[blue]Enter task description (optional)[/blue]", default="")

    priority = Prompt.ask(
        "[blue]Enter priority (high/medium/low)[/blue]",
        choices=["high", "medium", "low"],
        default="medium"
    )

    tags_input = Prompt.ask("[blue]Enter tags separated by commas (optional)[/blue]", default="")
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

    try:
        new_todo = manager.add_todo(task, description, priority, tags)
        console.print(f"[green]✓ Added todo:[/green] [bold]{new_todo['task']}[/bold] (ID: {new_todo['id']})")
        console.print(f"[blue]Priority:[/blue] {new_todo['priority']}")
        if new_todo['tags']:
            console.print(f"[blue]Tags:[/blue] {', '.join(new_todo['tags'])}")
        if new_todo['description']:
            console.print(f"[blue]Description:[/blue] {new_todo['description']}")
    except ValueError as e:
        console.print(f"[red]✗ Error:[/red] {e}")


def handle_view_tasks(manager: TodoManager):
    """Handle viewing all tasks."""
    todos = manager.list_todos()

    if not todos:
        console.print("[yellow]No todos found.[/yellow]")
        return

    # Create a unified table as requested
    console.print("\n[bold blue]All Todos:[/bold blue]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=5)
    table.add_column("Task", min_width=20)
    table.add_column("Status", width=10)
    table.add_column("Priority", width=10)
    table.add_column("Tags", min_width=15)

    for todo in todos:
        status_text = "[green]Completed[/green]" if todo['status'] == 'completed' else "[yellow]Pending[/yellow]"
        table.add_row(
            str(todo['id']),
            todo['task'],
            status_text,
            todo['priority'].title(),
            ', '.join(todo['tags']) if todo['tags'] else 'None'
        )
    console.print(table)


def handle_complete_task(manager: TodoManager):
    """Handle completing a task."""
    try:
        task_id = IntPrompt.ask("[blue]Enter the ID of the task to complete[/blue]")
        success = manager.complete_todo(task_id)
        if success:
            console.print(f"[green]✓ Marked todo {task_id} as completed[/green]")
    except ValueError as e:
        console.print(f"[red]✗ Error:[/red] {e}")
    except Exception:
        console.print("[red]✗ Invalid input. Please enter a valid task ID.[/red]")


def handle_delete_task(manager: TodoManager):
    """Handle deleting a task."""
    try:
        task_id = IntPrompt.ask("[blue]Enter the ID of the task to delete[/blue]")
        success = manager.delete_todo(task_id)
        if success:
            console.print(f"[red]✓ Deleted todo {task_id}[/red]")
    except ValueError as e:
        console.print(f"[red]✗ Error:[/red] {e}")
    except Exception:
        console.print("[red]✗ Invalid input. Please enter a valid task ID.[/red]")


def handle_update_task(manager: TodoManager):
    """Handle updating a task."""
    try:
        task_id = IntPrompt.ask("[blue]Enter the ID of the task to update[/blue]")

        console.print(f"[blue]Current task details:[/blue]")
        try:
            current_todo = manager.get_todo_by_id(task_id)
            console.print(f"  Task: {current_todo['task']}")
            console.print(f"  Description: {current_todo['description'] if current_todo['description'] else 'None'}")
        except ValueError:
            console.print(f"[red]✗ Task with ID {task_id} not found[/red]")
            return

        new_task = Prompt.ask("[blue]Enter new task title (press Enter to keep current)[/blue]", default="")
        new_description = Prompt.ask("[blue]Enter new description (press Enter to keep current)[/blue]", default="")

        # Determine which values to update
        task_to_update = new_task if new_task != "" else None
        desc_to_update = new_description if new_description != "" else None

        # At least one value must be provided for update
        if task_to_update is None and desc_to_update is None:
            console.print("[yellow]No updates provided. Task remains unchanged.[/yellow]")
            return

        success = manager.update_todo(task_id, task_to_update, desc_to_update)
        if success:
            console.print(f"[green]✓ Updated todo {task_id}[/green]")
            if task_to_update is not None:
                console.print(f"[blue]New task:[/blue] {task_to_update}")
            if desc_to_update is not None:
                console.print(f"[blue]New description:[/blue] {desc_to_update}")
    except ValueError as e:
        console.print(f"[red]✗ Error:[/red] {e}")
    except Exception:
        console.print("[red]✗ Invalid input. Please enter a valid task ID.[/red]")


def handle_search_filter(manager: TodoManager):
    """Handle searching/filtering tasks."""
    console.print("\n[bold yellow]Search/Filter Options[/bold yellow]")
    console.print("[1] Search by keyword")
    console.print("[2] Filter by status")
    console.print("[3] Filter by priority")
    console.print("[4] Filter by tag")

    try:
        choice = IntPrompt.ask("[blue]Select an option[/blue]", choices=[1, 2, 3, 4])

        if choice == 1:
            # Search by keyword
            keyword = Prompt.ask("[blue]Enter keyword to search[/blue]")
            results = manager.search_todos(keyword)

            if not results:
                console.print(f"[yellow]No todos found containing '{keyword}'.[/yellow]")
                return

            console.print(f"\n[bold blue]Search Results for '{keyword}'[/bold blue]")
            pending_results = [todo for todo in results if todo['status'] == 'pending']
            completed_results = [todo for todo in results if todo['status'] == 'completed']

            # Create a table for pending search results
            if pending_results:
                console.print("\n[bold blue]Pending Todos:[/bold blue]")
                pending_table = Table(show_header=True, header_style="bold magenta")
                pending_table.add_column("ID", style="dim", width=5)
                pending_table.add_column("Task", min_width=20)
                pending_table.add_column("Description", min_width=20)
                pending_table.add_column("Priority", width=10)
                pending_table.add_column("Tags", min_width=15)
                pending_table.add_column("Status", width=10)

                for todo in pending_results:
                    pending_table.add_row(
                        str(todo['id']),
                        todo['task'],
                        todo['description'],
                        todo['priority'].title(),
                        ', '.join(todo['tags']) if todo['tags'] else 'None',
                        "[yellow]Pending[/yellow]"
                    )
                console.print(pending_table)

            # Create a table for completed search results
            if completed_results:
                console.print("\n[bold green]Completed Todos:[/bold green]")
                completed_table = Table(show_header=True, header_style="bold magenta")
                completed_table.add_column("ID", style="dim", width=5)
                completed_table.add_column("Task", min_width=20)
                completed_table.add_column("Description", min_width=20)
                completed_table.add_column("Priority", width=10)
                completed_table.add_column("Tags", min_width=15)
                completed_table.add_column("Status", width=10)

                for todo in completed_results:
                    completed_table.add_row(
                        str(todo['id']),
                        todo['task'],
                        todo['description'],
                        todo['priority'].title(),
                        ', '.join(todo['tags']) if todo['tags'] else 'None',
                        "[green]Completed[/green]"
                    )
                console.print(completed_table)

        elif choice == 2:
            # Filter by status
            status = Prompt.ask(
                "[blue]Enter status to filter by (pending/completed)[/blue]",
                choices=["pending", "completed"],
                default="pending"
            )
            results = manager.filter_todos("status", status)

            if not results:
                console.print(f"[yellow]No todos found with status '{status}'.[/yellow]")
                return

            console.print(f"\n[bold blue]Filtered Results (Status: {status.title()})[/bold blue]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("ID", style="dim", width=5)
            table.add_column("Task", min_width=20)
            table.add_column("Description", min_width=20)
            table.add_column("Priority", width=10)
            table.add_column("Tags", min_width=15)
            table.add_column("Status", width=10)

            for todo in results:
                status_text = "[green]Completed[/green]" if todo['status'] == 'completed' else "[yellow]Pending[/yellow]"
                table.add_row(
                    str(todo['id']),
                    todo['task'],
                    todo['description'],
                    todo['priority'].title(),
                    ', '.join(todo['tags']) if todo['tags'] else 'None',
                    status_text
                )
            console.print(table)

        elif choice == 3:
            # Filter by priority
            priority = Prompt.ask(
                "[blue]Enter priority to filter by (high/medium/low)[/blue]",
                choices=["high", "medium", "low"],
                default="medium"
            )
            results = manager.filter_todos("priority", priority)

            if not results:
                console.print(f"[yellow]No todos found with priority '{priority}'.[/yellow]")
                return

            console.print(f"\n[bold blue]Filtered Results (Priority: {priority.title()})[/bold blue]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("ID", style="dim", width=5)
            table.add_column("Task", min_width=20)
            table.add_column("Description", min_width=20)
            table.add_column("Priority", width=10)
            table.add_column("Tags", min_width=15)
            table.add_column("Status", width=10)

            for todo in results:
                status_text = "[green]Completed[/green]" if todo['status'] == 'completed' else "[yellow]Pending[/yellow]"
                table.add_row(
                    str(todo['id']),
                    todo['task'],
                    todo['description'],
                    todo['priority'].title(),
                    ', '.join(todo['tags']) if todo['tags'] else 'None',
                    status_text
                )
            console.print(table)

        elif choice == 4:
            # Filter by tag
            tag = Prompt.ask("[blue]Enter tag to filter by[/blue]")
            results = manager.filter_todos("tag", tag)

            if not results:
                console.print(f"[yellow]No todos found with tag '{tag}'.[/yellow]")
                return

            console.print(f"\n[bold blue]Filtered Results (Tag: {tag})[/bold blue]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("ID", style="dim", width=5)
            table.add_column("Task", min_width=20)
            table.add_column("Description", min_width=20)
            table.add_column("Priority", width=10)
            table.add_column("Tags", min_width=15)
            table.add_column("Status", width=10)

            for todo in results:
                status_text = "[green]Completed[/green]" if todo['status'] == 'completed' else "[yellow]Pending[/yellow]"
                table.add_row(
                    str(todo['id']),
                    todo['task'],
                    todo['description'],
                    todo['priority'].title(),
                    ', '.join(todo['tags']) if todo['tags'] else 'None',
                    status_text
                )
            console.print(table)
    except ValueError as e:
        console.print(f"[red]✗ Error:[/red] {e}")
    except Exception:
        console.print("[red]✗ Invalid input. Please enter a valid choice.[/red]")


def interactive_menu():
    """Run the interactive menu loop."""
    manager = TodoManager()

    console.print("[bold green]Welcome to the Interactive Todo Manager![/bold green]")
    console.print("[blue]Managing your tasks in this session...[/blue]\n")

    while True:
        show_menu()

        try:
            # Using Prompt to get string input, then convert to int to avoid sequence errors
            choice_str = Prompt.ask("[blue]Select an option (0-6)[/blue]")
            
            # Validate and convert the input
            try:
                choice = int(choice_str)
            except ValueError:
                console.print("[red]Invalid input. Please enter a number.[/red]")
                continue
            
            # Check if choice is in valid range
            if choice not in [0, 1, 2, 3, 4, 5, 6]:
                console.print("[red]Invalid option. Please select a number between 0-6.[/red]")
                continue

            if choice == 1:
                handle_add_task(manager)
            elif choice == 2:
                handle_view_tasks(manager)
            elif choice == 3:
                handle_update_task(manager)
            elif choice == 4:
                handle_complete_task(manager)
            elif choice == 5:
                handle_delete_task(manager)
            elif choice == 6:
                handle_search_filter(manager)
            elif choice == 0:
                console.print("[bold green]Thank you for using Todo Manager![/bold green]")
                console.print("[blue]Goodbye![/blue]")
                break

            # Pause before showing menu again (handle EOFError for automated environments)
            try:
                console.input("\n[Press Enter to continue...]")
                console.clear()
            except (EOFError, OSError):
                # If input is not available (e.g., in automated environments), continue without pause
                console.print("[yellow]Continuing...[/yellow]")

        except KeyboardInterrupt:
            console.print("\n[red]Interrupted by user. Goodbye![/red]")
            break
        except Exception as e:
            console.print(f"[red]An unexpected error occurred: {e}[/red]")
            console.print("[yellow]Returning to menu...[/yellow]")


@app.command()
def add(task: str = typer.Argument(..., help="Task title to add"),
        description: str = typer.Argument("", help="Optional description for the task"),
        priority: str = typer.Option("medium", "--priority", "-p", help="Priority level (high, medium, low)",
                                    case_sensitive=False),
        tags: List[str] = typer.Option([], "--tag", "-t", help="Tags for the task (can be used multiple times)")):
    """Add a new todo item."""
    manager = TodoManager()
    try:
        new_todo = manager.add_todo(task, description, priority.lower(), tags)
        console.print(f"[green]Added todo:[/green] [bold]{new_todo['task']}[/bold] (ID: {new_todo['id']})")
        console.print(f"[blue]Priority:[/blue] {new_todo['priority']}")
        if new_todo['tags']:
            console.print(f"[blue]Tags:[/blue] {', '.join(new_todo['tags'])}")
        if new_todo['description']:
            console.print(f"[blue]Description:[/blue] {new_todo['description']}")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@app.command()
def list():
    """List all todo items."""
    manager = TodoManager()
    todos = manager.list_todos()

    if not todos:
        console.print("[yellow]No todos found.[/yellow]")
        return

    # Create a unified table as requested
    console.print("\n[bold blue]All Todos:[/bold blue]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=5)
    table.add_column("Task", min_width=20)
    table.add_column("Status", width=10)
    table.add_column("Priority", width=10)
    table.add_column("Tags", min_width=15)

    for todo in todos:
        status_text = "[green]Completed[/green]" if todo['status'] == 'completed' else "[yellow]Pending[/yellow]"
        table.add_row(
            str(todo['id']),
            todo['task'],
            status_text,
            todo['priority'].title(),
            ', '.join(todo['tags']) if todo['tags'] else 'None'
        )
    console.print(table)


@app.command()
def complete(id: int = typer.Argument(..., help="ID of the todo to complete")):
    """Mark a todo item as completed."""
    manager = TodoManager()
    try:
        success = manager.complete_todo(id)
        if success:
            console.print(f"[green]Marked todo {id} as completed[/green]")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@app.command()
def delete(id: int = typer.Argument(..., help="ID of the todo to delete")):
    """Delete a todo item."""
    manager = TodoManager()
    try:
        success = manager.delete_todo(id)
        if success:
            console.print(f"[red]Deleted todo {id}[/red]")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@app.command()
def update(id: int = typer.Argument(..., help="ID of the todo to update"),
           new_task: str = typer.Argument("", help="New task title (leave empty to keep current)"),
           new_description: str = typer.Argument("", help="New description (leave empty to keep current)")):
    """Update an existing todo item's title and/or description."""
    manager = TodoManager()

    # Determine which values to update
    task_to_update = new_task if new_task != "" else None
    desc_to_update = new_description if new_description != "" else None

    # At least one value must be provided for update
    if task_to_update is None and desc_to_update is None:
        console.print("[red]Error:[/red] You must provide at least a new task title or new description to update.")
        sys.exit(1)

    try:
        success = manager.update_todo(id, task_to_update, desc_to_update)
        if success:
            console.print(f"[green]Updated todo {id}[/green]")
            if task_to_update is not None:
                console.print(f"[blue]New task:[/blue] {task_to_update}")
            if desc_to_update is not None:
                console.print(f"[blue]New description:[/blue] {desc_to_update}")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@app.command()
def priority(id: int = typer.Argument(..., help="ID of the todo to set priority for"),
             priority_level: str = typer.Argument(..., help="Priority level (high, medium, low)")):
    """Set priority for a specific todo."""
    manager = TodoManager()
    try:
        success = manager.set_priority(id, priority_level.lower())
        if success:
            console.print(f"[green]Set priority to {priority_level.lower()} for todo {id}[/green]")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@app.command()
def tag(id: int = typer.Argument(..., help="ID of the todo to add tags to"),
        tags: List[str] = typer.Argument(..., help="Tags to add to the task")):
    """Add tags to a specific todo."""
    manager = TodoManager()
    try:
        success = manager.add_tags(id, tags)
        if success:
            console.print(f"[green]Added tags {', '.join(tags)} to todo {id}[/green]")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@app.command()
def view(id: int = typer.Argument(..., help="ID of the todo to view details for")):
    """View detailed information about a specific todo."""
    manager = TodoManager()
    try:
        todo = manager.get_todo_by_id(id)
        console.print(f"\n[bold blue]Todo Details (ID: {todo['id']})[/bold blue]")
        console.print(f"[bold]Task:[/bold] {todo['task']}")
        console.print(f"[bold]Description:[/bold] {todo['description'] if todo['description'] else 'None'}")
        console.print(f"[bold]Status:[/bold] {todo['status'].title()}")
        console.print(f"[bold]Priority:[/bold] {todo['priority'].title()}")
        console.print(f"[bold]Tags:[/bold] {', '.join(todo['tags']) if todo['tags'] else 'None'}")
        console.print(f"[bold]Created At:[/bold] {todo['created_at']}")
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@app.command()
def search(keyword: str = typer.Argument(..., help="Keyword to search for in tasks and descriptions")):
    """Search for todos containing the keyword."""
    manager = TodoManager()
    results = manager.search_todos(keyword)

    if not results:
        console.print(f"[yellow]No todos found containing '{keyword}'.[/yellow]")
        return

    console.print(f"\n[bold blue]Search Results for '{keyword}'[/bold blue]")
    pending_results = [todo for todo in results if todo['status'] == 'pending']
    completed_results = [todo for todo in results if todo['status'] == 'completed']

    # Create a table for pending search results
    if pending_results:
        console.print("\n[bold blue]Pending Todos:[/bold blue]")
        pending_table = Table(show_header=True, header_style="bold magenta")
        pending_table.add_column("ID", style="dim", width=5)
        pending_table.add_column("Task", min_width=20)
        pending_table.add_column("Description", min_width=20)
        pending_table.add_column("Priority", width=10)
        pending_table.add_column("Tags", min_width=15)
        pending_table.add_column("Status", width=10)

        for todo in pending_results:
            pending_table.add_row(
                str(todo['id']),
                todo['task'],
                todo['description'],
                todo['priority'].title(),
                ', '.join(todo['tags']) if todo['tags'] else 'None',
                "[yellow]Pending[/yellow]"
            )
        console.print(pending_table)

    # Create a table for completed search results
    if completed_results:
        console.print("\n[bold green]Completed Todos:[/bold green]")
        completed_table = Table(show_header=True, header_style="bold magenta")
        completed_table.add_column("ID", style="dim", width=5)
        completed_table.add_column("Task", min_width=20)
        completed_table.add_column("Description", min_width=20)
        completed_table.add_column("Priority", width=10)
        completed_table.add_column("Tags", min_width=15)
        completed_table.add_column("Status", width=10)

        for todo in completed_results:
            completed_table.add_row(
                str(todo['id']),
                todo['task'],
                todo['description'],
                todo['priority'].title(),
                ', '.join(todo['tags']) if todo['tags'] else 'None',
                "[green]Completed[/green]"
            )
        console.print(completed_table)


@app.command()
def filter(filter_type: str = typer.Argument(..., help="Type of filter (status, priority, tag)"),
           filter_value: str = typer.Argument(..., help="Value to filter by")):
    """Filter todos by status, priority, or tag."""
    manager = TodoManager()
    try:
        results = manager.filter_todos(filter_type.lower(), filter_value.lower())

        if not results:
            console.print(f"[yellow]No todos found matching the filter ({filter_type}: {filter_value}).[/yellow]")
            return

        console.print(f"\n[bold blue]Filtered Results ({filter_type.title()}: {filter_value.title()})[/bold blue]")
        pending_results = [todo for todo in results if todo['status'] == 'pending']
        completed_results = [todo for todo in results if todo['status'] == 'completed']

        # Create a table for pending filtered results
        if pending_results:
            console.print("\n[bold blue]Pending Todos:[/bold blue]")
            pending_table = Table(show_header=True, header_style="bold magenta")
            pending_table.add_column("ID", style="dim", width=5)
            pending_table.add_column("Task", min_width=20)
            pending_table.add_column("Description", min_width=20)
            pending_table.add_column("Priority", width=10)
            pending_table.add_column("Tags", min_width=15)
            pending_table.add_column("Status", width=10)

            for todo in pending_results:
                pending_table.add_row(
                    str(todo['id']),
                    todo['task'],
                    todo['description'],
                    todo['priority'].title(),
                    ', '.join(todo['tags']) if todo['tags'] else 'None',
                    "[yellow]Pending[/yellow]"
                )
            console.print(pending_table)

        # Create a table for completed filtered results
        if completed_results:
            console.print("\n[bold green]Completed Todos:[/bold green]")
            completed_table = Table(show_header=True, header_style="bold magenta")
            completed_table.add_column("ID", style="dim", width=5)
            completed_table.add_column("Task", min_width=20)
            completed_table.add_column("Description", min_width=20)
            completed_table.add_column("Priority", width=10)
            completed_table.add_column("Tags", min_width=15)
            completed_table.add_column("Status", width=10)

            for todo in completed_results:
                completed_table.add_row(
                    str(todo['id']),
                    todo['task'],
                    todo['description'],
                    todo['priority'].title(),
                    ', '.join(todo['tags']) if todo['tags'] else 'None',
                    "[green]Completed[/green]"
                )
            console.print(completed_table)

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@app.command()
def sort(sort_type: str = typer.Argument(..., help="Type of sort (priority, id)")):
    """Sort todos by priority or ID."""
    manager = TodoManager()
    try:
        results = manager.sort_todos(sort_type.lower())

        if not results:
            console.print("[yellow]No todos to sort.[/yellow]")
            return

        console.print(f"\n[bold blue]Sorted Results by {sort_type.title()}[/bold blue]")
        pending_results = [todo for todo in results if todo['status'] == 'pending']
        completed_results = [todo for todo in results if todo['status'] == 'completed']

        # Create a table for pending sorted results
        if pending_results:
            console.print("\n[bold blue]Pending Todos:[/bold blue]")
            pending_table = Table(show_header=True, header_style="bold magenta")
            pending_table.add_column("ID", style="dim", width=5)
            pending_table.add_column("Task", min_width=20)
            pending_table.add_column("Description", min_width=20)
            pending_table.add_column("Priority", width=10)
            pending_table.add_column("Tags", min_width=15)
            pending_table.add_column("Status", width=10)

            for todo in pending_results:
                pending_table.add_row(
                    str(todo['id']),
                    todo['task'],
                    todo['description'],
                    todo['priority'].title(),
                    ', '.join(todo['tags']) if todo['tags'] else 'None',
                    "[yellow]Pending[/yellow]"
                )
            console.print(pending_table)

        # Create a table for completed sorted results
        if completed_results:
            console.print("\n[bold green]Completed Todos:[/bold green]")
            completed_table = Table(show_header=True, header_style="bold magenta")
            completed_table.add_column("ID", style="dim", width=5)
            completed_table.add_column("Task", min_width=20)
            completed_table.add_column("Description", min_width=20)
            completed_table.add_column("Priority", width=10)
            completed_table.add_column("Tags", min_width=15)
            completed_table.add_column("Status", width=10)

            for todo in completed_results:
                completed_table.add_row(
                    str(todo['id']),
                    todo['task'],
                    todo['description'],
                    todo['priority'].title(),
                    ', '.join(todo['tags']) if todo['tags'] else 'None',
                    "[green]Completed[/green]"
                )
            console.print(completed_table)

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


def main():
    """Main application entry point."""
    # Check if arguments were provided
    if len(sys.argv) == 1:
        # No arguments provided, run interactive menu
        interactive_menu()
    else:
        # Arguments provided, run Typer CLI
        app()


if __name__ == "__main__":
    main()