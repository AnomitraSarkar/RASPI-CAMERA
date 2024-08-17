from picamera2 import Picamera2
picam2 = Picamera2()


video_config = picam2.video_configuration

# Configure resolution, format, and frame rate
video_config.main.size = (1920, 1080)       # Set resolution to 1280x720 (720p)
video_config.main.format = "RGB888"        # Set format to RGB888 (24-bit color)
video_config.controls.FrameDurationLimits = (16667, 16667)  # Set frame duration for 60 fps

# Apply the video configuration
picam2.configure("video")



# Set the video configuration
picam2.video_configuration.controls.FrameRate = 60.0
# picam2.video_configuration.controls.main.size = (1280,720)
# picam2.configure("video")

#picam2.set_controls({"FrameRate": 60})


picam2.start_and_record_video("res.mp4", duration=5)
