# API Server to receive GitHub webhook events and control the agent's workflow

import uvicorn
from fastapi import FastAPI, Request
from app.graph.workflow import app as agent_app
from app.tools.github_tools import github_tools

app = FastAPI()

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    config = {"configurable": {"thread_id": data["run_id"]}}
    input_data = {
        "messages": [("user", f"Fix the test failure in {data['repository']} file src/__tests__/App.test.tsx")],
        "tools": github_tools,
        **data
    }
    # Starts the agent, it will pause before applying the fix
    agent_app.invoke(input_data, config)
    print(f"Agent paused for Run ID: {data['run_id']}. Waiting for /approve.")
    return {"message": "Agent initiated and paused for approval"}

@app.post("/approve")
async def approve(run_id: str):
    config = {"configurable": {"thread_id": run_id}}
    # Resume the graph
    agent_app.invoke(None, config)
    return {"message": "Fix approved and pushed!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
