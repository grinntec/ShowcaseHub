# Version Bump and Change Log Script

This script automates the process of committing changes, bumping version numbers, and maintaining a changelog for a given Git repository. The script is interactive, prompting the user to make decisions at each step.

## Features
- **Detect and List Changes:** Detect and list changed and untracked files in the repository.
- **Interactive Addition of Changes:** Interactively add changed files to the staging area.
- **Commit Changes:** Commit the staged changes with a user-provided commit message.
- **Push to Remote:** Optionally push the commit to the remote repository.
- **Version Bumping:** Optionally bump the version (major, minor, or patch) and create a tag.
- **Changelog Update:** Update or create a `CHANGELOG.md` with the changes made, the new version number, and the date.
- **Changelog Commit:** Commit the updated `CHANGELOG.md`.

## Requirements
- Python 3.x
- GitPython package: Install using pip.
  ```sh
  pip install GitPython
  ```
- A local Git repository

## Usage
1. Place the script in an appropriate directory on your machine.
2. Adjust the `repo_path` variable in the script to point to your local Git repository.
3. Run the script using a Python interpreter.
   ```sh
   python <script_name>.py
   ```

### Steps
1. **Check for Changes:** The script will check for any uncommitted changes in the repository and list them.
2. **Stage Changes:** It will then ask whether you want to stage (add) these changes for commit. 
   - If yes, it will ask whether to stage all changes or specific ones.
3. **Commit Changes:** After staging, it will ask for a commit message and then commit the changes.
4. **Push Changes:** Optionally, you can choose to push these changes to the remote repository.
5. **Bump Version:** The script will then ask whether you want to bump the version.
   - If yes, it will ask for the type of version bump (major, minor, or patch) and create a new tag.
6. **Update Changelog:** Whether or not a version is bumped, it will update or create a `CHANGELOG.md` file with the details of the changes made and commit it.

## Notes
- Please make sure to adjust the `repo_path` variable in the script to point to the local path of your repository before running the script.
- Ensure that your working directory is clean or that you are aware of the changes before running the script to avoid unintended commits or tags.
- The script is interactive and will require user input at multiple steps, so please read the prompts carefully before responding.
