import numpy as np
import cv2 as cv
from multiprocessing.pool import ThreadPool
from collections import deque
import requests
import get_basic_data

import dbr
from dbr import *
BarcodeReader.init_license("t0068lQAAAJopJWTIJCSnLJxPUw1qhfe8F6DOWpvBxLKy2t+2h/nwWe9JhrF+eP33yU636fc6XERFjAnEwO0eUM/FruY6epk=;t0068lQAAAFaeIqz9aOqDpGSdfFGzoiO0veC6tpY7R9MmxIBjA4ZwaMibd3+LfKg0ICDhpwIq8c0sCxBvCdF9AzPDssMg4Js=")

reader = BarcodeReader()

# Adjust thread number based on system CPUs or needs
threadn = 1  # Increase if necessary for better performance
pool = ThreadPool(processes=threadn)
barcodeTasks = deque()

def process_frame(frame):
    results = None
    try:
        results = reader.decode_buffer(frame)
    except BarcodeReaderError as bre:
        print(f"BarcodeReaderError: {bre}")
    return results

def generate_frames():
    cap = cv.VideoCapture(0)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break  # Exit if the camera feed cannot be read

            # Handle barcode scanning
            while len(barcodeTasks) > 0 and barcodeTasks[0].ready():
                results = barcodeTasks.popleft().get()
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
                        output = get_basic_data.get_drug_info_by_code(code)
                        url = f'https://api.fda.gov/drug/label.json?search=openfda.package_ndc="{code}"'

                        #try:
                         #   resp = requests.get(url)
                          #  if resp.status_code == 200:
                           #     data = resp.json()
                                # Add additional processing of data if needed
                        print(f"Medicine: {output['name']}, Manufacturer: {output['manufacturer_name']}", flush=True)
#                            else:
 #                               print(f"Error: API call failed with status {resp.status_code}")
  #                      except requests.exceptions.RequestException as e:
   #                         print(f"Request error: {e}")
            
            # Add new tasks to process frames
            if len(barcodeTasks) < threadn:
                task = pool.apply_async(process_frame, (frame.copy(),))
                barcodeTasks.append(task)

            # Encode frame to JPEG
            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame to be sent to the browser
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    finally:
        # Release the camera resource when done
        cap.release()
