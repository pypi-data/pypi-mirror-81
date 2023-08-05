# Copyright (C) 2019, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class FSMOrder(models.Model):
    _inherit = 'fsm.order'

    order_activity_ids = fields.One2many('fsm.activity', 'fsm_order_id',
                                         'Activites')

    @api.multi
    @api.onchange('template_id')
    def _onchange_template_id(self):
        res = super()._onchange_template_id()
        for rec in self:
            if rec.template_id:
                activity_list = []
                for temp_activity in rec.template_id.temp_activity_ids:
                    activity_list.append((0, 0,
                                          {'name': temp_activity.name,
                                           'required': temp_activity.required,
                                           'ref': temp_activity.ref,
                                           'state': temp_activity.state}))
                rec.order_activity_ids = activity_list
                rec.template_id.temp_activity_ids.write(
                    {'fsm_template_id': False})
        return res

    @api.multi
    def action_complete(self):
        res = super().action_complete()
        for activity_id in self.order_activity_ids:
            if activity_id.required and activity_id.state == 'todo':
                raise ValidationError(_(
                    "You must complete activity '%s' before \
                    completing this order.") % activity_id.name)
        for activity_id in self.activity_ids:
            activity_id.done = True
        return res
