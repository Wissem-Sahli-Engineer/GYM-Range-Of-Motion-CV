# pyrefly: ignore [missing-import]
import cv2
# pyrefly: ignore [missing-import]
import mediapipe as mp
import time
from Pose_Tracking_Model.utils import PoseDetector
from utils import get_fps



def main():
    cap = cv2.VideoCapture(0)

    pTime = time.time()
    frame_count = 0

    detector = PoseDetector(model_path = "Pose_Tracking_Model/pose_landmarker_full.task",
                            num_poses = 3)

    while True:

        test , img = cap.read()
        if not test or img is None :
            break

        # preprocessing

        fps , pTime = get_fps(cap,pTime)

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)


        timestamp_ms = int((frame_count / get_fps(cap,0,type='cap')[0]) * 1000)
        frame_count += 1

        res = detector.landmarker.detect_for_video(mp_img, timestamp_ms)

        pose_data = detector.findPose(img, res,id = 14)

        print(pose_data)


        # display
        cv2.putText(img,str(int(fps)),
                (10,100),
                cv2.FONT_HERSHEY_PLAIN,
                7,(255,0,255),5)

        cv2.imshow('Video',img)
        if cv2.waitKey(1) & 0xFF==ord(' '):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()