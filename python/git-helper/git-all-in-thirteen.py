import os
import sys
import git
from semver import VersionInfo
import datetime

# ANSI escape codes for text colors and reset
BLUE_TEXT = '\033[94m'
GREEN_TEXT = '\033[92m'
RED_TEXT = '\033[91m'
YELLOW_TEXT = '\033[93m'
PURPLE_TEXT = '\033[95m'
CYAN_TEXT = '\033[96m'
RESET_TEXT = '\033[0m'

# ---- SET WORKING DIRECTORY ----
# ---- SET WORKING DIRECTORY ----
repo_path = '.'  # Current working directory
repo = git.Repo(repo_path, search_parent_directories=True)

# Print the repository working directory and active branch name with colors
print(f"\n{GREEN_TEXT}You are working in the {BLUE_TEXT}{repo.working_tree_dir}{GREEN_TEXT} repository on the {BLUE_TEXT}{repo.active_branch.name}{GREEN_TEXT} branch.{RESET_TEXT}\n")


# ---- CHECK CHANGED FILES ----
changed_files = [item.a_path for item in repo.index.diff(None)]
untracked_files = repo.untracked_files

if not changed_files and not untracked_files:
    print("No uncommitted changes detected.")
else:
    print(f"\n{GREEN_TEXT}Changed files:{RESET_TEXT}")
    for file in changed_files:
        print(f"{BLUE_TEXT}Modified: {file}{RESET_TEXT}")
        
    print(f"\n{GREEN_TEXT}Untracked files:{RESET_TEXT}")
    for file in untracked_files:
        print(f"{BLUE_TEXT}New file: {file}{RESET_TEXT}")


# --- CHECK UNPUSHED COMMITS ----
branch = repo.active_branch
tracking_branch = branch.tracking_branch()
unpushed_commits = []
if tracking_branch:
    unpushed_commits = list(repo.iter_commits(f'{branch.name}..{tracking_branch.name}'))
    if unpushed_commits:
        print(f"There are {len(unpushed_commits)} commits not pushed to remote.")
else:
    print(f"No tracking branch set for {branch.name}.")

if not changed_files and not untracked_files and not unpushed_commits:
    print(f"\n{RED_TEXT}Exiting as there are no changes or unpushed commits.{RESET_TEXT}\n")
    sys.exit(0)

# ---- ASK TO STAGE CHANGES ----
response = input("\nDo you want to stage these changes? (y/n): ").strip().lower()
if response.startswith('y'):
    repo.git.add(A=True)  # stages all changes (tracked and untracked)
elif response.startswith('n'):
    print(f"\n{RED_TEXT}Exiting without staging changes.{RESET_TEXT}\n")
    sys.exit(0)
else:
    print("Invalid response. Please respond with 'y' or 'n'.")
    sys.exit(1)

# ---- COMMIT CHANGES ----
commit_msg = input("\nEnter a commit message for example, Add new widget to app: \n").strip()
if not commit_msg:
    print("Commit message is required. Exiting.")
    sys.exit(1)
repo.index.commit(commit_msg)

# ---- PUSH CHANGES ----
response = input("\nDo you want to push these changes to the remote repository? (y/n): ").strip().lower()
if response.startswith('y'):
    repo.remotes.origin.push()
elif response.startswith('n'):
    print(f"\n{RED_TEXT}Exiting without pushing changes.{RESET_TEXT}\n")
else:
    print("Invalid response. Exiting.")
    sys.exit(1)

# ---- ASK TO BUMP VERSION ----
response = input("\nDo you want to bump the version? (y/n): ").strip().lower()
if response.startswith('y'):
    print("1. Major\n2. Minor\n3. Patch")
    response = input("Choose a version type to bump: ").strip().lower()
    if response not in ['1', '2', '3']:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    repo.remotes.origin.fetch(tags=True)
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    latest_tag = str(tags[-1]) if tags else '0.0.0'
    version = VersionInfo.parse(latest_tag)

    if response == '1':
        new_version = version.bump_major()
    elif response == '2':
        new_version = version.bump_minor()
    elif response == '3':
        new_version = version.bump_patch()

    repo.create_tag(str(new_version))
    repo.remotes.origin.push(tags=True)

    changelog_file = 'CHANGELOG.md'
    with open(changelog_file, 'a') as f:
        f.write(f"\n## [{new_version}] - {datetime.datetime.utcnow().strftime('%Y-%m-%d')}\n")
        f.write(f"- {commit_msg}\n")
    repo.index.add(changelog_file)
    repo.index.commit(f"Update {changelog_file} for version {new_version}")
    repo.remotes.origin.push()
elif response.startswith('n'):
    print("Exiting without bumping version.")
else:
    print("Invalid response. Exiting.")
    sys.exit(1)

print("\nScript executed successfully.")
