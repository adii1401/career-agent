import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

SYSTEM_PROMPT = """You are a Resume Tailoring Expert. Rewrite a candidate's resume bullets to better match a specific job description.

Rules:
- Never fabricate experience or skills that don't exist in the original resume
- Reorder and reword existing bullets to highlight relevant experience
- Use keywords from the JD naturally
- Keep bullets concise and achievement-focused
- Use action verbs

Return exactly these sections:

## Tailored Professional Summary
2-3 sentences targeting this specific role using JD keywords.

## Tailored AI Projects Section
Rewritten project bullets emphasizing aspects relevant to this JD.

## Tailored Experience Bullets
Rewritten work experience bullets highlighting relevant skills.

## Keywords Added
List of JD keywords successfully incorporated.

## What NOT to Change
Sections that are already well-targeted and should stay as-is."""

def tailor_resume(resume_text: str, jd_text: str, jd_analysis: str) -> str:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"""Tailor this resume for the job description.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

JD ANALYSIS (key requirements):
{jd_analysis}""")
    ]

    response = llm.invoke(messages)
    return response.content

if __name__ == "__main__":
    sample_resume = """
    Aditya Kumar Gupta — AI Automation Engineer
    3+ years at Cognizant in MFT/EDI and B2B integration.

    AI Projects:
    - MFT Operations Agent: LangGraph, FastAPI, ChromaDB, LLaMA 3.3, Docker, HF Spaces
    - MFT Email Responder: RAG, ChromaDB, Microsoft Graph API, Streamlit

    Experience:
    - Configured Seeburger BIS MFT for Hartford insurance, managing 50+ trading partners
    - Built Python automation saving 20+ hours per person per week
    - Developed EDI mappings and data transformations

    Skills: Python, LangGraph, FastAPI, ChromaDB, RAG, Groq, Docker, Git
    """

    sample_jd = """
    AI Automation Engineer - Build LLM-powered applications using Python, FastAPI, LangChain.
    Deploy on cloud platforms. Work with RAG pipelines and vector databases.
    Experience with enterprise integration a plus.
    """

    sample_jd_analysis = """
    Required: Python, LangChain/LangGraph, FastAPI, LLMs, Docker, Git
    Nice to have: ChromaDB, RAG, Cloud
    Keywords: AI Automation, LLM pipelines, enterprise integration, deployment
    """

    print(tailor_resume(sample_resume, sample_jd, sample_jd_analysis))