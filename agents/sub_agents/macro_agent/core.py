import json
from openai import OpenAI
from .tools.macro_data_tools import (
    get_macro_indicators,
    get_economic_calendar,
    get_financial_news
)

SYSTEM_PROMPT = """
You are the MacroAgent of WiseStreet.

Your role is to:
- Analyze macroeconomic trends
- Retrieve current economic indicators
- Look up upcoming events and announcements
- Summarize recent macroeconomic and financial news

You have 3 tools at your disposal:
1. Macro Indicators (scraped from TradingEconomics)
2. Economic Calendar (scraped for latest events)
3. Financial News (latest country-level news via API)
"""

def run_macro_agent(prompt: str, client: OpenAI, model: str) -> str:

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_macro_indicators",
                "description": "Returns latest macro indicators (GDP, inflation, interest rate, etc.)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "country": {"type": "string", "description": "Country to fetch data for (default: India)"}
                    },
                    "required": ["country"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_economic_calendar",
                "description": "Returns upcoming macroeconomic events and reports.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "country": {"type": "string", "description": "Country to fetch calendar for (default: India)"}
                    },
                    "required": ["country"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_financial_news",
                "description": "Fetches recent macro/financial news headlines by country.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "country": {"type": "string", "description": "Country to get news for (default: India)"}
                    },
                    "required": ["country"]
                }
            }
        }
    ]

    chat_history = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Analyze macroeconomic context for: {prompt}"}
    ]

    while True:
        response = client.chat.completions.create(
            model=model,
            messages=chat_history,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if message.tool_calls:
            print("🛠️ Tool calls received.")

            # Append the assistant's tool_call message first
            chat_history.append(message)

            # Collect tool results
            tool_responses = []

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                country = args.get("country", "India")

                print(f"🔧 Calling tool: {tool_name} with country={country}")

                if tool_name == "get_macro_indicators":
                    result = get_macro_indicators(country)
                elif tool_name == "get_economic_calendar":
                    result = get_economic_calendar(country)
                elif tool_name == "get_financial_news":
                    result = get_financial_news(country)
                else:
                    result = "[Unknown tool]"

                tool_responses.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": result
                })

            # Append all tool responses together (AFTER the assistant tool_call message)
            chat_history.extend(tool_responses)

        elif message.content:
            chat_history.append({"role": "assistant", "content": message.content})
            return message.content
