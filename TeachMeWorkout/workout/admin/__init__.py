from .coach import CoachAdmin
from .exercise import ExerciseAdmin
from .exercise_to_plan import ExerciseToPlanAdmin
from .inlines import ExerciseToPlanInlineForPlan, ExerciseToPlanInlineForExercise
from .training import TrainingAdmin
from .training_plan import TrainingPlanAdmin

__all__ = [
    "CoachAdmin",
    "ExerciseAdmin",
    "ExerciseToPlanAdmin",
    "ExerciseToPlanInlineForPlan",
    "ExerciseToPlanInlineForExercise",
    "TrainingAdmin",
    "TrainingPlanAdmin"
]