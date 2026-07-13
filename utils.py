import time, math
import cv2
# pyrefly: ignore [missing-import]
import numpy as np


# init " pTime = time.time() " before the While loop
def get_fps(cap, pTime,type='default'):
    if type == "default":
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        return fps, pTime

    elif type =="cap":
        fps= cap.get(cv2.CAP_PROP_FPS)
        if fps<= 0:
            return 30, pTime
        return fps, pTime
    else:
        return 30, pTime


def get_dist(point1,point2):
    return math.hypot(point1[1]-point2[1],point1[2]-point2[2])

# a and b form the angle
def get_angle(a,b,c):
    return math.degrees(math.acos((a**2 + b**2 - c**2) / ( 2 * a * b) ))




######################
#----------- Custom-render a highly aesthetic visual HUD ourselves
######################
def draw_biomechanics(img, pose_data, angle, min_angle=10, max_angle=175):
    """
    Draws custom glowing joints, connection lines, and a floating angle badge.
    """
    # 1. Extract clean coordinates
    x11, y11 = pose_data[11][1], pose_data[11][2]  # Shoulder
    x13, y13 = pose_data[13][1], pose_data[13][2]  # Elbow
    x15, y15 = pose_data[15][1], pose_data[15][2]  # Wrist

    # 2. Draw clean glowing arm lines (Pink/Red theme: BGR (93, 81, 183))
    cv2.line(img, (x11, y11), (x13, y13), (50, 50, 50), 8)
    cv2.line(img, (x13, y13), (x15, y15), (50, 50, 50), 8)
    cv2.line(img, (x11, y11), (x13, y13), (93, 81, 183), 4)
    cv2.line(img, (x13, y13), (x15, y15), (93, 81, 183), 4)

    # 3. Glowing joint circles
    for (x, y) in [(x11, y11), (x13, y13), (x15, y15)]:
        cv2.circle(img, (x, y), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (x, y), 14, (93, 81, 183), 2)

    # 4. Floating Angle Badge next to the elbow
    badge_w, badge_h = 100, 45
    bx, by = x13 + 25, y13 - 22
    
    # Dark semi-transparent overlay
    badge_overlay = img.copy()
    cv2.rectangle(badge_overlay, (bx, by), (bx + badge_w, by + badge_h), (30, 30, 30), cv2.FILLED)
    cv2.addWeighted(badge_overlay, 0.6, img, 0.4, 0, img)
    cv2.rectangle(img, (bx, by), (bx + badge_w, by + badge_h), (255, 255, 255), 1, cv2.LINE_AA)
    
    # Text inside badge
    cv2.putText(img, f"{int(angle)}deg", (bx + 12, by + 30), cv2.FONT_HERSHEY_SIMPLEX, 
                0.6, (255, 255, 255), 1, cv2.LINE_AA)


def draw_rom_bar(img, angle, min_angle=10, max_angle=175):
    """
    Draws a vertical Range of Motion (ROM) progress bar on the side of the screen.
    """
    # Map the angle (e.g. 35 to 160) to a scale of 100% to 0%
    rom_percentage = np.interp(angle, (min_angle, max_angle), (100, 0))
    rom_percentage = max(0, min(100, rom_percentage))  # Keep bounded

    bar_y_start = 150
    bar_y_end = 450
    bar_height = bar_y_end - bar_y_start

    # Draw Background Track
    cv2.rectangle(img, (50, bar_y_start), (80, bar_y_end), (40, 40, 40), cv2.FILLED)
    cv2.rectangle(img, (50, bar_y_start), (80, bar_y_end), (200, 200, 200), 2)

    # Calculate and draw dynamic filled bar
    fill_level = int(bar_y_end - (rom_percentage / 100 * bar_height))
    bar_color = (93, 81, 183) if rom_percentage < 80 else (100, 220, 100) # Green when contracted
    
    if fill_level < bar_y_end:
        cv2.rectangle(img, (52, fill_level), (78, bar_y_end - 2), bar_color, cv2.FILLED)

    # ROM Percentage text
    cv2.putText(img, f"{int(rom_percentage)}%", (40, bar_y_start - 15), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)


def draw_fps_capsule(img, fps):
    """
    Draws a clean modern capsule for the frame-rate in the top-left corner.
    """
    fps_overlay = img.copy()
    cv2.rectangle(fps_overlay, (15, 15), (115, 55), (0, 0, 0), cv2.FILLED)
    cv2.addWeighted(fps_overlay, 0.5, img, 0.5, 0, img)
    cv2.putText(img, f"FPS: {int(fps)}", (28, 42), cv2.FONT_HERSHEY_SIMPLEX, 
                0.55, (0, 255, 255), 1, cv2.LINE_AA)