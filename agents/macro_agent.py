import json
from openai import OpenAI
from agents.tools.macro.tradingeconomics import get_macro_te
from agents.tools.macro.worldbank import get_macro_wb

SYSTEM_PROMPT = """
You are the MacroAgent of WiseStreet.
You gather macroeconomic indicators such as inflation, GDP, interest rates, and global events.
"""

def get_macro(prompt: str, client: OpenAI) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Analyze macroeconomic context for: {prompt}"}
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_macro_te",
                "description": "Gets macroeconomic data from Trading Economics.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Topic or country name"}
                    },
                    "required": ["prompt"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_macro_wb",
                "description": "Gets macroeconomic data from the World Bank.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {"type": "string", "description": "Topic or country name"}
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

            if tool_call.function.name == "get_macro_te":
                result = get_macro_te(args["prompt"])
            elif tool_call.function.name == "get_macro_wb":
                result = get_macro_wb(args["prompt"])
            else:
                result = "[Unknown macro source]"

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

    return message.content or "No macro data found."