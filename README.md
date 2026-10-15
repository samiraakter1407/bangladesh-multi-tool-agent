# Bangladesh Multi-Tool AI Agent

A multi-tool AI assistant that answers questions about Bangladesh using three local SQLite databases and web search. Built with Python, LangChain, Google Gemini, and Tavily.

## Project Overview

The agent selects the appropriate tool based on the user's question:

- **Hospitals Database:** Searches healthcare facilities in Bangladesh.
- **Educational Institutions Database:** Searches schools, colleges, and other educational institutions.
- **Restaurants Database:** Searches restaurants using available names, locations, ratings, and review data.
- **Web Search Tool:** Retrieves information about general knowledge, policies, definitions, and current topics.

Google Gemini powers the agent's reasoning and tool selection. LangChain connects the model to the four tools, while SQLite stores the local datasets.

## Architecture

```text
User Question
     |
     v
Google Gemini + LangChain Agent
     |
     +-- Hospital Database Tool
     |
     +-- Institution Database Tool
     |
     +-- Restaurant Database Tool
     |
     +-- Tavily Web Search Tool
     |
     v
Final Answer
```

## Technologies Used

- Python
- LangChain
- LangChain Google GenAI
- Google Gemini API
- SQLite
- Pandas
- Tavily Search API
- python-dotenv

## Project Structure

```text
bangladesh-multi-tool-agent/
├── data/
│   ├── raw/
│   └── processed/
├── databases/
│   ├── hospitals.db
│   ├── institutions.db
│   └── restaurants.db
├── src/
│   ├── agent.py
│   ├── hospital_tool.py
│   ├── institution_tool.py
│   ├── restaurant_tool.py
│   ├── web_search_tool.py
│   ├── inspect_data.py
│   ├── prepare_data.py
│   ├── build_databases.py
│   ├── verify_databases.py
│   └── test_*.py
├── .env.example
├── .gitignore
└── README.md
```

## Datasets

This project uses the following datasets from Hugging Face:

1. [Institutional Information of Bangladesh](https://huggingface.co/datasets/Mahadih534/Institutional-Information-of-Bangladesh)
2. [All Bangladeshi Hospitals](https://huggingface.co/datasets/Mahadih534/all-bangladeshi-hospitals)
3. [Bangladeshi Restaurant Data](https://huggingface.co/datasets/Mahadih534/Bangladeshi-Restaurant-Data)

The datasets are processed into CSV files and stored in separate SQLite databases.

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/samiraakter1407/bangladesh-multi-tool-agent.git
cd bangladesh-multi-tool-agent
```

### 2. Install dependencies

Use Python 3.13 or another compatible Python version.

```bash
python -m pip install -U pandas langchain langchain-core langchain-google-genai langchain-tavily python-dotenv
```

### 3. Configure API keys

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Obtain your Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey) and your Tavily API key from [Tavily](https://app.tavily.com/).

**Never commit your actual API keys to GitHub.**

### 4. Run the agent

From the project root, execute:

```bash
python src/agent.py
```

Enter a question when prompted. The agent will select a relevant database or web-search tool and return an answer.

## Example Queries

### Hospitals

- Find 5 hospitals or healthcare facilities in Dhaka.
- Search for specialized healthcare facilities in Bangladesh.

### Educational Institutions

- Find 5 colleges in Dhaka, Bangladesh.
- Search for educational institutions by location and type.

### Restaurants

- Find 5 restaurants in Dhaka with a rating of at least 4.0.
- Search for restaurants by name or location.

### Web Search

- What are the main responsibilities of the Directorate General of Health Services (DGHS) in Bangladesh?
- Explain the role of the Ministry of Health and Family Welfare in Bangladesh.

### Multi-Tool Questions

The agent can use more than one tool when a question requires information from multiple sources.

## Testing

The project includes scripts for inspecting datasets, preparing CSV files, building SQLite databases, and verifying database contents.

Individual tool tests are available in the `src/` directory. The main agent can be tested interactively using `python src/agent.py`.

## Limitations

- Results depend on the completeness and accuracy of the source datasets.
- Location matching may include nearby administrative areas or locations with similar names.
- Available fields differ across datasets; for example, bed counts and doctor counts are not available as reliable fields in the supplied hospital dataset.
- Web-search results may contain irrelevant or outdated information and should be checked against authoritative sources.
- API access, model availability, and usage limits depend on the respective providers.

## Future Improvements

- Improve location filtering and result validation.
- Add more robust error handling and API retry strategies.
- Improve source attribution for web-search responses.
- Add an interactive web interface.
- Expand automated testing and documentation.

## License

No license has been specified yet. Check the source dataset licenses and choose a suitable project license before redistributing the code or data.
