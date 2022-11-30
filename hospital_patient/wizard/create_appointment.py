# -*- coding: utf-8 -*-

from odoo import api, fields, models


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    patient_id = fields.Many2one('hospital.patient', string='patient')
    appointment_date = fields.Date(string='Appointment Date')
    
    def print_report(self):
        print('self.read()[0]',self.read()[0])
        data={
            'model':'create.appointment',
            'form':self.read()[0]
        }
#        if data['form']['patient_id']:
#            selected_patient=data['form']['patient_id'][0]
#            appointments=self.env['hospital.appointment'].search([('patient_id','=', selected_patient)])
#        else:
#            appointments=self.env['hospital.appointment'].search([])
#        print('appointments----',appointments)
#        appointments_list=[]
#        for app in appointments:
#            vals={
#                'name':app.name,
#                'notes':app.notes,
#                'appointment_date':app.appointment_date
#                
#            }
#            appointments_list.append(vals)
#        data['appointments']=appointments_list
        return self.env.ref('hospital_patient.report_appointment').with_context(landscape=True).report_action(self,data=data)
    
    def create_appointment(self):
        vals={
        'patient_id':self.patient_id.id,
        'appointment_date':self.appointment_date,
        'notes': 'Created From The Wizard/Code'
        }
        self.patient_id.message_post(body="Appointment Created Successfully", subject="Appointment Creation")
        new_appointment=self.env['hospital.appointment'].create(vals)
        print('new_appointment',new_appointment)
        print('new_appointment.id',new_appointment.id)
        context = dict(self.env.context)
        context['form_view_initial_mode'] = 'edit'
        
        return {'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'hospital.appointment',
                'res_id': new_appointment.id,
                'context': context
                }
        
        
    def get_data(self):        
        print("Get Data")
        appointments=self.env['hospital.appointment'].search([('patient_id','=', 8)])
        appointments_count=self.env['hospital.appointment'].search_count([])
        print("Appointment Data",appointments)
        print("appointments_count",appointments_count)
        for rec in appointments:
            print('Name', rec.name)
        
        patients=self.env['hospital.patient'].search([])
        patients_count=self.env['hospital.patient'].search_count([])
        print("patients_count",patients_count)
        for rec in patients:
            print('patient name',rec.patient_name)
        return{
            "type":"ir.actions.do_nothing"
    }    


    def delete_patient(self):
        for rec in  self:
            print("rec vv",rec.patient_id)
            rec.patient_id.unlink()