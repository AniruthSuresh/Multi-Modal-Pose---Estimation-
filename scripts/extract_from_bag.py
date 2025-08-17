import rosbag
import rospy
import cv2
from cv_bridge import CvBridge
import os
import csv
import numpy as np

bag_file = "/home/aniruth/Desktop/Courses/Independent - Study/Own-Drone-setup/bag_data/drone_dataset_2025-08-17-14-43-17.bag.active"

output_dir = "drone_dataset_extracted"
os.makedirs(output_dir, exist_ok=True)

image_dir = os.path.join(output_dir, "rgb_images")
depth_dir = os.path.join(output_dir, "depth_images")
os.makedirs(image_dir, exist_ok=True)
os.makedirs(depth_dir, exist_ok=True)

bridge = CvBridge()

sonar_file = open(os.path.join(output_dir, "sonar.csv"), "w", newline="")
state_file = open(os.path.join(output_dir, "ground_truth_state.csv"), "w", newline="")

sonar_writer = csv.writer(sonar_file)
state_writer = csv.writer(state_file)

sonar_writer.writerow(["time", "front", "back", "left", "right"])
state_writer.writerow(["time", "x", "y", "z", "qx", "qy", "qz", "qw"])

sonar_data = {"front": None, "back": None, "left": None, "right": None}

with rosbag.Bag(bag_file, "r") as bag:
    for topic, msg, t in bag.read_messages():
        timestamp = t.to_sec()

        if topic == "/camera/rgb/image_raw":
            cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            cv2.imwrite(os.path.join(image_dir, f"{timestamp:.6f}.png"), cv_img)

        elif topic == "/camera/depth/depth/image_raw":
            depth_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")

            # Handle different encodings
            if depth_img.dtype == 'float32':  # 32FC1
                # Convert NaNs to zero
                depth_img = np.nan_to_num(depth_img, nan=0.0, posinf=0.0, neginf=0.0)
                # Normalize for visualization (0–255)
                depth_vis = cv2.normalize(depth_img, None, 0, 255, cv2.NORM_MINMAX)
                depth_vis = depth_vis.astype('uint8')
            elif depth_img.dtype == 'uint16':  # 16UC1
                # Normalize down to 8-bit for visualization
                depth_vis = cv2.normalize(depth_img, None, 0, 255, cv2.NORM_MINMAX)
                depth_vis = depth_vis.astype('uint8')
            else:
                depth_vis = depth_img  # Already something imwrite can handle

            cv2.imwrite(os.path.join(depth_dir, f"{timestamp:.6f}.png"), depth_vis)


        elif topic == "/sonar/front":
            sonar_data["front"] = msg.range
        elif topic == "/sonar/back":
            sonar_data["back"] = msg.range
        elif topic == "/sonar/left":
            sonar_data["left"] = msg.range
        elif topic == "/sonar/right":
            sonar_data["right"] = msg.range

            if all(v is not None for v in sonar_data.values()):
                sonar_writer.writerow([
                    timestamp,
                    sonar_data["front"],
                    sonar_data["back"],
                    sonar_data["left"],
                    sonar_data["right"]
                ])
                sonar_data = {"front": None, "back": None, "left": None, "right": None}

        elif topic == "/ground_truth/state":
            pos = msg.pose.pose.position
            ori = msg.pose.pose.orientation
            state_writer.writerow([
                timestamp,
                pos.x, pos.y, pos.z,
                ori.x, ori.y, ori.z, ori.w
            ])

sonar_file.close()
state_file.close()
print(f"Data extracted to {output_dir}")
