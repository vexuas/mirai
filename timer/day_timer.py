import datetime;
import asyncio;
from helpers import Helpers;
from threading import Timer;


class DayTimer():
  def __init__(self):
    self.date_now = datetime.datetime.now();
    # self.started_at = Helpers().format_to_datetime(countdown["started_at"]);
    # self.ends_at = Helpers().format_to_datetime(countdown["ends_at"]);
    # self.passed_days = (self.date_now - self.started_at).days
    # self.current_day = (self.ends_at - self.date_now).days + 1;

  async def start(self, channel, difference, current):  
    async def start_countdown():
      print('start day');
      print(current);
      print(datetime.datetime.now());
      await channel.send(f"Day {current}");
      return await asyncio.sleep(difference);

    await start_countdown()
