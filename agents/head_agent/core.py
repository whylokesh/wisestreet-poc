import json
from openai import OpenAI

# Import only the macro agent
# from agents.sub_agents.news_agent import run_news_agent
# from agents.sub_agents.sentiment_agent import run_sentiment_agent
# from agents.sub_agents.earnings_agent import run_earnings_agent
from agents.sub_agents.macro_agent import run_macro_agent
# from agents.sub_agents.valuation_agent import run_valuation_agent

# Define tools (only macro agent)
tools = [
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "run_news_agent",
    #         "description": "Summarizes recent financial, company, or macro news from multiple sources.",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "prompt": {
    #                     "type": "string",
    #                     "description": "A detailed instruction of the news topic to investigate (e.g., company, sector, region, theme)."
    #                 }
    #             },
    #             "required": ["prompt"]
    #         }
    #     }
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "run_sentiment_agent",
    #         "description": "Analyzes public sentiment from social media or forums about any financial or economic topic.",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "prompt": {
    #                     "type": "string",
    #                     "description": "Describe the asset, event, or topic whose sentiment you want analyzed."
    #                 }
    #             },
    #             "required": ["prompt"]
    #         }
    #     }
    # },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "run_earnings_agent",
    #         "description": "Summarizes the latest earnings report of a company, including revenue, EPS, and key metrics.",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "prompt": {
    #                     "type": "string",
    #                     "description": "Company name or ticker and optional time frame (e.g., 'Q2 earnings for Apple')"
    #                 }
    #             },
    #             "required": ["prompt"]
    #         }
    #     }
    # },
    {
        "type": "function",
        "function": {
            "name": "run_macro_agent",
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
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "run_valuation_agent",
    #         "description": "Estimates company valuation using P/E, DCF models, and peer comparisons.",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "prompt": {
    #                     "type": "string",
    #                     "description": "The company name or ticker to evaluate, and optionally any peers."
    #                 }
    #             },
    #             "required": ["prompt"]
    #         }
    #     }
    # }
]

# System prompt to define behavior of Head Agent
SYSTEM_PROMPT = """
You are WiseStreet, an intelligent financial research head agent.

Your job is to:
- Understand the user's financial question
- Break it into subtasks
- Call your expert sub-agents (news, sentiment, earnings, macro, valuation)
- Combine their responses into a final, smart recommendation

Each tool is a highly intelligent assistant — you don't fetch raw data, they do. You guide the workflow.

Use a loop of thinking → calling → observing → thinking again. Only stop when you are confident you've gathered enough to answer the user clearly.
"""

# Core loop of the Head Agent
def run_head_agent(user_query: str, client: OpenAI, model: str) -> str:
    chat_history = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]

    while True:
        response = client.chat.completions.create(
            model=model,
            messages=chat_history,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

       # 🔧 Handle tool calls
        if message.tool_calls:
            chat_history.append(message)  # 🟢 Append assistant message with tool_calls FIRST

            tool_messages = []
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                if tool_name == "run_macro_agent":
                    tool_result = run_macro_agent(args["prompt"], client, model)
                else:
                    tool_result = f"[Tool '{tool_name}' is not implemented yet]"

                tool_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": tool_result
                })

            chat_history.extend(tool_messages)  # 🟢 Append all tool messages AFTER assistant message

        # 💬 No tool call — final answer
        elif message.content:
            chat_history.append({"role": "assistant", "content": message.content})
            return message.content
