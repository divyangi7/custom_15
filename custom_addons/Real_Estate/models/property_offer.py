# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta

from itertools import groupby
import json

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty

from odoo.addons.payment import utils as payment_utils


class Propertyoffer(models.Model):
    _name = "property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string='Price')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)
    property_id = fields.Many2one('real_estate.order', string='Property', required=True)
    # best_offer = fields.Float(compute='_compute_best_offer', string='Best Offer', optional='hide')
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Dead line', compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    create_date = fields.Datetime(default=fields.Datetime.now)
    # propertytype = fields.Many2one("real.estate.properties", related='property_id.propertytype')




    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = offer.create_date + timedelta(days=offer.validity)

    # @api.depends('date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (fields.Datetime.to_datetime(record.date_deadline) - record.create_date).days

    def action_refuse(self):
        if self.status != 'accepted':
            self.status = 'refused'
            return True


    def action_accept(self):
        self.write({"status": "accepted"})
        self.property_id.write({
            "state": "offer_accepted",
            "selling_price": self.price,
            "buyer": self.partner_id})


    def write(self, vals):
        res = super().write(vals)
        self.property_id.state = "received"
        for rec in self:
            if rec.property_id.best_offer and rec.property_id.best_offer > rec.price:
                raise UserError(_("The offer must be higher"))
        return res






            # self.status = 'accepted'
            # property_id = self.property_id
            # property_id.write({'buyer_id': self.partner_id})
            # property_id.write({'selling_price': self.price})

    # def action_accept(self):
    #         self.status = 'accepted'
    #         self.property_id.selling_price = self.price
    #         self.property_id.buyer_id = self.partner_id

    # @api.onchange('status')
    # def onchange_status(self):
    #     if self.status == 'accepted':
    #         property_id = self.property_id
    #         property_id.buyer_id = self.partner_id
    #         property_id.selling_price = self.price














