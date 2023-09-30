import os
import sys
import git
from semver import VersionInfo
import datetime

# ---- SET WORKING DIRECTORY ----
repo_path = '.'  # Current working directory
repo = git.Repo(repo_path, search_parent_directories=True)
print(f"You are working in the {repo.working_tree_dir} repository.\n")

# ---- CHECK CHANGED FILES ----
changed_files = [item.a_path for item in repo.index.diff(None)]
untracked_files = repo.untracked_files
if not changed_files and not untracked_files:
    print("No uncommitted changes detected.")

# --- CHECK UNPUSHED COMMITS ----
branch = repo.active_branch
tracking_branch = branch.tracking_branch()
if tracking_branch:
    diff = list(repo.iter_commits(f'{branch.name}..{tracking_branch.name}'))
    if diff:
        print(f"There are {len(diff)} commits not pushed to remote.")
else:
    print(f"No tracking branch set for {branch.name}.")

if not changed_files and not untracked_files and not diff:
    print("Exiting as there are no changes or unpushed commits.")
    sys.exit(0)

# ---- ASK TO STAGE CHANGES ----
response = input("\nDo you want to stage these changes? (yes/no): ").strip().lower()
if response.startswith('y'):
    repo.git.add(A=True)  # stages all changes (tracked and untracked)
elif response.startswith('n'):
    print("Exiting without staging changes.")
    sys.exit(0)
else:
    print("Invalid response. Please respond with 'yes' or 'no'.")
    sys.exit(1)

# ---- COMMIT CHANGES ----
commit_msg = input("Enter a commit message: ").strip()
if not commit_msg:
    print("Commit message is required. Exiting.")
    sys.exit(1)
repo.index.commit(commit_msg)

# ---- PUSH CHANGES ----
response = input("\nDo you want to push these changes to remote? (yes/no): ").strip().lower()
if response == 'yes':
    repo.remotes.origin.push()
elif response == 'no':
    print("Exiting without pushing changes.")
else:
    print("Invalid response. Exiting.")
    sys.exit(1)

# ---- ASK TO BUMP VERSION ----
response = input("\nDo you want to bump the version? (yes/no): ").strip().lower()
if response == 'yes':
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
elif response == 'no':
    print("Exiting without bumping version.")
else:
    print("Invalid response. Exiting.")
    sys.exit(1)

print("\nScript executed successfully.")
