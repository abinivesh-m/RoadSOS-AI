class GPSManager:

    def __init__(self):

        self.latitude = 11.6643
        self.longitude = 78.1460
        self.speed = 0

    def get_location(self):

        return (
            self.latitude,
            self.longitude
        )

    def get_google_maps_link(self):

        return (
            f"https://maps.google.com/?q="
            f"{self.latitude},{self.longitude}"
        )

    def get_speed(self):

        return self.speed