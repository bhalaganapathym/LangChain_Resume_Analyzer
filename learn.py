from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model='gemini-3.5-flash')

conversation = []

def get_ai_response_wo_mem(query):
    response = llm.invoke(query)
    return response.text

def get_ai_response_mem(query):
    conversation.append(HumanMessage(content=query))
    response = llm.invoke(conversation)
    conversation.append(AIMessage(content=response.text))
    return response.text

# while True:
#     print(get_ai_response_mem(input()))

# PROMPT TEMPLATE

'''                 BASIC PROMPT TEMPLATE USAGE


prompt = ChatPromptTemplate.from_messages(messages=[
    ('system','you are a helpful assistant who answers with cold mentality'),
    ('human','{user_query}')
    ])

chain = prompt | llm

response = chain.invoke({'user_query':'I have decided to learn Agentic AI'})

print(response.text)

'''


#                     PROMPT TEMPLATE WITH MEMORY                     

prompt_wm = ChatPromptTemplate.from_messages(
    messages=[
        ('system','you are an cold replying helpful assistant'),
        ('placeholder','{chat_history}'),
        ('human','{user_query}')
        ]
)

chain = prompt_wm | llm

store = {}

def get_hist(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chat_wm = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_hist,
    input_messages_key='user_query',
    history_messages_key='chat_history'
)

while True:
    resp = chat_wm.invoke({'user_query':input("Enter prompt : ")}, {"configurable":{'session_id':input("enter user: ")}})
    print(resp.text)
