# Multimodal SLAM: RGB-D + Audio  

This project explores **multimodal SLAM (Simultaneous Localization and Mapping)** using **RGB images, depth data, and audio signals**.  
The current focus is on **pose estimation**, with the long-term goal of extending it to **echolocation-based mapping** and **lightweight, memory-efficient computation** (all done locally without requiring a server).  

---

## Dataset  

A sample recorded ROS bag file can be accessed here:  
[https://drive.google.com/drive/folders/1Wh-ExovXClhgEAsn9F70zVJ-l31-Trhy](#)  <!-- Replace with actual link -->

The dataset contains:  
- **RGB images** (`/camera/rgb/image_raw`)  
- **Depth images** (`/camera/depth/image_raw`)  
- **Sonar readings** (front, back, left, right)  
- **Ground-truth state** (pose and orientation)  

---

## Workflow  

1. **Simulation & Data Recording**  
   - Setup **ROS Noetic** inside Docker.  
   - Simulate a **quadcopter robot** in a custom world.  
   - Record the following topics using `rosbag`:  
     - RGB camera  
     - Depth camera  
     - Sonar sensors (to be extended for echolocation)  
     - Ground truth pose  

2. **Training & Processing**  
   - Extract RGB, Depth, and Sonar data from the recorded bag.  
   - Use the multimodal data to train pose estimation models.  
   - Future work:  
     - Extend to full SLAM with audio-based echolocation.  
     - Optimize for **on-device, memory-efficient computation**.  

---

## Roadmap  

- [x] RGB + Depth + Sonar data + Ground truth recording   
- [ ] Echolocation integration  
- [ ] Memory-efficient SLAM (edge-compute focus)  
- [ ] Full multimodal SLAM pipeline  

---

## TODO  

- [ ] Push the **Gazebo simulation setup** with the setup procedure . 


