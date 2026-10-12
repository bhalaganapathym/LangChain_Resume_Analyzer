import os
import json
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Load environment variables
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
HTML_DIR = BASE_DIR / "static" / "index.html"

###################################
#####      OUTPUT SCHEMA      #####
###################################

class StructuredOP(BaseModel):
    matching_skills: List[str]
    missing_skills: List[str]
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    overall_suitability: str
    rating: str

###################################
#####          LLM            #####
###################################

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0
)

structured_llm = llm.with_structured_output(StructuredOP)

###################################
#####         PROMPT          #####
###################################

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a technical HR professional.

Evaluate a candidate's resume against the provided job description.

Analyze:

1. Matching Skills
2. Missing Skills
3. Strengths
4. Weaknesses
5. Suggestions
6. Overall Suitability
7. Rating

Be objective and concise.
"""
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{user_query}")
    ]
)

###################################
#####          CHAIN          #####
###################################

chain = prompt | structured_llm

###################################
#####  MANUAL HISTORY STORE   #####
###################################

history_store = {}


def get_session_history(session_id: str):
    if session_id not in history_store:
        history_store[session_id] = []
    return history_store[session_id]


###################################
#####      FASTAPI ROUTES     #####
###################################

@app.get("/", response_class=FileResponse)
def show_homepage():
    return FileResponse(HTML_DIR)


@app.post("/send")
def get_details(
    resume: str = Form(...),
    jd: str = Form(...)
):

    user_query = f"""
ANALYZE THIS CANDIDATE

RESUME:
{resume}

JOB DESCRIPTION:
{jd}
"""

    session_id = "BGM"

    chat_history = get_session_history(session_id)

    ###################################
    #####      LLM INVOCATION     #####
    ###################################

    resp = chain.invoke(
        {
            "user_query": user_query,
            "chat_history": chat_history
        }
    )

    ###################################
    #####      SAVE HISTORY       #####
    ###################################

    chat_history.append(
        HumanMessage(content=user_query)
    )

    chat_history.append(
        AIMessage(content=resp.model_dump_json(indent=2))
    )

    ###################################
    #####         LOGGING         #####
    ###################################

    print(
        "\n================= AI HR ANALYSIS =================\n"
    )

    print(resp.model_dump())

    ###################################
    #####      API RESPONSE       #####
    ###################################

    return resp.model_dump()