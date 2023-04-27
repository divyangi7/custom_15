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


class realestateorder(models.Model):
    _name = "real_estate.order"
    _inherit = "mail.thread", "mail.activity.mixin", "mail.composer.mixin"
    _description = "Real Estate Order"
    _order = "id desc"

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description', required=False)
    postcode = fields.Char(string='Postcode', required=False)
    date_availability = fields.Date(string='Available Date', optional='hide')
    expected_price = fields.Float(string='Expected Price', store=True, required=False)
    selling_price = fields.Float(string='Selling Price', store=True)
    bedrooms = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], copy=False, index=True, tracking=3, default='draft')
    property_type_id = fields.Many2one('property.type', string='Property Type')
    other_info = fields.Text(string='Other Info', required=False)
    salesman = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer')
    # salesman_id = fields.Many2one('res.users', string='Salesman', default='Mitchell Admin')
    # buyer_id = fields.Many2one('res.partner', string='Buyer')
    tag_id = fields.Many2many('property.tag', string='Property Tag')
    offer_ids = fields.One2many('property.offer', 'property_id', string='Offers')
    total = fields.Float(compute='_compute_total', string='Total Area')
    best_offer = fields.Float(compute='_compute_best_offer_price', string='Best Offer', optional='hide')
    state = fields.Selection([
        ('new', 'New'),
        ('offer', 'Offer'),
        ('received', 'Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], copy=False, string='Status', default='new')
    # active = fields.Boolean(string="Active", default=False)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.user.company_id,
        required=True)
    email_id = fields.Char(string="Email")


    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.depends("garden_area", "living_area")
    def _compute_total(self):
        for rec in self:
            rec.total = 0
            rec.total = rec.garden_area + rec.living_area

    @api.depends("offer_ids.price")
    def _compute_best_offer_price(self):
        for rec in self:
            rec.best_offer = 0
            rec.best_offer = max(rec.offer_ids.mapped("price")) if rec.offer_ids else 0.0

    def action_cancel(self):
        if self.state != "sold":
            self.state = "canceled"
        else:
            raise UserError("A Sold Properties cannot be Canceled!!!")


    def action_sold(self):
        if self.state != "canceled":
            self.state = "sold"
        else:
            raise UserError("A canceled property cannot be sold!!!")


    @api.constrains('selling_price')
    def _check_selling_price(self):
        for rec in self:
            if rec.selling_price < rec.expected_price * 0.9:
                raise ValidationError(_("The selling price cannot be lower than 90% of the expected price."))


    @api.ondelete(at_uninstall=False)
    def _unlink_open(self):
        for rec in self:
            if rec.state not in ['new', 'canceled']:
                raise UserError(_("Only new and canceled properties can be deleted."))


    @api.model
    def _property_cron_job(self):
        pass

    def action_mail_send(self):
        # ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        # self.ensure_one()
        # template_id = self._find_mail_template()
        # lang = self.env.context.get('lang')
        # template = self.env['mail.template'].browse(template_id)
        # if template.lang:
        #     lang = template._render_lang(self.ids)[self.id]
        # ctx = {
        #     'default_model': 'real_estate.order',
        #     'default_res_id': self.ids[0],
        #     'default_use_template': bool(template_id),
        #     'default_template_id': template_id,
        #     'default_composition_mode': 'comment',
        #     'mark_so_as_sent': True,
        #     'custom_layout': "mail.mail_notification_paynow",
        #     'proforma': self.env.context.get('proforma', False),
        #     'force_email': True,
        #     'model_description': self.with_context(lang=lang).type_name,
        # }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            # 'context': ctx,
        }





     # name_search method


    # @api.model
    # def name_search(self, name='', args=None, operator='ilike', limit=100):
    #     if args in self:
    #         args = []
    #         domain = args + ['|', ('property_type_id', operator, name), ('tag_id', operator, name)]
    #         return super(realestateorder, self).search(domain, limit=limit).name_get()

    def action_send_by_mail(self):
        template = self.env.ref('real_estate.email_template_real_estate')
        for rec in self:
            template.send_mail(rec.id)

        # name_get_method


    # @api.multi
    # def name_get(self):
    #     return [(rec.id, "%s:%s" % (rec.name, rec.postcode)) for rec in self]





