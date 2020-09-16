from odoo import models

class PatientCardXLS(models.AbstractModel):
    _name = 'report.hospital_patient.report_patient_card_xls'
    _inherit = 'report.odoo_report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        print("lines", lines, data)
        # One sheet by partner
        for line in lines:   
            report_name = line.patient_name
            print('report_name',report_name)
            format1=workbook.add_format({'font_size':14, 'align':'vcenter', 'bold': True})
            format2=workbook.add_format({'font_size':10, 'align':'vcenter'})
            sheet = workbook.add_worksheet(report_name[:31])
            
            sheet.right_to_left()
            
            sheet.set_column(2, 2, 30)    
            sheet.set_column(3, 3, 50)
            sheet.write(2, 2, 'Name', format1)
            sheet.write(2, 3, line.patient_name, format2)
            sheet.write(3, 2, 'Age', format1)
            sheet.write(3, 3, line.patient_age, format2)


