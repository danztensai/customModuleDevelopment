# -*- coding: utf-8 -*-
from openerp import models, fields, api

class add_new_field(models.Model):
   
    _inherit = 'fleet.work.order'
    
   
    sealNo = fields.Char ('Seal No')   
    orderDate = fields.Datetime('Order Date')
    LoadingPlan = fields.Datetime('Loading Plan')
    ArrivalPlan = fields.Datetime('Arrival Plan')
    SPM = fields.Datetime('SPM')
    StartLoading = fields.Datetime('Start Loading')
    FinishLoading = fields.Datetime('Finish Loading')
    LoadingDocFinish = fields.Datetime('Doc Finish')
    DispatchFromOrigin = fields.Datetime('Dispatch From Origin')
    ActualArrivalTime = fields.Datetime('Arrival at Destination')
    StartUnloading = fields.Datetime('Start Unloading')
    FinishUnloading = fields.Datetime('Finish Unloading')
    FinishDocLoading = fields.Datetime('Finish Doc Loading')
    DepartFromDestination = fields.Datetime('Depart From Destination')
    Status = fields.Selection(selection=[('pod','POD'),('halfpod','Half POD'),('cancelled','CANCELLED')],String='Status')
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        domain="[('customer','=',True)]",
        readonly=True,
        states={
            'draft': [('readonly', False)],
        },
    )

    attachment_ids = fields.Many2many('ir.attachment','fleet_work_order_attachment','fleet_work_order_id_attachment',string='Attachment')
    

    DestinationCode = fields.Char(related='partner_id.DestinationCode',string='Destination Code')
    vehicle_id = fields.Many2one(
        string="Vehicle",
        comodel_name="fleet.vehicle",
        required=False,
        readonly=True,
        states={
            'draft': [('readonly', False)],
            'confirmed': [('readonly', False)],
            'depart': [('required', True)],
        },
    )

    VolumeVehicles = fields.Integer('Volume Vehicles  m³',store=True)
    WeightVehicles = fields.Integer('Weight Vehicles  Kg',store=True)
    licensePlate = fields.Char('License Plate')

    Location = fields.Char(related='vehicle_id.Location',string='Current Location')
    WeightVehiclesRelated = fields.Integer(related='vehicle_id.WeightVehicles')
    VolumeVehiclesRelated = fields.Integer(related='vehicle_id.VolumeVehicles')
    co_driver_id = fields.Char('Co Driver');

    state = fields.Selection(selection=[ ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("loading","Loading"),
            ("depart", "Depart"),
            ("arrive", "Arrive"),
            ("unloading","Unloading"),
            ("finish","Finish"),
            ("exception","Exception"),
            ("cancelled", "Cancelled")])

    Image = fields.Binary("Image",help="Insert Attachment Here")

    NoDn = fields.Char('No DN')
    Customer = fields.Char('Customer')
    PicPhoneTop = fields.Char('PIC/ Phone')
    SealNo = fields.Char('Seal No')
    Date = fields.Datetime('Date')
    NoOrder = fields.Char('No Order')
    NoTruck = fields.Char('No Truck')
    Consignee = fields.Char('Consignee')
    DestinationDeliveryNote = fields.Char('Destination/Address')
    PicPhoneBot = fields.Char('Pic / Phone')
    itemList = fields.One2many(string="Item List",
        comodel_name="fleet.work.order.item",
        inverse_name="id")

    
    def on_change_weight(self,cr,user,ids,WeightVehicles,WeightVehiclesRelated,context=None):
        #Calculate the total
        res={}

        if WeightVehicles > WeightVehiclesRelated:
        
            res = {
               'warning': {'title': 'Error!', 'message': 'Something went wrong! Please check your data, Its Overweight \n \n Please Pick Another Vehicle '}
              }
        
        #Return the values to update it in the view.
        return res

    def on_change_volume(self,cr,user,ids,VolumeVehicles,VolumeVehiclesRelated,context=None):
        #Calculate the total
        res={}

        if VolumeVehicles > VolumeVehiclesRelated:
        
            res = {
               'warning': {'title': 'Error!', 'message': 'Something went wrong! Please check your data, Its over Capacity \n Please Pick Another Vehicle '}
              }
        
        #Return the values to update it in the view.
        return res


    @api.one
    def button_loading(self):
        self.write({'state':'loading'})

    @api.one
    def button_unloading(self):
        self.write({'state':'unloading'})

    @api.one
    def button_finish(self):
        self.write({'state':'finish'})

    @api.one
    def button_exception(self):
        self.write({'state':'exception'})

    @api.multi
    def button_confirm(self):
        for order in self:
            order._action_confirm()

    @api.multi
    def button_depart(self):
        for order in self:
            order._action_depart(fields.Datetime.now(),
                                 order.start_odometer)

    @api.multi
    def button_arrive(self):
        for order in self:
            order._action_arrive(fields.Datetime.now(),
                                 order.end_odometer)

    @api.multi
    def button_cancel(self):
        for order in self:
            order._action_cancel()

    @api.multi
    def button_restart(self):
        for order in self:
            order._action_restart()

    @api.constrains("state", "vehicle_id", "driver_id")
    def _check_vehicle_driver(self):
        if self.state == "depart":
            if not self.vehicle_id or \
                    not self.driver_id:
                raise except_orm(_("Warning!"), _(
                    "Vehicle and driver required"))

    @api.onchange("vehicle_id")
    def onchange_vehicle_id(self):
        self.driver_id = False
        if self.vehicle_id:
            self.driver_id = self.vehicle_id.driver_id

    @api.onchange('type_id')
    def onchange_type_id(self):
        self.vehicle_id = False
        self.driver_id = False
        self.co_driver_id = False
        if self.type_id:
            wo_type = self.type_id
            self.vehicle_id = wo_type.vehicle_id and \
                wo_type.vehicle_id.id or False
            self.driver_id = wo_type.driver_id and \
                wo_type.driver_id.id or False
            self.co_driver_id = wo_type.co_driver_id and \
                wo_type.co_driver_id.id or False
            self.start_location_id = wo_type.start_location_id and \
                wo_type.start_location_id.id or False
            self.end_location_id = wo_type.end_location_id and \
                wo_type.end_location_id.id or False
            self.distance = wo_type.distance

    @api.multi
    def _action_confirm(self):
        self.ensure_one()
        self.write(self._prepare_confirm_data())

    @api.multi
    def _action_depart(self,
                       date_depart=fields.Datetime.now(),
                       starting_odometer=0.0):
        self.ensure_one()

        self.write(self._prepare_depart_data(date_depart,
                                             starting_odometer))

    @api.multi
    def _action_arrive(self,
                       date_arrive=fields.Datetime.now(),
                       ending_odometer=0.0):
        self.ensure_one()
        self.write(self._prepare_arrive_data(date_arrive,
                                             ending_odometer))

    @api.multi
    def _action_restart(self):
        self.ensure_one()
        self.write(self._prepare_restart_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            'state': 'confirmed'
        }

    @api.multi
    def _prepare_depart_data(self, date_depart, starting_odometer):
        self.ensure_one()
        return {
            'state': 'depart',
            'real_date_depart': date_depart,
            'start_odometer': starting_odometer,
        }

    @api.multi
    def _prepare_arrive_data(self, date_arrive, ending_odometer):
        self.ensure_one()
        return {
            'state': 'arrive',
            'real_date_arrive': date_arrive,
            'end_odometer': ending_odometer,
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            'state': 'cancelled',
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            'state': 'draft',
        }

