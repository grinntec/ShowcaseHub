import os
import sys
import semver
import git

# ---- SET WORKING DIRECTORY ----
repo_path = '.'  # Current working directory
repo = git.Repo(repo_path, search_parent_directories=True)

print(f"You are working in the {repo.working_tree_dir} repository.\n")






# ---- CHECK CHANGED FILES ----
# Check for changes in the repository
changed_files = [item.a_path for item in repo.index.diff(None)]
untracked_files = repo.untracked_files

if not changed_files and not untracked_files:
    print("No changes detected. Exiting.")
    exit(0)

print("\nChanged files:")
for file in changed_files:
    print(f"Modified: {file}")

print("\nUntracked files:")
for file in untracked_files:
    print(f"New file: {file}")

# ---- ASK TO STAGE CHANGES ----
# Confirm with user to stage files
response = input("\nDo you want to stage these changes? (yes/no): ").strip().lower()
if response.startswith('y'):
    repo.git.add(A=True)  # stages all changes (tracked and untracked)
elif response.startswith('n'):
    print("Exiting without staging changes.")
    sys.exit(0)
else:
    print("Invalid response. Please respond with 'yes' or 'no'.")
    sys.exit(1)
# Get commit message from user and commit changes
commit_msg = input("\nEnter a commit message: ").strip()
if not commit_msg:
    print("Commit message is required. Exiting.")
    exit(1)

# Confirm with user to push changes
response = input("\nDo you want to push these changes to remote? (yes/no): ").strip().lower()
if response == 'yes':
    repo.git.push()



# ---- ASK TO CHANGE VERSION ----
# Confirm with user to bump version
response = input("\nDo you want to bump the version? (yes/no): ").strip().lower()
if response == 'yes':
    print("1. Major\n2. Minor\n3. Patch")
    response = input("Choose a version type to bump: ").strip().lower()
    if response not in ['1', '2', '3']:
        print("Invalid choice. Exiting.")
        exit(1)

    # Fetch tags and get the latest tag (version)
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

    # Tag the new version and push tags to remote
    repo.create_tag(str(new_version))
    repo.remotes.origin.push('--tags')

    # Update CHANGELOG.md
    changelog_file = 'CHANGELOG.md'
    with open(changelog_file, 'a') as f:
        f.write(f"\n## [{new_version}] - {datetime.datetime.utcnow().strftime('%Y-%m-%d')}\n")
        f.write(f"- {commit_msg}\n")


# ---- PUSH CHANGES TO GIT REPOSITORY ----
    # Commit CHANGELOG.md
    repo.index.add(changelog_file)
    repo.index.commit(f"Update {changelog_file} for version {new_version}")
    repo.remotes.origin.push()

print("\nScript executed successfully.")