import re
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

BFORM_REGEX = re.compile(r"^\d{5}-\d{7}-\d{1}$")


class OpStudentSchool(models.Model):
    _inherit = "op.student"

    # NADRA Child Identity
    b_form = fields.Char(
        string="NADRA B-Form / CRC No.",
        size=15,
        help="Child Registration Certificate (CRC) issued by NADRA. Format: 12345-1234567-1",
        tracking=True,
    )

    # Family & Parent Contacts
    father_name = fields.Char("Father's Name", tracking=True)
    father_cnic = fields.Char("Father's CNIC", size=15, tracking=True)
    father_mobile = fields.Char(
        "Father's WhatsApp / Mobile",
        size=20,
        help="Primary contact number for school SMS, fee reminders, and WhatsApp announcements",
        tracking=True,
    )
    father_occupation = fields.Char("Father's Profession / Occupation")

    mother_name = fields.Char("Mother's Name")
    mother_cnic = fields.Char("Mother's CNIC", size=15)
    mother_occupation = fields.Char("Mother's Profession")

    # Pick & Drop / Logistics
    transport_mode = fields.Selection([
        ('parent_pick', 'Self / Parent Pick & Drop'),
        ('school_van', 'School Van / Bus'),
        ('private_van', 'Private Van Contractor'),
        ('walk', 'Walking (Local)'),
    ], string="Pick & Drop Mode", default="parent_pick", tracking=True)

    van_driver_name = fields.Char("Van Driver Name")
    van_driver_phone = fields.Char("Driver Mobile Number")
    van_number = fields.Char("Van / Vehicle Registration No.")
    pickup_point = fields.Char("Pickup Stop / Location")

    # School Activities & House
    house_id = fields.Many2one("darsentra.school.house", string="School House")
    religion = fields.Selection([
        ('islam', 'Islam'),
        ('christianity', 'Christianity'),
        ('hinduism', 'Hinduism'),
        ('other', 'Other'),
    ], string="Religion", default="islam")
    nazra_quran = fields.Boolean("Nazra Quran Enrolled", default=True)

    # Previous Academic History & Registration
    previous_school_name = fields.Char("Previous School Attended")
    previous_slc_number = fields.Char("Previous School Leaving Cert (SLC) No.")
    admission_date = fields.Date("Admission Date", default=fields.Date.today)

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

    @api.constrains("father_cnic")
    def _check_father_cnic_format(self):
        for rec in self:
            if rec.father_cnic:
                cleaned = re.sub(r"[^\d]", "", rec.father_cnic)
                if len(cleaned) == 13:
                    formatted = f"{cleaned[:5]}-{cleaned[5:12]}-{cleaned[12]}"
                    if rec.father_cnic != formatted:
                        rec.father_cnic = formatted
                elif not BFORM_REGEX.match(rec.father_cnic):
                    raise ValidationError(_(
                        "Invalid Father CNIC format '%(val)s'. Must be 13 digits formatted as XXXXX-XXXXXXX-X.",
                        val=rec.father_cnic,
                    ))
