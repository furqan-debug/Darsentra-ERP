from odoo import _, api, fields, models


class OpExamSchool(models.Model):
    _inherit = "op.exam"

    passing_marks = fields.Float("Passing Marks", default=33.0)


class OpMarksheetLineSchool(models.Model):
    _inherit = "op.marksheet.line"

    class_id = fields.Many2one("op.course", string="Class", related="marksheet_reg_id.exam_session_id.course_id", store=True)
    section_id = fields.Many2one("op.batch", string="Section", related="marksheet_reg_id.exam_session_id.batch_id", store=True)
    father_name = fields.Char("Father's Name", related="student_id.father_name", store=True)
    student_b_form = fields.Char("B-Form / CRC", related="student_id.b_form", store=True)

    school_grade = fields.Char(
        string="School Grade",
        compute="_compute_school_grade",
        store=True,
    )

    class_position = fields.Char(
        string="Class / Section Position",
        default="Pass",
        help="1st Position, 2nd Position, 3rd Position...",
    )
    position_rank = fields.Integer("Position Rank", default=0)

    teacher_remarks = fields.Char(
        string="Class Teacher Remarks",
        default="Satisfactory progress. Keep working hard.",
    )
    term_attendance_percentage = fields.Float("Term Attendance (%)", default=95.0)

    @api.depends("percentage")
    def _compute_school_grade(self):
        for line in self:
            p = line.percentage or 0.0
            if p >= 80.0:
                line.school_grade = "A+ (Outstanding)"
            elif p >= 70.0:
                line.school_grade = "A (Excellent)"
            elif p >= 60.0:
                line.school_grade = "B (Very Good)"
            elif p >= 50.0:
                line.school_grade = "C (Good)"
            elif p >= 40.0:
                line.school_grade = "D (Fair)"
            elif p >= 33.0:
                line.school_grade = "E (Pass)"
            else:
                line.school_grade = "F (Fail)"


class OpMarksheetRegisterSchool(models.Model):
    _inherit = "op.marksheet.register"

    def action_calculate_class_positions(self):
        """Calculate 1st, 2nd, 3rd class positions based on total marks / percentage."""
        for reg in self:
            sorted_lines = reg.marksheet_line.sorted(key=lambda l: (l.percentage or 0.0, l.total_marks or 0.0), reverse=True)
            for rank, line in enumerate(sorted_lines, start=1):
                line.position_rank = rank
                if rank == 1:
                    line.class_position = "1st Position 🏆"
                elif rank == 2:
                    line.class_position = "2nd Position 🥈"
                elif rank == 3:
                    line.class_position = "3rd Position 🥉"
                else:
                    line.class_position = f"{rank}th"
        return True
