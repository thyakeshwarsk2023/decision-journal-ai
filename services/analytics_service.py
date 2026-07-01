def confidence_error(
        confidence: int,
        outcome : int
):
    return abs(
        confidence - outcome
    )

def average_score(
        scores: list[int]
):
    if not scores:
        return 0
    
    return round(
        sum(scores) / len(scores),
        2
    )

def predicted_feeling(
        outcome_rating: int
):
    return(
        "proud"
        if outcome_rating >= 7
        else "regret"
    )
    