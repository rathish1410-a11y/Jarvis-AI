import speech_recognition as sr
import pyttsx3
import pyautogui
import os
import threading
import time
import math
import random
from datetime import datetime
import tkinter as tk

running = True
listening = False


def speak(text):
    update_reply(text)
    try:
        engine = pyttsx3.init("sapi5")
        voices = engine.getProperty("voices")
        if voices:
            engine.setProperty("voice", voices[0].id)
        engine.setProperty("rate", 195)
        engine.setProperty("volume", 1.0)
        time.sleep(0.08)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("Voice error:", e)


def take_command():
    global listening
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 300

    with sr.Microphone() as source:
        listening = True
        update_status("LISTENING")
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
        except sr.WaitTimeoutError:
            listening = False
            return ""

    try:
        command = recognizer.recognize_google(audio)
        command = command.lower().strip()
        update_user_text(command)
        listening = False
        return command
    except sr.UnknownValueError:
        listening = False
        return ""
    except sr.RequestError:
        listening = False
        speak("Internet is needed for speech recognition.")
        return ""


def take_screenshot():
    try:
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pyautogui.screenshot(filename)
        speak("Screenshot taken")
    except Exception as e:
        print("Screenshot error:", e)
        speak("Screenshot failed")


def volume_up():
    for _ in range(5):
        pyautogui.press("volumeup")
    speak("Volume increased")


def volume_down():
    for _ in range(5):
        pyautogui.press("volumedown")
    speak("Volume decreased")


def mute_volume():
    pyautogui.press("volumemute")
    speak("Muted")


def open_chrome():
    os.system("start chrome")
    speak("Opening Chrome")


def close_chrome():
    os.system("taskkill /IM chrome.exe /F >nul 2>&1")
    speak("Closing Chrome")


def open_notepad():
    os.system("start notepad")
    speak("Opening Notepad")


def open_calculator():
    os.system("start calc")
    speak("Opening Calculator")


def tell_time():
    current_time = datetime.now().strftime("%I:%M %p")
    speak(f"It is {current_time}")


def process_commands():
    global running
    speak("Hello Rathish. Jarvis is online.")

    while running:
        command = take_command()

        if not command:
            update_status("STANDBY")
            continue

        if "hello jarvis" in command or command == "hello":
            speak("Hello Rathish")
        elif "screenshot" in command:
            take_screenshot()
        elif "volume up" in command:
            volume_up()
        elif "volume down" in command:
            volume_down()
        elif "mute" in command:
            mute_volume()
        elif "open chrome" in command:
            open_chrome()
        elif "close chrome" in command:
            close_chrome()
        elif "open notepad" in command:
            open_notepad()
        elif "open calculator" in command:
            open_calculator()
        elif "time" in command:
            tell_time()
        elif "exit" in command or "stop" in command:
            speak("Shutting down interface")
            running = False
            root.after(500, root.destroy)
            break
        else:
            speak("Command not recognized")

        update_status("STANDBY")


def update_status(text):
    status_value.config(text=text)


def update_user_text(text):
    user_value.config(text=text)


def update_reply(text):
    reply_value.config(text=text)


def update_clock():
    if not running:
        return
    now = datetime.now()
    top_time.config(text=now.strftime("%I:%M:%S"))
    top_date.config(text=now.strftime("%d %b %Y"))
    root.after(1000, update_clock)


def draw_arc(cx, cy, r, width, start, extent, color, tag="hud"):
    canvas.create_arc(
        cx-r, cy-r, cx+r, cy+r,
        start=start, extent=extent,
        style="arc", outline=color,
        width=width, tags=tag
    )


def draw_ring(cx, cy, r, color, width=2, tag="hud"):
    canvas.create_oval(
        cx-r, cy-r, cx+r, cy+r,
        outline=color, width=width, tags=tag
    )


def draw_glow_line(x1, y1, x2, y2, color="#00F7FF", width=2):
    canvas.create_line(x1, y1, x2, y2, fill=color, width=width, tags="hud")


