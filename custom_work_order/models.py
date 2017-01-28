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
    Status = fields.Selection(selection=[('pod','POD'),('halfpod','Half POD'),('cancelled','CANCELLED')],String='Status')

    state = fields.Selection(selection=[ ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("loading","Loading"),
            ("depart", "Depart"),
            ("arrive", "Arrive"),
            ("unloading","Unloading"),
            ("finish","Finish"),
            ("exception","Exception"),
            ("cancelled", "Cancelled")])

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
    def _action_cancel(self):
        self.ensure_one()
        self.write(self._prepare_cancel_data())

    @api.multi
    def _action_restart(self):
        self.ensure_one()
        self.write(self._prepare_restart_data())

    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'fleet.work.order') or '/'
        return super(FleetWorkOrder, self).create(vals)

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

    Arrival = fields.Date('Arrival')
    ArrivalPlan = fields.Date('Arrival Plan')
    StartUnloading = fields.Date('Start Unloading')
    FinishUnloading = fields.Date('Finish Unloading')
    FinishUnloadingDoc = fields.Date('Finish Unloading Doc')
    DepartFromDestination = fields.Date('Depart From Dest')

