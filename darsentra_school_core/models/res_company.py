from odoo import fields, models


class ResCompanySchool(models.Model):
    _inherit = "res.company"

    is_school_setup_completed = fields.Boolean(
        "School Setup Completed",
        default=False,
        help="Indicates whether the basic school profile and onboarding have been configured.",
    )
    school_campus_city = fields.Char("Campus / City", default="Lahore")
    school_board = fields.Selection([
        ('punjab', 'Punjab BISE (Lahore/Rawalpindi/Faisalabad/Multan)'),
        ('federal', 'Federal Board (FBISE Islamabad)'),
        ('sindh', 'Sindh Board (BIEK/BSEK Karachi/Hyderabad)'),
        ('kpk', 'KPK Board (BISE Peshawar/Abbottabad)'),
        ('cambridge', 'Cambridge Assessment International (CAIE O/A Levels)'),
        ('other', 'Other Secondary Board'),
    ], string="Affiliated Board", default='punjab')

    school_level = fields.Selection([
        ('comprehensive', 'Comprehensive K-12 (Playgroup to Grade 10 / Matric / O-Levels)'),
        ('primary_middle', 'Primary & Middle School (Grade 1 - 8)'),
        ('high_school', 'High School (Matric / SSC)'),
        ('cambridge', 'Cambridge System (O-Levels / A-Levels)'),
    ], string="School Category", default='comprehensive')

    academic_session = fields.Char("Current Academic Session", default="2025-2026")
    admin_whatsapp = fields.Char("Admin / Principal WhatsApp Mobile")
