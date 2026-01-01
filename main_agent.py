from agent.agent import run_agent

while True:
    q = input("\nAsk SAP MM question (or exit): ")
    if q.lower() == "exit":
        break
    print("\n", run_agent(q))
