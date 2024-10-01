from odoo import api, fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer Model"

    price = fields.Float()
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(_compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + record.validity

    def _inverse_date_deadline(self):
        for record in self:
            record.create_date = record.date_deadline - record.validity
            record.validity = record.date_deadline - record.create_date
