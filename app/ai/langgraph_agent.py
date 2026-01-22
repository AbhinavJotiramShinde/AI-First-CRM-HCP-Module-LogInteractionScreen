from langgraph.graph import StateGraph
from app.ai.groq_client import get_llm
import json

llm = get_llm()

def extract_node(state: dict):
    user_input = state["input"]

    prompt = f"""
You are a pharma CRM assistant.

Return ONLY valid JSON. No markdown. No explanation.

Schema:
{{
  "hcp_name": "",
  "topics": [],
  "sentiment": "Positive|Neutral|Negative",
  "materials_shared": [],
  "samples_distributed": 0,
  "outcomes": [],
  "follow_ups": []
}}

Rules:
• Use "" for missing strings
• Use [] for missing lists
• Use 0 for missing numbers

Text:
\"\"\"{user_input}\"\"\"

Return JSON only.
"""

    result = llm.invoke(prompt)

    try:
        if isinstance(result.content, str):
            data = json.loads(result.content)
        else:
            data = result.content
    except Exception:
        data = {
            "hcp_name": "",
            "topics": [],
            "sentiment": "Neutral",
            "materials_shared": [],
            "samples_distributed": 0,
            "outcomes": [],
            "follow_ups": []
        }

    return {"output": data}


graph = StateGraph(dict)
graph.add_node("extract", extract_node)
graph.set_entry_point("extract")

agent = graph.compile()
