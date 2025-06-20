
import subprocess
import os
from pathlib import Path

# Set working directory to your script directory
project_dir = Path(__file__).resolve().parent
credentials_path = project_dir / "credentials.json"
token_path = project_dir / "token.json"

# Validate file presence
if not credentials_path.exists():
    raise FileNotFoundError(f"Missing credentials.json at: {credentials_path}")
if not token_path.exists():
    print("No token file found. First run will require Google authentication via browser.")

# Set environment variables for MCP
env = os.environ.copy()
env["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_path)
env["TOKEN_PATH"] = str(token_path)  # custom env var supported by some forks
env["GOOGLE_CALENDAR_MCP_TOKEN_PATH"] = str(token_path)  # custom env var supported by some forks 

def setupMCPServerAuth():
    # Set working directory to your script directory
    project_dir = Path(__file__).resolve().parent
    credentials_path = project_dir / "credentials.json"
    token_path = project_dir / "token.json"

    # check the file creation time for token.json if it is more than 1 hour run the authentication again
    if token_path.exists():
        token_creation_time = token_path.stat().st_mtime        
        print(f"Token creation time: {token_creation_time}")
        current_time = os.path.getmtime(__file__)
        if (current_time - token_creation_time) > 3600:
            print("Token file is older than 1 hour, re-authenticating...")
            token_path.unlink()
            mcp_index_js = project_dir / "node_modules" / "mcp-google-calendar" / "dist" / "index.js"
    else:
        print("Token file not found, running authentication setup...")
        mcp_index_js = project_dir / "node_modules" / "mcp-google-calendar" / "dist" / "index.js"
    
    # Run the MCP server
    print("Starting MCP Google Calendar Auth\n")
    process = subprocess.Popen(
        ["node", str(mcp_index_js)],
        cwd=project_dir,
        env=env,
        shell=True
    )

if __name__ == "__main__":
    setupMCPServerAuth()
