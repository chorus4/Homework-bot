import datetime

def join(arr: dict) -> str:
  return '\n'.join(arr)

def get_todays_weekday():
  return datetime.datetime.today().weekday()

def get_todays_day():
  return datetime.date.today()