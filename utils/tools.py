import datetime
import pytz
import locale
import calendar

# from langchain.pydantic_v1 import BaseModel, Extra, root_validator
from langchain.tools import StructuredTool

 

def get_date_time(self) -> str:
    """Tanggal dan Jam saat ini"""

    # Mengatur locale ke bahasa Indonesia
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')  # 'id_ID' untuk sistem operasi Linux
    day_name = calendar.day_name[datetime.datetime.today().weekday()]

    local_timezone = datetime.timezone(datetime.timedelta(hours=7))  # WIB (Jakarta)
    now = datetime.datetime.now(local_timezone)
    
    date_time = now.strftime("%d/%m/%Y, %H:%M")
    
    date_time_text = f"Hari ini {day_name}, tanggal {date_time} di {now.tzinfo}"
    
    return str(date_time_text)



def answer_general_query(question: str, **kwargs) -> str:
    from utils.whatsapp import prepare_message, phone_number
    # Menggunakan model OpenAI untuk mendapatkan jawaban
    # response = openai_model.predict(question)
    
    #print semua yang ada di *args, **kwargs
    print(f">> kwargs: {kwargs}")
    
    response = prepare_message(phone_number, question)

    print(f"Question: {question}")
    print(f"Answer: {response}")



    return response
