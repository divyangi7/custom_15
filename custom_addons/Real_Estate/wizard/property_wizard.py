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


class Propertywizard(models.TransientModel):
    _name = "property.wizard"
    _description = "Property Wizard"

    salesman = fields.Many2one('res.users', string='Salesman',default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer')



