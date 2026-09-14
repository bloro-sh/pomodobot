import os
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")


# 뽀모도로 시간 설정
# 테스트를 위해 초 단위로 설정
FOCUS_TIME = 10
SHORT_BREAK = 5

# Discord에 표시할 시간
# 테스트 중에는 실제 시간과 별도로 표시
FOCUS_MINUTES = 25
SHORT_BREAK_MINUTES = 5


# 현재 타이머 상태
timer_task = None
is_paused = False
remaining_time = 0
current_phase = None


# 현재 음성 채널 연결
voice_client = None


# 알람 파일 재생
async def play_alarm():
    global voice_client

    # 음성 채널에 연결되어 있지 않으면 종료
    if voice_client is None or not voice_client.is_connected():
        return

    # 이미 알람이 재생 중이라면 중지
    if voice_client.is_playing():
        voice_client.stop()

    # 알람 파일 재생
    audio = discord.FFmpegPCMAudio("alarm.mp3")
    voice_client.play(audio)


# 초를 분/초 형태로 변환
def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60

    return f"{minutes}분 {seconds}초"


intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} 봇이 온라인되었습니다!")


# 타이머 실행
async def run_timer(seconds):
    global remaining_time, is_paused

    remaining_time = seconds

    while remaining_time > 0:

        # 일시정지 상태라면 시간을 감소시키지 않음
        if is_paused:
            await asyncio.sleep(1)
            continue

        await asyncio.sleep(1)
        remaining_time -= 1


# 뽀모도로 시작
@bot.tree.command(name="뽀모시작", description="뽀모도로를 시작합니다.")
async def pomodoro_start(interaction: discord.Interaction):
    global timer_task, current_phase
    global is_paused, remaining_time

    # 이미 실행 중인 경우
    if timer_task is not None:
        await interaction.response.send_message(
            "이미 뽀모도로가 실행 중입니다."
        )
        return

    # 메시지를 보낼 채널 저장
    channel = interaction.channel

    # 일시정지 상태 초기화
    is_paused = False

    # 현재 단계 설정
    current_phase = "집중"

    await interaction.response.send_message(
        f"뽀모도로 시작! {FOCUS_MINUTES}분 동안 집중합니다."
    )

    # 집중 타이머 시작
    timer_task = asyncio.create_task(run_timer(FOCUS_TIME))

    try:
        await timer_task

    except asyncio.CancelledError:
        # /뽀모종료로 타이머가 취소된 경우
        return

    # 집중 종료 알람
    await play_alarm()

    await channel.send("집중 시간이 끝났습니다!")

    # 휴식 단계로 변경
    current_phase = "휴식"

    await channel.send(
        f"짧은 휴식을 시작합니다! "
        f"{SHORT_BREAK_MINUTES}분 동안 휴식합니다."
    )

    # 휴식 타이머 시작
    timer_task = asyncio.create_task(run_timer(SHORT_BREAK))

    try:
        await timer_task

    except asyncio.CancelledError:
        # /뽀모종료로 타이머가 취소된 경우
        return

    # 휴식 종료 알람
    await play_alarm()

    await channel.send("짧은 휴식이 끝났습니다!")

    # 모든 과정이 정상적으로 끝난 경우 상태 초기화
    timer_task = None
    is_paused = False
    remaining_time = 0
    current_phase = None


# 시간 설정
@bot.tree.command(name="시간설정", description="뽀모도로 시간을 설정합니다.")
async def set_time(
    interaction: discord.Interaction,
    집중: int,
    짧은휴식: int
):
    global FOCUS_TIME, SHORT_BREAK
    global FOCUS_MINUTES, SHORT_BREAK_MINUTES

    # 입력받은 분을 실제 타이머용 초로 변환
    FOCUS_TIME = 집중 * 60
    SHORT_BREAK = 짧은휴식 * 60

    # Discord 표시용 분 저장
    FOCUS_MINUTES = 집중
    SHORT_BREAK_MINUTES = 짧은휴식

    await interaction.response.send_message(
        f"시간이 설정되었습니다!\n"
        f"집중: {집중}분\n"
        f"짧은 휴식: {짧은휴식}분"
    )


