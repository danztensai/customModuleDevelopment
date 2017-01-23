# -*- coding: utf-8 -*-

from openerp import models, fields, api

class add_new_field(models.Model):
   
    _inherit = 'fleet.work.order'
    
   
    LoadingPlan = fields.Date('Loading Plan')
    ArrivalPlan = fields.Date('Arrival Plan')
    SPM = fields.Date('SPM')
    StartLoading = fields.Date('Start Loading')
    FinishLoading = fields.Date('Finish Loading')
    LoadingDocFinish = fields.Date('Loading Doc Finish')
    DispatchFromOrigin = fields.Date('Dispatch From Origin')
    ActualArrivalTime = fields.Date('Actual Arrival Time')
    StartUnloading = fields.Date('Start Unloading')
    FinishUnloading = fields.Date('Finish Unloading')
    FinishDocLoading = fields.Date('Finish Doc Loading')
    DepartFromDestination = fields.Date('Depart From Destination')
    Status = fields.Char(string='Status')
    Remark = fields.Char(string='Remark')
    
