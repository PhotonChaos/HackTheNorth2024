from flask import Flask, Response, render_template, jsonify, request
import atest  # Import your processing script
import groqtester
import get_basic_data
import json

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


def summarize_text(text, max_length=300):
    """Summarize the text to a specified length."""
    if len(text) > max_length:
        return text[:max_length] + '...'
    return text

def format_and_summarize_medication_info(data, max_length=300):
    results = []
    
    for result in data.get('results', []):
        # Extract and summarize information
        indications = summarize_text("\n".join(result.get('indications_and_usage', ['No data available'])), max_length)
        warnings = summarize_text("\n".join(result.get('warnings', ['No data available'])), max_length)
        side_effects = summarize_text("\n".join(result.get('adverse_reactions', ['No data available'])), max_length)
        
        # Format each section
        formatted_indications = "Indications and Usage:\n" + indications
        formatted_warnings = "Warnings:\n" + warnings
        formatted_side_effects = "Side Effects:\n" + side_effects
        
        # Combine all sections into a single string
        combined_info = f"{formatted_indications}\n\n{formatted_warnings}\n\n{formatted_side_effects}"
        results.append(combined_info)
    
    # Join all results into a single string with a delimiter if needed
    final_output = "\n\n---\n\n".join(results)
    
    return final_output


@app.route('/ask_question', methods=['POST'])
def ask_question():
    data = request.get_json()
    print(data)
    prompt = data.get('prompt')
    code = str(data.get('code'))

    # Call the groqs function and get the result
    if prompt and code:
        try:
            # Get the medication full data using it's code
            data = get_basic_data.get_drug_full_info_by_code(code)
            
            """results = []
    
            for result in data.get('results', []):
                # Extract relevant information
                indications = "\n".join(result.get('indications_and_usage', ['No data available']))
                warnings = "\n".join(result.get('warnings', ['No data available']))
                side_effects = "\n".join(result.get('adverse_reactions', ['No data available']))
                
                # Format each section
                formatted_indications = "Indications and Usage:\n" + indications
                formatted_warnings = "Warnings:\n" + warnings
                formatted_side_effects = "Side Effects:\n" + side_effects
                
                # Combine all sections into a single string
                combined_info = f"{formatted_indications}\n\n{formatted_warnings}\n\n{formatted_side_effects}"
                results.append(combined_info)
            
            # Join all results into a single string with a delimiter if needed
            full_info = "\n\n---\n\n".join(results)
            print(full_info)"""

            full_info = format_and_summarize_medication_info(data)
            print(full_info)

            # Call groqtester or whatever function you use to process the request
            answer = groqtester.groqs(prompt, full_info)
            print(answer)
            return answer
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid input"}), 400

if __name__ == "__main__":
    app.run(debug=True)
