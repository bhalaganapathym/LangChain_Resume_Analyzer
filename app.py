from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

###################################
#####          LLM            ##### 
###################################

llm = ChatGoogleGenerativeAI(model='gemini-3.5-flash')

###################################
#####         PROMPT          ##### 
###################################

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a technical HR professional.

        Evaluate a candidate's resume
        against the provided job description.

        Identify:
        - Matching skills
        - Missing skills
        - Strengths
        - Weaknesses
        - Suggestions
        - Overall suitability
        """
    ),

    (
        "placeholder",
        "{chat_history}"
    ),

    (
        "human",
        "{user_query}"
    )
])

###################################
#####         CHAIN           ##### 
###################################

chain = prompt | llm

###################################
#####     MEMORY STORE        ##### 
###################################

store = {}

def get_hist(s_id):
    if s_id not in store:
        store[s_id] = ChatMessageHistory()
    return store[s_id]

###################################
#####      ADDING MEMORY      ##### 
###################################

message = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_hist,
    input_messages_key='user_query',
    history_messages_key='chat_history'
)

###################################
#####         RESUME          ##### 
###################################

resume = input('\nPASTE YOUR RESUME HERE\n')
job_description = input('\nPASTE YOUR JOB DESCRIPTION\n')


###### USER QUERY #######

user_query = f'''
ANALYZE THIS CANDIDATE

RESUME : {resume}

JOB DESCRIPTION : {job_description}

'''

###################################
#####        RUN CHAIN        ##### 
###################################

resp = message.invoke(
    {
        'user_query' : user_query
    },
    config=
    {
        'configurable':
        {
            'session_id' : 'BGM'
        }
    }   
)

print('\n =================AI HR ANALYSIS====================\n')
print(resp.text)