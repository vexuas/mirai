import datetime;
from helpers import Helpers;

class DayTimer():
  def __init__(self, countdown):
    self.date_now = datetime.datetime.now();
    self.started_at = Helpers().format_to_datetime(countdown["started_at"]);
    self.ends_at = Helpers().format_to_datetime(countdown["ends_at"]);
    self.passed_days = (self.date_now - self.started_at).days;
    self.current_day = (self.ends_at - self.date_now).days + 1;

    print(self.passed_days);
    print(self.current_day);
     