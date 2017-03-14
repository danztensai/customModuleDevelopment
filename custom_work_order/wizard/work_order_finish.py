# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields


class WorkOrderFinish(models.TransientModel):
    _name = "fleet.work.order.finish"
    _description = "Work Order Finish"

    date_finish = fields.Datetime(
        string="Date Finish",
        required=True,
        default=fields.Datetime.now(),
    )

    @api.multi
    def button_finish(self):
        self.ensure_one()
        self._finish()

    @api.multi
    def _finish(self):
        order_ids = self.env.context["active_ids"]
        order = self.env["fleet.work.order"].browse(order_ids)

        order._action_finish(date_finish=self.date_finish,
                             )
