# Gesture-Controlled-Virtual-Steering-Wheel
An interactive Computer Vision project built with Python, OpenCV, and MediaPipe that transforms hand movements into a virtual steering wheel interface. By tracking two-hand gestures in real time, the system translates relative hand tilt into directional commands (Move Forward, Move Left, Move Right, and Stop) designed to control an external robot or vehicle via Serial (Arduino).
Features
Real-Time Hand Tracking: Detects up to two hands using MediaPipe's high-confidence landmark model.

Dynamic Palm Centering: Calculates hand centers based on palm keypoints (wrist and finger bases) rather than finger tips for stable tracking.

Virtual Steering Wheel Visualization: Draws a line connecting hand centers and renders a surrounding wheel with an interactive midpoint dot.

Intelligent Control Logic:

2 Hands Detected: Calculates wheel tilt angle.

Left hand elevated: Steers Right (R)

Right hand elevated: Steers Left (L)

Hands level: Drives Forward (F)

< 2 Hands Detected: Safely triggers a Stop state (S).

Microcontroller Ready: Includes commented PySerial logic ready to transmit bytes directly to an Arduino (COM8, 9600 baud).

🛠 Tech Stack
Language: Python 3.x

Computer Vision: OpenCV (cv2)

ML Infrastructure: MediaPipe Hands

Hardware Integration: PySerial (for microcontroller integration)
