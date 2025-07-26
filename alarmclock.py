from datetime import datetime
import asyncio
import random
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

class Alarm():

    _active = True

    def __init__ (self,spot,tag, mins = 0, hour = 0):
        self._mins = mins
        self._hour = hour
        self._spot = spot
        self.score = self.find_score()

    @property
    def mins (self):
        return self._mins
    
    @property
    def hour (self):
        return self._hour
    
    @hour.setter
    def hour (self,new):
        if 0 <= new <= 23:
            self._hour = new
            self.find_score()


    @mins.setter
    def mins (self,new):
        MINUTE_INTERVAL = 5
        MAX_MINUTE = 55
        if 0 <= new <= MAX_MINUTE and new % MINUTE_INTERVAL == 0:
            self._min = new
            self.find_score()

    def find_score(self):
        HOUR_TO_MIN = 60
        return self.mins + (self.hour * HOUR_TO_MIN)

    def is_time(self):
        print("beap beap")
        self.get_recommendation()
        self.play_song()

    def get_recommendation(self):
        recs = self._spot.recommendations(limit=1)
        self.track_uri = recs['tracks'][0]['uri']
        print("Recommended track URI:", self.track_uri)

    def stop_playback(self):
        self._spot.pause_playback()
        print("Playback paused.")

    def play_song(self):
        devices = self._spot.devices()
        if devices['devices']:
            device_id = devices['devices'][0]['id']
            self._spot.start_playback(device_id=device_id, uris=[self.track_uri])
            print("Playing on:", devices['devices'][0]['name'])
        else:
            print("No active devices found. Open Spotify on any device.")
    
class SetOfAlarms():

    
    alarm_list = []
    scheduler = AsyncIOScheduler()
    scheduler.start()

    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")

    spot = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri='http://127.0.0.1:8888/callback',
        scope='user-read-playback-state user-modify-playback-state'
        ))

    def new_alarm(self,tag, hours =0 , mins =0):
        alarm = Alarm(self.spot,tag, hours, mins)
        self.insert_sorted(alarm)

    async def add_alarm(self, hour, minute, tag="custom"):
        new_alarm = Alarm(hour, minute, tag)
        self.insert_sorted(new_alarm)

        job_id = f"alarm_{hour}_{minute}_{tag}"
        # Add the job to the running scheduler
        self.scheduler.add_job(
            new_alarm.is_time,
            trigger=CronTrigger(hour=hour, minute=minute),
            args=[new_alarm],
            id=job_id,
            name=f"Alarm {hour}:{minute} ({tag})"
        )

    def deactivate_alarm(self, hours, mins, tag):
        job_id = f"alarm_{hours}_{mins}_{tag}"
        self.scheduler.remove_job(job_id)
        self.alarm_list.remove(self.find_alarm(hours, mins))

    def deactivate_group(self, tag):
        for job in self.scheduler.get_jobs():
            if tag in job.id:
                self.scheduler.remove_job(job.id)
                self.delete_group(tag)

    def delete_group(self, tag_name):
        for alarm in self.alarms:
            if alarm.group == tag_name:
                self.alarm_list.remove(alarm)

    def insert_sorted(self,new_alarm):
        for i in range(len(self.alarm_list)):
            if new_alarm.score < self.alarm_list[i].score:
                self.alarm_list.insert(i, new_alarm)
                return
        self.alarm_list.append(new_alarm)
    
    #be able to say {action} the 5:30 alarm
    def find_alarm(self, hours, mins):
        HOUR_TO_MIN = 60
        wanted_score = mins + (hours * HOUR_TO_MIN)

        left = 0
        right = len(self.alarm_list) - 1

        while left <= right:
            mid = (left + right) // 2
            current_score = self.alarm_list[mid].score

            if current_score == wanted_score:
                return self.alarm_list[mid]
            elif current_score < wanted_score:
                left = mid + 1
            else:
                right = mid - 1

        print("that alarm does not exist")
        return None
    

                

    #set a time you must wake up and get multable trys to get up
    def must_get_up(self, hours, mins,quantity = 5):
        MINUTE_INTERVAL = 5
        MAX_MINUTE = 55
        for _ in range (quantity):
            self.new_alarm(hours=hours, mins=mins)

            if mins == 0:
                hours -= 1 #-1 hour of time 7:00 to 6:55
                mins = MAX_MINUTE
            else:
                mins -= MINUTE_INTERVAL

    








