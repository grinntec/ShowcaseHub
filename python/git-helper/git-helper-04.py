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

#################################################################################################################################################
#################################################################################################################################################
#################################################################################################################################################

# ---- DEFINE THE GITHUB REPOSITORY ---- #
def initialize_repository():
    """
    Initialize the git repository and return the Repo object, the active branch name, and the latest tag.
    :return: Tuple[git.Repo, str, str]
    """
    repo_path = os.path.dirname(os.getcwd())  # Set the parent directory of the current working directory as the repository path

    try:
        # Initializing the repository and getting the active branch name
        repo = git.Repo(repo_path, search_parent_directories=True)  # This will find the repository root by searching parent directories
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

#################################################################################################################################################
#################################################################################################################################################
#################################################################################################################################################

# --- COMPARE LOCAL WITH ORIGIN ---- #
def compare_with_origin(repo, branch_name):
    """
    Compare the working directory and the checked-out version against the origin and report any differences.
    """
    try:
        repo.remotes.origin.fetch()
        
        # Check for uncommitted changes and untracked files in the working directory
        uncommitted_changes = repo.is_dirty()
        untracked_files = repo.untracked_files
        
        # Get the commit SHA of the local branch and the corresponding remote branch
        local_commit = repo.commit(branch_name)
        remote_commit = repo.commit(f'origin/{branch_name}')
        
        # Compare the commit SHAs and report any differences
        if local_commit.hexsha == remote_commit.hexsha and not uncommitted_changes and not untracked_files:
            return f"{ANSWER_TEXT}The working directory and the local branch {branch_name} are up to date with the origin.{RESET_TEXT}"
        else:
            differences = []
            guidance = []
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


#################################################################################################################################################
#################################################################################################################################################
#################################################################################################################################################
def main():
    repo, branch_name, latest_tag = initialize_repository()
    print(f"\n{BOLD_TEXT}--- Repository Information ---{RESET_TEXT}")
    print(f"{OUTPUT_TEXT}You are working in the {ANSWER_TEXT}{repo.working_tree_dir}{OUTPUT_TEXT} repository on the {ANSWER_TEXT}{branch_name}{OUTPUT_TEXT} branch. The latest tag (version) is {ANSWER_TEXT}{latest_tag}{RESET_TEXT}\n")
    
    while True:
        print(f"{BOLD_TEXT}--- Status ---{RESET_TEXT}")
        comparison_result = compare_with_origin(repo, branch_name)
        print(comparison_result)
        
        print(f"\n{BOLD_TEXT}--- Options ---{RESET_TEXT}")
        print(f"{OUTPUT_TEXT}1. Push unpushed commits{RESET_TEXT}")
        print(f"{OUTPUT_TEXT}2. Commit uncommitted changes{RESET_TEXT}")
        print(f"{OUTPUT_TEXT}3. Add untracked files{RESET_TEXT}")
        print(f"{OUTPUT_TEXT}4. Exit{RESET_TEXT}")
        
        user_choice = input(f"\n{QUESTION_TEXT}Enter the number of your choice: {RESET_TEXT}")
        
        print(f"{BOLD_TEXT}--- Execution Result ---{RESET_TEXT}")
        if user_choice == '1':
            try:
                repo.git.push('origin', branch_name)
                print(f"{ANSWER_TEXT}Unpushed commits have been pushed to the origin.{RESET_TEXT}")
            except Exception as e:
                print(f"{ERROR_TEXT}Error pushing commits: {e}{RESET_TEXT}")
        elif user_choice == '2':
            commit_message = input(f"{QUESTION_TEXT}Enter a commit message: {RESET_TEXT}")
            try:
                repo.git.add('.')  # Stage all changes
                repo.git.commit('-m', commit_message)
                print(f"{ANSWER_TEXT}Uncommitted changes have been committed.{RESET_TEXT}")
            except Exception as e:
                print(f"{ERROR_TEXT}Error committing changes: {e}{RESET_TEXT}")
        elif user_choice == '3':
            try:
                repo.git.add('.')
                print(f"{ANSWER_TEXT}Untracked files have been added.{RESET_TEXT}")
            except Exception as e:
                print(f"{ERROR_TEXT}Error adding files: {e}{RESET_TEXT}")
        elif user_choice == '4':
            sys.exit(0)  # Exit the script immediately
        else:
            print(f"{ERROR_TEXT}Invalid choice. Please enter a number between 1 and 4.{RESET_TEXT}")
        
        print(f"{BOLD_TEXT}-----------------------------{RESET_TEXT}\n")

if __name__ == "__main__":
    main()


#################################################################################################################################################
#################################################################################################################################################
#################################################################################################################################################