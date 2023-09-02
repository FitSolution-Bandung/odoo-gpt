import datetime
from langchain.pydantic_v1 import BaseModel, Extra, root_validator


#Tools untuk mengetahui tanggal dan waktu hari ini
class GetDateTime(BaseModel):
  def run(self):
      now = datetime.datetime.now()
      date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
      print("date and time:",date_time)
      return str(date_time)