# Copyright 2026 Valutoria
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestHelpdeskProducts(BaseCommon):
    _test_user_groups = ()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_a = cls.env["product.product"].create({"name": "Product A"})
        cls.product_b = cls.env["product.product"].create({"name": "Product B"})
        cls.product_c = cls.env["product.product"].create({"name": "Product C"})
        cls.partner = cls.env["res.partner"].create({"name": "SO Partner"})
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    (0, 0, {"product_id": cls.product_a.id, "product_uom_qty": 1}),
                    (0, 0, {"product_id": cls.product_b.id, "product_uom_qty": 2}),
                ],
            }
        )
        cls.ticket = cls.env["helpdesk.ticket"].create(
            {
                "name": "Test Ticket",
                "description": "<p>Test</p>",
                "sale_order_ids": [(6, 0, cls.order.ids)],
            }
        )

    def test_so_product_ids_gathers_order_line_products(self):
        self.assertEqual(self.ticket.so_product_ids, self.product_a + self.product_b)

    def test_so_product_ids_empty_without_sale_orders(self):
        ticket = self.env["helpdesk.ticket"].create(
            {"name": "No SO Ticket", "description": "<p>Test</p>"}
        )
        self.assertFalse(ticket.so_product_ids)

    def test_product_ids_stores_selected_products(self):
        self.ticket.product_ids = [(6, 0, (self.product_a + self.product_c).ids)]
        self.assertEqual(self.ticket.product_ids, self.product_a + self.product_c)
