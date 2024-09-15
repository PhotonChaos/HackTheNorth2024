from flask import Flask, Response, render_template, jsonify
import atest  # Import your processing script

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    # Return the streaming response for the video feed
    return Response(atest.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    atest.clear_output()
    # Display the homepage with the video stream
    return render_template('index.html')

@app.route('/results')
def results():
    # Return the latest results as JSON
    return jsonify(atest.latest_output)

if __name__ == "__main__":
    app.run(debug=True)
