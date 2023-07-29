from entities import CoachAssessment
from use_cases.use_case import UseCase


class AddCoachAssessmentToEmployee(UseCase):
    def execute(self, employee_code: str, completed_on: str, leadership: float, technical: float, practice: float):
        coach = self.find_employee(employee_code)
        coach.assessments.append(
            CoachAssessment(
                completed_on=completed_on,
                leadership=leadership,
                technical=technical,
                practice=practice,
            )
        )
