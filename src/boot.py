import lcd
import lvgl as lv
import lvgl_helper as lv_h
from fpioa_manager import fm
from machine import I2C
from Maix import GPIO

######################################
# config options
config_touchscreen_support = False
board_m1n = False

######################################
# initialize lvgl and lcd

i2c = I2C(I2C.I2C0, freq=400000, scl=30, sda=31)
if not board_m1n:
    lcd.init()
else:
    lcd.init(type=2, freq=20000000)
if config_touchscreen_support:
    import touchscreen as ts
    ts.init(i2c)

lv.init()
disp_buf1 = lv.disp_buf_t()
buf1_1 = bytearray(320 * 10)
lv.disp_buf_init(disp_buf1, buf1_1, None, len(buf1_1) // 4)
disp_drv = lv.disp_drv_t()
lv.disp_drv_init(disp_drv)
disp_drv.buffer = disp_buf1
disp_drv.flush_cb = lv_h.flush
if board_m1n:
    disp_drv.hor_res = 240
    disp_drv.ver_res = 240
else:
    disp_drv.hor_res = 320
    disp_drv.ver_res = 240
lv.disp_drv_register(disp_drv)

if config_touchscreen_support:
    indev_drv = lv.indev_drv_t()
    lv.indev_drv_init(indev_drv)
    indev_drv.type = lv.INDEV_TYPE.POINTER
    indev_drv.read_cb = lv_h.read
    lv.indev_drv_register(indev_drv)

# lv.log_register_print_cb(lv_h.log)
lv.log_register_print_cb(
    lambda level, path, line, msg: print('%s(%d): %s' % (path, line, msg)))
##################################
# initialize mic

fm.register(20, fm.fpioa.I2S0_IN_D0, force=True)
fm.register(30, fm.fpioa.I2S0_WS,
            force=True)  # 19 on Go Board and Bit(new version)
fm.register(32, fm.fpioa.I2S0_SCLK,
            force=True)  # 18 on Go Board and Bit(new version)


##################################
# close WiFi
fm.register(8, fm.fpioa.GPIO0, force=True)
wifi_en = GPIO(GPIO.GPIO0, GPIO.OUT)
wifi_en.value(0)

##################################
# auto enter main loop in main.py
