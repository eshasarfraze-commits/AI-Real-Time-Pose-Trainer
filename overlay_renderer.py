import cv2
import mediapipe as mp

mp_draw = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
COLORS  = {"correct": (0, 220, 100), "low": (0, 120, 255), "high": (0, 60, 220)}

def draw_skeleton(frame, landmarks):
    mp_draw.draw_landmarks(
        frame, landmarks, mp_pose.POSE_CONNECTIONS,
        mp_draw.DrawingSpec(color=(200, 200, 200), thickness=2, circle_radius=3),
        mp_draw.DrawingSpec(color=(150, 150, 150), thickness=2)
    )

def draw_hud(frame, exercise_name, score, rep_count, joint_results, feedback_text):
    h, w = frame.shape[:2]
    overlay = frame.copy()

    # Top bar
    cv2.rectangle(overlay, (0, 0), (w, 60), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    cv2.putText(frame, exercise_name, (16, 38),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
    cv2.putText(frame, f"Reps: {rep_count}", (w - 180, 38),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # Score circle
    score_color = (0, 220, 100) if score >= 80 else (0, 180, 255) if score >= 50 else (0, 80, 220)
    cv2.circle(frame, (w - 60, h - 60), 40, score_color, -1)
    cv2.putText(frame, str(score),
                (w - 76 if score < 100 else w - 82, h - 52),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # Joint status bars
    for i, j in enumerate(joint_results):
        color = COLORS.get(j["status"], (200, 200, 200))
        label = f"{j['id']}: {j['angle']}°"
        cv2.rectangle(frame, (10, 70 + i * 34), (280, 100 + i * 34), (30, 30, 30), -1)
        cv2.rectangle(frame, (10, 70 + i * 34), (280, 100 + i * 34), color, 2)
        cv2.putText(frame, label, (18, 92 + i * 34),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)

    # Feedback banner
    if feedback_text:
        cv2.rectangle(frame, (0, h - 50), (w, h), (20, 20, 20), -1)
        cv2.putText(frame, feedback_text, (16, h - 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 220, 255), 2)

    # Controls hint
    cv2.putText(frame, "N: next exercise   P: prev exercise   Q: quit",
                (16, h - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)