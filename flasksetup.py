from flask import Flask, Response, render_template
import cv2
import atest

app = Flask(__name__)


@app.route('/video_feed')
def video_feed():
    # Return the streaming response for the video feed
    return Response(atest.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    # Display the homepage with the video stream
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
