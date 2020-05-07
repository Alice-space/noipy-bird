# game main loop
def getVoiceFreq():
    # get avarange frequency of sound
    # return a num in [0,255]
    from Maix import GPIO, I2S, FFT
    import image, lcd, math
    from board import board_info
    from fpioa_manager import fm
    from machine import Timer

    def timeCallBack():
        global next
        next = False

    next = True
    tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_ONE_SHOT, period=5, callback=timeCallBack, arg=on_timer,
                start=True, priority=1)
    sample_rate = 38640
    sample_points = 1024
    fft_points = 512
    hist_x_num = 50

    # close WiFi
    fm.register(8, fm.fpioa.GPIO0, force=True)
    wifi_en = GPIO(GPIO.GPIO0, GPIO.OUT)
    wifi_en.value(0)

    fm.register(20, fm.fpioa.I2S0_IN_D0, force=True)
    fm.register(30, fm.fpioa.I2S0_WS, force=True)  # 19 on Go Board and Bit(new version)
    fm.register(32, fm.fpioa.I2S0_SCLK, force=True)  # 18 on Go Board and Bit(new version)

    mic = I2S(I2S.DEVICE_0)
    mic.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode=I2S.STANDARD_MODE)
    mic.set_sample_rate(sample_rate)
    lstHeight = []
    while next:
        audio = mic.record(sample_points)
        fft_res = FFT.run(audio.to_bytes(), fft_points)
        fft_amp = FFT.amplitude(fft_res)
        for j in range(len(fft_amp)):
            lstHeight.append(fft_amp[j])
        lstHeight.sort()
        Freq = lstHeight[-1]
        fft_amp.clear()
    return Freq


import time

import lvgl as lv
from machine import Timer


class noipyBird:
    '''
    main class of noipy bird
    '''
    def __init__(self):
        self.welcomeGUI()

    def welcomeGUI(self):
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
        self.loop()

    def tutorialGUI(self):
        # paint tutorial gui
        pass

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

    def loop(self):
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
