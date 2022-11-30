# -*- coding: utf-8 -*-
from odoo import models, fields, api,  _

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Appointment'
    _order = "id desc"
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result
    
    def write(self, vals):
        res = super(HospitalAppointment, self).write(vals)
        print('Test function for write')
        return res
    
    def test_recordset(self):
        for rec in self:
            print("Odoo ORM: record set Operations")
            partners=self.env['res.partner'].search([])
            print("Partners-------------------",partners)
            print("Mapped Partners",partners.mapped('name'))
            print("Partners",partners.mapped('email'))
            print("Sorted Partners",partners.sorted(lambda o: o.write_date, reverse=True))
#            print("Filtered Partners",partners.filtered(lambda o: not o.customer))
    
    def _get_default_note(self):
        return "Subscirbe"
    
    def delete_lines(self):  
        for rec in self:
            rec.appointment_lines=[(5, 0, 0)]
    
    def action_confirm(self):  
        for rec in self:
            rec.state='confirm'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Appointment Confirmed... Thanks You',
                    'type': 'rainbow_man',
                }
            }
            
        
    def action_done(self):  
        for rec in self:
            rec.state='done'
            
    @api.onchange('partner_id')
    def onchnage_partner_id(self):  
        for rec in self:
            return {'domain': {'order_id': [('partner_id', '=', self.partner_id.id)]}}
        
    @api.model
    def default_get(self, fields):
        res = super(HospitalAppointment, self).default_get(fields)
        appointment_lines = []
        product_rec = self.env['product.product'].search([])
        for pro in product_rec:
            line = (0, 0, {
                'product_id': pro.id,
                'product_qty': 1,
            })
            appointment_lines.append(line)
        res.update({
            'appointment_lines': appointment_lines,
            'patient_id': 1,
            'notes': 'Like and Subscribe our channel To Get Notified'
        })
        return res

        
    
    name = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True,  
                       index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')    
    doctor_ids = fields.Many2many('hospital.doctor','hospital_patient_rel','appointment_id','doctor_id_rec', string='Doctors')    
    patient_age = fields.Integer('Age',related='patient_id.patient_age')
    notes = fields.Text(string="Registration Note", default=_get_default_note)
    doctor_note = fields.Text(string="Note")
    pharmacy_note = fields.Text(string="Note")
    appointment_date = fields.Date(string='Date')
    appointment_date_end = fields.Date(string='End Date')    
    appointment_datetime = fields.Datetime(string="DateTime")
    appointment_lines = fields.One2many('hospital.appointment.lines', 'appointment_id', string='Appointment Lines')
    partner_id = fields.Many2one('res.partner', string='Customer')
    order_id = fields.Many2one('sale.order', string='Sale Order')
    product_id = fields.Many2one('product.template', string='Product Template')
    amount = fields.Float(string="Total Amount")
    state = fields.Selection([
        ('draft', "Draft"),
        ('confirm', "Confirm"),
        ('done', "Done"),
        ('cancel', "Cancelled"),
    ], default='draft', string='State', readonly=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            lines=[(5,0,0)]
#            lines=[]
            print("self.product_id.product_variant_ids",self.product_id.product_variant_ids)
            for line in self.product_id.product_variant_ids:
                vals={
                    'product_id':line.id,
                    'product_qty':5
                }
                lines.append((0,0,vals))
            print("Lines---",lines)    
            rec.appointment_lines=lines
            
class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointment Lines'

    product_id = fields.Many2one('product.product', string='Medicine')
    product_qty = fields.Integer(string="Quantity")
    sequence = fields.Integer(string="Sequence")
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment ID')

