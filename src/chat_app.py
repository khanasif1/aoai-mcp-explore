import streamlit as st
import openai
import requests
import json

# --- Configuration ---
AZURE_OPENAI_ENDPOINT = "https://ai-agent-hub-service.openai.azure.com/"
AZURE_OPENAI_KEY = "5GIz4N7z4JZbuEnDLiPSlkCuv0oBbaroPnD8Rbj8w482hzvR7XgMJQQJ99BEACHYHv6XJ3w3AAAAACOGQFZh"
DEPLOYMENT_NAME = "gpt-4.1"
MCP_SERVER_URL = "http://localhost:3000/mcp/"

# --- Set up OpenAI client ---
openai.api_type = "azure"
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_key = AZURE_OPENAI_KEY
openai.api_version = "2023-07-01-preview"

# --- Define available functions ---
function_definitions = [
    {
        "name": "calendars",
        "description": "List all available Google Calendars",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "list_upcoming_events",
        "description": "List upcoming events from a calendar",
        "parameters": {
            "type": "object",
            "properties": {
                "calendarId": {"type": "string"},
                "maxResults": {"type": "integer", "default": 5}
            },
            "required": ["calendarId"]
        }
    },
    {
        "name": "create_event",
        "description": "Create an event in a Google Calendar",
        "parameters": {
            "type": "object",
            "properties": {
                "calendarId": {"type": "string"},
                "summary": {"type": "string"},
                "start": {"type": "string", "description": "Start time in RFC3339"},
                "end": {"type": "string", "description": "End time in RFC3339"}
            },
            "required": ["calendarId", "summary", "start", "end"]
        }
    },
    {
        "name": "delete_event",
        "description": "Delete an event from a calendar",
        "parameters": {
            "type": "object",
            "properties": {
                "calendarId": {"type": "string"},
                "eventId": {"type": "string"}
            },
            "required": ["calendarId", "eventId"]
        }
    }
]

# --- Function to call MCP server ---
# --- Function to call MCP server ---
def call_mcp(function_name, parameters):
    print(f"Calling MCP function: {function_name} with parameters: {parameters}")
    payload = {
        "function": function_name,
        "parameters": parameters
    }
    print(f"Payload for MCP: {MCP_SERVER_URL} with data: {payload}")
    response = requests.get(f"{MCP_SERVER_URL}{function_name}", json=payload)
    return response.json()

# --- Streamlit UI ---
st.set_page_config(page_title="Google Calendar Chat App", layout="wide")
st.title("📅 Google Calendar AI Assistant (via MCP + Azure OpenAI)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask about your calendar (list, create, delete events)...")

if user_input:
    messages = [
        {"role": "system", "content": "You are a helpful assistant that talks to the Google Calendar MCP server via function calls."},
    ] + st.session_state.chat_history + [
        {"role": "user", "content": user_input}
    ]

    response = openai.ChatCompletion.create(
        deployment_id=DEPLOYMENT_NAME,
        model="gpt-4-1106-preview",
        messages=messages,
        functions=function_definitions,
        function_call="auto"
    )

    choice = response["choices"][0]
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    if choice.get("finish_reason") == "function_call":
        func_call = choice["message"]["function_call"]
        func_name = func_call["name"]
        func_args = json.loads(func_call["arguments"])

        mcp_result = call_mcp(func_name, func_args)
        reply = f"**Function `{func_name}` executed.**\n\n```json\n{json.dumps(mcp_result, indent=2)}\n```"
    else:
        reply = choice["message"]["content"]

    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.markdown(reply)

# --- Display full history ---
with st.expander("🧾 Chat History"):
    for msg in st.session_state.chat_history:
        st.write(f"**{msg['role'].capitalize()}**: {msg['content']}")
