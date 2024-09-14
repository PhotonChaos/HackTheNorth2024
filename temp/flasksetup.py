from flask import Flask, Response, render_template, jsonify
import atest

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    return Response(atest.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/barcode_result')
def barcode_result():
    result = atest.generate_frames()  # Call to get the barcode result
    if result:
        return jsonify(result)  # Return JSON directly
    else:
        return jsonify({'error': 'No barcode detected'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show_barcode_result')
def show_barcode_result():
    return render_template('show_barcode_result.html')

if __name__ == "__main__":
    app.run(debug=True)
