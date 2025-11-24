
import asyncio
import os
import random
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


class Alarm:
    """Represents a single alarm that plays Spotify music."""

    _active = True

    def __init__(self, spot, job_id,discription= None, mins=0, hour=0):
        self._mins = mins
        self._hour = hour
        self._spot = spot
        self.score = self.find_score()
        self.job_id = job_id
        self.track_uri = None
        self.discription = discription #tts at the start of alarm (to be added)

    # --- Properties ---
    @property
    def mins(self):
        return self._mins

    @mins.setter
    def mins(self, new):
        MINUTE_INTERVAL = 5
        MAX_MINUTE = 55
        if 0 <= new <= MAX_MINUTE and new % MINUTE_INTERVAL == 0:
            self._mins = new
            self.score = self.find_score()

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self, new):
        if 0 <= new <= 23:
            self._hour = new
            self.score = self.find_score()

    # --- Helpers ---
    def find_score(self):
        HOUR_TO_MIN = 60
        return self._mins + (self._hour * HOUR_TO_MIN)

    # --- Alarm action ---
    async def is_time(self):
        print(f"⏰ Alarm {self.hour:02}:{self.mins:02} ringing! beap beap")
        await self.get_recommendation()
        await self.play_song()

    async def get_recommendation(self):
        if 7 < random.randint(0,11): #30% chance
            results = await asyncio.to_thread(self._spot.current_user_saved_tracks, limit=50)
            items = results["items"]
            if items:
                track = random.choice(items)["track"]
                print(f"🎲 Picked from liked songs: {track['name']} by {track['artists'][0]['name']}")
                self.track_uri = track['uri']
                print("🎵 Recommended track URI:", self.track_uri)
            else:
                print("⚠️ No liked songs found.")
                return None
            
        else:
            results = self._spot.search(q="year:2020", type="track", limit=50)
            track = random.choice(results["tracks"]["items"])
            self.track_uri = track["uri"] 


    async def play_song(self):
        devices = await asyncio.to_thread(self._spot.devices)
        if devices['devices']:
            device_id = devices['devices'][0]['id']
            await asyncio.to_thread(
                self._spot.start_playback,
                device_id=device_id,
                uris=[self.track_uri]
            )
            print("▶️ Playing on:", devices['devices'][0]['name'])
        else:
            print("⚠️ No active devices found. Open Spotify on any device.")

    async def stop_playback(self):
        await asyncio.to_thread(self._spot.pause_playback)
        print("⏹️ Playback paused.")

    async def skip_playback(self):
        devices = await asyncio.to_thread(self._spot.devices)
        if devices['devices']:
            device_id = devices['devices'][0]['id']
            await asyncio.to_thread(self._spot.next_track, device_id=device_id)
            print("⏭️ Skipped to next track.")
        else:
            print("⚠️ No active devices found. Open Spotify on any device.")


class SetOfAlarms:
    """Manages multiple alarms with an async scheduler + Spotify."""

    def __init__(self):
        self.alarm_list = []
        self.scheduler = AsyncIOScheduler()

        load_dotenv()
        client_id = os.getenv("client_id")
        client_secret = os.getenv("client_secret")

        self.spot = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://127.0.0.1:8888/callback",
            scope="user-read-playback-state user-modify-playback-state user-library-read"
        ))

    async def start(self):
        print("📅 Scheduler started.")
        self.scheduler.start()

    async def add_alarm(self, hour, minute,discription = None, tag="custom"):
        job_id = f"alarm_{hour}_{minute}_{tag}"
        new_alarm = Alarm(self.spot, job_id, discription, mins=minute, hour=hour)
        self.insert_sorted(new_alarm)

        self.scheduler.add_job(
            new_alarm.is_time,
            trigger=CronTrigger(hour=hour, minute=minute),
            id=job_id,
            name=f"Alarm {hour}:{minute} ({tag})"
        )
        print(f"✅ Added alarm at {hour:02}:{minute:02} with tag '{tag}'.")

    def deactivate_alarm(self, hours, mins, tag):
        job_id = f"alarm_{hours}_{mins}_{tag}"
        self.scheduler.remove_job(job_id)
        alarm = self.find_alarm(hours, mins)
        if alarm:
            self.alarm_list.remove(alarm)
        print(f"❌ Deactivated alarm {hours:02}:{mins:02} ({tag})")

    def deactivate_group(self, tag):
        for job in list(self.scheduler.get_jobs()):
            if tag in job.id:
                self.scheduler.remove_job(job.id)
        self.delete_group(tag)
        print(f"🗑️ Deactivated all alarms with tag '{tag}'.")

    def delete_group(self, tag_name):
        self.alarm_list = [
            alarm for alarm in self.alarm_list if not alarm.job_id.endswith(tag_name)
        ]

    def insert_sorted(self, new_alarm):
        for i, existing in enumerate(self.alarm_list):
            if new_alarm.score < existing.score:
                self.alarm_list.insert(i, new_alarm)
                return
        self.alarm_list.append(new_alarm)

    def find_alarm(self, hours, mins):
        HOUR_TO_MIN = 60
        wanted_score = mins + (hours * HOUR_TO_MIN)

        left, right = 0, len(self.alarm_list) - 1
        while left <= right:
            mid = (left + right) // 2
            current_score = self.alarm_list[mid].score

            if current_score == wanted_score:
                return self.alarm_list[mid]
            elif current_score < wanted_score:
                left = mid + 1
            else:
                right = mid - 1

        print("⚠️ That alarm does not exist.")
        return None

    async def multi_alarm(self, tag, hours, mins,discription, quantity=5):
        """Set multiple alarms every 5 mins before the target time."""
        MINUTE_INTERVAL = 5
        MAX_MINUTE = 55

        for _ in range(quantity):
            await self.add_alarm(hour=hours, minute=mins,discription = discription, tag=tag)

            if mins == 0:
                hours -= 1
                mins = MAX_MINUTE
            else:
                mins -= MINUTE_INTERVAL


# --- Test Runner ---
async def test_alarms():
    all_alarms = SetOfAlarms()
    await all_alarms.start()

    hour_24 = 18
    mins = 20
    await all_alarms.multi_alarm("test", hour_24, mins)

    while True:
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(test_alarms())






