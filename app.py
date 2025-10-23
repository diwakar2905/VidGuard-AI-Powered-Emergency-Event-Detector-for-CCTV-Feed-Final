import streamlit as st
import os
import tempfile
import cv2
import numpy as np
import base64
from utils import analyze_video_opencv, analyze_single_frame
from detect_events import classify_emergency


def display_event_card(event):
    """Helper function to display a styled event card."""
    st.markdown(f"""
    <div class="event-card">
        <div class="event-label">🛑 {event['label'].replace('_', ' ').upper()}</div>
        <div class="event-time">⏰ {event['timestamp']}</div>
        <div class="event-confidence">Confidence: {event['confidence'] * 100:.0f}%</div>
    </div>
    """, unsafe_allow_html=True)


def about_page():
    """Renders the About page content."""
    st.markdown("""
        <div class="about-container">
            <h1>About VidGuard</h1>
            <p>VidGuard is an innovative AI-powered surveillance solution designed to automatically detect emergency events from CCTV video feeds. In a world where security is paramount, VidGuard provides an extra layer of vigilance, monitoring footage to identify potential threats such as fires, accidents, or suspicious inactivity.</p>
            <p>Our mission is to enhance safety and security by leveraging cutting-edge computer vision. By providing timely alerts, VidGuard aims to reduce response times for emergency services, potentially saving lives and mitigating damage.</p>

            <h3>Technology Stack</h3>
            <div class="tech-stack">
                <ul>
                    <li>Python & Streamlit</li>
                    <li>OpenCV</li>
                    <li>HTML5 & CSS3</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)


def main_dashboard():
    """Renders the main dashboard for video and webcam analysis."""
    st.title("🚨 VidGuard Emergency Event Detector")

    st.markdown("""
    Upload a video file or use your webcam to detect potential emergency events in real-time.
    VidGuard can identify: `Large Motion`, `Fire`, and `Prolonged Lack of Motion`.
    """)

    # --- Video Upload and Analysis ---
    st.header("Analyze a Video File")
    uploaded_file = st.file_uploader("Choose a video file...", type=["mp4", "avi", "mov"])

    if uploaded_file is not None:
        # To read the file with OpenCV, we need to save it to a temporary file first.
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tfile:
            tfile.write(uploaded_file.read())
            video_path = tfile.name

        st.video(video_path)

        if st.button("Analyze Video"):
            with st.spinner('Analyzing video... This may take a moment.'):
                analysis_result = analyze_video_opencv(video_path)
                events = analysis_result.get("events", [])
                emergency_events = classify_emergency(events)

            st.subheader("Analysis Results")
            if not emergency_events:
                st.success("✅ No emergency events detected.")
            else:
                st.warning(f"🚨 Found {len(emergency_events)} potential emergency event(s).")
                for event in emergency_events:
                    display_event_card(event)

        # Clean up the temporary file
        os.unlink(video_path)

    # --- Webcam Analysis ---
    st.header("Live Webcam Analysis")
    img_file_buffer = st.camera_input("Use your webcam to detect fire in real-time")

    if img_file_buffer is not None:
        # To get the image data, we read the buffer
        bytes_data = img_file_buffer.getvalue()
        # Convert bytes to a numpy array for OpenCV
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        # Analyze the single frame
        with st.spinner("Analyzing frame..."):
            events = analyze_single_frame(cv2_img)
            emergency_events = classify_emergency(events)

        if not emergency_events:
            st.info("No fire detected in the current frame.")
        else:
            st.subheader("Live Event Detected!")
            for event in emergency_events:
                display_event_card(event)


def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="VidGuard", page_icon="🚨", layout="wide")

    # Inject custom CSS for styling
    # Ensure you have these files in the correct path relative to this script
    # For example: static/styles.css
    if os.path.exists("static/styles.css"):
        with open("static/styles.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "About"])

    if page == "Dashboard":
        main_dashboard()
    elif page == "About":
        about_page()

    st.sidebar.info("© 2025 VidGuard AI. All rights reserved.")


if __name__ == '__main__':
    main()
