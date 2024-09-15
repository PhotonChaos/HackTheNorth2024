import numpy as np
import cv2 as cv
import requests
import get_basic_data
import dbr
from dbr import *

BarcodeReader.init_license("t0068lQAAAJopJWTIJCSnLJxPUw1qhfe8F6DOWpvBxLKy2t+2h/nwWe9JhrF+eP33yU636fc6XERFjAnEwO0eUM/FruY6epk=;t0068lQAAAFaeIqz9aOqDpGSdfFGzoiO0veC6tpY7R9MmxIBjA4ZwaMibd3+LfKg0ICDhpwIq8c0sCxBvCdF9AzPDssMg4Js=")

reader = BarcodeReader()

# Global variable to store the latest output
latest_output = {}

def process_frame(frame):
    global latest_output
    results = None
    try:
        results = reader.decode_buffer(frame)
        if results is not None:
            for result in results:
                points = result.localization_result.localization_points
                # Draw lines around the barcode
                for i in range(4):
                    cv.line(frame, tuple(points[i]), tuple(points[(i + 1) % 4]), (0, 255, 0), 2)
                cv.putText(frame, result.barcode_text, tuple(points[0]), 
                           cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

                # Extract and format the barcode text
                barcode_text = result.barcode_text
                part1, part2, part3 = barcode_text[:5], barcode_text[5:8], barcode_text[8:10]
                code = f"{part1}-{part2}-{part3}"

                # Call external API to get drug info
                latest_output = get_basic_data.get_drug_info_by_code(code)
                print(f"{latest_output}", flush=True)

    except BarcodeReaderError as bre:
        print(f"BarcodeReaderError: {bre}")
    return frame

def generate_frames():
    cap = cv.VideoCapture(0)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break  # Exit if the camera feed cannot be read

            # Process the frame for barcode scanning
            frame = process_frame(frame)

            # Encode frame to JPEG
            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame to be sent to the browser
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    finally:
        # Release the camera resource when done
        cap.release()

def clear_output():
    global latest_output
    latest_output = None
