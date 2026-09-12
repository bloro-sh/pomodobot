# Discord Pomodoro Bot

Discord 음성 채널에서 사용할 수 있는 뽀모도로 타이머 봇입니다.

집중 시간과 휴식 시간을 설정하고, 타이머가 끝나면 음성 채널에서 알람을 재생합니다.

## 주요 기능

- `/입장` - 현재 음성 채널에 봇 입장
- `/퇴장` - 음성 채널에서 봇 퇴장
- `/뽀모시작` - 뽀모도로 시작
- `/뽀모종료` - 현재 뽀모도로 종료
- `/시간설정` - 집중 시간과 휴식 시간 설정
- `/일시정지` - 타이머 일시정지
- `/재시작` - 일시정지한 타이머 재시작
- `/상태` - 현재 뽀모도로 상태 확인
- 타이머 종료 시 음성 채널에서 알람 재생

## 사용 기술

- Python
- discord.py
- python-dotenv
- PyNaCl
- davey
- FFmpeg

## 프로젝트 구조

```text
pomodobot/
├── bot.py
├── alarm.mp3
├── .env.example
├── requirements.txt
├── .gitignore
└── README.md
```

## Discord Bot 만들기

이 프로젝트를 사용하려면 먼저 자신의 Discord Bot을 만들어야 합니다.

### 1. Discord Developer Portal 접속

Discord Developer Portal에 접속합니다.

https://discord.com/developers/applications

Discord 계정으로 로그인합니다.

### 2. 새로운 Application 만들기

왼쪽 탭의 **봇**을 클릭합니다.

봇의 이름을 입력합니다.

예를 들어:

```text
Pomodoro Bot
```

을 입력하고 생성합니다.

### 3. Bot Token 확인하기

Bot 설정 화면에서 **Token**을 확인할 수 있습니다.

Token은 봇의 비밀번호와 같은 중요한 정보입니다.

Token을 복사한 뒤 프로젝트의 `.env` 파일에 입력합니다.

```env
DISCORD_TOKEN=여기에_자신의_Bot_Token
```

예를 들어:

```env
DISCORD_TOKEN=실제_발급받은_TOKEN
```

**주의:** 실제 Token은 GitHub에 절대 올리지 마세요.

Token이 GitHub에 공개되었다면 즉시 Token을 재생성해야 합니다.

#### Bot 권한

이 프로젝트에서는 봇이 음성 채널에 들어가고 알람을 재생해야 하므로 다음 권한이 필요합니다.

설치 탭에 들어가서 길드설치 아래의 체크박스를 클릭해주세요

**스코프**

```text
☑ bot
☑ applications.commands
```

**권한**

```text
☑ 채널보기
☑ 연결
☑ 말하기
☑ 메시지보내기
```

필요한 권한을 선택한 후 위에 설치링크 디스코드제공링크 URL을 통해 Bot을 자신의 Discord 서버에 초대합니다.

### 6. Bot 실행하기

