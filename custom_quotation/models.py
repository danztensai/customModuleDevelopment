# -*- coding: utf-8 -*-

from openerp import models, fields, api

class add_new_field(models.Model):
    #Inhertis the model product.template
    _inherit = 'sale.order.line'
    
    Destination = fields.Char(string='Destination')
    DeliveryOrder = fields.Char(string='Delivery Order')
    Vehicle = fields.Many2one('fleet.vehicle','Vehicle')
    DeliveryDate = fields.Date('Delivery Date')
    DeliveryNumber = fields.Many2one('fleet.work.order','Delivery Order Number')

class add_new_field(models.Model):
    #Inhertis the model product.template
    _inherit = 'account.invoice.line'
    
    Destination = fields.Char(string='Destination')
    DeliveryOrder = fields.Char(string='Delivery Order')
    Vehicle = fields.Many2one('fleet.vehicle','Vehicle')
    DeliveryDate = fields.Date('Delivery Date')
    DeliveryNumber = fields.Many2one('fleet.work.order','Delivery Order Number')
