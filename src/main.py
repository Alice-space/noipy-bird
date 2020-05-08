# game main loop
import time

import lvgl as lv
import pngdecoder
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

############################
# define color
COLOR_SIZE = lv.color_t.SIZE
COLOR_IS_SWAPPED = hasattr(lv.color_t().ch, 'green_h')

############################
# per-load assest
# the bird
with open('img/bird.png', 'rb') as f:
    png_data = f.read()

bird_img = lv.img_dsc_t({'data_size': len(png_data), 'data': png_data})

# the pipe(barrier)
with open('img/pipe_bottom.png', 'rb') as f:
    png_data = f.read()

pipe_img_bottom = lv.img_dsc_t({'data_size': len(png_data), 'data': png_data})

with open('img/pipe_top.png', 'rb') as f:
    png_data = f.read()

pipe_img_top = lv.img_dsc_t({'data_size': len(png_data), 'data': png_data})


def getVoiceFreq():
    # get avarange frequency of sound
    # return a num in [0,256),usuall in [0,27]
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
    scr = lv.obj()
    btn = lv.btn(scr)
    btn.align(lv.scr_act(), lv.ALIGN.CENTER, 0, 0)
    label = lv.label(btn)
    label.set_text("Play")
    lv.scr_load(scr)
    # lv.task_create(testTask, 50, lv.TASK_PRIO.MID, 10)
    return loop()


def main():
    # main loop
    pass


def flushBird():
    # refresh bird on the screen
    scr = lv.obj()
    bird = lv.img(scr)
    bird.align(scr, lv.ALIGN.IN_LEFT_MID, 0, 0)
    bird.set_src(bird_img)
    print(bird_img)
    print('qwqwqwqw')
    # not dragable for no touchscreen
    # img1.set_drag(True)

    # Load the screen and display image
    lv.scr_load(scr)


def flushPipe():
    # refresh moving pipe
    scr = lv.obj()
    # Create bottom pipe
    lv.img.cache_set_size(2)
    pipe_bottom = lv.img(scr)
    pipe_bottom.align(scr, lv.ALIGN.IN_LEFT_MID, 113, 50)  # 这里的横纵坐标表示下柱子的位置
    pipe_bottom.set_src(pipe_img_bottom)
    # not dragable for no touchscreen
    # pipe_down.set_drag(True)

    # create top pipe
    pipe_top = lv.img(scr)
    pipe_top.align(scr, lv.ALIGN.IN_LEFT_MID, 113, -50)  # 这里的横纵坐标表示下柱子的位置
    pipe_top.set_src(pipe_img_top)

    # Load the screen and display image
    lv.scr_load(scr)


def deathGUI():
    scr = lv.obj()
    btn = lv.btn(scr)
    btn.align(lv.scr_act(), lv.ALIGN.CENTER, 0, 0)
    label = lv.label(btn)
    label.set_text("Game over")
    lv.scr_load(scr)


def loop():
    # main loop of lvgl
    def on_timer(timer):
        lv.tick_inc(5)

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


# welcomeGUI()
flushBird()
loop()
