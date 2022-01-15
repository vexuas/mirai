import datetime;
import asyncio
from helpers import Helpers;


class Timer():
  def __init__(self, channel, user, countdown, type="day"):
    self.date_now = datetime.datetime.now();
    self.started_at = Helpers().format_to_datetime(countdown["started_at"]);
    self.ends_at = Helpers().format_to_datetime(countdown["ends_at"]);
    self.days = countdown["days"]
    self.user = user;
    self.channel = channel;
    self.type = type;

    if self.type == 'day':
      self.passed_time = (self.date_now - self.started_at).days;
      self.current_time = self.days - self.passed_time;
      self.next_date = self.started_at + datetime.timedelta(days=self.passed_time + 1);
    if self.type == 'minute':
      self.ends_at = self.started_at + datetime.timedelta(minutes=countdown["days"]);
      self.passed_time = ((self.date_now - self.started_at).seconds // 60) % 60;
      self.current_time = self.days - self.passed_time;
      self.next_date = self.started_at + datetime.timedelta(minutes=self.passed_time + 1);

  async def start(self):
    if(self.date_now < self.ends_at):
      difference = (self.next_date - self.date_now).seconds
      await self.start_day_timer(self.user, self.channel, difference, self.current_time);
      await asyncio.sleep(3);
      self.update_next_timer();
      await self.start();
    else:
      await self.channel.send(f'{self.user.mention} Day 0');
    

  def update_next_timer(self):
    self.date_now = datetime.datetime.now();
    if self.type == 'day':
      self.passed_time = (self.date_now - self.started_at).days;
      self.current_time = self.days - self.passed_time;
      self.next_date = self.started_at + datetime.timedelta(days=self.passed_time + 1);
    if self.type == 'minute':
      self.passed_time = ((self.date_now - self.started_at).seconds // 60) % 60;
      self.current_time = self.days - self.passed_time;
      self.next_date = self.started_at + datetime.timedelta(minutes=self.passed_time + 1);

  async def start_day_timer(self, user, channel, difference, current):  
    async def start_countdown():
      countdown_message = f"{user.mention} Day {current}! Good luck :D" if current == self.days else f"{user.mention} Day {current}"
      await channel.send(countdown_message);
      return await asyncio.sleep(difference);

    await start_countdown()
