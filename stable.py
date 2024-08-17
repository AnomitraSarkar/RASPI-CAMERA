import cv2
import numpy as np

count = 0 #depends on fps

def counter_delay():
    global count, bf, keypoints_ref, descriptors_ref, gray_ref, orb
    if count==0:
        ret, reference_frame = cap.read()
        if not ret:
            print("Failed to capture video")
            cap.release()
            cv2.destroyAllWindows()
            exit()  # Exit if frame capture fails

        # Convert reference frame to grayscale
        gray_ref = cv2.cvtColor(reference_frame, cv2.COLOR_BGR2GRAY)

        # Create ORB detector
        orb = cv2.ORB_create()

        # Detect and compute keypoints and descriptors for the reference image
        keypoints_ref, descriptors_ref = orb.detectAndCompute(gray_ref, None)

        # Initialize BFMatcher
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        count = 50
        print("refreshed")
    count -= 1
    

# Initialize video capture
cap = cv2.VideoCapture(0)  # 0 for the default camera

# Set the camera resolution to 640x480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Read the first frame and set it as the reference image


# Define the codec and create VideoWriter objects
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' codec for MP4 format
original_output = cv2.VideoWriter('original_output.mp4', fourcc, 20.0, (1280, 720))  # 640x480 resolution
stabilized_output = cv2.VideoWriter('stabilized_output.mp4', fourcc, 20.0, (1280, 720))  # 640x480 resolution

while True:
    counter_delay()
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Write the original frame to the output file
    original_output.write(frame)

    # Convert current frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect and compute keypoints and descriptors for the current frame
    keypoints_frame, descriptors_frame = orb.detectAndCompute(gray_frame, None)

    # Match descriptors between the reference image and the current frame
    matches = bf.match(descriptors_ref, descriptors_frame)
    matches = sorted(matches, key=lambda x: x.distance)

    # Extract matched points
    if len(matches) > 20:  # Ensure enough matches
        points_ref = np.float32([keypoints_ref[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        points_frame = np.float32([keypoints_frame[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

        # Compute homography matrix
        homography_matrix, mask = cv2.findHomography(points_frame, points_ref, cv2.RANSAC)

        # If a homography matrix is found, warp the current frame to stabilize
        if homography_matrix is not None:
            stabilized_frame = cv2.warpPerspective(frame, homography_matrix, (frame.shape[1], frame.shape[0]))

            # Write the stabilized frame to the output file
            stabilized_output.write(stabilized_frame)

            # Show stabilized frame
            cv2.imshow('Stabilized Video', stabilized_frame)
        else:
            # If no homography matrix, just show the original frame
            cv2.imshow('Stabilized Video', frame)
            stabilized_output.write(frame)  # Write the original frame if stabilization fails
    else:
        # If not enough matches, just show the original frame
        cv2.imshow('Stabilized Video', frame)
        stabilized_output.write(frame)  # Write the original frame if not enough matches

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
original_output.release()
cv2.destroyAllWindows()
