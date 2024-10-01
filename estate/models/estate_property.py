from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property Model"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readOnly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Type',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        help='Type is used to define which orientation is used'
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default='new',
        copy=False,
        required=True
    )
    total_area = fields.Integer(compute='_compute_total_area', string='Total Area (sqm)')
    best_price = fields.Float(compute='_compute_best_price', string='Best Offer')
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False, readOnly=True)
    seller_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The Expected price should be greater than 0.'),
        ('check_selling_price', 'CHECK(selling_price > 0)',
         'The Selling price should be greater than 0.'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if not record.offer_ids:
                record.best_price = 0

            record.best_price = max(record.offer_ids.mapped('price'))

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = self.garden_orientation = False

        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'

    @api.constrains('selling_price')
    def _check_selling_price(self):
        # if not self.offer_accepted():
        #     raise ValidationError('No offers accepted yet!')

        for record in self:
            if float_compare(record.selling_price, (record.expected_price * 0.9), precision_rounding=None) < 0:
                raise ValidationError('Selling price is too low!')

    def offer_accepted(self):
        return 'accepted' in self.offer_ids.mapped('status')

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled properties cannot be sold.")

            record.state = 'sold'

    def action_cancel(self):
        self.state = 'cancelled'