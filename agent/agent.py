import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from agent.system_prompt import SYSTEM_PROMPT
from agent.tool_registry import TOOLS
from agent.validator import validate_params, validate_result
from agent.logger import log

load_dotenv()

BYTEZ_API_KEY = os.getenv("BYTEZ_API_KEY")
MODEL_NAME = os.getenv("BYTEZ_MODEL", "openai/gpt-oss-20b")

if not BYTEZ_API_KEY:
    raise RuntimeError("BYTEZ_API_KEY missing")

client = OpenAI(
    api_key=BYTEZ_API_KEY,
    base_url="https://api.bytez.com/models/v2/openai/v1"
)

def run_agent(question: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    for _ in range(5):  # safety loop
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=[{
                "type": "function",
                "function": {
                    "name": name,
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": meta["required"]
                    }
                }
            } for name, meta in TOOLS.items()],
            tool_choice="auto",
            temperature=0
        )

        msg = response.choices[0].message

        # TOOL CALL
        if msg.tool_calls:
            for call in msg.tool_calls:
                tool_name = call.function.name
                args = json.loads(call.function.arguments)

                tool = TOOLS.get(tool_name)
                if not tool:
                    return f"Unknown tool: {tool_name}"

                ok, err = validate_params(args, tool["required"])
                if not ok:
                    return f"Clarification needed: {err}"

                result = tool["function"](**args)
                if not validate_result(result):
                    return "I cannot answer due to insufficient data."

                log(question, tool_name, args, result)

                messages.append(msg)
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result, default=str)
                })
            continue

        return msg.content

    return "Unable to answer after multiple attempts."
