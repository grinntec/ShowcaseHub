import git

repo_path = r'C:\Users\212622123\github\212622123\tf_module-azure-resource-group'

repo = git.Repo(repo_path)

# Correct way to fetch all tags from remote
repo.remotes.origin.fetch(tags=True)

# Get the latest tag name
try:
    latest_tag = str(repo.tags[-1])
except IndexError:  # If there are no tags, start from 0.0.0
    latest_tag = '0.0.0'

major, minor, patch = map(int, latest_tag.split('.'))

# Increment the patch version
new_tag = f'{major}.{minor}.{patch + 1}'

# Create the new tag locally
repo.create_tag(new_tag)

# Push the new tag to the remote
repo.remotes.origin.push(new_tag)
