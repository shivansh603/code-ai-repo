import uuid 
import cv2 
import numpy as np 
import threading 
from concurrent.futures import ThreadPoolExecutor
import time 
from ultralytics import YOLO 
import firebase_admin
from firebase_admin import credentials, db
from concurrent.futures import ThreadPoolExecutor
import requests 
import os 
from Config import CLOUD_URL
executor = ThreadPoolExecutor(max_workers=2)

model = YOLO('latest_barcode.pt')

firebase_path="onm_main_key_firebase.json"
databaseURL= "https://owens-and-minor-inventory-default-rtdb.asia-southeast1.firebasedatabase.app"

creds = credentials.Certificate(firebase_path)
firebase_admin.initialize_app(creds, {
    'databaseURL': databaseURL
})


BARCODE = False
BLUR = False

# Function for YOLO inference
def yolo_inference(frame):
    global BARCODE
    s = time.time()
    results = model(frame)
    e = time.time()
    print(f'{e - s} seconds for YOLO inference')
    try:
        for result in results:
            names = result.names
            bbox = result.boxes.xyxy.tolist()
            conf = result.boxes.conf.tolist()
            label = result.boxes.cls.tolist()

        temp_image = frame.copy()
        for idx, lbl in enumerate(label):
            if names[lbl] == 'barcode' and conf[idx] > 0.8 :
                for box in bbox:
                    xmin, ymin, xmax, ymax = int(box[0]), int(box[1]), int(box[2]), int(box[3])
                    temp_image = cv2.rectangle(temp_image, (xmin, ymin), (xmax, ymax), (0,255,0), 3)
                BARCODE = True
                cv2.imwrite('annotated_img.jpg', temp_image)
                return True 
        BARCODE = False
    except Exception as e:
        print(f'{e} at line 26')
        BARCODE = False
    # return {'bbox': bbox, 'conf': conf, 'label': label}

# Function to detect blur using Laplacian variance
def detect_blur_lap(img_arr, threshold=500):
    global BLUR
    s = time.time()
    gray_frame = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray_frame, cv2.CV_64F).var()
    e = time.time()
    print(f'{e - s} for blur inference')
    print(f'####### VARIANCE : {variance} #######')
    BLUR = variance > threshold

def firebase_update(data, reference):
        # print('FIREBASE CALLED')
        # print(data, reference)
        if reference is not None:
                ref = db.reference(f'/ProductOnboarding/{reference}')
                ref.set(data)
        else:
            ref = db.reference(f'/ProductOnboarding')
            db_data = ref.get()
            # print(db_data)
            db_data['Voice_keyword'] = data 
            ref.update(db_data)

def firebase_cleanup():
    root_reference = '/ProductOnboarding'
    all_references = ['/get_data', '/object_annotations', '/status', '/left_orientation', '/right_orientation']
    for ref in all_references:
        ref = db.reference(root_reference + ref)
        dummy_data = {"client_id": "null"}
        ref.set(dummy_data)
    return True


class VideoStream(threading.Thread):
    def __init__(self, cam_id, w, h, fps):
        self.cap = cv2.VideoCapture(cam_id)
        self.w = w 
        self.h = h 
        self.cloud_ip = f'{CLOUD_URL}/ai/inference'
        self.fps = fps 
        self.codec = cv2.VideoWriter_fourcc(*'MJPG')
        self.old_fourcc = self.decode_fourcc(self.cap.get(cv2.CAP_PROP_FOURCC))
        self.res = self.cap.set(cv2.CAP_PROP_FOURCC, self.codec)
        self.thread = None
        self.resized_frame = None
        self.count = 0 
        self.check = 0
        self.client_id = None 
        self.frame = None 
        self.yolo_flag = False
        self.configure_camera()
    
    def decode_fourcc(self, v):
        v = int(v)
        return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])
    
    def configure_camera(self):
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.w)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.h)
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        ret, frame = self.cap.read()
        print(f' CAMERA CONFIGURED: {frame.shape}')
    def write_frame(self, frame):
        file_path = f'image_{int(time.time_ns())}.jpg'
        cv2.imwrite(file_path, frame)
        return file_path

    def cloud_backend(self, frame):
        file_path = self.write_frame(frame)
        try:
            url = f"{self.cloud_ip}?client_id={self.client_id}"
            print("url: ", url)
            # print(f'TRACK: {self.best_frame_score}')
            files = [('image', (file_path, open(file_path, 'rb'), 'image/png'))]
            headers = {}
            response = requests.request("POST", url, headers=headers, files=files, timeout=3)
            print(response.text)
        except Exception as e:
            print(f'error while posting frame to cloud : {str(e)}')
        finally:
            os.remove(file_path)
            pass

    def capture_frame(self, client_id):
        # ret, frame = self.cap.read()
        if client_id == '':
            client_id = 'temp_id' 
        if os.path.exists(client_id) is not True: 
            os.mkdir(client_id)
        # frame = cv2.resize(frame, (640, 480), cv2.INTER_LINEAR)   
        image_path = f'{client_id}/{uuid.uuid1()}_{client_id}.jpg'
        cv2.imwrite(image_path, self.resized_frame)
        print(f'Image Captured: @ path: {image_path}')
        return image_path 
        
    def get_frame(self, client_id):

        global BLUR, BARCODE
        self.client_id = client_id
        ret, frame = self.cap.read()
        # print(frame.shape)
        if ret is False:
            raise Exception('Error at line 25. {ret} is false')
        
        self.resized_frame = cv2.resize(frame, (1088, 832), interpolation=cv2.INTER_LINEAR)

        if self.yolo_flag is False:
            return frame
        
        


        if self.count % self.fps == 0:

            executor.submit(yolo_inference, self.resized_frame)
        detect_blur_lap(self.resized_frame)

        
       
            
      
        print(f'BARCODE Status : {BARCODE} & BLUR status : {BLUR}')


        print(f'Threading Active Count : {threading.active_count()}')

        if not BARCODE and not BLUR:
            # print("FIREBASE UPDATE CALLED")
            frame_status = {
                'client_id': client_id,
                'frame_status': False,
                'ui_message': 'Place Object in ROI'
            }
            executor.submit(firebase_update,frame_status, 'status')

        elif BARCODE and not BLUR:
            frame_status = {
                'client_id': client_id,
                'frame_status': False,
                'ui_message': "Barcode is Visible"
            }
            executor.submit(firebase_update,frame_status, 'status')

        elif BLUR and not BARCODE:
            frame_status = {
                'client_id': client_id,
                'frame_status': False,
                'ui_message': 'Frame is Clear'
            }
            executor.submit(firebase_update,frame_status, 'status')

        elif BARCODE and BLUR:
            self.check+=1 
            if self.check>=7:
                frame_status = {
                    'client_id': client_id,
                    'frame_status': True,
                    'ui_message': 'Processing Frame'
                }
                executor.submit(firebase_update,frame_status, 'status')
                self.check = 0
                BARCODE = False 
                BLUR = False
                cv2.imwrite('best_frame.jpg', frame)
                self.cloud_backend(frame)
                self.yolo_flag = False 
                # url = f"http://localhost:8000/flag/stream/false"
                # response = requests.request("GET", url, timeout=3)
                # print(response.text)
                # print('########## STREAM STOPPED #########')
                
        
        
        self.count += 1
        self.frame = frame 
        return frame
        
        

firebase_cleanup()