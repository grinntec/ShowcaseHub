import os
import sys
import git
import logging
import semver
from semver import VersionInfo
import datetime
from enum import Enum

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

class UserChoice(Enum):
    PUSH = '1'
    COMMIT = '2'
    ADD = '3'
    TAG = '4'
    EXIT = '5'

def initialize_repository():
    repo_path = os.path.dirname(os.getcwd())
    try:
        repo = git.Repo(repo_path, search_parent_directories=True)
        branch_name = repo.active_branch.name
        latest_tag = max(repo.tags, key=lambda t: semver.VersionInfo.parse(t.name)) if repo.tags else "No tags available"
    except git.InvalidGitRepositoryError:
        logger.error(f"{ERROR_TEXT}Invalid Git repository: {repo_path}{RESET_TEXT}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"{ERROR_TEXT}Error initializing repository: {e}{RESET_TEXT}")
        sys.exit(1)
    return repo, branch_name, str(latest_tag)

def compare_with_origin(repo, branch_name):
    try:
        repo.remotes.origin.fetch()
        uncommitted_changes = repo.is_dirty()
        untracked_files = repo.untracked_files
        local_commit = repo.commit(branch_name)
        remote_commit = repo.commit(f'origin/{branch_name}')
        
        if local_commit.hexsha == remote_commit.hexsha and not uncommitted_changes and not untracked_files:
            return f"{ANSWER_TEXT}The working directory and the local branch {branch_name} are up to date with the origin.{RESET_TEXT}"
        
        differences, guidance = [], []
        if local_commit.hexsha != remote_commit.hexsha:
            unpushed_commits = list(repo.iter_commits(f'origin/{branch_name}..{branch_name}'))
            formatted_unpushed_commits = '\n'.join([f"{OUTPUT_TEXT}  - {commit.message.strip()}{RESET_TEXT}" for commit in unpushed_commits])
            differences.append(f"{ERROR_TEXT}There are unpushed commits:{RESET_TEXT}\n{formatted_unpushed_commits}")
            guidance.append("Consider pushing your commits to synchronize with the remote repository.")
        if uncommitted_changes:
            modified_files = repo.git.diff('--name-only').splitlines()
            formatted_modified_files = '\n'.join([f"{OUTPUT_TEXT}  - {file}{RESET_TEXT}" for file in modified_files])
            differences.append(f"{ERROR_TEXT}There are uncommitted changes in the working directory:{RESET_TEXT}\n{formatted_modified_files}")
            guidance.append("Consider committing or stashing your changes before synchronizing with the remote repository.")
        if untracked_files:
            formatted_untracked_files = '\n'.join([f"{OUTPUT_TEXT}  - {file}{RESET_TEXT}" for file in untracked_files])
            differences.append(f"{ERROR_TEXT}There are untracked files:{RESET_TEXT}\n{formatted_untracked_files}")
            guidance.append("Consider adding new files to the repository or updating the .gitignore file if these files should not be tracked.")
        
        differences_str = '\n'.join(differences)
        guidance_str = '\n'.join(guidance)
        return f"{ERROR_TEXT}{differences_str}{RESET_TEXT}\n\n{HELP_TEXT}Guidance:\n{guidance_str}{RESET_TEXT}"
    except Exception as e:
        return f"{ERROR_TEXT}Error comparing with the origin: {e}{RESET_TEXT}"

def log_repository_info(repo, branch_name, latest_tag):
    logger.info(f"\n{BOLD_TEXT}--- Repository Information ---{RESET_TEXT}")
    logger.info(f"{OUTPUT_TEXT}You are working in the {ANSWER_TEXT}{repo.working_tree_dir}{OUTPUT_TEXT} repository on the {ANSWER_TEXT}{branch_name}{OUTPUT_TEXT} branch. The latest tag (version) is {ANSWER_TEXT}{latest_tag}{RESET_TEXT}\n")

def log_status(comparison_result):
    logger.info(f"{BOLD_TEXT}--- Status ---{RESET_TEXT}")
    logger.info(comparison_result)

def log_options():
    logger.info(f"\n{BOLD_TEXT}--- Options ---{RESET_TEXT}")
    for choice in UserChoice:
        logger.info(f"{OUTPUT_TEXT}{choice.value}. {choice.name.capitalize().replace('_', ' ').lower()}{RESET_TEXT}")

def get_user_choice():
    return input(f"\n{QUESTION_TEXT}Enter the number of your choice: {RESET_TEXT}")

def log_separator():
    logger.info(f"{BOLD_TEXT}-----------------------------{RESET_TEXT}\n")

def push_commits(repo, branch_name):
    try:
        repo.git.push('origin', branch_name)
        logger.info(f"{ANSWER_TEXT}Unpushed commits have been pushed to the origin.{RESET_TEXT}")
    except Exception as e:
        logger.error(f"{ERROR_TEXT}Error pushing commits: {e}{RESET_TEXT}")

def commit_changes(repo):
    commit_message = input(f"{QUESTION_TEXT}Enter a commit message: {RESET_TEXT}")
    try:
        repo.git.add('.')  # Stage all changes
        repo.git.commit('-m', commit_message)
        logger.info(f"{ANSWER_TEXT}Uncommitted changes have been committed.{RESET_TEXT}")
    except Exception as e:
        logger.error(f"{ERROR_TEXT}Error committing changes: {e}{RESET_TEXT}")

def add_files(repo):
    try:
        repo.git.add('.')
        logger.info(f"{ANSWER_TEXT}Untracked files have been added.{RESET_TEXT}")
    except Exception as e:
        logger.error(f"{ERROR_TEXT}Error adding files: {e}{RESET_TEXT}")

def tag_version(repo, latest_tag):
    current_version = VersionInfo.parse(latest_tag if latest_tag != "No tags available" else '0.0.0')
    logger.info(f"{OUTPUT_TEXT}Current version: {ANSWER_TEXT}{current_version}{RESET_TEXT}")
    logger.info(f"{OUTPUT_TEXT}1. Increment major version{RESET_TEXT}")
    logger.info(f"{OUTPUT_TEXT}2. Increment minor version{RESET_TEXT}")
    logger.info(f"{OUTPUT_TEXT}3. Increment patch version{RESET_TEXT}")
    
    version_choice = input(f"{QUESTION_TEXT}Enter the number of your choice: {RESET_TEXT}")
    if version_choice == '1':
        new_version = current_version.bump_major()
    elif version_choice == '2':
        new_version = current_version.bump_minor()
    elif version_choice == '3':
        new_version = current_version.bump_patch()
    else:
        logger.error(f"{ERROR_TEXT}Invalid choice. Please enter a number between 1 and 3.{RESET_TEXT}")
        return
    
    diff = repo.git.diff()
    repo.create_tag(str(new_version))
    
    with open('CHANGELOG.md', 'a') as f:
        f.write(f"\n## {new_version} - {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
        changes = input(f"{QUESTION_TEXT}Enter the changes included in this version (separate multiple changes with commas): {RESET_TEXT}")
        f.write(', '.join(changes.split(',')) + f"\n\n### Diff:\n```\n{diff}\n```\n")
    
    logger.info(f"{ANSWER_TEXT}A new version {new_version} has been tagged and the changelog has been updated.{RESET_TEXT}")

def main():
    repo, branch_name, latest_tag = initialize_repository()
    log_repository_info(repo, branch_name, latest_tag)
    
    while True:
        log_status(compare_with_origin(repo, branch_name))
        log_options()
        
        user_choice = get_user_choice()
        
        if user_choice == UserChoice.PUSH.value:
            push_commits(repo, branch_name)
        elif user_choice == UserChoice.COMMIT.value:
            commit_changes(repo)
        elif user_choice == UserChoice.ADD.value:
            add_files(repo)
        elif user_choice == UserChoice.TAG.value:
            tag_version(repo, latest_tag)
        elif user_choice == UserChoice.EXIT.value:
            sys.exit(0)
        else:
            logger.error(f"{ERROR_TEXT}Invalid choice. Please enter a valid number.{RESET_TEXT}")
        
        log_separator()

if __name__ == "__main__":
    main()
