from odoo import fields, models,api, _,tools
from datetime import date
from odoo.exceptions import ValidationError


class Family(models.Model):
    _name = 'bless.family'
    _description = 'Bless Family'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name='family_code'
    _order='family_code'

    family_code = fields.Char('Family Code',required=0,tracking=1)
    family_category = fields.Selection([('inside_service','Inside Service'),
                                      ('outside_service','Outside Service'),
                                      ('hidden_family','Hidden Family'),
                                      ('refugees','Refugees'),
                                      ('onetime_service','Onetime Service')],required=0,tracking=1)

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

    internal_notes=fields.Text("nternal Notes")

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id ,'%s - %s' % (record.family_code,record.husband_name)))
        return result
    @api.depends('givings_ids')
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
            r.family_member_count=len(r.member_ids.filtered(lambda x:x.dead==False))
            r.girls_member_count=len(r.member_ids.filtered(lambda x: x.role_in_family=='daughter' and x.dead==False))
            r.boys_member_count=len(r.member_ids.filtered(lambda x: x.role_in_family=='son' and x.dead==False))



class Member(models.Model):
    _name='bless.member'
    _description='Bless Members'

    name=fields.Char(required=1)
    # todo phone number Validation and National id validation

    role_in_family=fields.Selection([('husband','Husband'),
                                     ('wife','Wife'),
                                     ('son','Son'),
                                     ('daughter','Daughter'),
                                     ('other','Other')],required=1)
    egyptian=fields.Boolean(default=True,string="Egyptian")
    national_id=fields.Char()
    date_birth=fields.Date(compute='_compute_date_birth',store=1,readonly=False)
    phone_number=fields.Char(string='Phone Number')
    dead = fields.Boolean(default=False, string='Dead',tracking=1)
    family_id=fields.Many2one('bless.family',auto_join=1,tracking=1)
    family_category=fields.Selection(related='family_id.family_category',store=1)
    age=fields.Integer(compute='_compute_age',store=1,readonly=False)
    fr_of_confession=fields.Char(string='Fr of Confession')
    email=fields.Char()
    _sql_constraints = [
        ('unique_national_id',
         'unique(national_id)',
         'national_id must be unique'),

    ]
    @api.depends('date_birth','national_id')
    def _compute_age(self):
        for r in self:
            if r.date_birth or r.national_id:
                today = date.today()
                age = today.year - r.date_birth.year - ((today.month, today.day) < (r.date_birth.month, r.date_birth.day))
                r.age=age

    def compute_age(self):
        members=self.env['bless.member'].sudo().search([])
        for mem in members:
            mem._compute_age()

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



    @api.constrains('national_id')
    def check_national_id(self):
        for r in self:
            if r.egyptian and r.national_id:
                if len(r.national_id)!=14:
                    raise ValidationError(_("This egyptian National ID Is not Valid"))

    @api.constrains('phone_number')
    def check_phone_number(self):
        for r in self:
            if r.egyptian and r.phone_number:
                if len(r.phone_number) not in [10,11]:
                    raise ValidationError(_("This Phone Number Is not Valid %s",r.phone_number))

                elif not (r.phone_number.startswith('0')):
                    raise ValidationError(_("This Phone Number should start with (0) %s",r.phone_number))






