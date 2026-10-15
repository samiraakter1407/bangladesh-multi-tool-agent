
from pathlib import Path
import sys

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

# Configure project paths and environment variables
SRC_DIR = str(Path(__file__).resolve().parent)
PROJECT_DIR = Path(__file__).resolve().parent.parent

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

load_dotenv(PROJECT_DIR / ".env")

from hospital_tool import hospitals_db_tool
from institution_tool import institutions_db_tool
from restaurant_tool import restaurants_db_tool
from web_search_tool import web_search_tool


# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    max_retries=3,
)

# Register all four tools
tools = [
    hospitals_db_tool,
    institutions_db_tool,
    restaurants_db_tool,
    web_search_tool,
]

system_prompt = """
You are a helpful Bangladesh Multi-Tool Assistant.

Available tools:
- hospitals_db_tool: Search healthcare facilities in Bangladesh.
- institutions_db_tool: Search educational institutions in Bangladesh.
- restaurants_db_tool: Search restaurants in Bangladesh.
- web_search_tool: Search the web for general and current information.

Rules:
- Use the appropriate database tool for questions about hospitals,
  educational institutions, or restaurants.
- Use web_search_tool for general knowledge, policies, and current facts.
- Use multiple tools when a question requires multiple sources.
- Never invent results or claim a tool was used if it was not.
- Explain relevant limitations in the available data.
- Respond in the user's language when practical.
- Give clear, direct answers based on the tool results.
"""

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt,
)


def extract_text(content):
    """Extract readable text from a LangChain message."""
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text = item.get("text", "")
                if text:
                    parts.append(text)
        return "\n".join(parts)

    return str(content)


if __name__ == "__main__":
    question = input(
        "Ask the Bangladesh Multi-Tool Assistant: "
    ).strip()

    if not question:
        print("Please enter a question.")
    else:
        print("\nAgent is processing your question...\n")

        try:
            final_state = agent.invoke(
                {
                    "messages": [
                        {"role": "user", "content": question}
                    ]
                }
            )

            messages = final_state.get("messages", [])

            # Display the tools actually called
            called_tools = []
            for message in messages:
                for tool_call in getattr(message, "tool_calls", []):
                    name = tool_call.get("name", "unknown")
                    called_tools.append(name)

            if called_tools:
                for name in called_tools:
                    print(f"[TOOL CALLED] {name}")
            else:
                print("[INFO] No tools were called.")

            # Find the final assistant response
            answer = ""
            for message in reversed(messages):
                if getattr(message, "type", "") == "ai":
                    answer = extract_text(message.content)
                    if answer.strip():
                        break

            print("\nAssistant:\n")
            print(answer or "The agent returned no text response.")

        except Exception as error:
            print(f"\nAgent error: {error}")
