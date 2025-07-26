from datetime import datetime
import asyncio
import random
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from apscheduler.schedulers.blocking import BlockingScheduler

class Alarm():

    _active = True

    def __init__ (self,spot,tag, mins = 0, hour = 0):
        self._mins = mins
        self._hour = hour
        self._spot = spot
        self.score = self.find_score()
        self.tag = tag

    @property
    def active(self):
        return self._active

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

    @active.setter
    def active(self,new):
        self._active = new

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
    
    def deactivate_group(self, group_name):
        for alarm in self.alarms:
            if alarm.group == group_name:
                alarm.active = False

    def activate_group(self, group_name):
        for alarm in self.alarms:
            if alarm.group == group_name:
                alarm.active = True

    #set a time you must wake up and get multable trys to wake up
    def must_wake_up(self, hours, mins,quantity = 5):
        MINUTE_INTERVAL = 5
        MAX_MINUTE = 55
        for _ in range (quantity):
            self.new_alarm(hours=hours, mins=mins)

            if mins == 0:
                hours -= 1 #-1 hour of time 7:00 to 6:55
                mins = MAX_MINUTE
            else:
                mins -= MINUTE_INTERVAL

    async def do_alarms(self):
        scheduler = BlockingScheduler()

        # scheduler.add_job(alarm_action, 'cron', hour=7, minute=30)

        #scheduler.start()
        for x in range (len(self.alarm_list)):
            hour = self.alarm_list[x].hour
            mins = self.alarm_list[x].mis
            await scheduler.daily(datetime.time(hour=hour, minute=mins), some_action)






