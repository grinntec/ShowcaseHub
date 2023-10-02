# Importing necessary libraries and modules
import os  # Provides a way of using operating system dependent functionality
import sys  # Provides access to some variables used or maintained by the Python interpreter and to functions that interact strongly with the interpreter
import git  # GitPython library, used for interacting with Git repositories
from semver import VersionInfo  # Importing VersionInfo class from semver library for semantic versioning
import datetime  # Provides classes for working with dates and times

# ---- ANSI escape codes for text colors and reset ---- #
BOLD_TEXT = '\033[1m'
UNDERLINE_TEXT = '\033[4m'
QUESTION_TEXT = '\033[96m\033[1m'  # Bold Cyan
ANSWER_TEXT = '\033[92m'  # Green
ERROR_TEXT = '\033[91m\033[1m'  # Bold Red
OUTPUT_TEXT = '\033[97m'  # White
HELP_TEXT = '\033[90m'  # Grey
RESET_TEXT = '\033[0m'  # Reset

# Example using the ANSI escape code in the text output
# print(f"\n{QUESTION_TEXT}What do you want to do?{RESET_TEXT}")

# Initialize the git repository and return the Repo object and the active branch name
def initialize_repository():
    repo_path = '.'  # Set the current working directory as the repository path
    try:
        # Initializing the repository and getting the active branch name
        repo = git.Repo(repo_path, search_parent_directories=True)
        branch_name = repo.active_branch.name
        
        # Get the latest tag
        if repo.tags:
            latest_tag = str(repo.tags[-1])  # Convert TagReference to string to get the tag name
        else:
            latest_tag = "No tags available"
        
    except Exception as e:
        # Print error message and exit if an exception occurs during initialization
        print(f"{ERROR_TEXT}Error initializing repository: {e}{RESET_TEXT}")
        sys.exit(1)
    return repo, branch_name, latest_tag  # Return the Repo object, the active branch name, and the latest tag

# Call the function
repo, branch_name, latest_tag = initialize_repository()

# Print the results
print(f"\n{OUTPUT_TEXT}You are working in the {ANSWER_TEXT}{repo.working_tree_dir}{OUTPUT_TEXT} repository on the {ANSWER_TEXT}{branch_name}{OUTPUT_TEXT} branch. The latest tag (version) is {ANSWER_TEXT}{latest_tag}{RESET_TEXT}\n")