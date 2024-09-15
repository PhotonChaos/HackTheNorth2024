from flask import Flask, Response, render_template, jsonify, request
import atest  # Import your processing script
import groqtester
import get_basic_data

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    # Return the streaming response for the video feed
    return Response(atest.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    atest.clear_output()
    # Display the intro page
    return render_template('index.html')

@app.route('/main')
def main():
    # Display the main page with the video stream
    return render_template('main.html')

@app.route('/results')
def results():
    # Return the latest results as JSON
    return jsonify(atest.latest_output)

@app.route('/manualcode', methods=['POST'])
def manualcode():
    # Return the latest results as JSON
    data = request.get_json()
    code = str(data.get('code'))
    return jsonify(get_basic_data.get_drug_info_by_code(code))


@app.route('/clear_results', methods=['POST'])
def clear_results():
    # Reset the latest_output to an empty state
    atest.latest_output = {}
    return jsonify({"status": "success", "message": "Results cleared"})

@app.route('/ask_question', methods=['POST'])
def ask_question():
    data = request.get_json()
    print(data)
    prompt = data.get('prompt')
    drug = str(data.get('drug'))

    # Call the groqs function and get the result
    if prompt and drug:
        try:
            # Call groqtester or whatever function you use to process the request
            answer = groqtester.groqs(prompt, drug)
            return answer
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid input"}), 400

if __name__ == "__main__":
    app.run(debug=True)
