import json

EXERCISES_FILE = "exercises/exercises.json"

def load_all_exercises():
    with open(EXERCISES_FILE) as f:
        return json.load(f)

class ExerciseManager:
    def __init__(self):
        self.library     = load_all_exercises()
        self.keys        = list(self.library.keys())
        self.current_idx = 0
        self.current     = self.library[self.keys[0]]
        self.rep_state   = "up"
        self.rep_count   = 0

    def next_exercise(self):
        self.current_idx = (self.current_idx + 1) % len(self.keys)
        self._switch()

    def prev_exercise(self):
        self.current_idx = (self.current_idx - 1) % len(self.keys)
        self._switch()

    def _switch(self):
        self.current   = self.library[self.keys[self.current_idx]]
        self.rep_count = 0
        self.rep_state = "up"
        print(f"Switched to: {self.current['name']}")

    def count_rep(self, joint_results):
        cfg       = self.current
        rep_joint = next((j for j in joint_results if j["id"] == cfg["rep_joint"]), None)
        if not rep_joint:
            return
        angle = rep_joint["angle"]
        if self.rep_state == "up" and angle < cfg["rep_down_angle"]:
            self.rep_state = "down"
        elif self.rep_state == "down" and angle > cfg["rep_up_angle"]:
            self.rep_state = "up"
            self.rep_count += 1