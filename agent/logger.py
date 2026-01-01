# agent/logger.py

import datetime

def log(question, tool, args, result):
    with open("agent.log", "a") as f:
        f.write(f"""
{datetime.datetime.now()}
QUESTION: {question}
TOOL: {tool}
ARGS: {args}
RESULT: {result}
-------------------------
""")
