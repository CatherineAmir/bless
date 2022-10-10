from odoo import fields, models, api


class Giving(models.Model):
    _name = 'bless.giving'
    _description = 'Bless Giving'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order='id desc'

    name = fields.Char(compute='_compute_name',store=1)
    giving_date=fields.Date(required=1,string='Giving date',traking=1)
    family_id=fields.Many2one('bless.family',autojoin=1,string='Family Code',traking=1)
    family_husband=fields.Char(related='family_id.husband_name',store=1,string='Husband name')
    family_category=fields.Selection(related='family_id.family_category',store=1)
    people_count=fields.Integer(related='family_id.family_member_count',store=1,string='family member count')
    occasion_id=fields.Many2one('bless.occasions',required=1,string='Occasion',traking=1)
    computed_cost=fields.Float(compute='compute_giving_cost',store=1,readonly=False,string='cost')
    giving_category=fields.Selection([('hand_giving','Hand Giving'),
                                   ('coupons','coupons'),
                                      ('money_giving','Money Giving')],required=1,string='Giving Type')

    giving_lines_food=fields.One2many('bless.giving.line','giving_id',autojoin=1,domain=[('giving_type','=','food_beverage')])
    giving_lines_concrete=fields.One2many('bless.giving.line','giving_id',autojoin=1,domain=[('giving_type','=','concrete_giving')])
    create_date=fields.Datetime(default=lambda self: fields.datetime.now(),readonly=1)
    create_by=fields.Many2one('res.users',default=lambda self:self.env.user.id,readonly=1)
    def compute_giving_cost(self):
        pass
    @api.depends('giving_category')
    def _compute_name(self):
        for r in self:
            if r.giving_category=='hand_giving':
                r.name=self.env['ir.sequence'].next_by_code('bless.giving_hand_giving')
            elif r.giving_category=='money_giving':
                r.name=self.env['ir.sequence'].next_by_code('bless.giving_money_giving')
            else:
                r.name = self.env['ir.sequence'].next_by_code('bless.giving_coupons')


class Giving(models.Model):
    _name = 'bless.giving.line'
    _description = 'Bless Giving'
    # to be serial
    name=fields.Char()
    giving_id=fields.Many2one('bless.giving',requried=1,autojoin=1)
    giving_category=fields.Selection(related='giving_id.giving_category',store=1,string='Giving category')
    giving_type=fields.Selection([('food_beverage','Food Beverage'),('concrete_giving',' Concrete Giving')])
    beverage_id=fields.Many2one('bless.beverage',string="Food And Beverage")
    unit_id=fields.Many2one(related='beverage_id.unit_id',store=1,readonly=False)
    concrete_id=fields.Many2one('bless.concrete',store=1,string="Concrete Giving")
    cost=fields.Float(compute='_compute_cost',store=1,readonly=False,string='cost')

    def _compute_cost(self):
        pass



