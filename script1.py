import cv2,time,pandas
from datetime import datetime

first_frame=None
status_list=[0,0]
times=[]
df=pandas.DataFrame(columns=["START","END"])

video=cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    status=0

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)           # get blurred image, helps with motion detection

# to get the first frame of the video and we go back to second iteration
    if first_frame is None:
        first_frame=gray
        continue

    '''this section is responsible for blurring and creating threshold'''
    delta_frame=cv2.absdiff(first_frame,gray)   # get the diff between first frame and current frame
    thresh_frame=cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]   # to classify whtie and black colors to detect motion better
    #thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)

    #below --- find all the conturs of all distinct objects in the image and store in cnts variable.
    # syntax of variable is for python3

    (_,cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status=1
        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h),(0,255,0),3)
    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    cv2.imshow("delta_frame",delta_frame)
    cv2.imshow("gray_image",gray)
    cv2.imshow("Threshold",thresh_frame)
    cv2.imshow("frame",frame)
    key=cv2.waitKey(100)

    if key == ord('q'):
        if status==1:
            times.append(datetime.now())
        break

print(status_list)
print(times)

for i in range(0,len(times),2):
    df=df.append({"START":times[i],"END":times[i+1]},ignore_index=True)

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows()