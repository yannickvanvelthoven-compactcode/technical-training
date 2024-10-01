from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer Model"

    price = fields.Float()
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    estate_id = fields.Many2one("estate.property", string="Property", required=True)
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False
    )