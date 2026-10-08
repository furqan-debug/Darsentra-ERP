import re
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

BFORM_REGEX = re.compile(r"^\d{5}-\d{7}-\d{1}$")


class OpAdmissionSchool(models.Model):
    _inherit = "op.admission"

    b_form = fields.Char(
        string="NADRA B-Form / CRC No.",
        size=15,
        help="Format: XXXXX-XXXXXXX-X",
    )
    father_name = fields.Char("Father's Name")
    father_cnic = fields.Char("Father's CNIC", size=15)
    father_mobile = fields.Char("Father's WhatsApp / Mobile", size=20)
    father_occupation = fields.Char("Father's Occupation")

    mother_name = fields.Char("Mother's Name")
    mother_cnic = fields.Char("Mother's CNIC", size=15)
    mother_occupation = fields.Char("Mother's Occupation")

    transport_mode = fields.Selection([
        ('parent_pick', 'Self / Parent Pick & Drop'),
        ('school_van', 'School Van / Bus'),
        ('private_van', 'Private Van Contractor'),
        ('walk', 'Walking (Local)'),
    ], string="Pick & Drop Mode", default="parent_pick")

    van_driver_name = fields.Char("Van Driver Name")
    van_driver_phone = fields.Char("Driver Phone")
    van_number = fields.Char("Van Number")
    pickup_point = fields.Char("Pickup Point / Stop")

    house_id = fields.Many2one("darsentra.school.house", string="School House")
    religion = fields.Selection([
        ('islam', 'Islam'),
        ('christianity', 'Christianity'),
        ('hinduism', 'Hinduism'),
        ('other', 'Other'),
    ], string="Religion", default="islam")
    nazra_quran = fields.Boolean("Nazra Quran Enrolled", default=True)

    previous_school_name = fields.Char("Previous School")
    previous_slc_number = fields.Char("Previous SLC No.")

    @api.constrains("b_form")
    def _check_b_form_format(self):
        for rec in self:
            if rec.b_form:
                cleaned = re.sub(r"[^\d]", "", rec.b_form)
                if len(cleaned) == 13:
                    formatted = f"{cleaned[:5]}-{cleaned[5:12]}-{cleaned[12]}"
                    if rec.b_form != formatted:
                        rec.b_form = formatted
                elif not BFORM_REGEX.match(rec.b_form):
                    raise ValidationError(_(
                        "Invalid B-Form number '%(val)s'. Must be 13 digits formatted as XXXXX-XXXXXXX-X.",
                        val=rec.b_form,
                    ))

    def enroll_student(self):
        res = super(OpAdmissionSchool, self).enroll_student()
        for admission in self:
            if admission.student_id:
                admission.student_id.write({
                    'b_form': admission.b_form,
                    'father_name': admission.father_name,
                    'father_cnic': admission.father_cnic,
                    'father_mobile': admission.father_mobile,
                    'father_occupation': admission.father_occupation,
                    'mother_name': admission.mother_name,
                    'mother_cnic': admission.mother_cnic,
                    'mother_occupation': admission.mother_occupation,
                    'transport_mode': admission.transport_mode,
                    'van_driver_name': admission.van_driver_name,
                    'van_driver_phone': admission.van_driver_phone,
                    'van_number': admission.van_number,
                    'pickup_point': admission.pickup_point,
                    'house_id': admission.house_id.id if admission.house_id else False,
                    'religion': admission.religion,
                    'nazra_quran': admission.nazra_quran,
                    'previous_school_name': admission.previous_school_name,
                    'previous_slc_number': admission.previous_slc_number,
                })
        return res
