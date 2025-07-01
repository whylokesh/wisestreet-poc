import json
from openai import OpenAI
from .tools.reddit import get_sentiment_reddit
from .tools.youtube import get_sentiment_youtube

SYSTEM_PROMPT = """
You are the SentimentAgent of WiseStreet.
You analyze social sentiment around finance using multiple specialized sub-agents.
"""

def run_sentiment_agent(prompt: str, client: OpenAI, model: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Analyze sentiment for: {prompt}"}
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "reddit_sentiment_agent",
                "description": "Sub-agent that analyzes Reddit sentiment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Topic or asset"}
                    },
                    "required": ["prompt"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "youtube_sentiment_agent",
                "description": "Sub-agent that analyzes YouTube sentiment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Topic or asset"}
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

            if tool_name == "reddit_sentiment_agent":
                tool_result = get_sentiment_reddit(args["prompt"])
            elif tool_name == "youtube_sentiment_agent":
                tool_result = get_sentiment_youtube(args["prompt"])
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

    return message.content or "No sentiment found."
