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

class propertytype(models.Model):
    _name = "property.type"
    _description = "Real Estate Property Type"
    _order = "name"

    name = fields.Char(string='name')
    # property_id = fields.One2many('real_estate.order', 'property_type_id', string='Properties')
    # offer_ids = fields.Many2many('property.offer', 'property_type_id')
    property_id = fields.One2many('real_estate.order', 'property_type_id', string='Properties')
    sequence = fields.Integer("Sequence", defualt=10)

