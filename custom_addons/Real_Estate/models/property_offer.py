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

    price = fields.Float(string='Price')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)
    property_id = fields.Many2one('real_estate.order', string='Property', required=True)
    best_offer = fields.Float(compute='_compute_best_offer', string='Best Offer', optional='hide')
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Dead line', compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    create_date = fields.Datetime(default=fields.Datetime.now)

    @api.depends("price")
    def _compute_best_offer(self):
        for rec in self:
            rec.best_offer = rec.price

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = offer.create_date + timedelta(days=offer.validity)

    # @api.depends('date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (fields.Datetime.to_datetime(record.date_deadline) - record.create_date).days

    def action_refuse(self):
        for rec in self:
            rec.status == "refused"

    def action_accept(self):
        for rec in self:
            rec.status == "accepted"







