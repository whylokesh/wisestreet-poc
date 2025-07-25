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

TOOLS = [
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

def run_macro_agent(prompt: str, client: OpenAI, model: str) -> str:
    print(f"🧠 [MacroAgent] Invoked with prompt: {prompt}")

    chat_history = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Analyze macroeconomic context for: {prompt}"}
    ]

    while True:
        print("💬 [MacroAgent] Sending prompt to OpenAI...")

        response = client.chat.completions.create(
            model=model,
            messages=chat_history,
            tools=TOOLS,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # 🛠️ Handle tool calls
        if message.tool_calls:
            print("🛠️ [MacroAgent] Tool call(s) received.")
            chat_history.append(message)

            tool_responses = []

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                country = args.get("country", "India")

                print(f"🔧 [MacroAgent] Calling tool: {tool_name} with country={country}")

                # 🧠 Execute the tool
                if tool_name == "get_macro_indicators":
                    result = get_macro_indicators(country)
                elif tool_name == "get_economic_calendar":
                    result = get_economic_calendar(country)
                elif tool_name == "get_financial_news":
                    result = get_financial_news(country)
                else:
                    result = "[Unknown tool]"

                print(f"📤 [MacroAgent] Result: {result[:200]}{'...' if len(result) > 200 else ''}")

                tool_responses.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": result
                })

            chat_history.extend(tool_responses)
            print("📚 [MacroAgent] Tool responses appended to history.")

        # ✅ Final message from assistant
        elif message.content:
            print("✅ [MacroAgent] Final answer ready.")
            chat_history.append({"role": "assistant", "content": message.content})
            return message.content