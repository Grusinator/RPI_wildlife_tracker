#from gpiozero import MotionSensor
import logging
from datetime import datetime
from subprocess import call
import picamera
import time
import os
from motion_detection import captureTestImage, testHasChanged

data_path = '/home/pi/wildlife_tracker_data/'
images_path = data_path + 'images/' 
logs_path = data_path + 'logs/'

def createIfNotExists(path):
    if not os.path.exists(data_path):
        os.mkdir(data_path)
        print("created path: "+ data_path)

paths_list = [data_path, images_path, logs_path]

[createIfNotExists(path) for path in paths_list]


logfile = logs_path + "/wildlife_tracker_log-"+str(datetime.now().strftime("%Y%m%d-%H%M"))+".csv"
logging.basicConfig(filename=logfile, level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d, %H:%M:%S,')


print('Starting')
logging.info('Starting')

# Wait an initial duration to allow PIR and Camera to settle
time.sleep(2)

image1, buffer1 = captureTestImage()

image1, buffer1 = captureTestImage()

# Reset last capture time
lastCapture = time.time()

#main loop
while True:    
    time.sleep(2)
    
    # Get comparison image
    image2, buffer2 = captureTestImage()

    #test for motions
    if testHasChanged(image1, image2, buffer1, buffer2):

        #pir.wait_for_motion()
        logging.info('Motion detected')
        print('Motion detected')

        print('Taking photo')
        ts = '{:%Y%m%d-%H%M%S}'.format(datetime.now())
        logging.info('Taking photo: '+ str(ts)+'.jpg')
        with picamera.PiCamera() as cam:
            cam.resolution=(1024,768)
            filename = images_path + ts + '.jpg'
            cam.capture(filename)
           

        #print('Motion Ended')
        #logging.info('Motion Ended')

    # Swap comparison buffers
    image1 = image2
    buffer1 = buffer2
