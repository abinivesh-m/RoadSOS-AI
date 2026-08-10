def calculate_risk_score(
    phone_alert_timer,
    drowsy_alert_timer,
    speed
):

    score = 0

    # Phone Usage
    if phone_alert_timer > 0:
        score += 40

    # Drowsiness
    if drowsy_alert_timer > 0:
        score += 40

    # Speed Risk
    if speed > 60:
        score += 20

    if speed > 80:
        score += 30

    if score > 100:
        score = 100

    return score