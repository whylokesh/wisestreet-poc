import json
from openai import OpenAI
from .tools.alpha import get_news_alpha
from .tools.catcher import get_news_catcher

SYSTEM_PROMPT = """
You are the NewsAgent of WiseStreet.
You specialize in fetching and summarizing relevant financial or macroeconomic news using multiple sub-agent tools.

Your job is to think step-by-step, choose which news sub-agent to use, observe results, and return a clean summary.
"""

def run_news_agent(prompt: str, client: OpenAI, model: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Fetch news for: {prompt}"}
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "alpha_news_agent",
                "description": "Sub-agent that fetches financial news from Alpha Vantage based on topic.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Topic or query for news"}
                    },
                    "required": ["prompt"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "catcher_news_agent",
                "description": "Sub-agent that fetches financial news using NewsCatcher API.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Topic or query for news"}
                    },
                    "required": ["prompt"]
                }
            }
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            if tool_name == "alpha_news_agent":
                tool_result = get_news_alpha(args["prompt"])
            elif tool_name == "catcher_news_agent":
                tool_result = get_news_catcher(args["prompt"])
            else:
                tool_result = "[Unknown sub-agent]"

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": tool_result
            })

        final = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return final.choices[0].message.content

    return message.content or "No news found."
