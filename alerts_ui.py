# =====================================
# ALERT MESSAGE MANAGER
# =====================================

def get_alert_message(
        phone_alert_timer,
        drowsy_alert_timer,
        speed,
        accident_manager
):

    alert_message = "Monitoring Rider"
    alert_color = (255, 255, 255)

    if phone_alert_timer > 0:

        alert_message = "Mobile Usage Detected"
        alert_color = (0, 255, 255)

    if speed > 60:

        alert_message = "Overspeed Warning"
        alert_color = (0, 255, 255)

    if speed > 80:

        alert_message = "Dangerous Speed"
        alert_color = (0, 0, 255)

    if drowsy_alert_timer > 0:

        alert_message = "Drowsiness Detected"
        alert_color = (0, 0, 255)

    if (
        accident_manager.is_accident()
        and not accident_manager.is_sos_sent()
    ):

        alert_message = "ACCIDENT DETECTED"
        alert_color = (0, 0, 255)

    if accident_manager.is_sos_sent():

        alert_message = "Emergency Services Notified"
        alert_color = (0, 0, 255)

    return alert_message, alert_color