from odoo import fields, models, api


class CreateGiving(models.TransientModel):
    _name = 'bless.create.givings'
    _description = 'Create simple Givings'

    giving_date=fields.Date(required=1,string='Giving Date')
    family_ids = fields.Many2many('bless.family', string='Family Code',required=1)
    occasion_id = fields.Many2one('bless.occasions', required=1, string='Occasion')
    giving_category = fields.Selection([('hand_giving', 'Hand Giving'),
                                        ('coupons', 'coupons'),
                                        ('money_giving', 'Money Giving')], required=1, string='Giving Type')
    cost = fields.Float(string='cost',compute='compute_cost',store=1,readonly=False)
    giving_lines_food = fields.Many2many('bless.create.givings.lines','lines_food', 'src_id', 'dest_id',
                                         auto_join=1)

    giving_lines_concrete = fields.Many2many('bless.create.givings.lines','lines_concrete', 'src_id', 'dest_id', auto_join=1)

    coupon_category = fields.Selection([('food', 'Food'),
                                        ('clothes', 'Clothes'),
                                        ], string='Coupon type')
    from_receipt_time = fields.Float()
    from_period = fields.Selection([('pm', 'PM'), ('am', 'Am')])
    to_receipt_time = fields.Float()
    to_period = fields.Selection([('pm', 'PM'), ('am', 'Am')])

    @api.depends('giving_lines_food','giving_lines_concrete')
    def compute_cost(self):
        for r in self:
            r.cost=sum(r.giving_lines_food.mapped('cost'))+sum(r.giving_lines_concrete.mapped('cost'))




    def create_many_givings(self):

        print('read',self.read()[0])
        givings=[]
        if self.giving_category in ['coupons', 'money_giving']:
            for family in self.family_ids:
                one_giving= {
                'giving_date':self.giving_date,
                'giving_category':self.giving_category,
                'family_id':family.id,
                'cost':self.cost,
                'occasion_id':self.occasion_id.id,
                'coupon_category':self.coupon_category,
                'from_receipt_time':self.from_receipt_time,
                'from_period':self.from_period,
                'to_receipt_time':self.to_receipt_time,
                'to_period':self.to_period,


            }
                givings.append(one_giving)
            created_givings = self.env['bless.giving'].create(givings)
            print('givings', created_givings)
        else:
            food_lines=[]
            print('self.giving_lines_food',self.giving_lines_food)

            for line in self.giving_lines_food:
                food_line={
                'giving_type':'food_beverage',
                'beverage_id':line.beverage_id.id,
                'quantity':line.quantity,
                'unit_id':line.unit_id.id,
                'cost':line.cost,
                }

                food_lines.append(food_line)
            print('food_lines', food_lines)
            concrete_lines=[]
            print('self.giving_lines_concrete', self.giving_lines_concrete)
            for line in self.giving_lines_concrete:
                concrete_line = {
                    'giving_type': 'concrete_giving',
                    'concrete_id': line.concrete_id.id,
                    'quantity':line.quantity,
                    'cost': line.cost,
                }
                concrete_lines.append(concrete_line)
            print('concrete_lines',concrete_lines)
            for family in self.family_ids:
                one_giving = {
                    'giving_date': self.giving_date,
                    'giving_category': self.giving_category,
                    'family_id': family.id,
                    'cost': self.cost,
                    'occasion_id': self.occasion_id.id,
                    'giving_lines_food':[(0,0,food) for food in food_lines],
                    'giving_lines_concrete':[(0,0,concrete) for concrete in concrete_lines],

                }
                givings.append(one_giving)
            created_givings = self.env['bless.giving'].create(givings)
            print('givings_handed', created_givings)














class CreateGivingLines(models.TransientModel):
    _name = 'bless.create.givings.lines'
    _description = 'Create  Givings Lines'

    giving_id = fields.Many2many('bless.create.givings', auto_join=1,ondelete='cascade')
    giving_category = fields.Selection(related='giving_id.giving_category', store=1, string='Giving category')
    # giving_type = fields.Selection([('food_beverage', 'Food Beverage'), ('concrete_giving', ' Concrete Giving')])
    beverage_id = fields.Many2one('bless.beverage', string="Food And Beverage")
    unit_id = fields.Many2one(related='beverage_id.unit_id', store=1, readonly=False)
    concrete_id = fields.Many2one('bless.concrete', store=1, string="Concrete Giving")
    cost = fields.Float(compute='_compute_cost', store=1, readonly=False, string='cost')
    quantity = fields.Float('Quantity', default=1)

