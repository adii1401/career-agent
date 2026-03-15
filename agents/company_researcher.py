import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from tavily import TavilyClient

load_dotenv()

SYSTEM_PROMPT = """You are a Company Research Agent. Analyze the provided search results and produce a structured company intelligence briefing.

Structure your response as:
## Company Overview
## Recent News
## Tech Stack
## Culture & Values  
## Business Model
## Why Work Here

Be concise, factual, and cite sources where relevant."""

def research_company(company_name: str) -> str:
    tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

    # Step 1: Search for company info directly
    print(f"Searching for {company_name}...")
    
    search1 = tavily.search(query=f"{company_name} company overview business", max_results=3)
    search2 = tavily.search(query=f"{company_name} tech stack engineering technology", max_results=3)
    search3 = tavily.search(query=f"{company_name} recent news 2025 2026", max_results=3)

    # Step 2: Compile search results
    all_results = []
    for results in [search1, search2, search3]:
        for r in results["results"]:
            all_results.append(f"Source: {r['url']}\n{r['content']}")

    compiled = "\n\n---\n\n".join(all_results)

    # Step 3: LLM analyzes and structures the results
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Company to research: {company_name}\n\nSearch Results:\n{compiled}")
    ]

    response = llm.invoke(messages)
    return response.content

if __name__ == "__main__":
    print(research_company("Cognizant Technology Solutions"))