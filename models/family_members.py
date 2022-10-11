from odoo import fields, models,api, _,tools
from datetime import date
from odoo.exceptions import ValidationError


class Family(models.Model):
    _name = 'bless.family'
    _description = 'Bless Family'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name='family_code'
    _order='family_code'

    family_code = fields.Char('Family Code',required=1,tracking=1)
    family_category = fields.Selection([('inside_service','Inside Service'),
                                      ('outside_service','Outside Service'),
                                      ('hidden_family','Hidden Family'),
                                      ('refugees','Refugees'),
                                      ('onetime_service','Onetime Service')],required=1,tracking=1)

    responsible_servant=fields.Many2one('bless.servants',string='Responsible Servant',tracking=1)

    member_ids=fields.One2many('bless.member','family_id',string='Family Members')
    family_member_count=fields.Integer(compute='_compute_family_count',store=1)
    girls_member_count=fields.Integer(compute='_compute_family_count',store=1)
    boys_member_count=fields.Integer(compute='_compute_family_count',store=1)
    husband_name=fields.Char(compute='_compute_husband_name',store=1,string='Husband Name')

    # address_fields
    district=fields.Many2one('bless.regions',string='District',tracking=1)
    nearby = fields.Char(string='Nearby',tracking=1)
    building_number = fields.Char(string='Building Number')
    apartment_number = fields.Char( string='Apartment Number')
    givings_ids = fields.One2many('bless.giving','family_id',string='Givings',tracking=1)
    givings_count=fields.Integer(compute='compute_givings_count',store=1,tracking=1)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id ,'%s - %s' % (record.family_code,record.husband_name)))
        return result
    def compute_givings_count(self):
        for r in self:
            r.givings_count=len(r.givings_ids)
    def get_family_givings(self):
        action = self.env.ref('bless.'
                              'all_givings_act_window').read()[0]
        action['domain'] = [('family_id', '=', self.id)]
        return action

    @api.depends('member_ids')
    def _compute_husband_name(self):
        for r in self:
            husband = r.member_ids.filtered(lambda x: x.role_in_family == 'husband')

            if len(husband)==0:
                pass
            elif len(husband)==1:
                r.husband_name=husband.name
            else:
                raise ValidationError(_("Family Can Only Contain one Husband"))




    @api.depends('member_ids')
    def _compute_family_count(self):
        for r in self:
            r.family_member_count=len(r.member_ids)
            r.girls_member_count=len(r.member_ids.filtered(lambda x: x.role_in_family=='daughter'))
            r.boys_member_count=len(r.member_ids.filtered(lambda x: x.role_in_family=='daughter'))



class Member(models.Model):
    _name='bless.member'
    _description='Bless Members'

    name=fields.Char(required=1)

    role_in_family=fields.Selection([('husband','Husband'),
                                     ('wife','Wife'),
                                     ('son','Son'),
                                     ('daughter','Daughter'),
                                     ('other','Other')],required=1)
    egyptian=fields.Boolean(default=True,string="Egyptian")
    national_id=fields.Char()
    date_birth=fields.Date(compute='_compute_date_birth',store=1,readonly=False)
    phone_number=fields.Char(string='Phone Number')
    family_id=fields.Many2one('bless.family',auto_join=1)
    family_category=fields.Selection(related='family_id.family_category',store=1)

    email=fields.Char()



    @api.depends('national_id')
    def _compute_date_birth(self):
        for r in self:
            if r.national_id and r.egyptian:
                id= r.national_id
                if id.startswith('2'):
                    year = '19' + id[1] + id[2]
                elif id.startswith('3'):
                    year = '20' + id[1] + id[2]
                else:
                    year = 'invalid'
                    raise ValidationError(_("This egyptian National ID Is not Valid"))



                month = id[3:5]

                day = id[5:7]

                try:
                    bithdate = date(int(year), int(month), int(day))

                    r.date_birth=bithdate
                except Exception as e:
                    raise ValidationError(_("This egyptian National ID Is not Valid %s",e))
            if not r.national_id:
                r.date_birth=False









