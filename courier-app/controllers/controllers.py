# -*- coding: utf-8 -*-
from odoo import http
from odoo import models, fields, api, _
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)
# class Courier-app(http.Controller):
#     @http.route('/courier-app/courier-app/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/courier-app/courier-app/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('courier-app.listing', {
#             'root': '/courier-app/courier-app',
#             'objects': http.request.env['courier-app.courier-app'].search([]),
#         })

#     @http.route('/courier-app/courier-app/objects/<model("courier-app.courier-app"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('courier-app.object', {
#             'object': obj
#         })

class orders_tracking(http.Controller):
    @http.route('/orders/tracking', type='http', auth='public', website=True)
    def show_orders_tracking_webpage(self, **kw):
        return http.request.render('courier-app.order_track', {})


class vehicle_order_tracking(http.Controller):
    @http.route(['/orders/vehicle/tracking'], methods=['GET', 'POST'], type='http', auth='public', website=True)
    def show_orders_tracking_webpage(self, **kw):
        return http.request.render('courier-app.track_vehicle_website', {})

class order_status(http.Controller):
    @http.route(['/orders/tracking/submit_order_tracking'], type='http', methods=['GET', 'POST'],auth='public', website=True)

    def submit_order_tracking_method(self, **post):
        order_number = post['order_number']
        #_logger.debug('post order_number! "%s"' % (order_number))

        if order_number is not None and order_number.isdigit():
            sale_model = http.request.env['sale.order'].sudo().search([('name','=',order_number)])
            driver_name = http.request.env['res.users'].sudo().search([('id', '=', int(sale_model[0]['x_sale_order_driver_name']))])
            # return http.request.render('sale_extend_addon.order_tracking_status', {
            # order_num:sale_model[0]['name'],
            # order_courier_status: sale_model[0]['x_Sale_Order_In_Transit_State'],
            # order_customer_status: sale_model[0]['x_Sale_Order_Scheduled_State'],
            # order_courier_delivery_status: sale_model[0]['x_Sale_Order_Delivered_State'],
            # order_expected_delivery_date: sale_model[0]['x_Call_Center_Date'],
            # order_expected_delivery_time: sale_model[0]['x_Call_Center_Schedule_Time'],
            # })
            return http.request.render('courier-app.order_tracking_status', {
                'order': sale_model,
                'driver':driver_name
            })