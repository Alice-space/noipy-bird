# game main loop
import time

import lvgl as lv
from pngdecoder import get_png_info, open_png
from machine import Timer
from Maix import FFT, I2S
from Maix import GPIO

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
# Register png image decoder
decoder = lv.img.decoder_create()
decoder.info_cb = get_png_info
decoder.open_cb = open_png
# cache size
lv.img.cache_set_size(2)

############################
# register boot button
button = GPIO(GPIO.GPIO1, GPIO.IN)


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
    with open('img/cute_bird.png', 'rb') as f:
        png_data = f.read()
    cute_bird_img_dsc = lv.img_dsc_t({
        'data_size': len(png_data),
        'data': png_data
    })
    scr = lv.obj()
    cute_bird_img = lv.img(scr)
    cute_bird_img.align(scr, lv.ALIGN.CENTER, 0, 0)
    cute_bird_img.set_src(cute_bird_img_dsc)
    btn = lv.btn(scr)
    btn.align(lv.scr_act(), lv.ALIGN.CENTER, 0, 0)
    label = lv.label(btn)
    label.set_text("Play")
    lv.scr_load(scr)
    while True:
        if button.value() == 0:
            label.set_text("NICE")


class Bird:
    # refresh bird on the screen
    def __init__(self, scr, x0=0, y0=0):
        # the bird
        with open('img/bird.png', 'rb') as f:
            png_data = f.read()
        bird_img = lv.img_dsc_t({'data_size': len(png_data), 'data': png_data})
        self.bird = lv.img(scr)
        self.bird.align(scr, lv.ALIGN.IN_LEFT_MID, x0, y0)
        self.bird.set_src(bird_img)
        # not dragable for no touchscreen
        # img1.set_drag(True)

    def set_pos(self, x, y):
        self.bird.set_pos(x, y)


class Pipe:
    # refresh pipe on the screen
    def __init__(self, scr, x1=113, y1=50, x2=113, y2=-50):
        # the pipe
        with open('img/pipe_bottom.png', 'rb') as f:
            png_data = f.read()
        pipe_img_bottom = lv.img_dsc_t({
            'data_size': len(png_data),
            'data': png_data
        })
        self.pipe_bottom = lv.img(scr)
        self.pipe_bottom.align(scr, lv.ALIGN.IN_LEFT_MID, x1, y1)
        self.pipe_bottom.set_src(pipe_img_bottom)

        with open('img/pipe_top.png', 'rb') as f:
            png_data = f.read()
        pipe_img_top = lv.img_dsc_t({
            'data_size': len(png_data),
            'data': png_data
        })
        self.pipe_top = lv.img(scr)
        self.pipe_top.align(scr, lv.ALIGN.IN_LEFT_MID, x2, y2)
        self.pipe_top.set_src(pipe_img_top)

    def set_pos(self, x1, y1, x2, y2):
        self.pipe_bottom.set_pos(x1, y1)
        self.pipe_top.set_pos(x2, y2)


def deathGUI():
    with open('img/sad.png', 'rb') as f:
        png_data = f.read()
    sad_img_dsc = lv.img_dsc_t({'data_size': len(png_data), 'data': png_data})
    scr = lv.obj()
    sad_img = lv.img(scr)
    sad_img.align(scr, lv.ALIGN.IN_LEFT_MID, 0, 0)
    sad_img.set_src(sad_img_dsc)
    btn = lv.btn(scr)
    btn.align(lv.scr_act(), lv.ALIGN.CENTER, 0, -30)
    label = lv.label(btn)
    label.set_text("Game over")
    lv.scr_load(scr)


def regTimer():
    # register timer
    def on_timer(timer):
        lv.tick_inc(5)
        lv.task_handler()

    Timer(Timer.TIMER0,
          Timer.CHANNEL0,
          mode=Timer.MODE_PERIODIC,
          period=5,
          unit=Timer.UNIT_MS,
          callback=on_timer,
          arg=None)


regTimer()
welcomeGUI()
