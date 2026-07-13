# pyrefly: ignore [missing-import]
import cv2
# pyrefly: ignore [missing-import]
import mediapipe as mp
import time
from Pose_Tracking_Model.utils import PoseDetector
from utils import get_fps , get_dist , get_angle
from utils import draw_fps_capsule, draw_biomechanics , draw_rom_bar


def main():
    cap = cv2.VideoCapture("video.mp4")

    pTime = time.time()
    frame_count = 0

    detector = PoseDetector(model_path = "Pose_Tracking_Model/pose_landmarker_full.task",
                            num_poses = 1)
    
    angleList= []

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

        pose_data = detector.findPose(img, res, draw=False)

        if len(pose_data) != 0:
            pose_data = pose_data[0]

            a = get_dist(pose_data[11],pose_data[13])
            b = get_dist(pose_data[13],pose_data[15])
            c = get_dist(pose_data[11],pose_data[15])

            angle = get_angle(a,b,c)

            angleList.append(angle)

            draw_biomechanics(img, pose_data, angle)
            draw_rom_bar(img, angle)
            
            """
            cv2.putText(img,str(int(angle)),
                        (pose_data[13][1]+10,pose_data[13][2]),
                        cv2.FONT_HERSHEY_COMPLEX, 
                        2, (183,81,93) , 1)
            """

        # display
        draw_fps_capsule(img, fps)

        """
        cv2.putText(img,str(int(fps)),
                (10,100),
                cv2.FONT_HERSHEY_PLAIN,
                7,(255,0,255),5)
        """
        cv2.imshow('Video',img)
        if cv2.waitKey(1) & 0xFF==ord(' '):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(max(angleList),min(angleList))

if __name__ == "__main__":
    main()