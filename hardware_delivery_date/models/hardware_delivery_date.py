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


class HardwareDelivery(models.Model):
    _name = 'hardware.delivery'

    start_delivery_date = fields.Date(string="Start Date")
    end_delivery_date = fields.Date(string="End Date")
    period = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly')
    ], string="Period")
    number_of_deliveries = fields.Integer(string="End Date")
    product_hardware = fields.Many2one('x_producthardware')

#
class Lead(models.Model):
    _inherit = 'x_producthardware'

    hardware_delivery_date = fields.One2many('hardware.delivery', 'product_hardware', string='Delivery date')

    def create_hardware_delivery_date(self):
        product_hardware = self.env['hardware.delivery']
        for rec in self:
            start_date = rec.start_delivery_date
            end_date = start_date + relativedelta(months=DIVISION[rec.period], days=-1)
            expire_date = rec.date
            # num_months = (expire_date.year - start_date.year) * 12 + (expire_date.month - start_date.month)
            budget_lines = int(rec.number_of_deliveries / DIVISION[rec.period])

            for line in range(budget_lines):
                product_hardware.create({
                    'product_hardware': rec.id,
                    'start_delivery_date': start_date,
                    'end_delivery_date': end_date,
                    'period': rec.period,
                    'number_of_deliveries': rec.number_of_deliveries
                })
                start_date = start_date + relativedelta(months=DIVISION[rec.period])
                end_date = end_date + relativedelta(months=DIVISION[rec.period])
