# game main loop
def getVoiceFreq():
    # get avarange frequency of sound
    # return a num in [0,255]
    pass


class fileIO():
    # restore or read dict from txt on sdcard
    def __init__(self):
        try:
            with open('data.txt', 'r') as f:
                self.dict = eval(f.read())
        except OSError:
            self.dict = {'isfirst': True}
            with open('data.txt', 'w') as f:
                f.write(self.dict)

    def isfirst(self):
        # get info dict
        return self.dict['isfirst']

    def setInfo(self, isfirst=True):
        # not first open
        if not isfirst:
            self.dict['isfirst'] = True
            with open('data.txt', 'w') as f:
                f.write(self.dict)


class noipyBird:
    '''
    main class of noipy bird
    '''
    def __init__(self):
        pass

    def welcomeGUI(self):
        # paint welcome gui
        pass

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
