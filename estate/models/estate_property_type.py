from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type Model"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")

    _sql_constraints = [
        ('name_unique', 'unique(name)',
         'A property type must be unique.')
    ]