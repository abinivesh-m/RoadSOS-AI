def get_status(
    phone_alert_timer,
    drowsy_alert_timer,
    speed,
    accident_manager
):

    status = "SAFE"
    status_color = (0, 255, 0)

    if (
        phone_alert_timer > 0
        or speed > 60
    ):
        status = "WARNING"
        status_color = (0, 255, 255)

    if (
        drowsy_alert_timer > 0
        or speed > 80
    ):
        status = "DANGER"
        status_color = (0, 0, 255)

    if (
        accident_manager.is_accident()
        or accident_manager.is_sos_sent()
    ):
        status = "ACCIDENT"
        status_color = (0, 0, 255)

    return status, status_color