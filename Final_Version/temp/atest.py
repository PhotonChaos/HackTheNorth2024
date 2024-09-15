import numpy as np
import cv2 as cv
from multiprocessing.pool import ThreadPool
from collections import deque
import requests
import get_basic_data
import dbr
from dbr import BarcodeReader, BarcodeReaderError

BarcodeReader.init_license("your_license_key_here")

reader = BarcodeReader()

threadn = 1
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
    barcode_found = False
    barcode_result = None

    try:
        while not barcode_found:
            ret, frame = cap.read()
            if not ret:
                break

            if len(barcodeTasks) < threadn:
                task = pool.apply_async(process_frame, (frame.copy(),))
                barcodeTasks.append(task)

            while len(barcodeTasks) > 0 and barcodeTasks[0].ready():
                results = barcodeTasks.popleft().get()
                if results is not None:
                    for result in results:
                        points = result.localization_result.localization_points
                        for i in range(4):
                            cv.line(frame, tuple(points[i]), tuple(points[(i + 1) % 4]), (0, 255, 0), 2)
                        cv.putText(frame, result.barcode_text, tuple(points[0]), 
                                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

                        barcode_text = result.barcode_text
                        part1, part2, part3 = barcode_text[:5], barcode_text[5:8], barcode_text[8:10]
                        code = f"{part1}-{part2}-{part3}"

                        output = get_basic_data.get_drug_info_by_code(code)
                        barcode_result = output
                        
                        barcode_found = True
                        break

            if barcode_found:
                break

            ret, buffer = cv.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    finally:
        cap.release()

    return barcode_result
