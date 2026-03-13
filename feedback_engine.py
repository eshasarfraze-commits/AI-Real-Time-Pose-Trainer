import time
import threading

try:
    import pyttsx3
    tts_engine = pyttsx3.init()
    tts_engine.setProperty("rate", 160)
    TTS_AVAILABLE = True
except:
    TTS_AVAILABLE = False

class FeedbackEngine:
    def __init__(self, cooldown=3.0):
        self.cooldown   = cooldown
        self.last_spoke = {}

    def get_priority_feedback(self, joint_results):
        for j in joint_results:
            if j["status"] != "correct" and j["feedback"]:
                return j["feedback"]
        return None

    def speak(self, text):
        if not TTS_AVAILABLE:
            return
        now = time.time()
        if now - self.last_spoke.get(text, 0) > self.cooldown:
            self.last_spoke[text] = now
            threading.Thread(
                target=lambda: (tts_engine.say(text), tts_engine.runAndWait()),
                daemon=True
            ).start()

    def process(self, joint_results):
        feedback = self.get_priority_feedback(joint_results)
        if feedback:
            self.speak(feedback)
        return feedback