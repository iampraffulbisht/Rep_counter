
<img width="1680" alt="Screenshot 2024-06-30 at 12 34 05 AM-min" src="https://github.com/iampraffulbisht/Rep_counter/assets/114369813/b78cd565-0477-4491-ae62-7a790a689d27">
<img width="1280" alt="Screenshot 2024-06-30 at 12 31 57 AM-min" src="https://github.com/iampraffulbisht/Rep_counter/assets/114369813/00faf5fb-1db3-494f-aaaf-1fddece0909d">

# AI Gym Trainer: Posture Detection

This project uses computer vision to detect and analyze body posture during workouts. It leverages OpenCV for video capture, MediaPipe for pose detection, and a custom posture detection module to track workout progress.

## Prerequisites

Ensure you have Python 3.6 or higher installed on your system.

## Setup

1. **Clone the Repository**

    ```bash
    git clone https://github.com/your-username/ai-gym-trainer.git](https://github.com/iampraffulbisht/Rep_counter
    cd ai-gym-trainer
    ```

2. **Create a Virtual Environment**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the Dependencies**

    ```bash
    pip install opencv-python
    pip install mediapipe
    pip install numpy
    ```

4. **Download the `posture_detection_module.py`**

    Ensure you have the `posture_detection_module.py` file in your project directory. This module should contain the pose detection logic using MediaPipe.

## Running the Code

Run the script to start the webcam and begin posture detection.

```bash
python main.py
```

License

This project is licensed under the MIT License.

Acknowledgements

OpenCV
MediaPipe
