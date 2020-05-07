# game main loop
def getVoiceFreq():
    # get avarange frequency of sound
    # return a num in [0,255]
    pass


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


noipyBird = noipyBird()