# 일시정지
@bot.tree.command(name="일시정지", description="현재 타이머를 일시정지합니다.")
async def pause_timer(interaction: discord.Interaction):
    global is_paused

    # 타이머가 실행 중인지 확인
    if timer_task is None:
        await interaction.response.send_message(
            "현재 실행 중인 뽀모도로가 없습니다."
        )
        return

    # 이미 일시정지 상태인지 확인
    if is_paused:
        await interaction.response.send_message(
            "이미 일시정지된 상태입니다."
        )
        return

    is_paused = True

    await interaction.response.send_message(
        f"타이머가 일시정지되었습니다!\n"
        f"남은 시간: {format_time(remaining_time)}"
    )


# 재시작
@bot.tree.command(name="재시작", description="일시정지한 타이머를 다시 시작합니다.")
async def resume_timer(interaction: discord.Interaction):
    global is_paused

    # 타이머가 실행 중인지 확인
    if timer_task is None:
        await interaction.response.send_message(
            "현재 실행 중인 뽀모도로가 없습니다."
        )
        return

    # 일시정지 상태가 아닌 경우
    if not is_paused:
        await interaction.response.send_message(
            "현재 타이머가 일시정지 상태가 아닙니다."
        )
        return

    is_paused = False

    await interaction.response.send_message(
        f"타이머를 다시 시작합니다!\n"
        f"남은 시간: {format_time(remaining_time)}"
    )


# 뽀모도로 종료
@bot.tree.command(name="뽀모종료", description="현재 뽀모도로를 종료합니다.")
async def pomodoro_stop(interaction: discord.Interaction):
    global timer_task, is_paused
    global remaining_time, current_phase

    # 실행 중인 타이머가 없는 경우
    if timer_task is None:
        await interaction.response.send_message(
            "현재 실행 중인 뽀모도로가 없습니다."
        )
        return

    # 실행 중인 타이머 취소
    timer_task.cancel()

    # 알람이 재생 중이라면 알람도 중지
    if voice_client is not None and voice_client.is_playing():
        voice_client.stop()

    # 상태 초기화
    timer_task = None
    is_paused = False
    remaining_time = 0
    current_phase = None

    await interaction.response.send_message(
        "뽀모도로를 종료했습니다!"
    )


# 음성 채널 입장
@bot.tree.command(name="입장", description="현재 음성 채널에 봇을 입장시킵니다.")
async def join_voice(interaction: discord.Interaction):
    global voice_client

    # 명령어를 사용한 사람이 음성 채널에 있는지 확인
    if interaction.user.voice is None:
        await interaction.response.send_message(
            "먼저 음성 채널에 들어가주세요!"
        )
        return

    channel = interaction.user.voice.channel

    # 이미 음성 채널에 연결되어 있다면
    if voice_client is not None:

        # 같은 음성 채널이라면
        if voice_client.channel == channel:
            await interaction.response.send_message(
                "이미 이 음성 채널에 있습니다!"
            )
            return

        # 다른 음성 채널이라면 이동
        await voice_client.move_to(channel)

    else:
        # 음성 채널에 새로 연결
        voice_client = await channel.connect()

    await interaction.response.send_message(
        f"{channel.name}에 입장했습니다!"
    )


# 음성 채널 퇴장
@bot.tree.command(name="퇴장", description="음성 채널에서 봇을 내보냅니다.")
async def leave_voice(interaction: discord.Interaction):
    global voice_client

    # 음성 채널에 연결되어 있지 않은 경우
    if voice_client is None:
        await interaction.response.send_message(
            "현재 음성 채널에 연결되어 있지 않습니다."
        )
        return

    # 음성 채널에서 퇴장
    await voice_client.disconnect()

    voice_client = None

    await interaction.response.send_message(
        "음성 채널에서 나갔습니다!"
    )


# 현재 상태 확인
@bot.tree.command(name="상태", description="현재 뽀모도로 상태를 확인합니다.")
async def timer_status(interaction: discord.Interaction):

    # 실행 중인 뽀모도로가 없는 경우
    if current_phase is None:
        await interaction.response.send_message(
            "현재 실행 중인 뽀모도로가 없습니다."
        )
        return

    # 현재 상태 확인
    if is_paused:
        status = "일시정지"
    else:
        status = "진행 중"

    await interaction.response.send_message(
        f"현재 뽀모도로 상태\n"
        f"단계: {current_phase}\n"
        f"남은 시간: {format_time(remaining_time)}\n"
        f"상태: {status}"
    )


bot.run(TOKEN)