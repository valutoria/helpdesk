# Copyright 2026 Valutoria
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    @api.onchange("sale_order_ids", "partner_id")
    def _onchange_partner_sale_order(self):
        if not self.partner_id and self.sale_order_ids:
            self.partner_id = self.sale_order_ids[0].partner_id
        if self.partner_id and self.sale_order_ids:
            self.sale_order_ids = self.sale_order_ids.filtered(
                lambda order: order.partner_id == self.partner_id
            )
