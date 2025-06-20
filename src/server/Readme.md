***All the script are tested on Windows with Powershell*** 
## Run the Server

-  Get in src folder 
```
    cd .\src\
```
- Authenticate to Google Calendar
```python
 python .\mcp-server-auth.py
```
If you feel the terminal it stuck try couple of Ctrl+C

- Run server script

```python
python mcp-server.py

```
- Open another Powershell terminal, run below API. Your server must be running

```
(Invoke-WebRequest http://localhost:3000/mcp/calendars).Content
```

# Server API 

- Get list of all the API which MCP server can server
```
 (Invoke-WebRequest http://localhost:3000/mcp/info).Content
```
***Sample out is available at src\api\mcp-info.json***