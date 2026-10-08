from odoo import fields, models


class DarsentraSchoolHouse(models.Model):
    _name = "darsentra.school.house"
    _description = "School House (Sports & Discipline)"
    _order = "name"

    name = fields.Char("House Name", required=True)
    color_code = fields.Char("Color (Hex or Name)", default="#1e40af")
    motto = fields.Char("House Motto")
    house_master_id = fields.Many2one("op.faculty", string="House Incharge Teacher")
    student_count = fields.Integer("Students", compute="_compute_student_count")

    def _compute_student_count(self):
        for house in self:
            house.student_count = self.env["op.student"].search_count([("house_id", "=", house.id)])