def animate_hud():
    global a1, a2, a3, pulse

    if not running:
        return

    canvas.delete("hud")

    # Background tiny dots
    for i in range(35):
        x = (i * 53 + a1 * 3) % screen_w
        y = (i * 41 + a2 * 4) % screen_h
        canvas.create_oval(x, y, x+2, y+2, fill="#0dc7d6", outline="", tags="hud")

    # faint horizontal lines
    for y in range(100, screen_h, 120):
        canvas.create_line(20, y, screen_w-20, y, fill="#05222A", width=1, tags="hud")

    # top index numbers
    for i in range(1, 31):
        x = 15 + i * 58
        txt = f"{i:02d}"
        color = "#00eaff" if i != 21 else "#00151b"
        if i == 21:
            canvas.create_rectangle(x-10, 8, x+22, 44, fill="#2ef3ff", outline="#2ef3ff", tags="hud")
            canvas.create_text(x+6, 26, text=txt, fill="#00151b", font=("Consolas", 18, "bold"), tags="hud")
        else:
            canvas.create_text(x+6, 26, text=txt, fill="#00eaff", font=("Consolas", 18, "bold"), tags="hud")

    # center main reactor
    cx, cy = screen_w // 2, screen_h // 2 + 10
    pulse += pulse_dir[0] * 1.4
    if pulse > 172:
        pulse_dir[0] = -1
    elif pulse < 156:
        pulse_dir[0] = 1

    draw_ring(cx, cy, pulse, "#06343E", 3)
    draw_ring(cx, cy, 175, "#0EF0FF", 5)
    draw_ring(cx, cy, 150, "#0AC3DE", 3)
    draw_ring(cx, cy, 118, "#0EF0FF", 3)
    draw_ring(cx, cy, 92, "#0A8DA3", 2)
    canvas.create_oval(cx-74, cy-74, cx+74, cy+74, fill="#041820", outline="#0EF0FF", width=2, tags="hud")
    canvas.create_oval(cx-24, cy-24, cx+24, cy+24, fill="#35e8ff", outline="#7cf6ff", width=2, tags="hud")
    canvas.create_oval(cx-12, cy-12, cx+12, cy+12, fill="#9afcff", outline="", tags="hud")

    draw_arc(cx, cy, 205, 6, a1, 65, "#0EF0FF")
    draw_arc(cx, cy, 205, 6, a1+140, 45, "#0A8DA3")
    draw_arc(cx, cy, 230, 4, -a2, 50, "#27FFD3")
    draw_arc(cx, cy, 230, 4, -a2+180, 45, "#0EF0FF")
    draw_arc(cx, cy, 255, 3, a3+40, 35, "#73F7FF")
    draw_arc(cx, cy, 255, 3, a3+220, 35, "#73F7FF")

    for i in range(36):
        ang = math.radians(i * 10 + a1)
        x1 = cx + math.cos(ang) * 135
        y1 = cy + math.sin(ang) * 135
        x2 = cx + math.cos(ang) * 165
        y2 = cy + math.sin(ang) * 165
        canvas.create_line(x1, y1, x2, y2, fill="#0EF0FF", width=2, tags="hud")

    # upper small circles
    draw_stat_circle(430, 190, 78, "CPU\n74\nI:57", a1, "#11eaff")
    draw_stat_circle(650, 120, 95, "RAM:\n75\nSWAP:\n49", -a2, "#11eaff")
    draw_stat_circle(1020, 170, 92, "2:40", a3, "#11eaff", center_size=24)

    # left month/date circle
    draw_stat_circle(170, 190, 105, "JUNE\n21", -a1, "#11eaff", center_size=28)

    # left lower widgets
    draw_stat_circle(165, 540, 70, "POWER\n100%", a2, "#11eaff", center_size=18)
    draw_stat_circle(430, 875, 82, "0.0k\n1.6k", -a3, "#11eaff", center_size=18)

    # right lower circles
    draw_stat_circle(1170, 615, 85, "ART", a2, "#11eaff", center_size=18)
    draw_stat_circle(1455, 615, 85, "TRASH", -a2, "#11eaff", center_size=18)

    # left info rails
    draw_panel_frames()

    # connecting lines
    draw_glow_line(275, 190, 340, 190)
    draw_glow_line(510, 190, 640, 190)
    draw_glow_line(745, 120, 930, 120)
    draw_glow_line(1110, 170, 1280, 170)

    draw_glow_line(510, 875, 740, 875)
    draw_glow_line(940, 875, 1110, 875)
    draw_glow_line(1260, 615, 1370, 615)

    # listening bars near center bottom
    bar_x = cx - 140
    for i in range(30):
        h = random.randint(10, 80) if listening else 16
        color = "#14f3ff" if listening else "#0a4a57"
        canvas.create_line(bar_x + i * 9, cy + 255, bar_x + i * 9, cy + 255 - h, fill=color, width=4, tags="hud")

    # bottom line chart
    base_y = screen_h - 135
    last_x = 1110
    last_y = base_y
    for i in range(40):
        x = 1110 + i * 17
        y = base_y - random.randint(0, 35)
        canvas.create_line(last_x, last_y, x, y, fill="#1af0ff", width=2, tags="hud")
        last_x, last_y = x, y

    # right weather style column
    weather_x = screen_w - 255
    canvas.create_text(weather_x, 120, text="13°C", fill="#42f6ff", font=("Arial", 40, "bold"), tags="hud")
    canvas.create_text(weather_x, 170, text="CLEAR", fill="#9bfbff", font=("Arial", 20, "bold"), tags="hud")
    canvas.create_text(weather_x, 215, text="HUMIDITY: 77%\nWIND: 3 km/h\nVISIBILITY: 10 km", fill="#72edf4",
                       font=("Consolas", 16), justify="left", tags="hud")
    canvas.create_oval(screen_w-135, 75, screen_w-35, 175, fill="#85f7ff", outline="#d4ffff", width=2, tags="hud")

    forecast_y = 350
    days = ["TODAY", "TOMORROW", "FRIDAY", "SATURDAY", "SUNDAY", "MONDAY", "TUESDAY"]
    temps = ["11°", "23° / 11°", "23° / 11°", "19° / 12°", "17° / 11°", "19° / 11°", "22° / 12°"]
    for i, day in enumerate(days):
        y = forecast_y + i * 92
        canvas.create_text(screen_w-255, y, text=day, fill="#37efff", font=("Arial", 22, "bold"), anchor="w", tags="hud")
        canvas.create_text(screen_w-255, y+32, text=temps[i], fill="#88f9ff", font=("Arial", 16), anchor="w", tags="hud")
        canvas.create_oval(screen_w-88, y-8, screen_w-38, y+34, fill="#9dfaff", outline="", tags="hud")

    # top labels
    canvas.create_text(screen_w//2, 58, text="Laichzeit", fill="#23f2ff", font=("Arial", 28, "bold"), tags="hud")
    canvas.create_text(screen_w//2, 88, text="Rammstein", fill="#75f7ff", font=("Arial", 20), tags="hud")
    canvas.create_text(screen_w-175, 48, text="Moscow, Russia", fill="#27f1ff", font=("Arial", 22, "bold"), tags="hud")

    # status under center
    canvas.create_text(cx, cy+315, text="STARK INDUSTRIES", fill="#25f0ff", font=("Arial", 26, "bold"), tags="hud")

    a1 = (a1 + 3) % 360
    a2 = (a2 + 2) % 360
    a3 = (a3 + 1) % 360

    root.after(40, animate_hud)


def draw_stat_circle(cx, cy, r, text, angle, color, center_size=20):
    draw_ring(cx, cy, r, color, 4)
    draw_arc(cx, cy, r, 10, angle, 240, color)
    canvas.create_oval(cx-r+18, cy-r+18, cx+r-18, cy+r-18, fill="#04161D", outline="", tags="hud")
    canvas.create_text(cx, cy, text=text, fill="#38f5ff", font=("Consolas", center_size, "bold"), tags="hud")


def draw_panel_frames():
    # left side lines
    canvas.create_rectangle(55, 70, 305, 760, outline="#11eaff", width=2, tags="hud")
    canvas.create_line(55, 760, 370, 760, fill="#11eaff", width=2, tags="hud")
    canvas.create_line(55, 860, 305, 860, fill="#11eaff", width=2, tags="hud")
    canvas.create_rectangle(55, 780, 305, 1010, outline="#11eaff", width=2, tags="hud")

    # right side lines
    canvas.create_rectangle(screen_w-335, 70, screen_w-55, screen_h-60, outline="#11eaff", width=2, tags="hud")

    # boxes and labels
    canvas.create_text(115, 350, text="LOCAL DISK", fill="#49f4ff", font=("Arial", 16, "bold"), anchor="w", tags="hud")
    canvas.create_text(115, 388, text="USED: 100 G\nFREE: 2 G", fill="#79f9ff", font=("Consolas", 18), anchor="w", tags="hud")

    canvas.create_text(105, 665, text="BASKET\n0 FILES", fill="#49f4ff", font=("Arial", 18, "bold"), anchor="w", tags="hud")
    canvas.create_text(105, 735, text="WORK TIME: 1 d 4 h 0 min", fill="#79f9ff", font=("Consolas", 16), anchor="w", tags="hud")

    canvas.create_text(95, 812, text="COMMUNICATION", fill="#49f4ff", font=("Arial", 18, "bold"), anchor="w", tags="hud")
    canvas.create_text(220, 812, text="NEW MAIL", fill="#49f4ff", font=("Arial", 18, "bold"), anchor="w", tags="hud")

    canvas.create_text(95, 875, text="• PROGRAMS\n• MAIL\n• AGENT\n• CONTACTS", fill="#79f9ff",
                       font=("Consolas", 18), anchor="w", justify="left", tags="hud")

    canvas.create_text(92, 965, text="OPERATIONS\n• SHUTDOWN\n• RESTART", fill="#49f4ff",
                       font=("Consolas", 18, "bold"), anchor="w", justify="left", tags="hud")

    canvas.create_text(660, 405, text="Dead Space\nLimbo\nBastion\nAIMP 2\nSprint Layout 5.0\nArduino",
                       fill="#33efff", font=("Consolas", 18), anchor="w", justify="left", tags="hud")

    canvas.create_text(650, 735, text="• Games\n• Programs\n• Skydrive\n• Electronics",
                       fill="#33efff", font=("Consolas", 20), anchor="w", justify="left", tags="hud")

    canvas.create_text(545, 548, text="STARK\nEXPO\n2010", fill="#12d8e2",
                       font=("Arial", 36, "bold"), tags="hud")

    canvas.create_text(screen_w-240, 230, text="UPDATED 12:30 PM", fill="#53f8ff", font=("Arial", 16), tags="hud")


def close_app(event=None):
    global running
    running = False
    root.destroy()


root = tk.Tk()
root.title("JARVIS HUD")
root.attributes("-fullscreen", True)
root.configure(bg="black")
root.bind("<Escape>", close_app)

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

canvas = tk.Canvas(root, width=screen_w, height=screen_h, bg="black", highlightthickness=0)
canvas.place(x=0, y=0)

# overlays
top_time = tk.Label(root, text="", font=("Consolas", 28, "bold"), fg="#28efff", bg="black")
top_time.place(x=120, y=52)

top_date = tk.Label(root, text="", font=("Consolas", 13), fg="#7af8ff", bg="black")
top_date.place(x=122, y=95)

status_label = tk.Label(root, text="STATUS", font=("Consolas", 14), fg="#61f6d7", bg="black")
status_label.place(x=screen_w//2 - 45, y=115)

status_value = tk.Label(root, text="BOOTING", font=("Consolas", 16, "bold"), fg="#21ffd8", bg="black")
status_value.place(x=screen_w//2 - 55, y=145)

user_label = tk.Label(root, text="USER INPUT", font=("Consolas", 14, "bold"), fg="#ffffff", bg="black")
user_label.place(x=90, y=220)

user_value = tk.Label(root, text="waiting...", font=("Consolas", 16), fg="#ffffff", bg="black",
                      justify="left", anchor="nw", wraplength=250)
user_value.place(x=90, y=255, width=250, height=110)

reply_label = tk.Label(root, text="JARVIS OUTPUT", font=("Consolas", 14, "bold"), fg="#17f0ff", bg="black")
reply_label.place(x=90, y=435)

reply_value = tk.Label(root, text="system idle", font=("Consolas", 16), fg="#17f0ff", bg="black",
                       justify="left", anchor="nw", wraplength=250)
reply_value.place(x=90, y=470, width=250, height=110)

tip_label = tk.Label(
    root,
    text="ESC = CLOSE   |   COMMANDS: hello jarvis, time, screenshot, volume up, volume down, mute, open chrome, close chrome, open notepad, open calculator, exit",
    font=("Consolas", 12),
    fg="#5defff",
    bg="black"
)
tip_label.place(x=200, y=screen_h-42)

a1 = 0
a2 = 0
a3 = 0
pulse = 156
pulse_dir = [1]

threading.Thread(target=process_commands, daemon=True).start()
update_clock()
animate_hud()
root.mainloop()