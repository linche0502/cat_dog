import numpy as np
import cv2, os, sqlite3, base64, time
from ultralytics import YOLO



# 注意: 影片畫質太高或時間太長，可能會直接導致記憶體爆炸 (1080p影片，一帧約8MB。以30fps來算，1秒約240MB)    (棄用)
path = "data/video/catt.mp4"
imgWidth= 640
imgHeight= 360


base_path= os.path.abspath(os.path.dirname(__file__))

# 開啟電腦鏡頭
# capture = cv2.VideoCapture(0)
# 從youtube下載(預定)
if path.startswith("http"):
    from pytube import YouTube
    youtube= YouTube(path)
    video= youtube.streams.filter().first()
    video.download(os.path.join(base_path,"data/video/temp.mp4"))
    capture = cv2.VideoCapture(os.path.join(base_path,"data/video/temp.mp4"))

# 載入現有影片
else:
    capture = cv2.VideoCapture(os.path.join(base_path, path))

model = YOLO(base_path+ '/yolo2/best2.pt')

# frames = []
ret = True
num= 0
while ret:
    # ret: 是否擷取成功，frame: 擷取下來的一幀影像
    ret, frame = capture.read() # read one frame from the 'capture' object; img is (H, W, C)
    frameHeight, frameWidth, _= frame.shape
    # verbose=False: terminal dont print
    results = model.predict(frame, verbose=False)
    
    if ret:
        for result in results:
            boxes =  result.boxes
            for box in boxes:
                # 框框的左.上.右.下 座標
                left, top, right, bottom= box.xyxy[0]
                left, top, right, bottom= int(left), int(top), int(right), int(bottom)
                # 如果擷取下來的長寬比大於需求，則增加擷取高度
                scale= imgWidth/imgHeight
                if abs(right-left)/abs(bottom-top) > scale:
                    diffHeight= abs(right-left)/scale- abs(bottom-top)
                    top, bottom= int(top-diffHeight/2), int(bottom+diffHeight/2)
                    # 超過畫面邊界時的校正
                    if top<0: top,bottom= 0, bottom-top
                    elif bottom>frameHeight: top,bottom= top-(bottom-frameHeight), frameHeight
                # 如果擷取下來的長寬比小於需求，則增加擷取寬度
                elif abs(right-left)/abs(bottom-top) < scale:
                    diffWidth= abs(bottom-top)*scale- abs(right-left)
                    left, right= int(left-diffWidth/2), int(right+diffWidth/2)
                    if left<0: left,right= 0, right-left
                    elif right>frameWidth: left,right= left-(right-frameWidth), frameWidth
                # 縮放擷取影片的大小，並儲存
                resizeCapture= cv2.resize(frame[top:bottom,left:right], (imgWidth, imgHeight), interpolation=cv2.INTER_NEAREST)
                cv2.imwrite(base_path+ f'/data/images/capture/{num :05d}.jpg', resizeCapture)
                # 自已畫框(測試用)
                # cv2.rectangle(frame, (left, top), (right,bottom), (0, 255, 0), 2)
                # cv2.putText(frame, model.names[int(box.cls)], (left,top), None, 0.75,(255,255,255),3)
                num+= 1
        
        # 開啟測試用視窗看結果
        cv2.imshow('YOLO v8 cat & dog', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# video = np.stack(frames, axis=0)