# Copyright 2026 Valutoria
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    product_ids = fields.Many2many(
        comodel_name="product.product",
        relation="helpdesk_ticket_product_rel",
        column1="ticket_id",
        column2="product_id",
        string="Products",
    )
    so_product_ids = fields.Many2many(
        comodel_name="product.product",
        compute="_compute_so_product_ids",
        string="Sale Order Products",
    )

    @api.depends("sale_order_ids.order_line.product_id")
    def _compute_so_product_ids(self):
        for ticket in self:
            lines = ticket.sale_order_ids.order_line.filtered("product_id")
            ticket.so_product_ids = lines.mapped("product_id")
