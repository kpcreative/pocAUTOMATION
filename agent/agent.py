# import os
# import json
# from dotenv import load_dotenv
# from openai import OpenAI

# from agent.system_prompt import SYSTEM_PROMPT
# from agent.tool_registry import TOOLS
# from agent.validator import validate_params, validate_result
# from agent.logger import log

# load_dotenv()

# BYTEZ_API_KEY = os.getenv("BYTEZ_API_KEY")
# MODEL_NAME = os.getenv("BYTEZ_MODEL", "openai/gpt-oss-20b")

# if not BYTEZ_API_KEY:
#     raise RuntimeError("BYTEZ_API_KEY missing")

# client = OpenAI(
#     api_key=BYTEZ_API_KEY,
#     base_url="https://api.bytez.com/models/v2/openai/v1"
# )

# def run_agent(question: str):
#     messages = [
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {"role": "user", "content": question}
#     ]

#     for _ in range(5):  # safety loop
#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=messages,
#             tools=[{
#                 "type": "function",
#                 "function": {
#                     "name": name,
#                     "parameters": {
#                         "type": "object",
#                         "properties": {},
#                         "required": meta["required"]
#                     }
#                 }
#             } for name, meta in TOOLS.items()],
#             tool_choice="auto",
#             temperature=0
#         )

#         msg = response.choices[0].message

#         # TOOL CALL
#         if msg.tool_calls:
#             for call in msg.tool_calls:
#                 tool_name = call.function.name
#                 args = json.loads(call.function.arguments)

#                 tool = TOOLS.get(tool_name)
#                 if not tool:
#                     return f"Unknown tool: {tool_name}"

#                 ok, err = validate_params(args, tool["required"])
#                 if not ok:
#                     return f"Clarification needed: {err}"

#                 result = tool["function"](**args)
#                 if not validate_result(result):
#                     return "I cannot answer due to insufficient data."

#                 log(question, tool_name, args, result)

#                 messages.append(msg)
#                 messages.append({
#                     "role": "tool",
#                     "tool_call_id": call.id,
#                     "content": json.dumps(result, default=str)
#                 })
#             continue

#         return msg.content

#     return "Unable to answer after multiple attempts."
import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

from agent.system_prompt import SYSTEM_PROMPT
from agent.tool_registry import TOOLS
from agent.validator import validate_params, validate_result
from agent.logger import log

# =================================================
# ENV
# =================================================
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.0-flash"

# =================================================
# CONVERSATION STATE (GENERALIZED)
# =================================================
session_state = {
    "entities": {
        "po": None,
        "supplier": None,
        "service": None,
        "gr": None,
    },
    "facts": {},
    "last_focus": None,     # po | supplier | service | delivery | reconciliation
}

# =================================================
# TOOL REGISTRATION
# =================================================
function_declarations = []
for name, meta in TOOLS.items():
    function_declarations.append(
        types.FunctionDeclaration(
            name=name,
            description=meta["description"],
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={k: types.Schema(type=types.Type.STRING) for k in meta["parameters"]},
                required=list(meta["parameters"].keys()),
            ),
        )
    )
tool = types.Tool(function_declarations=function_declarations)

# =================================================
# SERIALIZER (SAFE)
# =================================================
def serialize(obj):
    try:
        import pandas as pd, numpy as np
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient="records")
        if isinstance(obj, np.generic):
            return obj.item()
    except Exception:
        pass

    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [serialize(v) for v in obj]
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return str(obj)

# =================================================
# ENTITY + FOCUS RESOLUTION (CORE LOGIC)
# =================================================
def resolve_context(question: str):
    q = question.lower()

    # Explicit PO
    po_match = re.findall(r"\b45\d{7}\b", question)
    if po_match:
        session_state["entities"]["po"] = po_match[-1]
        session_state["last_focus"] = "po"
        return

    # Explicit supplier
    if "supplier" in q:
        session_state["last_focus"] = "supplier"
        return

    # Explicit service
    if "service" in q:
        session_state["last_focus"] = "service"
        return

    # Delivery / quantity
    if any(k in q for k in ["delivered", "delivery", "quantity", "pending"]):
        session_state["last_focus"] = "delivery"
        return

    # Reconciliation
    if "reconcil" in q:
        session_state["last_focus"] = "reconciliation"
        return

    # Conversational reference
    if any(w in q for w in ["above", "that", "this", "same", "it"]):
        return  # keep last_focus

# =================================================
# MEMORY UPDATE
# =================================================
def update_memory(tool_name, args, result):
    if "po_number" in args:
        session_state["entities"]["po"] = args["po_number"]
        session_state["last_focus"] = "po"

    if isinstance(result, dict):
        if "SUPPLIER_ID" in result:
            session_state["entities"]["supplier"] = result["SUPPLIER_ID"]

        for k in ["ORDERED_QTY", "DELIVERED_QTY", "PENDING_QTY", "DELIVERY_STATUS"]:
            if k in result:
                session_state["facts"][k] = result[k]

# =================================================
# MAIN AGENT
# =================================================
def run_agent(question: str) -> str:
    resolve_context(question)

    memory_block = f"""
Conversation State:
Entities: {session_state["entities"]}
Facts: {session_state["facts"]}
Current Focus: {session_state["last_focus"]}

Rules:
- Use current focus if user says "above / this / that / it"
- Do NOT ask for PO/supplier/service if already known
- Only ask clarification if entity is truly missing
"""

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=question)]
        )
    ]

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT + "\n" + memory_block,
        tools=[tool],
        temperature=0
    )

    while True:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=config
        )

        if not response.function_calls:
            return response.text

        contents.append(response.candidates[0].content)

        parts = []
        for call in response.function_calls:
            tool_name = call.name
            args = call.args or {}

            if tool_name not in TOOLS:
                continue

            ok, _ = validate_params(args, list(TOOLS[tool_name]["parameters"].keys()))
            if not ok:
                continue

            result = TOOLS[tool_name]["function"](**args)
            if not validate_result(result):
                continue

            log(question, tool_name, args, result)
            update_memory(tool_name, args, result)

            parts.append(
                types.Part.from_function_response(
                    name=tool_name,
                    response={"result": serialize(result)}
                )
            )

        if not parts:
            return "I need more context to proceed."

        contents.append(types.Content(role="tool", parts=parts))
