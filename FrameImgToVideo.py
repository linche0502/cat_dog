import numpy as np
import cv2, os, re



# 自動抓data/images/capture/ 裡的檔案
startImg = "00000.jpg"
endImg= "00070.jpg"
# 輸出檔案位置
# export= "data/video/cattOutput.mp4"
# 輸出資料夾(自動流水號命名)
# exportFile= "data/video/lie"
exportFile= "data/video/sit"
# exportFile= "data/video/stand"
imgWidth= 640
imgHeight= 360


base_path= os.path.abspath(os.path.dirname(__file__))
# 讀取圖片
imgNames= os.listdir(os.path.join(base_path, "data/images/capture"))
imgNames= imgNames[imgNames.index(startImg):imgNames.index(endImg)+1]


# 輸出影片
videoNames= (os.listdir(os.path.join(base_path, exportFile)) or [""])[-1].replace(".mp4",'') or 0
fourcc = cv2.VideoWriter_fourcc(*'XVID')
outputVideo = cv2.VideoWriter(f"{exportFile}/{int(videoNames)+1}", fourcc, 10.0, (imgWidth,imgHeight)) 


# 逐幀閱讀
for i,imgName in enumerate(imgNames):
    outputVideo.write(cv2.imread(os.path.join(base_path, "data/images/capture", imgName)))
    # 純粹為了好看用的進度條，這邊記得+1，以避免最後不確定會停在98%(總幀數少的話) or 99%
    persent= int((i+1)/len(imgNames)*100)
    print(f"[{'#'*persent}{' '*(100-persent)}]", end='\r')


# 轉換完成後，刪除原檔案
for imgName in imgNames:
    os.remove(os.path.join(base_path, "data/images/capture", imgName))
print("\nfin")





