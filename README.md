
# Git Branch Cleaner

[Article](https://medium.com/@tomaszs2/automate-git-branch-cleanup-with-python-say-goodbye-to-manual-tidying-e79e8a2e3155)

A Python script to help manage and clean up Git branches in your repository. This tool allows you to:
- **Delete unused local branches** that haven’t been pushed to the remote or have not been updated recently.
- **Delete merged branches** that have already been merged into the main branch, allowing you to keep your repository organized and free of redundant branches.

## Features

- **Unused Branch Cleanup**: Searches for local branches that haven't been pushed to the remote and optionally checks if they haven't been updated in a certain period. You can customize this period or disable the time check.
- **Merged Branch Cleanup**: Identifies remote branches that have already been merged into the main branch and prompts for deletion.
- **Interactive Deletion**: For each branch identified, the script will display the branch name, its last edited or merged time, and prompt you to confirm deletion.

## Configuration

At the top of the script, you can customize the following options:

- `DELETE_UNPUSHED_BRANCHES`: Set to `True` to delete unpushed branches (default is `True`).
- `CHECK_LAST_MODIFIED_TIME`: Set to `True` to only delete branches that haven’t been modified within a certain period (defined by `LAST_MODIFIED_CUTOFF`). If `False`, the script will ignore last modification dates.
- `DELETE_MERGED_BRANCHES`: Set to `True` to delete branches that have been merged into the main branch (default is `True`).
- `LAST_MODIFIED_CUTOFF`: The time threshold for branch inactivity, used only if `CHECK_LAST_MODIFIED_TIME` is set to `True`.
- `DEFAULT_BRANCH`: The main branch (e.g., `"main"` or `"master"`) to check against for merged branches.

## Usage

1. **Clone the repository** or download the script.
2. **Navigate to the repository** where you want to run the cleanup script.
3. **Run the script**:
    ```bash
    python git_branch_cleaner.py
    ```
4. **Select an option**:
    - `[D]`: Delete unused and merged branches. This will first delete unused local branches, then proceed to delete merged branches.
    - `[S]`: Additional actions (optional placeholder for other operations).
    - `[Q]`: Quit the script.

5. **Confirm Deletion**:
    - For each branch, the script will display the branch name, last modified or merged time, and prompt you with options:
        - **`y`**: Delete the branch.
        - **`n`**: Skip the branch.
        - **`q`**: Cancel the operation and return to the main menu.

## Creating an Alias for the Script

To make it easier to run this script, you can create an alias in your terminal. This allows you to run the script with a simple command like `branch-clean` instead of typing the full path each time.

1. **Open your shell profile**:
   - For **bash**: Open `~/.bashrc`
   - For **zsh**: Open `~/.zshrc`
   - For **fish**: Open `~/.config/fish/config.fish`

2. **Add the alias**:
   Add the following line, replacing `/path/to/git_branch_cleaner.py` with the full path to the script file:

   ```bash
   alias branch-clean='python /path/to/git_branch_cleaner.py'
   ```

3. **Save and apply**:
   - For **bash** and **zsh**: Run `source ~/.bashrc` or `source ~/.zshrc`.
   - For **fish**: Run `source ~/.config/fish/config.fish`.

4. **Run the script using the alias**:
   Now you can simply type:

   ```bash
   branch-clean
   ```

   This will execute the script using the alias.

## Requirements

- **Python 3.6+**
- **Git CLI**: Make sure Git is installed and available in your PATH.

## Example

```plaintext
[D] Delete unused and merged branches
[S] Something else
[Q] Quit

Select an option (D/S/Q): d

Searching for unused branches...

┌──────────────┬─────────────┐
│ Branch       │ Last Edited │
├──────────────┼─────────────┤
│ feature-x    │ 2023-01-15  │
└──────────────┴─────────────┘

Delete this branch locally? (y/n/q to cancel): y

Branch 'feature-x' deleted.

Searching for merged branches...

┌──────────────┬─────────────┐
│ Branch       │ Merge Time  │
├──────────────┼─────────────┤
│ feature-y    │ 2023-02-01  │
└──────────────┴─────────────┘

Delete this merged branch locally? (y/n/q to cancel): n
...
```

## License

This project is open-source and available under the MIT License.

## Contributions

Contributions are welcome! Feel free to submit issues or pull requests for new features or improvements.
