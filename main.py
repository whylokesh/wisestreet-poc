import os
from openai import OpenAI
from dotenv import load_dotenv

from agents.head_agent import run_head_agent  # ✅ Now active

load_dotenv() 

def test_openai_api(user_query: str, client: OpenAI, model: str) -> str:
    """
    You are a helpful AI assistant. Answer the user query in a polite and respectful way.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": user_query}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error while calling OpenAI API: {e}"


def main():
    print("🧠 Welcome to WiseStreet - Your AI Investment Research Assistant\n")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Please set the OPENAI_API_KEY environment variable.")
        return

    model = os.getenv("OPENAI_MODEL")  # Default to gpt-4o if not set
    client = OpenAI(api_key=api_key)

    while True:
        try:
            user_query = input("🧾 Ask a financial question (or type 'exit' to quit):\n> ")
            if user_query.lower() in ["exit", "quit"]:
                print("👋 Exiting WiseStreet. See you soon.")
                break

            print("\n💡 Thinking...\n")
            # 🔁 Core workflow - uses macro agent for now
            answer = run_head_agent(user_query, client, model)
            # For test purposes only:
            # answer = test_openai_api(user_query, client, model)

            print(f"\n✅ Answer:\n{answer}\n")

        except KeyboardInterrupt:
            print("\n👋 Exiting WiseStreet. Goodbye!")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}\n")

if __name__ == "__main__":
    main()