class add_new_field_multiroute(models.Model):

    _inherit = 'fleet.route'

    Arrival = fields.Datetime('Arrival')
    ArrivalPlan = fields.Datetime('Arrival Plan')
    StartUnloading = fields.Datetime('Start Unloading')
    FinishUnloading = fields.Datetime('Finish Unloading')
    FinishUnloadingDoc = fields.Datetime('Finish Unloading Doc')
    DepartFromDestination = fields.Datetime('Depart From Dest')

class add_new_field_vehicles(models.Model):

    _inherit ='fleet.vehicle'

    VolumeVehicles = fields.Integer('Max Volume Vehicles m³')
    WeightVehicles = fields.Integer('Max Weight Vehicles Kg')
    GPSLongtitudeLocation = fields.Float('Longtitude')
    GPSLatitudeLocation = fields.Float('Latitude')
    Location = fields.Char('Location')
    Quantity = fields.Char('Quaintity')

class add_new_field_customer(models.Model):

    _inherit ='res.partner'

    DestinationCode = fields.Char('Destination Code')

class fleet_work_order_note(models.Model):

    _name = 'fleet.work.order.item'

    itemName = fields.Char('Item')
    unit = fields.Char('Unit')
    qty = fields.Integer('Quantity')
    remark = fields.Char('Remark')
    

