import io
from PIL import Image, ImageChops
import picamera
import math




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
        return False
    else:
        current_image = Image.open(stream)
        # Compare current_image to prior_image to detect motion. This is
        # left as an exercise for the reader!

        diff_image = ImageChops.difference(prior_image,current_image)

        value = image_entropy(diff_image)
        print('%.2f' %value)
        # Once motion detection is done, make the prior image the current
        prior_image = current_image

        if prior_detect & value > 5 | value > 6:
            prior_detect = True
            return prior_image, prior_detect
        else:
            prior_detect = False
            return prior_image, prior_detect


def motion_detection():
    prior_image = None
    prior_detect = False

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

                    if detect_motion(camera):
                        print("motion detected.. upload image here")

                    # as long as the image keep changing keep the loop on 
                    while prior_detect:
                        camera.wait_recording(1)
                        prior_image, prior_detect = detect_motion(camera, prior_image, prior_detect)
                        
                    
                    print('Motion stopped!')
                    camera.split_recording(stream)
        finally:
            camera.stop_recording()

if __name__ == "__main__":
    motion_detection()
