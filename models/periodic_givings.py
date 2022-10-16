from odoo import fields, models, api


class Giving(models.Model):
    _name = 'bless.giving'
    _description = 'Bless Giving'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order='id desc'

    name = fields.Char(compute='_compute_name',store=1)
    state= fields.Selection([
        ('opened', 'Opened'),
        ('closed', 'Closed')], default='opened',copy=False, tracking=True,required=1)
    giving_date=fields.Date(required=1,string='Giving date',tracking=1,readonly=True,states={'opened':[('readonly', False)]})

    family_id=fields.Many2one('bless.family',string='Family Code',tracking=1,readonly=True,
                              states={'opened':[('readonly', False)]})
    family_husband=fields.Char(related='family_id.husband_name',store=1,string='Husband name')
    family_category=fields.Selection(related='family_id.family_category',store=1)
    people_count=fields.Integer(related='family_id.family_member_count',store=1,string='family member count')
    occasion_id=fields.Many2one('bless.occasions',required=1,string='Occasion',tracking=1,
       readonly=True,states={'opened': [('readonly', False)]})
    cost=fields.Float(compute='compute_giving_cost',store=1,readonly=False,string='cost',state={'closed': [('readonly', True)]},tracking=1)
    only_cost=fields.Char('Only Cost',readonly=True,states={'opened':[('readonly', False)]},tracking=1)

    giving_category=fields.Selection([('hand_giving','Hand Giving'),
                                   ('coupons','Coupons'),
                                      ('money_giving','Money Giving')],required=1,string='Giving Type',readonly=True,tracking=1)


    coupon_category=fields.Selection([('food','Food'),
                                     ('clothes','Clothes'),
                                   ],string='Coupon type',readonly=True,states={'opened': [('readonly', False)]})
    from_receipt_time=fields.Float(readonly=True,states={'opened': [('readonly', False)]},string='From')
    from_period=fields.Selection([('pm','PM'),('am','Am')],readonly=True,states={'opened': [('readonly', False)]})
    to_receipt_time=fields.Float(readonly=True,states={'opened': [('readonly', False)]},string='To')
    to_period = fields.Selection([('pm', 'PM'), ('am', 'Am')],readonly=True,states={'opened': [('readonly', False)]})


    giving_lines_food=fields.One2many('bless.giving.line','giving_id',auto_join=1,
                                      domain=[('giving_type','=','food_beverage')],readonly=True,states={'opened': [('readonly', False)]})
    giving_lines_concrete=fields.One2many('bless.giving.line','giving_id',auto_join=1,
                                          domain=[('giving_type','=','concrete_giving')],readonly=True,states={'opened': [('readonly', False)]})
    create_date=fields.Datetime(default=lambda self: fields.datetime.now(),readonly=1)
    create_by=fields.Many2one('res.users',default=lambda self:self.env.user.id,readonly=1)



    def action_close(self):
        for r in self:
            r.state='closed'

    def action_open(self):
        for r in self:
            r.state='opened'

    @api.depends('giving_lines_food', 'giving_lines_concrete')
    def compute_giving_cost(self):
        for r in self:
            r.cost = sum(r.giving_lines_food.mapped('cost')) + sum(r.giving_lines_concrete.mapped('cost'))


    @api.depends('giving_category')
    def _compute_name(self):
        for r in self:
            if r.giving_category=='hand_giving':
                r.name=self.env['ir.sequence'].next_by_code('bless.giving_hand_giving')
            elif r.giving_category=='money_giving':
                r.name=self.env['ir.sequence'].next_by_code('bless.giving_money_giving')
            else:
                r.name = self.env['ir.sequence'].next_by_code('bless.giving_coupons')


class GivingLine(models.Model):
    _name = 'bless.giving.line'
    _description = 'Bless Giving'
    # to be serial
    # name=fields.Char()
    giving_id = fields.Many2one('bless.giving',required=1,auto_join=1)
    giving_category = fields.Selection(related='giving_id.giving_category',store=1,string='Giving category')
    giving_type = fields.Selection([('food_beverage','Food Beverage'),('concrete_giving',' Concrete Giving')])
    beverage_id = fields.Many2one('bless.beverage',string="Food And Beverage")
    unit_id = fields.Many2one(related='beverage_id.unit_id',store=1,readonly=False)
    concrete_id = fields.Many2one('bless.concrete',store=1,string="Concrete Giving")
    cost = fields.Float(compute='_compute_cost',store=1,readonly=False,string='cost')
    quantity=fields.Float('Quantity',default=1)

    @api.model
    def default_get(self, fields):
        """ BUG ODOO??? """

        if 'default_giving_type' in self._context:
            fields += ['giving_type']
        return super(GivingLine, self).default_get(fields)




