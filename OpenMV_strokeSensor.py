import sensor, image, time, math, pyb, struct
from pyb import LED

usb = pyb.USB_VCP()

# tracks white, dependent on room lighting
GRAYSCALE_THRESHOLD = [(150, 255)]

# initialize LEDs
red_led = LED(1)
green_led = LED(2)

# first ROI = top of image, second ROI = bottom of image
# ROI = [initial x pos, initial y pos, x distance, y distance, weight]
ROIS = [(0, 0, 160, 40, 0.3), (0, 80, 160, 40, 0.7)]

# camera setup
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # grayscale
sensor.set_framesize(sensor.QQVGA) # QQVGA for speed
# higher exposure = lower fps; lower exposure = higher fps
sensor.set_auto_exposure(False,exposure_us=1000)
sensor.skip_frames(time = 2000) # new settings take effect
sensor.set_auto_gain(False) # turned off for color tracking
sensor.set_auto_whitebal(False) # turned off for color tracking
clock = time.clock() # tracks FPS

while(True):

    clock.tick() # track elapsed milliseconds between snapshots()
    img = sensor.snapshot() # take a picture and return image

    center_sum = 0

    for r in ROIS:
        for blob in img.find_blobs(GRAYSCALE_THRESHOLD, roi=r[0:4], area_threshold=100, pixels_threshold=100, merge=True):

            img.draw_rectangle(blob.rect(), color=127)
            img.draw_cross(blob.cx(), blob.cy(), color=127)

            center_sum += blob.cx() * r[4] # r[4] is the roi weight

            if blob:
                green_led.toggle()

    center_pos = center_sum # center of line

    hip_angle = 0
    # frame size: half of x-axis (width) = 80 and half of y-axis (height) = 60
    hip_angle = abs(-math.atan((center_pos-80)/60))
    # convert angle in radians to degrees
    hip_angle = abs(round(math.degrees(hip_angle) - 30))

    # print statements
    #print("Hip Angle: %f" % hip_angle)
    print("%f" % hip_angle)
    #print(clock.fps())

    usb.send(str(hip_angle), timeout=100)
