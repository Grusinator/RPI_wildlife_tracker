import io
import os
from PIL import Image, ImageChops
import argparse
try:
    import picamera
except:
    print("not on pi")
import math
import datetime
from rest_client import ImageRestClient




def image_entropy(img):
    """calculate the entropy of an image"""
    # this could be made more efficient using numpy
    histogram = img.histogram()
    histogram_length = sum(histogram)
    samples_probability = [float(h) / histogram_length for h in histogram]
    return -sum([p * math.log(p, 2) for p in samples_probability if p != 0])



def detect_motion(camera, prior_image = None, prior_detect = False):
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg', use_video_port=True)
    stream.seek(0)
    if prior_image is None:
        prior_image = Image.open(stream)
        prior_detect = False
        return prior_image, prior_detect
    else:
        current_image = Image.open(stream)
        # Compare current_image to prior_image to detect motion. This is
        # left as an exercise for the reader!

        diff_image = ImageChops.difference(prior_image,current_image)

        value = image_entropy(diff_image)
        print('%.2f' %value)
        # Once motion detection is done, make the prior image the current
        prior_image = current_image

        # if detection occured in frame before, the threshold is not as high.
        if prior_detect & (value > 5) | (value > 6):
            prior_detect = True
            return prior_image, prior_detect
        else:
            prior_detect = False
            return prior_image, prior_detect


def motion_detection(server="http://192.168.10.136:8000", no_upload=False):
    prior_image = None
    prior_detect = False

    output_path = "/home/pi/wildlife_tracker_data/"
    if not no_upload:
        rest = ImageRestClient(server)

    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        stream = picamera.PiCameraCircularIO(camera, seconds=10)
        camera.start_recording(stream, format='h264')
        try:
            while True:
                camera.wait_recording(1)
                print(".")

                # compare image with previous image
                prior_image, prior_detect = detect_motion(camera, prior_image, prior_detect)

                # if change was found
                if prior_detect:
                    print('Motion detected!')
                    # As soon as we detect motion, split the recording to
                    # record the frames "after" motion
                    camera.split_recording('after.h264')
                    # Write the 10 seconds "before" motion to disk as well
                    stream.copy_to('before.h264', seconds=10)
                    stream.clear()
                    # Wait until motion is no longer detected, then split
                    # recording back to the in-memory circular buffer
                    image_fn = "img_" + str(datetime.datetime.now()) + ".jpg"

                    image_path = os.path.join(output_path, image_fn)
                    prior_image.save(image_path)
                    if not no_upload:
                        print("motion detected.. upload image here")
                        rest.upload_image(image_path, os.path.basename(image_fn), "PI upload")

                    # as long as the image keep changing keep the loop on 
                    while prior_detect:
                        camera.wait_recording(1)
                        prior_image, prior_detect = detect_motion(camera, prior_image, prior_detect)
                        
                    
                    print('Motion stopped!')
                    camera.split_recording(stream)
        finally:
            camera.stop_recording()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--no_upload", help="select to not upload to server", action='store_true')
    parser.add_argument("--server", help="select server")
    args = parser.parse_args()

    if args.server:
        server = args.server


    motion_detection(server=args.server, no_upload=args.no_upload)
