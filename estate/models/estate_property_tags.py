from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.tags"
    _description = "Estate property tags Model"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('name_unique', 'unique(name)',
         'A tag name must be unique.')
    ]