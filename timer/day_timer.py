import datetime;
import asyncio;
from helpers import Helpers;
from threading import Timer;


class DayTimer():
  def __init__(self, countdown):
    self.date_now = datetime.datetime.now();
    self.started_at = Helpers().format_to_datetime(countdown["started_at"]);
    self.ends_at = Helpers().format_to_datetime(countdown["ends_at"]);
    self.passed_days = (self.date_now - self.started_at).days
    self.current_day = (self.ends_at - self.date_now).days + 1;

    self.ends_at_minute = self.date_now + datetime.timedelta(minutes=10);
    self.passed_minute = ((self.date_now - self.date_now).seconds // 60) % 60;
    self.current_minute = ((self.ends_at_minute - self.date_now).seconds // 60) % 60;
    self.next_minute_date = self.date_now + datetime.timedelta(minutes=self.passed_minute + 1);

    print(self.date_now);
    print(self.ends_at_minute);
    print(self.next_minute_date);
    print(self.passed_minute);
    print(self.current_minute);

  async def start(self, channel):  
    difference = (self.next_minute_date - self.date_now).seconds
    async def countdown():
      print('countdown');
      await asyncio.sleep(difference);
      return await channel.send(f"Day {self.current_minute - 1}");
    print('run')
    await countdown()
