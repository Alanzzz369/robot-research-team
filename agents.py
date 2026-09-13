import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def planner_node(state):
    topic = state["topic"]
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"Break this research topic into 3-5 clear, specific sub-questions. Topic: {topic}. Reply with only a numbered list, nothing else."
    )
    text = response.text
    subtopics = [line.split(".", 1)[1].strip() for line in text.split("\n") if line.strip() and line[0].isdigit()]
    state["subtopics"] = subtopics
    state["log"].append(f"Planner created {len(subtopics)} sub-questions.")
    return state


def researcher_node(state):
    findings = []
    for question in state["subtopics"]:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"Answer this research question thoroughly using what you know: {question}"
        )
        findings.append({"question": question, "answer": response.text})
        time.sleep(3)
    state["findings"] = findings
    state["log"].append(f"Researcher answered {len(findings)} questions.")
    return state


def critic_node(state):
    findings_text = "\n\n".join([f"Q: {f['question']}\nA: {f['answer']}" for f in state["findings"]])
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"Review this research for gaps or weak answers:\n\n{findings_text}\n\nReply with 'GOOD' if it's solid, or 'MORE: <what's missing>' if something needs more digging."
    )
    verdict = response.text.strip()
    state["critique"] = verdict
    state["needs_more_research"] = verdict.startswith("MORE")
    state["loop_count"] = state.get("loop_count", 0) + 1
    if state["loop_count"] >= 3:
        state["needs_more_research"] = False
    state["log"].append(f"Critic verdict: {verdict[:50]}...")
    time.sleep(3)
    return state


def writer_node(state):
    findings_text = "\n\n".join([f"Q: {f['question']}\nA: {f['answer']}" for f in state["findings"]])
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"Write a clean, well-organized report on '{state['topic']}' using this research:\n\n{findings_text}\n\nInclude a short intro, sections per subtopic, and a conclusion."
    )
    state["final_report"] = response.text
    state["log"].append("Writer finished the final report.")
    return state