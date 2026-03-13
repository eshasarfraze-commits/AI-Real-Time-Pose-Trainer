import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose

def get_landmark_coords(landmarks, name):
    lm = landmarks[mp_pose.PoseLandmark[name].value]
    return [lm.x, lm.y]

def calc_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))

def analyze_pose(landmarks, exercise_config):
    results = []
    for joint in exercise_config["joints"]:
        a = get_landmark_coords(landmarks, joint["landmarks"][0])
        b = get_landmark_coords(landmarks, joint["landmarks"][1])
        c = get_landmark_coords(landmarks, joint["landmarks"][2])
        angle = calc_angle(a, b, c)
        ideal = joint["ideal_angle"]
        tol   = joint["tolerance"]
        diff  = angle - ideal

        if abs(diff) <= tol:
            status   = "correct"
            feedback = None
        elif diff < 0:
            status   = "low"
            feedback = joint["feedback_low"]
        else:
            status   = "high"
            feedback = joint["feedback_high"]

        results.append({
            "id":       joint["id"],
            "angle":    round(angle, 1),
            "ideal":    ideal,
            "status":   status,
            "feedback": feedback
        })
    return results

def compute_score(joint_results):
    if not joint_results:
        return 0
    correct = sum(1 for j in joint_results if j["status"] == "correct")
    return int((correct / len(joint_results)) * 100)