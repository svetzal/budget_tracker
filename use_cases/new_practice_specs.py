from entities import CoachingPracticeFinance
from verifiers import verify_model


def test_new_practice_is_empty():
    practice = CoachingPracticeFinance()
    verify_model(practice)
