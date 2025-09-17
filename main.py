"""Departure Warning System with a Monocular Camera"""

__author__ = "Junsheng Fu"
__email__ = "junsheng.fu@yahoo.com"
__date__ = "March 2017"


from lane_updated import *
from moviepy.editor import VideoFileClip
import os
import numpy as np


if __name__ == "__main__":

    demo = 2 # 1: image, 2 video

    if demo == 1:
        imagepath = 'examples/test11.jpg'
        img = cv2.imread(imagepath)
        img = cv2.resize(img, (1280, 720))  # Resize to 1280x720

        img_aug = process_frame(img)

        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(25, 9))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        ax1.imshow(img)
        ax1.set_title('Original Image', fontsize=30)
        img_aug = cv2.cvtColor(img_aug, cv2.COLOR_BGR2RGB)
        ax2.imshow(img_aug)
        ax2.set_title('Augmented Image', fontsize=30)
        plt.savefig('output_debug.png')
        plt.show()

    else:
        video_path = "examples/front_forward1.mp4"
        video_output = 'examples/front_forward1_test.mp4'

        if not os.path.exists(video_path):
            print(f"[INFO] Video not found at {video_path}. Falling back to single image demo.")
            imagepath = 'examples/test11.jpg'
            img = cv2.imread(imagepath)
            img = cv2.resize(img, (1280, 720))
            img_aug = process_frame(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_aug = cv2.cvtColor(img_aug, cv2.COLOR_BGR2RGB)
            plt.figure(figsize=(12,6))
            plt.subplot(1,2,1); plt.imshow(img); plt.title('Original'); plt.axis('off')
            plt.subplot(1,2,2); plt.imshow(img_aug); plt.title('Augmented'); plt.axis('off')
            plt.savefig('output_debug.png')
            plt.show()
        else:
            clip1 = VideoFileClip(video_path)

            # MoviePy provides RGB frames; convert to BGR before processing, then back to RGB
            def process_frame_rgb(frame_rgb):
                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                out_bgr = process_frame(frame_bgr)
                return cv2.cvtColor(out_bgr, cv2.COLOR_BGR2RGB)

            clip = clip1.fl_image(process_frame_rgb)
            clip.write_videofile(video_output, audio=False)

