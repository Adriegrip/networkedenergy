# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

DIVISION = {
    'Year': 12,
    'Half Year': 6,
    'Quarter': 3,
    'Month': 1,
}


class Lead(models.Model):
    _inherit = 'crm.lead'

    product_hardware = fields.One2many('product.hardware', 'crm_lead', string='Delivery date')


class HardwareDelivery(models.Model):
    _name = 'hardware.delivery'

    start_delivery_date = fields.Date(string="Start Date")
    end_delivery_date = fields.Date(string="End Date")
    period = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly')
    ], string="Period")
    number_of_deliveries = fields.Integer(string="Number of Deliveries")
    delivery_product_hardware = fields.Many2one('product.hardware')


class ProductHardware(models.Model):
    _name = 'product.hardware'

    product_id = fields.Many2one('product.template', string='Product Hardware')
    product_group = fields.Selection(related='product_id.x_studio_product_group',
                                     store=True, readonly=True, string='Product Group')
    product_family = fields.Char(related='product_id.x_studio_product_family',
                                 store=True, readonly=True, string='Product Family')
    sales_price = fields.Float(related='product_id.list_price',
                               store=True, readonly=True, string='Sale Price')
    cost_price = fields.Float(related='product_id.standard_price',
                              store=True, readonly=True, string='Cost Price')
    amount = fields.Integer('Amount')
    total = fields.Integer('Total', compute='_compute_total')
    start_delivery_date = fields.Date(string="Start Date")
    end_delivery_date = fields.Date(string="End Date")
    period = fields.Selection([
        ('Month', 'Monthly'),
        ('Quarter', 'Quarterly'),
        ('Year', 'Yearly')
    ], string="Period")
    number_of_deliveries = fields.Integer(string="Number of deliveries")
    hardware_delivery_date = fields.One2many('hardware.delivery', 'delivery_product_hardware', string='Delivery date')
    crm_lead = fields.Many2one('crm.lead')

    @api.onchange('amount')
    def _compute_total(self):
        for rec in self:
            if rec.sales_price and rec.amount:
                rec.total = rec.sales_price * rec.amount

    def create_hardware_delivery_date(self):
        product_hardware = self.env['hardware.delivery']
        for rec in self:
            start_date = rec.start_delivery_date
            end_date = start_date + relativedelta(months=DIVISION[rec.period], days=-1)
            budget_lines = int(rec.number_of_deliveries)

            for line in range(budget_lines):
                product_hardware.create({
                    'delivery_product_hardware': rec.id,
                    'start_delivery_date': start_date,
                    'end_delivery_date': end_date,
                })
                start_date = start_date + relativedelta(months=DIVISION[rec.period])
                end_date = end_date + relativedelta(months=DIVISION[rec.period])
