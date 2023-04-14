from odoo.tools import float_is_zero, html_keep_url, is_html_empty
from odoo import models, api
from odoo.addons.payment import utils as payment_utils



class EstateProperty(models.Model):
    _inherit = 'estate.property'


    def action_sold(self):
        res = super(EstateProperty, self).action_sold()
        for record in self:
            partner_id = record.buyer_id.id
            move_type = 'out_invoice'
            move_vals = {
                'partner_id': partner_id,
                'move_type': move_type}
            new_move = self.env['account.move'].sudo().create(move_vals)
            price = record.selling_price
            quantity = 1
            admin_fee = 100.00
            invoice_lines = [
                {
                    'name': 'Selling Price',
                    'quantity': quantity,
                    'price_unit': price * 0.06,
                    'move_id': new_move.id,
                },
                {
                    'name': 'Administrative Fees',
                    'quantity': quantity,
                    'price_unit': admin_fee,
                    'move_id': new_move.id,
                },
            ]
            self.env['account.move.line'].sudo().create(invoice_lines)
        return res


