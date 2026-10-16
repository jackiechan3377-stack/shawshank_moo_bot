import datetime
import json
import os
import requests
from gtts import gTTS

# GitHub Secrets에서 안전하게 토큰을 가져옵니다
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = "8986966488"

# 시작 기준일 (2026-10-16 기준 Day 1 시작)
START_DATE = datetime.date(2026, 10, 16)
today = datetime.date.today()
day_index = (today - START_DATE).days

# 대본 파일 불러오기
with open("shawshank.json", "r", encoding="utf-8") as f:
  script_list = json.load(f)

# 365일 순환
item = script_list[day_index % len(script_list)]

# 1. 영어 대본 5문장 발송 (발음/단어 없이 문장+해석만)
msg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
requests.post(msg_url, json={"chat_id": CHAT_ID, "text": item["text"]})

# 2. 영문 원어민 발음(mp3) 생성 및 발송
audio_file = "shawshank_audio.mp3"
tts = gTTS(text=item["audio_text"], lang="en")
tts.save(audio_file)

audio_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendAudio"
with open(audio_file, "rb") as f:
  requests.post(
      audio_url,
      data={
          "chat_id": CHAT_ID,
          "title": f"쇼생크 탈출 - Day {item['day']}",
          "performer": "The Shawshank Redemption",
      },
      files={"audio": f},
  )

if os.path.exists(audio_file):
  os.remove(audio_file)
