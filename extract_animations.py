import cv2
import mediapipe as mp
import json
import os

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

VIDEOS_DIR = "Videos_Sentence_Level/are you free today"
OUTPUT_DIR = "pose_data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_keypoints(video_path, output_json):
    cap = cv2.VideoCapture(video_path)
    holistic = mp_holistic.Holistic(static_image_mode=False)

    frames_data = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(rgb)

        frame_data = {
            "pose": [(lm.x, lm.y, lm.z) for lm in results.pose_landmarks.landmark] if results.pose_landmarks else [],
            "left_hand": [(lm.x, lm.y, lm.z) for lm in results.left_hand_landmarks.landmark] if results.left_hand_landmarks else [],
            "right_hand": [(lm.x, lm.y, lm.z) for lm in results.right_hand_landmarks.landmark] if results.right_hand_landmarks else []
        }
        frames_data.append(frame_data)

    with open(output_json, "w") as f:
        json.dump(frames_data, f)

    cap.release()
    holistic.close()

# Loop over all videos in the folder and extract JSONs
for root, dirs, files in os.walk(VIDEOS_DIR):
    for file in files:
        if file.lower().endswith(".mp4"):
            video_path = os.path.join(root, file)
            json_name = file.replace(".mp4", ".json").replace(" ", "_")
            output_path = os.path.join(OUTPUT_DIR, json_name)
            print(f"[INFO] Processing: {video_path} -> {output_path}")
            extract_keypoints(video_path, output_path)

print("[DONE] All videos processed into pose JSON files.")

# Example
#extract_keypoints("Videos_Sentence_Level/are you free today/are you free today.mp4",
#                "Videos_Sentence_Level/are you free today/free (2).mp4",
 #               "Videos_Sentence_Level/are you free today/free (3).mp4",
 #               "Videos_Sentence_Level/are you free today/free (4).mp4",
 #               "Videos_Sentence_Level/are you free today/free (5).mp4",
 #               "Videos_Sentence_Level/are you free today/free.mp4",
 #               "Videos_Sentence_Level/are you hiding something/are you hiding something (2).mp4",
 #               "Videos_Sentence_Level/are you hiding something/are you hiding something.mp4")
