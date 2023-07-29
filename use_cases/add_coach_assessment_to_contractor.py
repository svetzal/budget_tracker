from entities import CoachAssessment
from use_cases.use_case import UseCase


class AddCoachAssessmentToContractor(UseCase):
    def execute(self, contractor_code: str, completed_on: str, leadership: float, technical: float, practice: float):
        coach = self.find_contractor(contractor_code)
        coach.assessments.append(
            CoachAssessment(
                completed_on=completed_on,
                leadership=leadership,
                technical=technical,
                practice=practice,
            )
        )
