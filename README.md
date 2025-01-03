# Identity Recognition Defense System (IRDS)
A projectile/laser turret guided by facial recognition. The facial recognition is programmed in Python, which sends unrecognized face coordinates from an external webcam to an Arduino IDE where they are converted to corresponding angles and updated constantly for two servo motors on a custom PCB using an ESP32-DevKitC. The projectile gearbox is actuated by a N-Channel MOSFET (RFP30N06LE) and controlled by the Arduino IDE. The servo structures, gearbox attachments, and electronics housing are designed in CAD and 3D printed. The objective of this project was to develop experience in designing and programming embedded systems, utilizing serial connections to transmit information across different platforms for execution, and integrating electronic components and hardware into a custom circuit.
<p align = "center">
  <img src="https://github.com/user-attachments/assets/4c4b9978-79f9-4a76-b641-4c870453d31d" width=50% height=50%>
</p>

<p align = "center">
  Demos:
  <br>Actuation - https://youtube.com/shorts/FE57_PTdPvw?si=3Otmu_hgnJ35llEw
  <br>Tracking - https://youtube.com/shorts/putWm9wyfx4?si=dXoKtPFu8kXs6i-v
</p>
