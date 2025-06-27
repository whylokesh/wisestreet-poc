import json
from openai import OpenAI
from agents.tools.news.alpha import get_news_alpha
from agents.tools.news.catcher import get_news_catcher

SYSTEM_PROMPT = """
You are the NewsAgent of WiseStreet.
You specialize in fetching and summarizing relevant financial or macroeconomic news using multiple tools.

Your job is to think step-by-step, choose which news tool to use, observe results, and return a clean summary.
"""

def get_news(prompt: str, client: OpenAI) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Fetch news for: {prompt}"}
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_news_alpha",
                "description": "Fetches financial news from Alpha Vantage based on topic.",
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
                "name": "get_news_catcher",
                "description": "Fetches financial news using NewsCatcher API.",
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
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            if tool_name == "get_news_alpha":
                tool_result = get_news_alpha(args["prompt"])
            elif tool_name == "get_news_catcher":
                tool_result = get_news_catcher(args["prompt"])
            else:
                tool_result = "[Unknown tool]"

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_name,
                "content": tool_result
            })

        final = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return final.choices[0].message.content

    return message.content or "No news found."