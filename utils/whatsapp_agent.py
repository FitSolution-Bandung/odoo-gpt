from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.callbacks import get_openai_callback

import os
from dotenv import load_dotenv
 

import jsonpickle

from utils.database import db_sqlalchemy, app
from utils.database import User as User, inspect_db, call_memory


load_dotenv('.credentials/.env')
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]


search = GoogleSearchAPIWrapper()
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="berguna ketika Anda perlu menjawab pertanyaan tentang informasi terkini",
    )
]


prefix = """Lakukan percakapan dengan manusia, jawablah pertanyaan-pertanyaan berikut sebaik mungkin. Anda memiliki akses ke tools berikut:"""
suffix = """Mulai!

{chat_history}
Question: {input}
{agent_scratchpad}"""


prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)




def get_memory(phone):
    
    buf_memory_json = call_memory(phone)
            
    if buf_memory_json is None:
        memory = ConversationBufferMemory(memory_key="chat_history")
    else:
        memory = jsonpickle.decode(buf_memory_json)
        
    # memory = ConversationBufferMemory(memory_key="chat_history")
       
    return memory


def save_memory(phone, memory):
    with app.app_context():
        user_query = User.query.filter_by(phone_number=phone).first()
        # user_query = jsonpickle.encode(memory)

        user_query.entity_memory =jsonpickle.encode(memory)
        db_sqlalchemy.session.commit()


    
    return memory
        


def predict_gpt(phone_number, incoming_message):

    memory = get_memory(phone_number)
    # print(f'\nMemory from database: {memory}')
   

    MODEL = 'gpt-3.5-turbo'

    llm_chain = LLMChain(llm=OpenAI(temperature=0, model=MODEL), prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
    agent_chain = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=True, memory=memory
    )


    try:
        with get_openai_callback() as cb:
            # output = Conversation.run(input=incoming_message)


            
            output = agent_chain.run(input=incoming_message)
            
            print(f'\nOutput: {output}\n')

            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (IDR): IDR {cb.total_cost*15000}\n")

    except Exception as e:
        print(f'Error: {e} [predict_gpt] line 109]')
        output = str(e)

    memory = save_memory(phone_number, memory)
    # print(f'\nMemory saved to database (after): {memory}')



    return output
    

# while True:


#     # print field phone number dari table user
#     with app.app_context():
#         #ambil semua data user field phone_number
#         user_query = User.query.all()
#         # print semua data user field phone_number
#         for user in user_query:
#             print(f'\nUser Phone Number: {user.phone_number}')


#     #user input
#     phone = 6281384604433
#     user_input = input("Masukkan pertanyaan anda: ")
#     print(predict_gpt(phone, user_input))
