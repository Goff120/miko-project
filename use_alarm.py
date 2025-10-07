from datetime import datetime, timedelta
from alarmclock import SetOfAlarms as days
from time import sleep 
from dotenv import load_dotenv
import asyncio
import os
import psycopg2

#interaction.user.id

class day_data():

    _days_numbers = {
        "sunday" : 0,
        "monday" : 1,
        "tuesday" : 2,
        "wednesday" : 3,
        "thursday" : 4,
        "friday" : 5,
        "saturday" : 6
    }

    def __init__ (self):
        load_dotenv()
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"))
        self.cur = self.conn.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_name TEXT NOT NULL,
            start_time TIME NOT NULL,
            day_of_week INTEGER NOT NULL, -- Which weekday
            start_date DATE NOT NULL,
            end_date DATE,
            if_temp BOOLEAN, 
            override BOOLEAN DEFAULT False, --if True priority
            discription TEXT,        
        );
        """)

    @property
    def days_numbers(self):
        return self._days_numbers

    def add_event(self,job_name, start_time, start_date, end_date, if_temp, discription, day_of_week = None):
        if day_of_week == None:
            date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            day_of_week = date.weekday()

        try:
            self.cur.execute(
                """
                INSERT INTO events (job_name, start_time, day_of_week, start_date, end_date, if_temp, override, discription)
                VALUES (%s, %s, %s, %s, %s, %s, FALSE, %s)
                ON CONFLICT (start_time, day_of_week)
                DO UPDATE SET override = TRUE
                """,
                (job_name, start_time, day_of_week, start_date, end_date, if_temp, discription)
            )
            if self.cur.rowcount == 0:
                print("Inserted new event.")
            else:
                print("Override occurred: existing event updated with override=TRUE.")
                #later make miko say this and ask if wana keep it 
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting event: {e}")

    def remove_event(self, job_name, start_time, day_of_week):
        try:
            self.cur.execute(
                """
                DELETE FROM events WHERE job_name = %s and start_time = %s and day_of_week = %s;
                """,
                (job_name, start_time, day_of_week)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Error removing event: {e}")


    def find_todays_events(self):
        time = datetime.now()
        weekday = int(time.weekday()) #0-6, sun = 0
 
        self.cur.execute("""
            SELECT job_name, start_time, discription
            FROM events e1
            WHERE day_of_week = %s
              AND start_date <= CURRENT_DATE
              AND (
              override = TRUE
              OR NOT EXISTS (
                  SELECT 1 FROM events e2
                  WHERE e2.start_time = e1.start_time
                AND e2.day_of_week = e1.day_of_week
                AND e2.override = TRUE
              )
              )
        """, (weekday))

        result = self.cur.fetchone()

    def until_end_date(self, job_name, start_time, start_date, end_date, discription):
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        delta = (end - start).days

        for i in range(delta + 1):
            current_date = start + timedelta(days=i)
            day_of_week = current_date.weekday()
            self.add_event(job_name, start_time, start_date, end_date, False, discription, day_of_week)


    #to have every mom sun and wen have something or thu fri sat
    def many_days_in_week(self,day_list,job_name, start_time, start_date, end_date, if_temp, discription):
        for day in day_list:
            day_of_week = self.days_numbers[day.lower()]
            self.add_event(self,job_name, start_time, start_date, end_date, if_temp, discription, day_of_week)

    #edit temp so if temp = true end date is the next day (to get rid of that data)

    #to delete days when it has gone past check on the 3rd if any 2nd at 00 :05


async def time_align():
    while True:
        time = datetime.now()
        if time.strftime("%S") == "00":
            
            print("now cheaking every min")
            while True:
            
                if int(time.strftime("%M")) % 5 == 0:
                    print("now cheaking every 5 mins")
                    return None
                else:
                    await sleep(60)
                    time = datetime.now()

async def test_alarms():
    all_alarms = days()
    await all_alarms.start()

    hour_24 = 18
    mins = 20
    await all_alarms.multi_alarm("test", hour_24, mins)

    while True:
        await time_align()
        await asyncio.sleep(60*5)


if __name__ == "__main__":
    test_alarms()()