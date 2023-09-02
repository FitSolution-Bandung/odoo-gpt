import datetime
from langchain.pydantic_v1 import BaseModel, Extra, root_validator


#Tools untuk mengetahui tanggal dan waktu hari ini
class GetDateTime(BaseTool):


    name="Get Date and Time",
    description="berguna ketika Anda perlu menjawab pertanyaan tentang tanggal, hari dan jam (waktu) saat ini",

    def _run(self) -> str:
        now = datetime.datetime.now()
        date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
        date_time_text = f"Hari ini tanggal :{date_time}"
        
        return str(date_time_text)
    


