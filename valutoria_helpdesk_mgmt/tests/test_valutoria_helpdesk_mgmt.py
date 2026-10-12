# Copyright 2026 Valutoria
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon
from odoo.tests.common import Form


class TestValutoriaHelpdeskMgmt(BaseCommon):
    _test_user_groups = ()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create({"name": "Product"})
        cls.partner_x = cls.env["res.partner"].create({"name": "Partner X"})
        cls.partner_y = cls.env["res.partner"].create({"name": "Partner Y"})
        cls.order_x = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner_x.id,
                "order_line": [
                    (0, 0, {"product_id": cls.product.id, "product_uom_qty": 1}),
                ],
            }
        )
        cls.order_y = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner_y.id,
                "order_line": [
                    (0, 0, {"product_id": cls.product.id, "product_uom_qty": 1}),
                ],
            }
        )

    def test_sale_order_auto_fills_partner(self):
        form = Form(self.env["helpdesk.ticket"])
        form.name = "SO First"
        form.description = "<p>Test</p>"
        form.sale_order_ids.add(self.order_x)
        ticket = form.save()
        self.assertEqual(ticket.partner_id, self.partner_x)

    def test_partner_change_drops_other_partners_orders(self):
        form = Form(self.env["helpdesk.ticket"])
        form.name = "Partner First"
        form.description = "<p>Test</p>"
        form.partner_id = self.partner_y
        form.sale_order_ids.add(self.order_y)
        form.sale_order_ids.add(self.order_x)
        ticket = form.save()
        self.assertEqual(ticket.sale_order_ids, self.order_y)

    def test_switching_partner_clears_mismatched_orders(self):
        form = Form(self.env["helpdesk.ticket"])
        form.name = "Switch Partner"
        form.description = "<p>Test</p>"
        form.partner_id = self.partner_x
        form.sale_order_ids.add(self.order_x)
        form.partner_id = self.partner_y
        ticket = form.save()
        self.assertFalse(ticket.sale_order_ids)
