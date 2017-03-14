# -*- coding: utf-8 -*-

from openerp import models, fields, api

class add_new_field_inherit(models.Model):
    #Inhertis the model product.template
    _inherit = 'sale.order.line'
    
    Destination = fields.Char(string='Destination')
    DeliveryOrder = fields.Char(string='Delivery Order')
    Vehicle_id = fields.Many2one('fleet.vehicle','Vehicle')
    DeliveryDate = fields.Date('Delivery Date')
    DeliveryNumber_id = fields.Many2one('fleet.work.order','Delivery Order Number')
    
    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
        ret = super(add_new_field_inherit, self)._prepare_order_line_invoice_line(cr, uid, line, account_id=False, context=context)
        if line.product_id: 
            if line.Destination:
                ret['Destination'] = line.Destination
            if line.DeliveryOrder:
                ret['DeliveryOrder'] = line.DeliveryOrder
           
                ret['Vehicle_id'] = line.Vehicle_id.id
            if line.DeliveryDate:
                ret['DeliveryDate'] = line.DeliveryDate
            
                ret['DeliveryNumber_id'] = line.DeliveryNumber_id.id
            

        return ret 

class add_new_field(models.Model):
    #Inhertis the model product.template
    _inherit = 'account.invoice.line'
    
    Destination = fields.Char(string='Destination')
    DeliveryOrder = fields.Char(string='Delivery Order')
    Vehicle_id = fields.Many2one('fleet.vehicle','Vehicle')
    DeliveryDate = fields.Date('Delivery Date')
    DeliveryNumber_id = fields.Many2one('fleet.work.order','Delivery Order Number')
