import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

SYSTEM_PROMPT = """You are a Job Description Analyzer. Extract and structure key information from job descriptions.

Analyze the JD and return a structured analysis with exactly these sections:

## Role Summary
One line describing the role.

## Required Skills
List every required technical skill, tool, language, framework mentioned.

## Nice to Have
List optional/preferred skills.

## Seniority Level
Junior / Mid / Senior / Lead — based on years of experience and responsibilities.

## Key Responsibilities
Top 5 responsibilities in bullet points.

## Red Flags
Any concerning requirements (unrealistic expectations, too many skills, etc.)

## Keywords for Resume
Top 10 ATS keywords from this JD that should appear in a tailored resume.

Be precise and extract only what is explicitly stated in the JD."""

def analyze_jd(jd_text: str) -> str:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Analyze this job description:\n\n{jd_text}")
    ]
    
    response = llm.invoke(messages)
    return response.content

if __name__ == "__main__":
    sample_jd = """
    AI Automation Engineer - 2-5 years experience
    We are looking for an AI Engineer to build and deploy LLM-powered applications.
    
    Required:
    - Python programming
    - LangChain or LangGraph experience
    - FastAPI for building REST APIs
    - Experience with LLMs (OpenAI, Groq, or similar)
    - Docker and deployment experience
    - Git version control
    
    Nice to have:
    - ChromaDB or vector databases
    - RAG pipeline experience
    - Cloud experience (AWS/GCP/Azure)
    - Enterprise integration experience
    
    Responsibilities:
    - Build AI-powered automation tools
    - Design and implement LLM pipelines
    - Deploy applications to cloud platforms
    - Collaborate with cross-functional teams
    - Write clean, documented code
    """
    print(analyze_jd(sample_jd))