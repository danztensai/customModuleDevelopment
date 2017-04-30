# -*- coding: utf-8 -*-
import logging
import datetime
from random import randint
from openerp import models, fields, api

class add_new_field_res_partner(models.Model):
	_inherit = 'res.partner'
	customerCode = fields.Char('Customer Code')  
	customerAccountName = fields.Char('Customer Accout Name')

class modifyProductCategry(models.Model):
	_inherit = 'product.category'
	complete_name = fields.Char('Category Name',store=True,select_level=1)

