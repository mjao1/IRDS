# facial-recognition-turret
A projectile/laser turret guided by facial recognition. The facial recognition is programmed in Python, which sends unrecognized face coordinates from an external webcam to an Arduino IDE where they are converted to corresponding angles and updated constantly for two servo motors on an Arduino UNO R4 WiFi (Later switched to a custom PCB using an ESP32-DevKitC). The projectile gearbox is actuated by a N-Channel MOSFET (RFP30N06LE) and controlled by the Arduino IDE. The servo structures, gearbox attachments, and electronics housing are designed in CAD and 3D printed. The goal of this project was to develop a cohesive, portable turret capable of recognizing and tracking faces based on checking images from folders containing known faces to act as a harmless local defense system against unknown identities.
<p align = "center">
  <img src="https://github.com/user-attachments/assets/4c4b9978-79f9-4a76-b641-4c870453d31d" width=50% height=50%>
</p>

<p align = "center">
  Demos:
  <br>Actuation - https://youtube.com/shorts/FE57_PTdPvw?si=3Otmu_hgnJ35llEw
  <br>Tracking - https://youtube.com/shorts/putWm9wyfx4?si=dXoKtPFu8kXs6i-v
</p>
