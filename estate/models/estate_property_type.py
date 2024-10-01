from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type Model"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)',
         'A property type must be unique.')
    ]