# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields


class WorkOrderUnloading(models.TransientModel):
    _name = "fleet.work.order.unloading"
    _description = "Work Order Unloading"

    date_arrive = fields.Datetime(
        string="Date Arrive",
        required=True,
        default=fields.Datetime.now(),
    )
    
    @api.multi
    def button_unloading(self):
        self.ensure_one()
        self._arrive()

    @api.multi
    def _arrive(self):
        self.ensure_one()
        order_ids = self.env.context["active_ids"]
        order = self.env["fleet.work.order"].browse(order_ids)

        order._action_unloading(date_arrive=self.date_arrive)
