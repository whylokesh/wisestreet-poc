import json
from openai import OpenAI
from agents.tools.earnings.alpha import get_earnings_alpha

SYSTEM_PROMPT = """
You are the EarningsAgent of WiseStreet.
You specialize in extracting company earnings data like revenue, EPS, and YoY trends.
"""

def get_earnings(prompt: str, client: OpenAI) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Get earnings for: {prompt}"}
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_earnings_alpha",
                "description": "Fetches earnings data (revenue, EPS, etc.) from Alpha Vantage.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Company name or ticker"}
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
        tool_call = message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)

        tool_result = get_earnings_alpha(args["prompt"])

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_call.function.name,
            "content": tool_result
        })

        final = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return final.choices[0].message.content

    return message.content or "No earnings data found."