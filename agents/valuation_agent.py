import json
from openai import OpenAI
from agents.tools.valuation.alpha import get_valuation_alpha
from agents.tools.valuation.fmp import get_valuation_fmp

SYSTEM_PROMPT = """
You are the ValuationAgent of WiseStreet.
You estimate fair value of stocks using valuation models, P/E ratios, and peer comparisons.
"""

def get_valuation(prompt: str, client: OpenAI) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Estimate valuation for: {prompt}"}
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_valuation_alpha",
                "description": "Fetches valuation metrics like P/E from Alpha Vantage.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Company name or ticker"}
                    },
                    "required": ["prompt"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_valuation_fmp",
                "description": "Fetches fair value estimation using FMP.",
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
        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments)

            if tool_call.function.name == "get_valuation_alpha":
                result = get_valuation_alpha(args["prompt"])
            elif tool_call.function.name == "get_valuation_fmp":
                result = get_valuation_fmp(args["prompt"])
            else:
                result = "[Unknown valuation tool]"

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.function.name,
                "content": result
            })

        final = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return final.choices[0].message.content

    return message.content or "No valuation data found."