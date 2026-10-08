from datetime import timedelta
from odoo import _, api, fields, models


class AccountMoveSchoolFee(models.Model):
    _inherit = "account.move"

    is_school_fee = fields.Boolean("Is School Monthly Challan", default=False)
    billing_month = fields.Char("Fee Month / Period", tracking=True)

    student_id = fields.Many2one("op.student", string="Student", tracking=True)
    roll_number = fields.Char("Roll No.", compute="_compute_school_student_info", store=True)
    student_b_form = fields.Char("B-Form / CRC", compute="_compute_school_student_info", store=True)
    father_name = fields.Char("Father's Name", compute="_compute_school_student_info", store=True)
    father_mobile = fields.Char("Father's WhatsApp / Mobile", compute="_compute_school_student_info", store=True)

    class_id = fields.Many2one("op.course", string="Class (Grade)")
    section_id = fields.Many2one("op.batch", string="Section")

    consumer_number = fields.Char(
        string="1Link / Kuickpay Consumer ID",
        compute="_compute_consumer_number",
        store=True,
    )

    bank_account_id = fields.Many2one(
        "res.partner.bank",
        string="School Bank Account",
        help="Designated bank branch where fees can be deposited",
    )

    validity_date = fields.Date(
        string="Bank Payment Validity Date",
        compute="_compute_validity_date",
        readonly=False,
        store=True,
    )

    sibling_discount_percent = fields.Float("Sibling Discount (%)", default=0.0)
    sibling_discount_amount = fields.Monetary(
        "Sibling Discount (PKR)",
        currency_field="currency_id",
        default=0.0,
    )

    arrears_amount = fields.Monetary(
        string="Previous Arrears (PKR)",
        currency_field="currency_id",
        default=0.0,
        help="Pending balance brought forward from previous unpaid months",
    )

    late_fee_surcharge = fields.Monetary(
        string="Late Fee Surcharge",
        currency_field="currency_id",
        default=300.0,
    )

    total_with_late_fee = fields.Monetary(
        string="Total After Due Date",
        currency_field="currency_id",
        compute="_compute_total_with_late_fee",
        store=True,
    )

    @api.depends("student_id")
    def _compute_school_student_info(self):
        for move in self:
            if move.student_id:
                move.student_b_form = move.student_id.b_form
                move.father_name = move.student_id.father_name
                move.father_mobile = move.student_id.father_mobile
                active_course = move.student_id.course_detail_ids.filtered(lambda c: c.state == 'running')[:1]
                move.roll_number = active_course.roll_number if active_course else move.student_id.gr_no
                if not move.class_id and active_course:
                    move.class_id = active_course.course_id
                if not move.section_id and active_course:
                    move.section_id = active_course.batch_id
            else:
                move.student_b_form = False
                move.father_name = False
                move.father_mobile = False
                move.roll_number = False

    @api.depends("invoice_date_due")
    def _compute_validity_date(self):
        for move in self:
            if move.invoice_date_due:
                move.validity_date = move.invoice_date_due + timedelta(days=10)
            else:
                move.validity_date = False

    @api.depends("name", "company_id")
    def _compute_consumer_number(self):
        for move in self:
            if move.id:
                prefix = "1002"
                move.consumer_number = f"{prefix}{move.id:08d}"
            else:
                move.consumer_number = False

    @api.depends("amount_total", "late_fee_surcharge")
    def _compute_total_with_late_fee(self):
        for move in self:
            move.total_with_late_fee = (move.amount_total or 0.0) + (move.late_fee_surcharge or 0.0)
