import datetime;
import asyncio
from helpers import Helpers;


class Timer():
  def __init__(self, channel, user, countdown):
    self.date_now = datetime.datetime.now();
    self.started_at = Helpers().format_to_datetime(countdown["started_at"]);
    self.ends_at = Helpers().format_to_datetime(countdown["ends_at"]);
    self.days = countdown["days"]
    self.user = user;
    self.channel = channel;

    self.passed_days = (self.date_now - self.started_at).days;
    self.current_day = self.days - self.passed_days;
    self.next_day_date = self.date_now + datetime.timedelta(days=self.passed_days + 1);

    self.ends_at_minute = self.date_now + datetime.timedelta(minutes=10);
    self.passed_minute = ((self.date_now - self.started_at).seconds // 60) % 60;
    self.current_minute = self.days - self.passed_minute;
    self.next_minute_date = self.date_now + datetime.timedelta(minutes=self.passed_minute + 1);

  async def start(self):
    if(self.date_now < self.ends_at_minute):
      difference = (self.next_minute_date - self.date_now).seconds
      await self.start_day_timer(self.user, self.channel, difference, self.current_minute);
      await asyncio.sleep(3);
      self.update_next_timer();
      await self.start();
    else:
      await self.channel.send(f'{self.user} Day 0');
    

  def update_next_timer(self):
    self.date_now = datetime.datetime.now();
    self.passed_minute = ((self.date_now - self.started_at).seconds // 60) % 60;
    self.current_minute = self.days - self.passed_minute;
    self.next_minute_date = self.started_at + datetime.timedelta(minutes=self.passed_minute + 1);

    self.passed_days = (self.date_now - self.started_at).days;
    self.current_day = self.days - self.passed_days;
    self.next_day_date = self.date_now + datetime.timedelta(days=self.passed_days + 1);

  async def start_day_timer(self, user, channel, difference, current):  
    async def start_countdown():
      await channel.send(f"{user.mention} Day {current}");
      return await asyncio.sleep(difference);

    await start_countdown()
