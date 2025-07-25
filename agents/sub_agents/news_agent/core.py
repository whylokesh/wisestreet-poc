import json
from openai import OpenAI
from .tools.news_tools import search_news, extract_news_content

SYSTEM_PROMPT = """
You are the NewsAgent of WiseStreet.

Your job is to:
- Investigate financial, economic, or company-specific news
- Search for the latest updates on any topic (using a web news API)
- If needed, dig deeper by reading the full content of specific articles

Use these two tools:
1. `search_news` — finds recent news headlines on a topic
2. `extract_news_content` — reads a full article from a given link
"""

TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "search_news",
                "description": "Searches recent news articles about a topic using NewsData.io.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Topic to search (e.g., 'Adani bonds')"},
                        "country": {"type": "string", "description": "Country code (e.g., 'in')"}
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "extract_news_content",
                "description": "Extracts the full text from a news article URL.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "URL of the article to analyze"}
                    },
                    "required": ["url"]
                }
            }
        }
    ]

def run_news_agent(prompt: str, client: OpenAI, model: str) -> str:
    print(f"🧠 [NewsAgent] Invoked with prompt: {prompt}")

    chat_history = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Find news and insights about: {prompt}"}
    ]

    while True:
        print("💬 [NewsAgent] Sending prompt to OpenAI...")

        response = client.chat.completions.create(
            model=model,
            messages=chat_history,
            tools=TOOLS,
            tool_choice="auto"
        )

        message = response.choices[0].message

        tool_responses = []

        if message.tool_calls:
            print("🛠️ [NewsAgent] Tool call(s) received.")

            chat_history.append(message)

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                print(f"🔧 [NewsAgent] Executing tool: {tool_name}")
                print(f"📥 [NewsAgent] With args: {args}")

                # Execute the tool
                if tool_name == "search_news":
                    result = search_news(args["query"], args.get("country", "in"))
                elif tool_name == "extract_news_content":
                    result = extract_news_content(args["url"])
                else:
                    result = f"[Unknown tool: {tool_name}]"

                print(f"📤 [NewsAgent] Result: {result[:200]}{'...' if len(result) > 200 else ''}")

                tool_responses.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": result
                })

            chat_history.extend(tool_responses)
            print("📚 [NewsAgent] Tool response(s) appended to history.")

        elif message.content:
            print("✅ [NewsAgent] Final answer ready.")
            chat_history.append({"role": "assistant", "content": message.content})
            return message.content