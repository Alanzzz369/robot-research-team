from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json
from graph import graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/research-stream")
def research_stream(topic: str):
    def event_generator():
        initial_state = {
            "topic": topic,
            "subtopics": [],
            "findings": [],
            "critique": "",
            "needs_more_research": False,
            "loop_count": 0,
            "final_report": "",
            "log": []
        }
        for step in graph.stream(initial_state):
            node_name = list(step.keys())[0]
            node_state = step[node_name]
            payload = {
                "node": node_name,
                "log": node_state.get("log", [])[-1] if node_state.get("log") else "", 
                "final_report": node_state.get("final_report", "")
            }
            yield f"data: {json.dumps(payload)}\n\n"
        yield "data: {\"node\": \"done\"}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

app.mount("/", StaticFiles(directory="static", html=True), name="static")