# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class PatientCardReport(models.AbstractModel):
    _name = 'report.hospital_patient.report_patient_card'
    _description = 'Patient Card Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("Hello There...........",docids)
        docs = self.env['hospital.patient'].browse(docids[0])
        print("docs------",docs)
        print("data------",data)
        appointments=self.env['hospital.appointment'].search([('patient_id', '=',docids[0])])
        print("appointments------",appointments)
        appointments_list=[]
        for app in appointments:
            vals = {
            'name':app.name,
            'notes':app.notes,
            'appointment_date':app.appointment_date,
            }
            appointments_list.append(vals)
            
        print("appointments List------",appointments_list)            
        return {
            'doc_model': 'hospital.patient',
            'data': data,
            'docs': docs,
            'appointments_list': appointments_list,
        }
