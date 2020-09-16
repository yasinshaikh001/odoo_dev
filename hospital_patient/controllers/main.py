from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class AppointmentController(http.Controller):

    @http.route('/om_hospital/appointments', auth='user', type='json')
    def appointment_banner(self):
        return {
            'html': """
                    <div>
                        <link>
                        <center><h1><font color="red">Subscribe the channel.......!</font></h1></center>
                        <center>
                        <p><font color="blue"><a href="https://www.youtube.com/channel/UCVKlUZP7HAhdQgs-9iTJklQ/videos">
                            Get Notified Regarding All The Odoo Updates!</a></p>
                            </font></div></center> """
                                }


  