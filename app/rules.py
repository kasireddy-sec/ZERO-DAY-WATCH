def qualifies_zero_day(a, rules):
    if not a or not a.is_security_issue:
        return False
    if a.confidence < float(rules["zero_day"]["minimum_confidence"]):
        return False
    if not a.evidence and rules["zero_day"]["require_evidence"]:
        return False
    strong = 0
    if a.previously_unknown: strong += 1
    if a.active_exploitation: strong += 1
    if a.exploitation_status == "confirmed": strong += 1
    if a.patch_available is False: strong += 1
    if a.zero_day_candidate: strong += 1
    if a.poc_available and strong == 0:
        return False
    return strong >= 2
