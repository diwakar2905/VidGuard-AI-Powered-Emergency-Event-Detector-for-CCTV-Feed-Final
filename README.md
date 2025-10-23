# VidGuard: AI-Powered Emergency Event Detector for CCTV Feeds

![VidGuard Logo](https://raw.githubusercontent.com/your-username/VidGuard/main/VidGuard/Black%20and%20Blue%20Modern%20Cyber%20Tech%20Logo.png)

VidGuard is a powerful, AI-driven tool designed to automatically detect emergency events from CCTV footage. By leveraging computer vision techniques, VidGuard can identify critical situations such as fires, accidents, and other anomalies, enabling faster response times and improved security.

## Features

- **Emergency Event Detection:** VidGuard can detect a variety of emergency events, including:
  - `large_motion`: Significant movement that could indicate a fight, accident, or other disturbance.
  - `fire_detected`: The presence of fire or smoke in the video.
  - `no_motion_long`: A prolonged lack of movement, which might suggest a fall, collapse, or other medical emergency.
- **Real-time Analysis:** A dedicated endpoint allows for the real-time processing of individual video frames, making it suitable for live camera feeds.
- **RESTful API:** A clean and simple Flask-based API allows for easy integration with other systems and applications.
- **Scalable and Deployable:** The application is container-ready and can be easily deployed to cloud platforms like Render.

## Tech Stack

- **Backend:** Python, Flask
- **Computer Vision:** OpenCV
- **Deployment:** Gunicorn, Render

## Getting Started

### Prerequisites

- Python 3.7+
- pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/VidGuard.git
    cd VidGuard
    ```
2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Application Locally

To run the Flask application on your local machine, execute the following command:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`.

### API Endpoints

#### `POST /upload`

Upload a video file for analysis. The request should be a `multipart/form-data` request with the video file attached to the `video` field.

**Example using cURL:**

```bash
curl -X POST -F "video=@/path/to/your/video.mp4" http://127.0.0.1:5000/upload
```

#### `GET /get_events`

Retrieve the results of the last video analysis as a JSON object.

**Example using cURL:**

```bash
curl -X GET http://127.0.0.1:5000/get_events
```

#### `POST /process_frame`

Process a single video frame in real-time. The request should be a JSON object containing the base64-encoded image.

**Example using Python:**

```python
import requests
import base64

with open("path/to/your/image.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

response = requests.post("http://127.0.0.1:5000/process_frame", json={"image": encoded_string})
print(response.json())
```

## Deployment on Render

This application is ready to be deployed on Render. The `render.yaml` file in the repository is already configured for this.

1.  **Create a new Web Service on Render.**
2.  **Connect your Git repository.**
3.  **Render will automatically use the `render.yaml` file for configuration.**
    -   **Build Command:** `pip install -r requirements.txt`
    -   **Start Command:** `gunicorn app:app`
4.  **Deploy the service.**

## Project Structure

```
VidGuard/
├── app.py              # Main Flask application
├── detect_events.py    # Emergency event classifier
├── utils.py            # Helper functions for video analysis
├── videos/             # Directory for uploaded videos
├── outputs/            # Directory for analysis results
├── requirements.txt    # Project dependencies
├── render.yaml         # Render deployment configuration
├── static/               # Static files for the frontend
│   ├── styles.css
│   └── app.js
├── templates/          # HTML templates for the frontend
│   ├── index.html
│   └── about.html
└── README.md           # This file
```

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.