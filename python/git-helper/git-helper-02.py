import os
import sys
import git
import logging
import semver
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# ANSI escape codes for text colors and reset
BOLD_TEXT = '\033[1m'
UNDERLINE_TEXT = '\033[4m'
QUESTION_TEXT = '\033[96m\033[1m'  # Bold Cyan
ANSWER_TEXT = '\033[92m'  # Green
ERROR_TEXT = '\033[91m\033[1m'  # Bold Red
OUTPUT_TEXT = '\033[97m'  # White
HELP_TEXT = '\033[90m'  # Grey
RESET_TEXT = '\033[0m'  # Reset

def initialize_repository():
    """
    Initialize the git repository and return the Repo object, the active branch name, and the latest tag.
    :return: Tuple[git.Repo, str, str]
    """
    repo_path = '.'
    try:
        repo = git.Repo(repo_path, search_parent_directories=True)
        branch_name = repo.active_branch.name
        
        # Get the latest tag using semantic version sorting
        if repo.tags:
            latest_tag = max(repo.tags, key=lambda t: semver.VersionInfo.parse(t.name))
        else:
            latest_tag = "No tags available"
        
    except git.InvalidGitRepositoryError:
        logger.error(f"{ERROR_TEXT}Invalid Git repository: {repo_path}{RESET_TEXT}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"{ERROR_TEXT}Error initializing repository: {e}{RESET_TEXT}")
        sys.exit(1)
    return repo, branch_name, str(latest_tag)  # Convert TagReference to string to get the tag name

def main():
    repo, branch_name, latest_tag = initialize_repository()
    logger.info(f"\n{OUTPUT_TEXT}You are working in the {ANSWER_TEXT}{repo.working_tree_dir}{OUTPUT_TEXT} repository on the {ANSWER_TEXT}{branch_name}{OUTPUT_TEXT} branch. The latest tag (version) is {ANSWER_TEXT}{latest_tag}{RESET_TEXT}\n")

if __name__ == "__main__":
    main()
