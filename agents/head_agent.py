import json
from openai import OpenAI

# Import all sub-agents
from agents.news_agent import get_news
from agents.sentiment_agent import get_sentiment
from agents.earnings_agent import get_earnings
from agents.macro_agent import get_macro
from agents.valuation_agent import get_valuation

# Define each sub-agent tool schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_news",
            "description": "Summarizes recent financial, company, or macro news from multiple sources.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "A detailed instruction of the news topic to investigate (e.g., company, sector, region, theme)."
                    }
                },
                "required": ["prompt"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_sentiment",
            "description": "Analyzes public sentiment from social media or forums about any financial or economic topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Describe the asset, event, or topic whose sentiment you want analyzed."
                    }
                },
                "required": ["prompt"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_earnings",
            "description": "Summarizes the latest earnings report of a company, including revenue, EPS, and key metrics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Company name or ticker and optional time frame (e.g., 'Q2 earnings for Apple')"
                    }
                },
                "required": ["prompt"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_macro",
            "description": "Provides macroeconomic insights, like inflation, GDP, interest rate trends or country-level events.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Describe the macroeconomic trend, region, or event to analyze."
                    }
                },
                "required": ["prompt"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_valuation",
            "description": "Estimates company valuation using P/E, DCF models, and peer comparisons.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The company name or ticker to evaluate, and optionally any peers."
                    }
                },
                "required": ["prompt"]
            }
        }
    }
]

# System prompt to define behavior of Head Agent
SYSTEM_PROMPT = """
You are WiseStreet, an intelligent financial research head agent.

Your job is to:
- Understand the user’s financial question
- Break it into subtasks
- Call your expert sub-agents (news, sentiment, earnings, macro, valuation)
- Combine their responses into a final, smart recommendation

Each tool is a highly intelligent assistant — you don’t fetch raw data, they do. You guide the workflow.

Use a loop of thinking → calling → observing → thinking again. Only stop when you are confident you’ve gathered enough to answer the user clearly.
"""

# Core loop of the Head Agent
def head_agent(user_query: str, client: OpenAI) -> str:
    chat_history = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]

    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=chat_history,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                # Dynamically map tool name to agent function
                if tool_name == "get_news":
                    tool_result = get_news(args["prompt"])
                elif tool_name == "get_sentiment":
                    tool_result = get_sentiment(args["prompt"])
                elif tool_name == "get_earnings":
                    tool_result = get_earnings(args["prompt"])
                elif tool_name == "get_macro":
                    tool_result = get_macro(args["prompt"])
                elif tool_name == "get_valuation":
                    tool_result = get_valuation(args["prompt"])
                else:
                    tool_result = f"[Tool '{tool_name}' is not implemented yet]"

                chat_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": tool_result
                })

        else:
            chat_history.append({"role": "assistant", "content": message.content})
            return message.content
