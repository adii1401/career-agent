import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

SYSTEM_PROMPT = """You are a Career Gap Analyzer. Compare a candidate's resume against a job description analysis and provide an honest gap assessment.

Return exactly these sections:

## Fit Score
A score from 0-100 with one line explanation.

## Strong Matches
Skills and experiences from the resume that directly match the JD requirements.

## Gaps
Skills required by the JD that are missing or weak in the resume. Be honest.

## Partial Matches
Skills where the candidate has related but not exact experience.

## Competitive Advantages
Unique things in the resume that make this candidate stand out for this role.

## Recommendation
Should they apply? Strong Yes / Yes / Maybe / No — with one paragraph explanation.

Be honest and direct. Do not sugarcoat gaps."""

def analyze_gap(resume_text: str, jd_analysis: str) -> str:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"""Compare this resume against the job requirements.

RESUME:
{resume_text}

JD ANALYSIS:
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
    
    Skills: Python, LangGraph, FastAPI, ChromaDB, RAG, Groq, Docker, Git, Seeburger BIS, EDI
    """

    sample_jd_analysis = """
    ## Required Skills
    - Python, LangChain/LangGraph, FastAPI, LLMs, Docker, Git
    ## Nice to Have
    - ChromaDB, RAG, Cloud (AWS/GCP/Azure)
    ## Seniority Level: Mid (2-5 years)
    ## Keywords: AI Automation, Python, LangChain, FastAPI, LLM, Docker
    """

    print(analyze_gap(sample_resume, sample_jd_analysis))