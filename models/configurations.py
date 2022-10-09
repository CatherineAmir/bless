from odoo import fields, models, api


class Regions(models.Model):
    _name = 'bless.regions'
    _description = 'Regions'

    name = fields.Char()

class Servants(models.Model):
    _name = 'bless.servants'
    _description = 'Servants'

    name=fields.Char()
    user_id=fields.Many2one('res.users')

class Occasions(models.Model):
    _name ='bless.occasions'
    _description = 'Occasions'
    name=fields.Char()


class Units(models.Model):
    _name='bless.units'
    _description='Units'
    name = fields.Char()

class FoodBeverage(models.Model):
    _name='bless.beverage'
    _description='Bless Food and Bevereage'
    name = fields.Char()
    unit_id=fields.Many2one('bless.units',string='Unit')
    price=fields.Float(string='Price')

class Concrete(models.Model):
    _name="bless.concrete"
    _description ='Bless Concrete'
    name = fields.Char()


