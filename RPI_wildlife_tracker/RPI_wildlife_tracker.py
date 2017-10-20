#from gpiozero import MotionSensor
import logging
from datetime import datetime
from subprocess import call
import picamera
import time
import os

logfile = "/home/pi/trailcam_log/trailcam_log-"+str(datetime.now().strftime("%Y%m%d-%H%M"))+".csv"
logging.basicConfig(filename=logfile, level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d, %H:%M:%S,')

#pir = MotionSensor(17)

print('Starting')
logging.info('Starting')

# Wait an initial duration to allow PIR to settle
time.sleep(10)

while True:    
    time.sleep(10)
   
    #pir.wait_for_motion()
    logging.info('Motion detected')
    print('Motion detected')
    timepoint = datetime.now

    #wait for 5 seconds 
    while timepoint + 5 < datetime.now:
        print('Taking photo')
        ts = '{:%Y%m%d-%H%M%S}'.format(datetime.now())
        logging.info('Taking photo: '+ str(ts)+'.jpg')
        with picamera.PiCamera() as cam:
            cam.resolution=(1024,768)
            cam.annotate_background = picamera.Color('black')

            cam.start_recording('/home/pi/video.h264')
            start = datetime.now()
            while (datetime.now() - start).seconds < 30:
                cam.annotate_text = "Peak Nature "+datetime.now().strftime('%d-%m-%y %H:%M:%S')
                cam.wait_recording(0.2)
            cam.stop_recording()
        time.sleep(5)
        timestamp = datetime.now().strftime('%d-%m-%y_%H-%M-%S')
        input_video = "/home/pi/video.h264"

        logging.info('Attempting to save image')

        if os.path.isdir('mnt/usb1/videos'):
            logging.info('Saving to /mnt/usb1/videos/')
            output_video = "/mnt/usb1/videos/{}.mp4".format(timestamp)
        elif os.path.isdir('mnt/usb2/videos'):
            logging.info('Saving to /mnt/usb2/videos/')
            output_video = "/mnt/usb2/videos/{}.mp4".format(timestamp)
        else:
            logging.info('Saving to /home/pi/videos/')
            output_video = "/home/pi/videos/{}.mp4".format(timestamp)

        call(["MP4Box", "-add", input_video, output_video])
        time.sleep(10)
    print('Motion Ended')
    logging.info('Motion Ended')