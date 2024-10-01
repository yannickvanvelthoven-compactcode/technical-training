from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.tags"
    _description = "Estate property tags Model"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)',
         'A tag name must be unique.')
    ]