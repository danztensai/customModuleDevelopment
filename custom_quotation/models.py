# -*- coding: utf-8 -*-

from openerp import models, fields, api

class add_new_field(models.Model):
    #Inhertis the model product.template
    _inherit = 'sale.order.line'
    
    Destination = fields.Char(string='Destination')
    DeliveryOrder = fields.Char(string='Delivery Order')
    Vehicle = fields.Many2one('fleet.vehicle','Vehicle')

    
