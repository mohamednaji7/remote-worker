import os
import subprocess
import sys
import logging

# Configure logging to output plain text to stdout
logging.basicConfig(
    level=logging.DEBUG,       # Set the minimum logging level
    format="%(message)s",     # Text-only format
    stream=sys.stdout,        # Redirect all logs to stdout
)


def clone_or_update_repo(REPO_URL, REPO_NAME):
    """
    Clone or update a repository.
    
    Args:
        REPO_URL (str): URL of the repository
        REPO_NAME (str): Name of the repository directory
    """
    if os.path.exists(REPO_NAME):
        # Update existing repository
        logging.info(f"Updating repository {REPO_NAME}")
        os.chdir(REPO_NAME)
        subprocess.run(['git', 'pull'], check=True)
        os.chdir('..')
    else:
        # Clone repository
        logging.info(f"Cloning repository {REPO_NAME}")
        subprocess.run(['git', 'clone', REPO_URL, REPO_NAME], check=True)
def run_script(repo_name, script_dir, script_name):
    """
    Run a script in a specified directory.
    
    Args:
        repo_name (str): Name of the repository
        script_dir (str): Directory containing the script
        script_name (str): Name of the script to run
    """
    script_path = os.path.join(repo_name, script_dir, script_name)
    script_dir_path = os.path.join(repo_name, script_dir)
    
    logging.info(f"Executing script: {script_path}")
    
    try:
        # Change to the script directory
        os.chdir(script_dir_path)
        
        # Run the script
        result = subprocess.run(
            [sys.executable, script_name],
            text=True,
            check=True
        )
        
 
    except subprocess.CalledProcessError as e:
        # Log any stderr output or error messages
        logging.error("Script Execution Failed:")
        logging.error(e.stderr.strip() if e.stderr else "No additional error details available.")
        raise  # Re-raise the exception for further handling
    finally:
        # Change back to the original working directory
        os.chdir('..')

def main():
    # Retrieve environment variables
    REPO_URL = os.environ.get('REPO_URL')
    REPO_NAME = os.environ.get('REPO_NAME')
    SCRIPT_DIR = os.environ.get('SCRIPT_DIR')
    SCRIPT_NAME = os.environ.get('SCRIPT_NAME')
    
    # Validate environment variables
    if not all([REPO_URL, REPO_NAME, SCRIPT_DIR, SCRIPT_NAME]):
        logging.error("Error: Missing required environment variables")
        # sys.exit(1)
        # return 
        logging.info("Fallback to tempelate handler!")
        result = subprocess.run(
            [sys.executable, '/src/handler.py'],
            text=True,
            check=True
        )
        logging.info(result)



    
    # Store original working directory
    ORIGINAL_DIR = os.getcwd()
    
    try:
        # Clone or update repository
        clone_or_update_repo(REPO_URL, REPO_NAME)
        
        # Run the specified script
        run_script(REPO_NAME, SCRIPT_DIR, SCRIPT_NAME)
    
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing command: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        # Return to original working directory
        os.chdir(ORIGINAL_DIR)

if __name__ == "__main__":
    main()

