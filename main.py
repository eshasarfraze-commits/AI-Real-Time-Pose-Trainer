import cv2
import mediapipe as mp
from pose_analyzer    import analyze_pose, compute_score
from exercise_manager import ExerciseManager
from feedback_engine  import FeedbackEngine
from overlay_renderer import draw_skeleton, draw_hud

mp_pose = mp.solutions.pose

def main():
    manager  = ExerciseManager()
    feedback = FeedbackEngine(cooldown=3.0)
    cap      = cv2.VideoCapture(0)

    with mp_pose.Pose(min_detection_confidence=0.6,
                      min_tracking_confidence=0.6) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame  = cv2.flip(frame, 1)
            rgb    = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = pose.process(rgb)

            joint_results = []
            score         = 0
            feedback_text = None

            if result.pose_landmarks:
                draw_skeleton(frame, result.pose_landmarks)
                joint_results = analyze_pose(result.pose_landmarks.landmark,
                                             manager.current)
                score         = compute_score(joint_results)
                manager.count_rep(joint_results)
                feedback_text = feedback.process(joint_results)

            draw_hud(frame,
                     manager.current["name"],
                     score,
                     manager.rep_count,
                     joint_results,
                     feedback_text)

            cv2.imshow("AI Pose Trainer", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('n'):
                manager.next_exercise()
            elif key == ord('p'):
                manager.prev_exercise()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()