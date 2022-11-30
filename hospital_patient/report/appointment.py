# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AppointmentReport(models.AbstractModel):
    _name = 'report.hospital_patient.appointment_report'
    _description = 'Appointment Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("Hello There...........",docids)
        patient_name=""
        if data['form']['patient_id']:
            selected_patient=data['form']['patient_id'][0]
            appointments=self.env['hospital.appointment'].search([('patient_id','=', selected_patient)])
            patient_name=appointments.patient_id.patient_name
            print('patient_name----',appointments.patient_id.patient_name)             
        else:
            appointments=self.env['hospital.appointment'].search([])
        print('appointments----',appointments)
        
        return {
            'doc_model': 'hospital.patient',
            'appointments': appointments,
            'selected_patient':patient_name
        }
