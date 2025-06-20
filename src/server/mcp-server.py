
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
# if not token_path.exists():
#     print("No token file found. First run will require Google authentication via browser.")

# Set environment variables for MCP
env = os.environ.copy()
env["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_path)
env["TOKEN_PATH"] = str(token_path)  # custom env var supported by some forks
env["GOOGLE_CALENDAR_MCP_TOKEN_PATH"] = str(token_path)  # custom env var supported by some forks 

def start_mcp_google_calendar():
    
    #enable this to get token file created
    #mcp_index_js = project_dir / "node_modules" / "mcp-google-calendar" / "dist" / "index.js"
    
    mcp_index_js = project_dir / "node_modules" / "google-calendar-mcp" / "dist" / "index.js"
    # Validate file presence
    if not mcp_index_js.exists():
        raise FileNotFoundError(f"Cannot find MCP entry file: {mcp_index_js}")
    
    # Run the MCP server
    print("Starting MCP Google Calendar using Node.js...\n")
    process = subprocess.Popen(
        ["node", str(mcp_index_js)],
        cwd=project_dir,
        env=env,
        shell=True
    )
    process.wait()
    print("Still running...")

if __name__ == "__main__":  

    #rename mcp-google-calendar-token.json to token.json
    token_file = project_dir / "mcp-google-calendar-token.json"
    if token_file.exists():
        token_file.rename(token_path)              
        print(f"Token file created and renamed to: {token_path}")
  
    print("MCP authentication setup complete.")
    print("Starting MCP Google Calendar server...\n")
    start_mcp_google_calendar()
