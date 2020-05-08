# game main loop
import time

import lvgl as lv
from machine import Timer
from Maix import FFT, I2S

############################
# config record constant
sample_rate = 38640
sample_points = 1024
fft_points = 512

mic = I2S(I2S.DEVICE_0)  # 新建一个I2S对象，麦克风
mic.channel_config(mic.CHANNEL_0, mic.RECEIVER,
                   align_mode=I2S.STANDARD_MODE)  # 配置通道
mic.set_sample_rate(38640)  # 采样率38640

freq_lis = []


def getVoiceFreq():
    # get avarange frequency of sound
    # return a num in [0,512)
    global freq_lis
    audio = mic.record(sample_points)
    fft_res = FFT.run(audio.to_bytes(), fft_points)
    fft_amp = FFT.amplitude(fft_res)
    freq = fft_amp.index(max(fft_amp))
    fft_amp.clear()
    if freq < 200:
        if len(freq_lis) < 20:
            freq_lis.append(freq)
        else:
            freq_lis.pop(0)
            freq_lis.append(freq)
    return sum(freq_lis) / len(freq_lis)



def welcomeGUI():
    # paint welcome guis
    # need a png background
    # shout to start flotting letters
    # a line of tutorial
    scr = lv.obj()
    btn = lv.btn(scr)
    btn.align(lv.scr_act(), lv.ALIGN.CENTER, 0, 0)
    label = lv.label(btn)
    label.set_text("Button")
    lv.scr_load(scr)
    # lv.task_create(testTask, 50, lv.TASK_PRIO.MID, 10)
    return loop()


def main(self):
    # main loop
    pass


def flushBird(self):
    # refresh bird on the screen
    pass


def flushPipe(self):
    # refresh movin pipe
    pass


def deathGUI(self):
    pass


def loop():
    # main loop of lvgl
    def on_timer(timer):
        lv.tick_inc(5)
        print(getVoiceFreq())

    timer = Timer(Timer.TIMER0,
                  Timer.CHANNEL0,
                  mode=Timer.MODE_PERIODIC,
                  period=5,
                  unit=Timer.UNIT_MS,
                  callback=on_timer,
                  arg=None)

    while True:
        tim = time.ticks_ms()
        lv.task_handler()
        while time.ticks_ms() - tim < 5:
            pass


welcomeGUI()
