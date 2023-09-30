import os
import sys
import semver
import git
from semver import VersionInfo
import datetime

repo_path = '.'
repo = git.Repo(repo_path, search_parent_directories=True)

print(f"You are working in the {repo.working_tree_dir} repository.\n")

changed_files = [item.a_path for item in repo.index.diff(None)]
untracked_files = repo.untracked_files

if not changed_files and not untracked_files:
    print("No changes detected. Exiting.")
    sys.exit(0)

print("\nChanged files:")
for file in changed_files:
    print(f"Modified: {file}")

print("\nUntracked files:")
for file in untracked_files:
    print(f"New file: {file}")

response = input("\nDo you want to stage these changes? (yes/no): ").strip().lower()
if response.startswith('y'):
    repo.git.add(A=True)
elif response.startswith('n'):
    print("Exiting without staging changes.")
    sys.exit(0)
else:
    print("Invalid response. Please respond with 'yes' or 'no'.")
    sys.exit(1)

commit_msg = input("\nEnter a commit message: ").strip()
if not commit_msg:
    print("Commit message is required. Exiting.")
    sys.exit(1)

repo.index.commit(commit_msg)

response = input("\nDo you want to bump the version? (yes/no): ").strip().lower()
if response == 'yes':
    print("1. Major\n2. Minor\n3. Patch")
    response = input("Choose a version type to bump: ").strip().lower()

    if response not in ['1', '2', '3']:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    repo.remotes.origin.fetch('--tags')
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
    repo.remotes.origin.push('--tags')

    changelog_file = 'CHANGELOG.md'
    with open(changelog_file, 'a') as f:
        f.write(f"\n## [{new_version}] - {datetime.datetime.utcnow().strftime('%Y-%m-%d')}\n")
        f.write(f"- {commit_msg}\n")
    repo.index.add(changelog_file)
    repo.index.commit(f"Update {changelog_file} for version {new_version}")

# Push changes whether or not the version was bumped
repo.remotes.origin.push()

print("\nScript executed successfully.")
