import argparse
import git

# Argument Parsing
parser = argparse.ArgumentParser(description='Bump version number of the repo.')
parser.add_argument('bump_type', choices=['major', 'minor', 'patch'], help='The type of version bump to perform')
args = parser.parse_args()

repo_path = r'C:\Users\212622123\github\212622123\tf_module-azure-resource-group'

repo = git.Repo(repo_path)

# Fetch all tags from remote
repo.remotes.origin.fetch(tags=True)

# Get the latest tag name
try:
    latest_tag = str(repo.tags[-1])
except IndexError:  # If there are no tags, start from 0.0.0
    latest_tag = '0.0.0'

major, minor, patch = map(int, latest_tag.split('.'))

# Bump the version based on the provided bump_type
if args.bump_type == 'major':
    major += 1
    minor = 0
    patch = 0
elif args.bump_type == 'minor':
    minor += 1
    patch = 0
else:  # patch
    patch += 1

new_tag = f'{major}.{minor}.{patch}'

# Create the new tag locally
repo.create_tag(new_tag)

# Push the new tag to the remote
repo.remotes.origin.push(new_tag)
