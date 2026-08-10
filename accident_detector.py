import time


class AccidentManager:

    def __init__(self):
     self.accident_detected = False
     self.sos_sent = False

     self.accident_start_time = 0
     self.remaining_time = 10

     self.impact = 0
     self.tilt = 0
     self.no_movement = False
     self.accident_confidence = 0
    def trigger_accident(self):

        self.accident_detected = True

        self.sos_sent = False

        self.accident_start_time = time.time()

        self.remaining_time = 10

    def cancel_accident(self):

        self.accident_detected = False

        self.sos_sent = False

        self.remaining_time = 10

    def update(self):

        if self.accident_detected and not self.sos_sent:

            elapsed_time = time.time() - self.accident_start_time

            self.remaining_time = max(
                0,
                10 - int(elapsed_time)
            )

            if elapsed_time >= 10:

                self.sos_sent = True

    def is_accident(self):

        return self.accident_detected

    def is_sos_sent(self):

        return self.sos_sent

    def get_countdown(self):

        return self.remaining_time

    def calculate_confidence(self):

        score = 0

        if self.impact > 70:
            score += 40

        if self.tilt > 45:
            score += 30

        if self.no_movement:
            score += 30

        self.accident_confidence = score

        if score >= 70:
            self.trigger_accident()

    def get_confidence(self):

        return self.accident_confidence