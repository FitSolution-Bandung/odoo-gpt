
import os
import openai

from langchain import LLMMathChain, OpenAI, SerpAPIWrapper, SQLDatabase, SQLDatabaseChain
from langchain.llms import OpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType


import printMessages as PR





# from database import User, Message, app, db_sqlalchemy, inspect_db





OPENAI_API_KEY = os.environ['OPENAI_KEY']

def response_schema():
    response_schemas = [
        ResponseSchema(name="model", description="model odoo versi 12 yang relevan. Apabila tidak relevan kosongkan response ini dan berikutnya."),
        ResponseSchema(name="field", description="field odoo yang relevan untuk model yang dipilih, lebih dari satu field dipisahkan dengan koma (,)"),
        ResponseSchema(name="filter", description="filter/domain sesuai dengan ORM odoo, dengan format [['field_name','operator','value']]. apabila value adalah string gunakan operator 'ilike' alih-alih '='"),
        ResponseSchema(name="groupby", description="groupby sesuai dengan ORM odoo, dengan format 'field_name'"),
        ResponseSchema(name="order", description="orderby sesuai dengan ORM odoo, dengan format 'fieldname asc/desc'"),
        ResponseSchema(name="limit", description="limit sesuai dengan ORM odoo sebagai numerik integer"),
        ResponseSchema(name="method", description="berikan method di odoo dengan pilihan 'search_read', 'search_count', 'fields_get'"),
        
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template("Selain merupakan expert Odoo, Saya adalah asisten yang memiliki pengetahuan dibidang Konstruksi, IT dan Multimedia. Apabila perlu menjawab seputar bisnis, Berikan jawaban yang relevan bersumber dari sistem ERP Odoo versi 12. Sebagai informasi hari ini adalah tangal 02/08/2023\n{format_instructions}\n{question}")  
        ],
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )


    chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY, verbose=True )


    messages = []

    while True:
        message = input("input : ")
        _input = prompt.format_prompt(question=message)
        usr_msg = HumanMessage(content=message)
       
        messages.append(usr_msg)
        output = chat(_input.to_messages())
        print(f'output : {output.content}')
       
   
 
def cetak():
    # print("cetak")
    return "cetak"
     

def cari():
    # print("cari")
    return "cari"
     



llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY, verbose=True )
# llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
# search = SerpAPIWrapper()
# llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
# db = SQLDatabase.from_uri("sqlite:///../../../../../notebooks/Chinook.db")

cetak = cetak
cari = cari   

# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///user_data.db'
# db_sqlalchemy.init_app(app)

# with app.app_context():


# db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# A = PR.run("Andhi")

tools = [
    Tool(
        name = "Kalau ada perintah semacam print atau cetak, jalankan fungsi ini",
        func=cetak,
        description="kalo diminta cetak, cetak aja"
    ),
    Tool(
        name="Search. Kalau ada instruksi semacam cari, jalankan fungsi ini",
        func= cari, #response_schema(),
        description="useful for when you need to answer questions about math"
    )
    # Tool(
    #     name="FooBar-DB",
    #     func=db_chain.run,
    #     description="useful for when you need to answer questions about FooBar. Input should be in the form of a question containing full context"
    # )
]

agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
agent.run("coba cetak dulu")

# agent.run("Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?")

# messages = []
# while True:
#     message = input("input : ")
#     print(f'message : {message}')
#     # _input = prompt.format_prompt(question=message)
#     # usr_msg = HumanMessage(content=message)
   
#     # messages.append(usr_msg)
#     output = agent.run(message)
#     print(f'output : {output}')










# prompt = PromptTemplate(
#     input_variables=["ml_concept"],
#     template="Turn the concept description of {ml_concept} and explain it to me like I'm five in 500 words",
# )
# chain_two = LLMChain(llm=llm, prompt=prompt)

     

# chat = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0.3, openai_api_key=OPENAI_API_KEY,verbose=True)



# messages = [
#     SystemMessage(content="Today is 02/08/2023. You are an expert Odoo Functional. Convert Sentences to Odoo ORM Parameters"),
#     HumanMessage(content="Berapakah total penjualan bulan ini")
# ]
# response=chat(messages)

# print(response.content,end='\n')


from langchain import LLMMathChain, OpenAI, SerpAPIWrapper, SQLDatabase, SQLDatabaseChain

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=OPENAI_API_KEY )
 
search = SerpAPIWrapper(serpapi_api_key = )
