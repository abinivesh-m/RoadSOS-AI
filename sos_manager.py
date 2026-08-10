class SOSManager:

    def __init__(self):

        self.status = "IDLE"
        self.already_sent = False

    def update(self, accident_manager):

        if accident_manager.is_accident():

            self.status = "COUNTDOWN"

        if accident_manager.is_sos_sent():

            self.status = "SENT"

    def get_message(self):

        if self.status == "COUNTDOWN":

            return "ACCIDENT DETECTED"

        if self.status == "SENT":

            return "Emergency Services Notified"

        return "Monitoring Rider"

    def send_sos(
        self,
        gps_manager
    ):

        if self.already_sent:
            return

        self.already_sent = True

        latitude, longitude = (
            gps_manager.get_location()
        )

        maps_link = (
            gps_manager.get_google_maps_link()
        )

        message = f"""
EMERGENCY ALERT

Possible Accident Detected

Latitude: {latitude}
Longitude: {longitude}

Location:
{maps_link}

RoadSOS AI
"""

        print(message)

        return message