import git
import os
import datetime

# Prompt user for the type of version bump
bump_type = input('Enter the type of version bump (major/minor/patch): ')
while bump_type not in ['major', 'minor', 'patch']:
    print('Invalid input. Please enter major, minor, or patch.')
    bump_type = input('Enter the type of version bump (major/minor/patch): ')

# Prompt user for the description of the changes
changes = input('Enter the description of the changes made in this version: ')

repo_path = r'C:\Users\212622123\github\212622123\tf_module-azure-resource-group'
repo = git.Repo(repo_path)

# Check for uncommitted changes
if repo.is_dirty(untracked_files=True):
    print("There are uncommitted changes in the repository. Please commit them before proceeding.")
    exit(1)

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

# Prompt user for confirmation
confirmation = input(f'You are about to bump the {bump_type} version and append the following changes to CHANGELOG.md:\n{changes}\nDo you want to proceed? (y/n): ')
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
    file.write(f'{changes}\n\n')

# Commit the changelog changes
repo.index.add([changelog_file])
repo.index.commit(f'Update CHANGELOG.md for version v{new_tag}')

# Push the new tag and the commit to the remote
repo.remotes.origin.push(new_tag)
repo.remotes.origin.push('HEAD')
