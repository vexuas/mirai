import datetime;
import asyncio;
from timer.day_timer import DayTimer


class FullTimer():
  def __init__(self, channel):
    self.date_now = datetime.datetime.now();
    self.started_date = self.date_now;
    self.channel = channel;
    self.ends_at_minute = self.date_now + datetime.timedelta(minutes=10);
    self.passed_minute = ((self.date_now - self.started_date).seconds // 60) % 60;
    self.current_minute = 10 - self.passed_minute;
    self.next_minute_date = self.date_now + datetime.timedelta(minutes=self.passed_minute + 1);

    print(self.date_now);
    print(self.ends_at_minute);
    print(self.next_minute_date);
    print(self.passed_minute);
    print(self.current_minute);

  async def start(self):
    if(self.date_now < self.ends_at_minute):
      print('start full');
      difference = (self.next_minute_date - self.date_now).seconds
      await DayTimer().start(self.channel, difference, self.current_minute);
      await asyncio.sleep(3);
      self.update_next_timer();
      await self.start();
    else:
      print('end');
      await self.channel.send('Day 0');
    

  def update_next_timer(self):
    self.date_now = datetime.datetime.now();
    self.passed_minute = ((self.date_now - self.started_date).seconds // 60) % 60;
    self.current_minute = 10 - self.passed_minute;
    self.next_minute_date = self.started_date + datetime.timedelta(minutes=self.passed_minute + 1);
    print('----------');
    print('next day');
    print(self.date_now);
    print(self.ends_at_minute);
    print(self.next_minute_date);
    print(self.passed_minute);
    print(self.current_minute);
