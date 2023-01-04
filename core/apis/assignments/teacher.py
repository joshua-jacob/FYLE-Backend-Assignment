from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema,AssignmentGradeSchema
teacher_assignment_resources = Blueprint('teacher_assignment_resources', __name__)


@teacher_assignment_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments"""
    teacher_assignment = Assignment.get_assignments_by_teacher(p.teacher_id)
    teacher_assignment_dump = AssignmentSchema().dump(teacher_assignment, many=True)
    return APIResponse.respond(data=teacher_assignment_dump)





@teacher_assignment_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    """Submit an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.grading(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
