import datetime



#Tools untuk mengetahui tanggal dan waktu hari ini
def get_date_time():
  now = datetime.datetime.now()
  date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
  return date_time