import os
import sys
import semver
import git

# ---- SET WORKING DIRECTORY ----
repo_path = '.'  # Current working directory
repo = git.Repo(repo_path, search_parent_directories=True)

print(f"You are working in the {repo.working_tree_dir} repository.\n")





# ---- CHECK CHANGED FILES ----
# Check if there are any uncommitted changes
changed_files = [item.a_path for item in repo.index.diff(None)]
untracked_files = repo.untracked_files

print("Changed files:")
for file in changed_files:
    print(f"Modified: {file}")

print("\nUntracked files:")
for file in untracked_files:
    print(f"New file: {file}")






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

commit_msg = input("Enter a commit message: ").strip()
repo.index.commit(commit_msg)











# ---- ASK TO CHANGE VERSION ----
response = input("Do you want to bump the version? (yes/no): ").strip().lower()
if response.startswith('y'):
    # Retrieve tags and find the latest
    tags = sorted(repo.tags, key=lambda t: semver.parse_version_info(t.name))
    latest_tag = tags[-1] if tags else '0.0.0'

    # Ask the user what part of the version to bump
    response = input(f"Latest version is {latest_tag}. What part would you like to bump? (major/minor/patch): ").strip().lower()
    new_version = semver.bump_major(latest_tag.name) if response == 'major' else (
        semver.bump_minor(latest_tag.name) if response == 'minor' else semver.bump_patch(latest_tag.name))

    # Create new tag
    repo.create_tag(new_version)
    print(f"Created new tag: {new_version}")

    # Generate changelog
    with open("CHANGELOG.md", "a") as f:
        f.write(f"## {new_version}\n")
        f.write(f"{commit_msg}\n\n")
elif not response.startswith('n'):
    print("Invalid response. Please respond with 'yes' or 'no'.")
    sys.exit(1)











# ---- PUSH CHANGES TO GIT REPOSITORY ----
# Push changes
repo.git.push('origin', 'HEAD')
repo.git.push('origin', '--tags')
print("Changes pushed to remote repository.")

print("Script has finished executing.")
