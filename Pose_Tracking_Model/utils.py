# pyrefly: ignore [missing-import]
import cv2
# pyrefly: ignore [missing-import]
import mediapipe as mp
# pyrefly: ignore [missing-import]
from mediapipe.tasks.python.vision import drawing_utils

# custom styles
custom_dots = drawing_utils.DrawingSpec(color=(255, 0, 0),
                                        thickness=5, 
                                        circle_radius=4
                                        )

custom_lines = drawing_utils.DrawingSpec(color=(0, 255, 0), 
                                        thickness=5
                                        )

class PoseDetector():
    def __init__(self,
                model_path = "pose_landmarker_full.task",
                num_poses = 1,
                confidence = 0.5):
        
        # Arguments
        self.model_path = model_path
        self.num_poses = num_poses
        self.confidence = confidence

        # APIs
        self.Baseoptions = mp.tasks.BaseOptions
        self.poseLandmarker = mp.tasks.vision.PoseLandmarker
        self.poseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
        self.VisionRunningMode = mp.tasks.vision.RunningMode

        #  Options configuration
        self.Options = self.poseLandmarkerOptions(
            base_options = self.Baseoptions(model_asset_path=self.model_path),
            num_poses = num_poses,
            running_mode = self.VisionRunningMode.VIDEO,
            min_pose_detection_confidence = self.confidence,
            min_pose_presence_confidence = self.confidence,
            min_tracking_confidence = self.confidence
        )

        # Build
        self.landmarker = self.poseLandmarker.create_from_options(self.Options)

    def findPose(self,img,res, draw = True, id = -1):

        h, w, c = img.shape
        AllPoses = []

        if res.pose_landmarks :
            for pose in res.pose_landmarks:

                if draw:
                    drawing_utils.draw_landmarks(
                        img,
                        pose,
                        mp.tasks.vision.PoseLandmarksConnections.POSE_LANDMARKS,
                        landmark_drawing_spec=custom_dots,
                        connection_drawing_spec=custom_lines,
                    )

                lmList = []
                for id,lm in enumerate(pose):
                    cx , cy = int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy])
                
                AllPoses.append(lmList)

        if id != -1 :

            coor = []
            for id , pose in enumerate(AllPoses):
                if len(AllPoses) != 0:
                    cx , cy = pose[id][1] , pose[id][2]
                    coor.append([id+1,cx,cy])

            return coor

        return AllPoses 
