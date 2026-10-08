from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DarsentraSchoolCertificate(models.Model):
    _name = "darsentra.school.certificate"
    _description = "School Certificates (SLC / Character / Bonafide)"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "issue_date desc, id desc"
    _rec_name = "certificate_number"

    certificate_type = fields.Selection([
        ('slc', 'School Leaving Certificate (SLC)'),
        ('character', 'Character & Conduct Certificate'),
        ('bonafide', 'Bonafide Student Certificate'),
    ], string="Certificate Type", default="slc", required=True, tracking=True)

    certificate_number = fields.Char(
        string="Certificate Serial No.",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
    )

    student_id = fields.Many2one("op.student", string="Student", required=True, tracking=True)
    gr_no = fields.Char("General Register (GR) No.", related="student_id.gr_no", store=True)
    father_name = fields.Char("Father's Name", related="student_id.father_name", store=True)
    b_form = fields.Char("B-Form / CRC No.", related="student_id.b_form", store=True)
    birth_date = fields.Date("Date of Birth", related="student_id.birth_date")

    date_of_admission = fields.Date("Date of Admission", related="student_id.admission_date", readonly=False)
    date_of_leaving = fields.Date("Date of Leaving", default=fields.Date.today)
    issue_date = fields.Date("Certificate Issue Date", default=fields.Date.today, required=True)

    class_at_leaving = fields.Many2one("op.course", string="Class at the Time of Leaving")
    section_at_leaving = fields.Many2one("op.batch", string="Section at Leaving")
    class_promoted_to = fields.Char("Promoted to Class")

    reason_for_leaving = fields.Selection([
        ('transfer', 'Parent Job Transfer'),
        ('relocation', 'Family Residence Relocation'),
        ('passed_out', 'Completed Highest Grade / Matric'),
        ('financial', 'Financial / Personal Reasons'),
        ('other', 'Other'),
    ], string="Reason for Leaving", default="relocation")

    reason_detail = fields.Char("Reason Detail")
    conduct_and_character = fields.Selection([
        ('exemplary', 'Exemplary / Excellent'),
        ('good', 'Good'),
        ('satisfactory', 'Satisfactory'),
    ], string="General Conduct & Character", default="good", required=True)

    dues_cleared = fields.Boolean(
        string="All Dues & Books Cleared",
        default=True,
        help="Verified that all school fees, library books, and sports equipment have been returned",
    )

    remarks = fields.Text("Special Remarks / Remarks for School Record")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved by Incharge'),
        ('issued', 'Issued'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default="draft", tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('certificate_number', _('New')) == _('New'):
                prefix = 'SLC' if vals.get('certificate_type') == 'slc' else 'CERT'
                vals['certificate_number'] = self.env['ir.sequence'].next_by_code('darsentra.school.certificate') or f"{prefix}/{fields.Date.today().year}/{self.search_count([]) + 1:04d}"
        return super(DarsentraSchoolCertificate, self).create(vals_list)

    @api.onchange("student_id")
    def _onchange_student_id(self):
        if self.student_id:
            active_enrollment = self.student_id.course_detail_ids.filtered(lambda c: c.state == 'running')[:1]
            if active_enrollment:
                self.class_at_leaving = active_enrollment.course_id
                self.section_at_leaving = active_enrollment.batch_id

    def action_approve(self):
        self.state = 'approved'

    def action_issue(self):
        if not self.dues_cleared:
            raise ValidationError(_("Cannot issue certificate while student dues remain pending!"))
        self.state = 'issued'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_reset_draft(self):
        self.state = 'draft'
