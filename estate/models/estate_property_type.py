from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type Model"

    name = fields.Char(required=True)