from datetime import date, timedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class DarsentraMonthlyFeeWizard(models.TransientModel):
    _name = "darsentra.monthly.fee.wizard"
    _description = "School Bulk Monthly Fee Generator"

    billing_month = fields.Char(
        string="Fee Month / Period",
        required=True,
        default=lambda self: date.today().strftime("%B %Y"),
    )

    class_id = fields.Many2one("op.course", string="Target Class (Leave blank for whole school)")
    section_id = fields.Many2one("op.batch", string="Target Section")

    invoice_date = fields.Date("Issue Date", default=fields.Date.today, required=True)
    due_date = fields.Date(
        "Due Date",
        default=lambda self: fields.Date.today() + timedelta(days=10),
        required=True,
    )
    validity_date = fields.Date(
        "Bank Validity Date",
        default=lambda self: fields.Date.today() + timedelta(days=20),
        required=True,
    )

    tuition_fee_amount = fields.Float("Monthly Tuition Fee (PKR)", default=3500.0, required=True)
    apply_sibling_discount = fields.Boolean("Enable Automatic Sibling Discount", default=True)
    second_child_discount = fields.Float("2nd Sibling Discount (%)", default=10.0)
    third_child_discount = fields.Float("3rd+ Sibling Discount (%)", default=20.0)

    include_exam_fund = fields.Boolean("Include Exam / Paper Fund", default=False)
    exam_fund_amount = fields.Float("Exam Fund (PKR)", default=500.0)

    late_fee_surcharge = fields.Float("Late Fee Fine (PKR)", default=300.0)

    def action_generate_monthly_fees(self):
        domain = [('state', '=', 'running')]
        if self.class_id:
            domain.append(('course_id', '=', self.class_id.id))
        if self.section_id:
            domain.append(('batch_id', '=', self.section_id.id))

        student_courses = self.env['op.student.course'].search(domain)
        if not student_courses:
            raise UserError(_("No enrolled students found matching the selected Class / Section."))

        # Group students by Father's CNIC or Father's Mobile to calculate Sibling Rank
        family_map = {}
        for sc in student_courses:
            st = sc.student_id
            family_key = (st.father_cnic or st.father_mobile or f"st_{st.id}").strip()
            family_map.setdefault(family_key, []).append(sc)

        created_moves = self.env['account.move']
        partner_obj = self.env['res.partner']
        account_journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)

        for family_key, cohort in family_map.items():
            # Sort siblings by birth date descending (younger siblings get the discount)
            sorted_siblings = sorted(cohort, key=lambda s: s.student_id.birth_date or date(2000, 1, 1))

            for index, sc in enumerate(sorted_siblings):
                student = sc.student_id
                partner = student.partner_id

                discount_pct = 0.0
                if self.apply_sibling_discount and len(sorted_siblings) > 1:
                    if index == 1:
                        discount_pct = self.second_child_discount
                    elif index >= 2:
                        discount_pct = self.third_child_discount

                discount_amount = round((self.tuition_fee_amount * discount_pct) / 100.0, 2)
                net_tuition = self.tuition_fee_amount - discount_amount

                lines = [
                    (0, 0, {
                        'name': f"Monthly Tuition Fee - {self.billing_month}",
                        'quantity': 1,
                        'price_unit': self.tuition_fee_amount,
                    })
                ]

                if discount_amount > 0:
                    lines.append((0, 0, {
                        'name': f"Sibling Discount ({discount_pct}%)",
                        'quantity': 1,
                        'price_unit': -discount_amount,
                    }))

                if self.include_exam_fund and self.exam_fund_amount > 0:
                    lines.append((0, 0, {
                        'name': f"Exam & Paper Fund - {self.billing_month}",
                        'quantity': 1,
                        'price_unit': self.exam_fund_amount,
                    }))

                move_vals = {
                    'move_type': 'out_invoice',
                    'partner_id': partner.id,
                    'journal_id': account_journal.id if account_journal else False,
                    'invoice_date': self.invoice_date,
                    'invoice_date_due': self.due_date,
                    'is_school_fee': True,
                    'billing_month': self.billing_month,
                    'student_id': student.id,
                    'class_id': sc.course_id.id,
                    'section_id': sc.batch_id.id,
                    'sibling_discount_percent': discount_pct,
                    'sibling_discount_amount': discount_amount,
                    'late_fee_surcharge': self.late_fee_surcharge,
                    'validity_date': self.validity_date,
                    'invoice_line_ids': lines,
                }

                move = self.env['account.move'].create(move_vals)
                created_moves |= move

        return {
            'name': _(f"Generated Challans - {self.billing_month}"),
            'view_mode': 'list,form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', created_moves.ids)],
        }
