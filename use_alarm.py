from datetime import datetime, timedelta
from alarmclock import SetOfAlarms as days
from dotenv import load_dotenv
import asyncio
import os
import psycopg2

#interaction.user.id

class DatabaseForDays():

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
            dbname="phy_miko",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"))
        self.cur = self.conn.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            job_name TEXT NOT NULL,
            start_time TIME NOT NULL,
            day_of_week INTEGER NOT NULL, -- Which weekday
            start_date DATE NOT NULL,
            end_date DATE,
            if_temp BOOLEAN, 
            override BOOLEAN DEFAULT False, --if True priority
            discription TEXT,
            if_multi INTEGER NOT NULL,    
            UNIQUE (start_time, day_of_week)    
        );
        """)
        self.conn.commit()
        
        self.cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        print(self.cur.fetchall())

    @property
    def days_numbers(self):
        return self._days_numbers

    def add_event(self,job_name,discription, start_time, start_date, 
        end_date = None, if_temp = False, day_of_week = None, if_multi = 1):
        if day_of_week == None:
            date = datetime.strptime(start_date, "%Y-%m-%d").date()
            day_of_week = date.weekday()

        if if_temp and end_date is None:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = start_dt + timedelta(days=1)
            day_of_week = int(day_of_week)

        try:
            self.cur.execute(
                """
                INSERT INTO events (job_name, start_time, day_of_week, start_date, 
                end_date, if_temp, override, discription,if_multi)
                VALUES (%s, %s, %s, %s, %s, %s, FALSE, %s,%s)
                ON CONFLICT (start_time, day_of_week)
                DO UPDATE SET override = TRUE
                """,
                (job_name, start_time, day_of_week, start_date,
                end_date, if_temp, discription, if_multi)
            )
            if self.cur.rowcount == 0:
                print("Inserted new event.")
            else:
                print("Override occurred: existing event updated with override=TRUE.")
                #later make miko say this and ask if wana keep it 
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting event: {e}")
            self.conn.rollback()

    def remove_event(self, job_name, start_time, day_of_week):
        try:
            self.cur.execute(
                """
                DELETE FROM events WHERE job_name = %s and start_time = %s and day_of_week = %s;
                """,
                (job_name, start_time, day_of_week)
            )
            self.conn.commit()
            print("removed")
        except Exception as e:
            print(f"Error removing event: {e}")
            self.conn.rollback()


    def find_todays_events(self):
        time = datetime.now()
        weekday = int(time.weekday()) #0-6, sun = 0
 
        self.cur.execute("""
            SELECT job_name, start_time, discription, if_multi
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
        """, (weekday,))

        return self.cur.fetchall()

    def until_end_date(self, job_name, start_time, 
                       start_date, end_date, discription):
        #reapeats all days of the week until the end date
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        delta = (end - start).days

        for i in range(delta + 1):
            current_date = start + timedelta(days=i)
            day_of_week = current_date.weekday()
            self.add_event(job_name, start_time, 
                           start_date, end_date, False, discription, day_of_week)


    #to have every mom sun and wen have something or thu fri sat
    def many_days_in_week(self,day_list,job_name,discription, start_time, 
                          start_date, end_date, if_temp):
        for day in day_list:
            day_of_week = self.days_numbers[day.lower()]
            self.add_event(job_name,discription, start_time, start_date, 
        end_date = end_date, if_temp = if_temp, day_of_week = day_of_week,)

    #auto delete useed items after using for the last time 
    #select all for that day delete if needed after
    def delete_used (self):
        end_date = datetime.now().date() 

        self.cur.execute(
                """
                DELETE FROM events WHERE end_date = %s;
                """,
                (end_date,)
            )
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()


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
                    await asyncio.sleep(60)
                    time = datetime.now()

def test_data(DataBase):
    DataBase.add_event("test1", "deep", "19:50:00", "2025-10-21", 
        if_temp = True, day_of_week = None, if_multi = 5)
    
    DataBase.add_event("test2", "beep", "19:50:00", "2025-10-21", 
        if_temp = True, day_of_week = None, if_multi = 2)
    
    DataBase.add_event("test3", "meep", "00:05:00", "2025-10-21", 
        if_temp = True, day_of_week = None, if_multi = 1)
    
    DataBase.add_event("test4", "sheep", "18:05:00", "2025-10-21", 
        if_temp = True, day_of_week = None, if_multi = 4)
    
    DataBase.many_days_in_week(
        day_list=["monday", "wednesday", "friday"],
        job_name="creek",
        discription="recurring alarm",
        start_time="09:00:00",
        start_date="2025-10-21",
        end_date="2025-12-31",
        if_temp=True,
        )
    
    # Note: day_of_week parameter is 2 = Tuesday (0=sunday, 1=monday, etc.)
    # Assuming "test1" was added for a specific day, you should use the correct day_of_week
    DataBase.remove_event("test1", "19:50:00", 1)  # Change 2 to the correct day_of_week




async def test_alarms():

    DataBase = DatabaseForDays()
    DataBase.conn.rollback()
    all_alarms = days()
    await all_alarms.start()

    test_data(DataBase)

    start_day = True
    while True:

        if start_day:
            await time_align()
            start_day = False

        elif datetime.now().strftime("%H:%M:%S") == "00:05:00":
            start_day = True
            today_events = DataBase.find_todays_events()
            
            for event in today_events:
                hold = event[1].split(":")
                hour = hold[0]
                min = hold[1]

                if event[3] == 1:
                    all_alarms.add_alarm(event[0],hour,min,event[2])
                else:
                    all_alarms.multi_alarm(event[0],hour,min,event[2], quantity=event[3])

            DataBase.delete_used()

        await asyncio.sleep(60*5)


if __name__ == "__main__":
    asyncio.run(test_alarms())