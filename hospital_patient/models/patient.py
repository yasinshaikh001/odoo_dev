# -*- coding: utf-8 -*-
from odoo import models, fields, api,  _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def create(self, vals_list):
        res = super(ResPartner, self).create(vals_list)
        print('Yes Working')
        return res
    
class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    
    patient_name = fields.Char(string="Patient Name")
    
    def action_confirm(self):
        print("Hello there!")
        res = super(SaleOrderInherit, self).action_confirm()
        return res
    
class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Selection(selection_add=[('om', 'Odoo Mates'), ('odoodev', 'Odoo Dev')])
    


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Record'
    _rec_name = 'patient_name'
    
    def action_patients(self):
        print("Helooooooooooooooooooooo Server Action")
        return {
            'name': _('Patient Server Action'),
            'domain': [],
            'res_model': 'hospital.patient',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
    
    def print_report(self):
        return self.env.ref('hospital_patient.action_report_hospital_patient').report_action(self)
        
    def print_report_excel(self):
        return self.env.ref('hospital_patient.action_report_hospital_patient_xlx').report_action(self)
        
    
    @api.model
    def test_cron_job(self):
        print("AAAAAAAAAAAAAAAAAAAAAAAAA")
        for rec in self:
            print("Test Cron Job Executed for",rec.patient_name)
    
    def name_get(self):
        res=[]
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.name_seq, rec.patient_name)))
        return res    
    
    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValidationError(_('The must be greater than 5'))
    
    
    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age:
                if rec.patient_age < 18:
                    rec.age_group='minor'
                else:    
                    rec.age_group='major'
                    
    def open_patient_appointment(self):    
        return {
            'name': _('Appointments'),
            'domain': [('patient_id', '=',self.id)],
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
        
    def get_appointment_count(self):    
        count=self.env['hospital.appointment'].search_count([('patient_id', '=',self.id)])
        self.appointment_count=count
        
        
    @api.onchange("doctor_id")    
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_id:
                rec.doctor_gender=rec.doctor_id.gender

    def action_send_card(self):
        # sending the patient report to patient via email
        template_id = self.env.ref('hospital_patient.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        
    @api.depends('patient_name')
    def _compute_upper_name(self):
        for rec in self:
            rec.patient_name_upper = rec.patient_name.upper() if rec.patient_name else False
    
    def _inverse_upper_name(self):
        for rec in self:
            rec.patient_name = rec.patient_name_upper.lower() if rec.patient_name_upper else False
            
        

    patient_name = fields.Char(string="Name", required=True,track_visibility = 'always')
    patient_age = fields.Integer('Age',track_visibility = 'always', group_operator=False)
    patient_age2 = fields.Float(string="Age2")    
    notes = fields.Text(string="Notes")
    image = fields.Binary(string="Image", attachment=True)
    name = fields.Char(string='Test')
    name_seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,  
                           index=True, default=lambda self: _('New'))
    gender = fields.Selection([
            ('male', 'Male'),
            ('fe_male', 'Female'),
            ], string="Gender" ,default='male')
    age_group = fields.Selection([
            ('major', 'Major'),
            ('minor', 'Minor'),
            ], string="Age Group" ,compute='set_age_group', store=True)
    appointment_count = fields.Integer(string='Appointment',compute='get_appointment_count')            
    active = fields.Boolean('Active', default=True)
    
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    user_id = fields.Many2one('res.users', string="PRO")
    doctor_gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], string="Doctor Gender")

    email_id = fields.Char(string="Email")
    user_id = fields.Many2one('res.users', string="PRO")
    patient_name_upper = fields.Char(compute='_compute_upper_name', inverse='_inverse_upper_name')    

            
                               
                           
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result
                           
    
    