프로젝트 폴더에서 필요한 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```

`.env`에 자신의 Bot Token이 설정되어 있는지 확인합니다.

그 다음:

```bash
python bot.py
```

를 실행합니다.

터미널에 다음과 비슷한 메시지가 나타나면 정상적으로 실행된 것입니다.

```text
Pomodoro Bot 봇이 온라인되었습니다!
```

### 7. Discord에서 사용하기

Bot이 온라인 상태가 되면 Discord 서버에서 사용할 수 있습니다.

먼저 음성 채널에 들어간 후:

```text
/입장
```

을 실행합니다.

봇이 음성 채널에 들어오면:

```text
/시간설정
```

으로 집중 시간과 휴식 시간을 설정할 수 있습니다.

예:

```text
/시간설정 집중:25 짧은휴식:5
```

그 다음:

```text
/뽀모시작
```

을 실행하면 뽀모도로가 시작됩니다.

집중 시간이 끝나면 `alarm.mp3`가 음성 채널에서 재생됩니다.

## 실행 전 준비

다음 프로그램이 필요합니다.

- Python
- FFmpeg
- Discord 계정
- Discord Developer Portal에서 생성한 Discord Bot

### 1. 프로젝트 다운로드

GitHub에서 프로젝트를 다운로드하거나 clone합니다.

```bash
git clone [GitHub 저장소 주소]
cd pomodobot
```

### 2. 가상환경 생성

```bash
python -m venv venv
```

가상환경을 실행합니다.

Mac / Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 3. 필요한 라이브러리 설치

```bash
pip install -r requirements.txt
```

### 4. Discord Bot Token 설정

`.env.example` 파일을 복사하여 `.env` 파일을 만듭니다.

```bash
cp .env.example .env
```

Windows에서는 다음과 같이 만들 수 있습니다.

```bash
copy .env.example .env
```

`.env` 파일을 열고 자신의 Discord Bot Token을 입력합니다.

```env
DISCORD_TOKEN=여기에_자신의_봇_TOKEN을_입력
```

**주의:** `.env` 파일에는 실제 Bot Token이 들어가기 때문에 GitHub에 업로드하면 안 됩니다.

### 5. FFmpeg 설치

이 봇은 음성 채널에서 `alarm.mp3`를 재생하기 위해 FFmpeg가 필요합니다.

Mac에서는 Homebrew를 사용하여 설치할 수 있습니다.

```bash
brew install ffmpeg
```

```bash
ffmpeg -version //버전설치확인
```

Windows와 Linux 사용자는 자신의 운영체제에 맞는 방법으로 [FFmpeg](https://ffmpeg.org/)를 설치해주세요.

### 6. 봇 실행

```bash
python bot.py
```

터미널에 다음과 비슷한 메시지가 나오면 봇이 정상적으로 실행된 것입니다.

```text
봇이 온라인되었습니다!
```

## Discord에서 사용하기

봇을 Discord 서버에 추가한 후 음성 채널에 들어갑니다.

먼저:

```text
/입장
```

을 실행하여 봇을 음성 채널에 입장시킵니다.

그 다음:

```text
/시간설정 25 5
```

와 같이 집중 시간과 휴식 시간을 설정할 수 있습니다.

예를 들어 위 명령어를 사용하면:

- 집중: 25분
- 짧은 휴식: 5분

으로 설정됩니다.

이후:

```text
/뽀모시작
```

을 실행하면 뽀모도로가 시작됩니다.

## 명령어

| 명령어      | 설명                       |
| ----------- | -------------------------- |
| `/입장`     | 음성 채널에 봇 입장        |
| `/퇴장`     | 음성 채널에서 봇 퇴장      |
| `/시간설정` | 집중 시간과 휴식 시간 설정 |
| `/뽀모시작` | 뽀모도로 시작              |
| `/뽀모종료` | 뽀모도로 종료              |
| `/일시정지` | 타이머 일시정지            |
| `/재시작`   | 타이머 다시 시작           |
| `/상태`     | 현재 상태 확인             |

## 주의사항

### Bot Token을 공개하지 마세요

Discord Bot Token은 비밀번호와 같은 중요한 정보입니다.

`.env` 파일은 GitHub에 업로드하지 마세요.

이 프로젝트에서는 `.gitignore`를 통해 `.env`가 Git에 추가되지 않도록 설정합니다.

### alarm.mp3

봇이 알람을 재생하기 위해 프로젝트 폴더에 `alarm.mp3` 파일이 필요합니다.

```text
pomodobot/
├── bot.py
└── alarm.mp3
```

`alarm.mp3`를 다른 사람에게 배포할 경우 해당 음원의 사용 및 재배포 권한을 확인해주세요.

## 직접 봇을 만들어 사용하기

이 프로젝트는 하나의 Bot Token을 여러 사람이 공유하는 방식이 아닙니다.

각 사용자가 자신의 Discord Developer Portal에서 Bot을 만들고 자신의 Token을 `.env`에 입력하여 실행하는 방식입니다.

즉,

```text
GitHub 프로젝트
       ↓
프로젝트 다운로드
       ↓
자신의 Discord Bot 생성
       ↓
자신의 Bot Token 설정
       ↓
python bot.py
       ↓
자신의 Discord 서버에서 사용
```

의 방식으로 사용할 수 있습니다.

## License

이 프로젝트의 라이선스는 저에게 있습니다
