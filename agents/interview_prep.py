import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

SYSTEM_PROMPT = """You are an Interview Preparation Coach. Generate targeted interview questions and suggested answers based on a job description and candidate's resume.

Return exactly these sections:

## Technical Questions
5 technical questions likely to be asked based on the JD requirements.
For each: Question → Suggested Answer (based on candidate's actual experience)

## Behavioral Questions
3 behavioral questions relevant to this role.
For each: Question → Suggested Answer using STAR format (Situation, Task, Action, Result)

## Questions to Ask the Interviewer
5 smart questions the candidate should ask — shows research and genuine interest.

## Watch Out For
2-3 topics where the candidate has gaps — how to handle these honestly in the interview.

Base suggested answers strictly on the candidate's actual resume experience. Never fabricate."""

def generate_interview_prep(resume_text: str, jd_text: str, company_research: str) -> str:
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"""Generate interview prep for this candidate.

CANDIDATE RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

COMPANY RESEARCH:
{company_research}""")
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
    
    Skills: Python, LangGraph, FastAPI, ChromaDB, RAG, Groq, Docker, Git
    """

    sample_jd = """
    AI Automation Engineer - Build LLM-powered applications using Python, FastAPI, LangChain.
    Deploy on cloud platforms. Work with RAG pipelines and vector databases.
    """

    sample_company = """
    Company focuses on enterprise AI automation. 
    Recently expanded into generative AI products.
    Tech stack includes Python, cloud infrastructure, and LLM integrations.
    """

    print(generate_interview_prep(sample_resume, sample_jd, sample_company))