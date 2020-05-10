# game main loop
import lvgl as lv
import utime
from machine import Timer
from Maix import FFT, GPIO, I2S
from pngdecoder import get_png_info, open_png

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
lv.img.cache_set_size(10)
# img load
with open('img/bird.png', 'rb') as f:
    png_data = f.read()
bird_img = lv.img_dsc_t({'data_size': len(png_data), 'data': png_data})

with open('img/pipe_bottom.png', 'rb') as f:
    png_data = f.read()
pipe_img_bottom = lv.img_dsc_t({'data_size': len(png_data), 'data': png_data})

with open('img/pipe_top.png', 'rb') as f:
    png_data = f.read()
pipe_img_top = lv.img_dsc_t({'data_size': len(png_data), 'data': png_data})

with open('img/cute_bird.png', 'rb') as f:
    png_data = f.read()
cute_bird_img_dsc = lv.img_dsc_t({
    'data_size': len(png_data),
    'data': png_data
})
with open('img/sad.png', 'rb') as f:
    png_data = f.read()
sad_img_dsc = lv.img_dsc_t({'data_size': len(png_data), 'data': png_data})

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
    ampl = max(fft_amp)
    freq = fft_amp.index(ampl)
    fft_amp.clear()
    if freq < 200 and ampl > 10:
        if len(freq_lis) < 5:
            freq_lis.append(freq)
        else:
            freq_lis.pop(0)
            freq_lis.append(freq)
    return 0 if not freq_lis else sum(freq_lis) / len(freq_lis)


def welcomeGUI():
    # paint welcome guis
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
            btn.set_toggle(True)
            return True


class Bird:
    # refresh bird on the screen
    def __init__(self, scr, x0=5, y0=0):
        # the bird
        self.bird = lv.img(scr)
        self.bird.align(scr, lv.ALIGN.IN_LEFT_MID, x0, y0)
        self.bird.set_src(bird_img)
        self.bird.set_drag(True)

    def set_pos(self, x, y):
        self.bird.set_pos(x, y)


class Pipe:
    # refresh pipe on the screen
    def __init__(self, scr, x=300, y=50):
        # the pipe
        self.pipe_bottom = lv.img(scr)
        self.pipe_bottom.align(scr, lv.ALIGN.IN_LEFT_MID, x, y)
        self.pipe_bottom.set_src(pipe_img_bottom)
        self.pipe_bottom.set_drag(True)

        self.pipe_top = lv.img(scr)
        self.pipe_top.align(scr, lv.ALIGN.IN_LEFT_MID, x, y - 400)
        self.pipe_top.set_src(pipe_img_top)
        self.pipe_top.set_drag(True)

    def set_pos(self, x, y):
        self.pipe_bottom.set_pos(x, y)
        self.pipe_top.set_pos(x, y - 400)

    def flush_forward(self, delta_x):
        self.set_pos(self.get_x() + delta_x, self.get_y())

    def get_x(self):
        return int(self.pipe_bottom.get_x())

    def get_y(self):
        return int(self.pipe_bottom.get_y())


def deathGUI():
    # GUI when died
    scr = lv.obj()
    sad_img = lv.img(scr)
    sad_img.align(scr, lv.ALIGN.IN_LEFT_MID, 0, 0)
    sad_img.set_src(sad_img_dsc)
    btn = lv.btn(scr)
    btn.align(lv.scr_act(), lv.ALIGN.CENTER, 0, -30)
    label = lv.label(btn)
    label.set_text("Game over")
    lv.scr_load(scr)
    while True:
        if button.value() == 0:
            btn.set_toggle(True)
            return True


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


def collision_detect(bird_y, y):
    # return true if collision
    if bird_y > (y+40) or bird_y < (y - 100):
        return True
    else:
        return False


def mainloop():
    scr = lv.obj()
    bird = Bird(scr)
    pipes = [Pipe(scr, x=600 - i * 150, y=lstHeight[i]) for i in range(6)]
    lv.scr_load(scr)
    j = 6
    while True:
        # set bird
        bird_y = int(getVoiceFreq() * 10)
        bird.set_pos(5, bird_y)
        # draw pipe
        for pipe in pipes:
            pipe.flush_forward(-1)
        # collision detect
        # TODO need adjust
        if pipes[-1].get_x() == 10:
            if collision_detect(bird_y, pipes[-1].get_y()):
                return True
        if pipes[-1].get_x() < 0:
            pipe = pipes.pop(-1)
            pipe.set_pos(900, lstHeight[j])
            j = j + 1
            pipes.insert(0, pipe)

lstHeight = [10, 40, 30, 35, 15, 45, 100, 120, 100, 105, 115, 105, 100, 120, 95, 105, 90, 120, 125, 120, 95, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90]
regTimer()
while True:
    welcomeGUI()
    if mainloop():
        deathGUI()
        utime.sleep_ms(700)
