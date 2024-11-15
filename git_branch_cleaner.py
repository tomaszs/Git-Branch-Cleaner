from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta
import subprocess

console = Console()

# Configuration
DELETE_UNPUSHED_BRANCHES = True  # Set to False to skip deletion of unpushed branches
CHECK_LAST_MODIFIED_TIME = True  # Set to False to ignore the last modified time when checking branches
DELETE_MERGED_BRANCHES = True  # Set to False to skip deletion of merged branches
LAST_MODIFIED_CUTOFF = datetime.now() - timedelta(days=0)
DEFAULT_BRANCH = "main"  # Branch to switch to before deletion if on the branch to be deleted

def get_local_branches():
    result = subprocess.run(
        ["git", "for-each-ref", "--sort=-committerdate", "--format='%(refname:short) %(committerdate:iso8601)'", "refs/heads/"],
        capture_output=True,
        text=True
    )
    branches = result.stdout.strip().splitlines()
    
    branch_info = []
    for line in branches:
        name, date_str = line.strip("'").split(maxsplit=1)
        date = datetime.fromisoformat(date_str)
        branch_info.append((name, date))
    
    return branch_info

def get_current_branch():
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def switch_to_default_branch():
    subprocess.run(["git", "checkout", DEFAULT_BRANCH], check=True)
    console.print(f"[bold green]Switched to '{DEFAULT_BRANCH}' branch.[/]")

def delete_unused_branches():
    console.print("\n[bold red]Searching for unused branches...[/]\n")
    branch_info = get_local_branches()
    unused_branches_found = False

    for branch, last_commit_date in branch_info:
        last_commit_date = last_commit_date.replace(tzinfo=None)

        # Check if the branch is pushed to remote, ignoring date if CHECK_LAST_MODIFIED_TIME is False
        is_pushed = subprocess.run(
            ["git", "rev-parse", "--verify", f"origin/{branch}"],
            capture_output=True,
            text=True
        ).returncode == 0
        
        # Include the branch if it's unpushed, and if CHECK_LAST_MODIFIED_TIME is True, check the date
        if not is_pushed and (not CHECK_LAST_MODIFIED_TIME or last_commit_date < LAST_MODIFIED_CUTOFF):
            unused_branches_found = True
            show_branch_info(branch, last_commit_date)

            if DELETE_UNPUSHED_BRANCHES:
                console.print("[bold cyan]Delete this branch locally? (y/n/q to cancel): ", end="")
                choice = input().strip().lower()
                if choice == "y":
                    current_branch = get_current_branch()
                    if current_branch == branch:
                        switch_to_default_branch()
                    try:
                        subprocess.run(["git", "branch", "-D", branch], check=True)
                        console.print(f"\n[bold green]Branch '{branch}' deleted.[/]")
                    except subprocess.CalledProcessError:
                        console.print(f"\n[bold red]Failed to delete branch '{branch}'.[/]")
                elif choice == "n":
                    console.print(f"\n[bold yellow]Branch '{branch}' skipped.[/]")
                elif choice == "q":
                    console.print("\n[bold yellow]Operation canceled, returning to menu...[/]")
                    return  # Only return if 'q' is selected to cancel

    if not unused_branches_found:
        console.print("[bold yellow]No unused branches found that meet the criteria.[/]")

def delete_merged_branches():
    if not DELETE_MERGED_BRANCHES:
        return
    
    console.print("\n[bold red]Searching for merged branches...[/]\n")
    subprocess.run(["git", "fetch", "--all"], check=True)

    merged_branches = subprocess.run(
        ["git", "branch", "-r", "--merged", f"origin/{DEFAULT_BRANCH}"],
        capture_output=True,
        text=True
    ).stdout.splitlines()
    
    # Filter out HEAD and main branches
    merged_branches = [branch.strip() for branch in merged_branches if not branch.endswith("/HEAD") and not branch.endswith(f"/{DEFAULT_BRANCH}")]
    
    if not merged_branches:
        console.print("[bold yellow]No merged branches found.[/]")
        return

    for branch in merged_branches:
        # Extract branch name and retrieve the merge time
        local_branch_name = branch.replace("origin/", "")
        merge_time = subprocess.run(
            ["git", "log", "-1", "--format=%ci", f"{DEFAULT_BRANCH}..{branch}"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Display branch info and prompt for deletion
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Branch", style="cyan")
        table.add_column("Merge Time", style="yellow")
        table.add_row(local_branch_name, merge_time if merge_time else "Unknown")
        console.print(table)

        console.print("[bold cyan]Delete this merged branch locally? (y/n/q to cancel): ", end="")
        choice = input().strip().lower()
        if choice == "y":
            try:
                subprocess.run(["git", "branch", "-d", local_branch_name], check=True)
                console.print(f"\n[bold green]Branch '{local_branch_name}' deleted.[/]")
            except subprocess.CalledProcessError:
                console.print(f"\n[bold red]Failed to delete branch '{local_branch_name}'.[/]")
        elif choice == "n":
            console.print(f"\n[bold yellow]Branch '{local_branch_name}' skipped.[/]")
        elif choice == "q":
            console.print("\n[bold yellow]Operation canceled, returning to menu...[/]")
            return  # Only return if 'q' is selected to cancel

def show_branch_info(branch, last_commit_date):
    table = Table(title="Branch Information", show_header=True, header_style="bold magenta")
    table.add_column("Branch", style="cyan", justify="left")
    table.add_column("Last Edited", style="yellow", justify="right")
    table.add_row(branch, last_commit_date.strftime('%Y-%m-%d'))
    console.print(table)

def something_else():
    console.print("[bold green]Doing something else...[/]")

def show_menu():
    console.print("\n[D] [cyan]Delete unused and merged branches[/]")
    console.print("[S] [cyan]Something else[/]")
    console.print("[Q] [cyan]Quit[/]")

def main():
    while True:
        show_menu()
        console.print("\n[bold magenta]Select an option (D/S/Q): ", end="")
        choice = input().strip().lower()
        if choice == "d":
            delete_unused_branches()
            delete_merged_branches()
        elif choice == "s":
            something_else()
        elif choice == "q":
            console.print("[bold yellow]Exiting...[/]")
            break

if __name__ == "__main__":
    main()
