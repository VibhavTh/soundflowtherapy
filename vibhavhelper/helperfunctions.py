import random
import datetime

def get_random_number(base: int=0, ceiling: int=100) -> int:
    random_int = random.randint(base, ceiling)
    return random_int

def get_formatted_date() -> str:
   today = datetime.date.today()
   return today.strftime("%Y%m%d")

def create_playlist_name() -> str:
    # name = str(get_formatted_date()) + "-"+ str(get_random_number(100,10000))
    name = " ID: " + str(get_random_number(100,10000))
    return name

def get_random_mood()-> str:
    return ['happy','sad','angry','relaxed'][get_random_number(0,3)]


