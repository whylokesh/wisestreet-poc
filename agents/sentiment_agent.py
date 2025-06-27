import json
from openai import OpenAI
from agents.tools.sentiment.reddit import get_sentiment_reddit
from agents.tools.sentiment.youtube import get_sentiment_youtube

SYSTEM_PROMPT = """
You are the SentimentAgent of WiseStreet.
You analyze social media sentiment for financial topics using multiple tools.
"""

def get_sentiment(prompt: str, client: OpenAI) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Analyze sentiment for: {prompt}"}
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_sentiment_reddit",
                "description": "Fetches Reddit sentiment on a financial topic.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Topic or stock name"}
                    },
                    "required": ["prompt"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_sentiment_youtube",
                "description": "Fetches YouTube sentiment for a finance-related topic.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Topic or stock name"}
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

            if tool_name == "get_sentiment_reddit":
                tool_result = get_sentiment_reddit(args["prompt"])
            elif tool_name == "get_sentiment_youtube":
                tool_result = get_sentiment_youtube(args["prompt"])
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

    return message.content or "No sentiment found."