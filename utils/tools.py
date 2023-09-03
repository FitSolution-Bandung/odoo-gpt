import datetime
import pytz

# from langchain.pydantic_v1 import BaseModel, Extra, root_validator
from langchain.tools import StructuredTool


def get_date_time(self) -> str:
    """Tanggal dan Jam saat ini"""
    local_timezone = datetime.timezone(datetime.timedelta(hours=7))  # WIB (Jakarta)
    now = datetime.datetime.now(local_timezone)
    
    date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
    
    date_time_text = f"Hari ini tanggal: {date_time} di {now.tzinfo}"
    
    return str(date_time_text)


# tool = StructuredTool.from_function(get_date_time)


#Tools untuk mengetahui tanggal dan waktu hari ini
# class GetDateTime(BaseTool):


#     name="Get Date and Time",
#     description="berguna ketika Anda perlu menjawab pertanyaan tentang tanggal, hari dan jam (waktu) saat ini",

#     def _run(self) -> str:
#         now = datetime.datetime.now()
#         date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
#         date_time_text = f"Hari ini tanggal :{date_time}"
        
#         return str(date_time_text)
    


