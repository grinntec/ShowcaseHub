import git
import os
import datetime

repo_path = r'C:\Users\212622123\github\212622123\tf_module-azure-resource-group'
repo = git.Repo(repo_path)

# Initialize variables to hold commit message and changed files
commit_message = ""
changed_files = []

# Check for uncommitted changes
if repo.is_dirty(untracked_files=True):
    print("There are uncommitted changes in the repository.")

    # Ask the user if they want to add changes
    add_changes = input("Do you want to add changes? (y/n): ")
    if add_changes.lower() == 'y':
        # Ask the user if they want to add all changes or specify files
        add_all = input("Do you want to add all changes? (y/n): ")
        if add_all.lower() == 'y':
            changed_files = [item.a_path for item in repo.index.diff(None)] + repo.untracked_files
            repo.git.add(all=True)
        else:
            changed_files = input("Enter the names of the files you want to add, separated by space: ").split()
            repo.index.add(changed_files)

    # Print the captured changed files for debugging
    print("Changed Files: ", changed_files)

    # Ask the user for a commit message and commit the changes
    commit_message = input("Enter the commit message: ")
    repo.index.commit(commit_message)

    # Ask the user if they want to push the changes
    push_changes = input("Do you want to push the changes? (y/n): ")
    if push_changes.lower() == 'y':
        repo.remotes.origin.push('HEAD')

# If there is no commit message, prompt user for the description of the changes
if not commit_message:
    commit_message = input('Enter the description of the changes made in this version: ')

# Prompt user for the type of version bump
bump_type = input('Enter the type of version bump (major/minor/patch): ')
while bump_type not in ['major', 'minor', 'patch']:
    print('Invalid input. Please enter major, minor, or patch.')
    bump_type = input('Enter the type of version bump (major/minor/patch): ')

# Fetch all tags from remote
repo.remotes.origin.fetch(tags=True)

# Get the latest tag name
try:
    latest_tag = str(repo.tags[-1])
except IndexError:  # If there are no tags, start from 0.0.0
    latest_tag = '0.0.0'

major, minor, patch = map(int, latest_tag.split('.'))

# Bump the version based on the provided bump_type
if bump_type == 'major':
    major += 1
    minor = 0
    patch = 0
elif bump_type == 'minor':
    minor += 1
    patch = 0
else:  # patch
    patch += 1

new_tag = f'{major}.{minor}.{patch}'

# Confirmation
confirmation = input(f'You are about to bump the {bump_type} version and append the following changes to CHANGELOG.md:\n{commit_message}\nDo you want to proceed? (y/n): ')
if confirmation.lower() != 'y':
    print("Operation cancelled by user.")
    exit(1)

# Create the new tag locally
repo.create_tag(new_tag)

# Append the new changes to CHANGELOG.md
changelog_file = repo_path + '\\CHANGELOG.md'

# Check if CHANGELOG.md exists, if not create it
if not os.path.exists(changelog_file):
    with open(changelog_file, 'w') as file:
        file.write('# Changelog\n\n')

# Append the new changes to CHANGELOG.md
with open(changelog_file, 'a') as file:
    file.write(f'## [v{new_tag}] - {datetime.datetime.now().strftime("%Y-%m-%d")}\n')
    file.write(f'{commit_message}\n')
    if changed_files:
        file.write('Changed Files:\n')
        for file_name in changed_files:
            file.write(f'- {file_name}\n')
    file.write('\n')

# Commit the changelog changes
repo.index.add([changelog_file])
repo.index.commit(f'Update CHANGELOG.md for version v{new_tag}')

# Push the new tag and the commit to the remote
repo.remotes.origin.push(new_tag)
repo.remotes.origin.push('HEAD')
