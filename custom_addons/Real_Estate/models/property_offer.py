#-*- coding: utf-8 -*-
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
    validity_date = fields.Float(string='Validity (days)')
    dead_line = fields.Date(compute='_compute_dead_line', string='Dead line')


    @api.depends("price")
    def _compute_best_offer(self):
        for rec in self:
            rec.best_offer = rec.price

    @api.depends("dead_line","validity_date")
    def _compute_dead_line(self):
        for rec in self:
           if rec.validity_date and  rec.dead_line:
               date = self.dead_line -

