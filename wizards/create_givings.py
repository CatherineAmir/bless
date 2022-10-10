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
    cost = fields.Float(required=1, string='cost')

    def create_many_givings(self):

        if self.giving_category in ['coupons','money_giving']:
            givings=[]

            for family in self.family_ids:

               one_giving= {
                    'giving_date':self.giving_date,
                    'giving_category':self.giving_category,
                    'family_id':family.id,
                    'computed_cost':self.cost,
                    'occasion_id':self.occasion_id.id
                }
               givings.append(one_giving)
            created_givings=self.env['bless.giving'].create(givings)







        else:
        # TODO for giving
            pass


