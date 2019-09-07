# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

# _logger = logging.getLogger(__name__)

import logging
import odoo.addons.decimal_precision as dp
import datetime
import json

import base64

_logger = logging.getLogger(__name__)


class extend_sale_order(models.Model):
    _inherit = 'sale.order'

    # _logger.info('FYI: This is happening')

    @api.constrains('name')
    def _get_call(self):
        # self.cr.execute('select  "x_Company_Call_Script" from res_partner where id = 7')
        results = self.env['res.partner'].search([('id', '=', int(self.partner_id))])
        _logger.info('self.partner_id maged ! "%s"' % (str(self.partner_id)))
        _logger.info('results maged ! "%s"' % (str(results)))
        _logger.info('results[0][x_Company_Call_Script] maged ! "%s"' % (str(results[0]['x_Company_Call_Script'])))
        self.callScript = results[0]['x_Company_Call_Script']
        # self.callScript = 'Maged'

    callScript = fields.Text(string='Call Center Script', compute='_get_call', copy=False, required=False)

    first_call = fields.Boolean(string="1st Call", default=False)
    second_call = fields.Boolean(string="2nd Call", default=False)
    third_call = fields.Boolean(string="3rd Call", default=False)
    fourth_call = fields.Boolean(string="4th Call", default=False)

    x_sale_order_shipping_address = fields.Text(store=True, copy=True, string="Shipping Address",
                                                help="Shipping Address", track_visibility='onchange')
    x_Sale_Order_Customer_name = fields.Text(track_visibility='onchange', string="Customer Name", store=True, copy=True,
                                             help="Customer Name", index=True)
    x_Sale_Order_Cust_Comment = fields.Text(track_visibility='onchange', string="Customer Comment",
                                            help="Customer Comment", copy=True, store=True)
    x_Sale_Order_Cust_Prod = fields.Text(track_visibility='onchange', string="Customer Product", help="Customer Product", copy=True,
                                         store=True, index=True)
    x_cust_call_center_comment = fields.Text(track_visibility='onchange', string="Other Comment",
                                             help="Sale Order Other Comment", store=True, copy=True)
    x_call_center_comment = fields.Text(track_visibility='onchange', string="Call Center Comment",
                                        help="Call Center Comment", store=True, copy=True)
    # x_sale_order_driver_name = fields.Text(track_visibility='onchange',string="Driver Name",help="Driver Name",store=True,copy=True)

    x_sale_order_driver_name = fields.Many2one('res.users',
                                               domain="[('x_is_courier', '=', True)]",
                                               string='Driver Name', help="Driver Name", store=True, index=True,
                                               track_visibility='onchange')

    x_sale_order_picking_driver_name = fields.Many2one('res.users',
                                                       domain="[('x_is_courier', '=', True)]",
                                                       string='Picking Driver Name', help="Picking Driver Name",
                                                       store=True,
                                                       index=True, track_visibility='onchange')

    x_Sale_Order_COD = fields.Boolean(track_visibility='onchange', store=True, index=True, copy=True, string="COD",
                                      help="COD", default=False)

    reversed_order = fields.Boolean(track_visibility='onchange', store=True, index=True, copy=True,
                                    string="Reversed Order",
                                    help="Is Reversed Order", default=False)

    x_Sale_Order_COD_Done = fields.Boolean(track_visibility='onchange', store=True, index=True, copy=True,
                                           string="COD Recieved", help="COD Recieved", default=False)

    x_sale_order_schedule_confirmed = fields.Boolean(track_visibility='onchange', store=True, index=True,
                                                     string="Schedule Confirmation",
                                                     help="Sale Order Schedule Confirmation")

    x_Sale_Order_Phone_Number = fields.Char(track_visibility='onchange', string="Phone Number", help="Phone Number",
                                            index=True, store=True, copy=True)
    x_Sale_order_Mobile_No = fields.Char(track_visibility='onchange', string="Mobile Number", help="Mobile Number",
                                         store=True, copy=True, size=20, index=True)

    x_Sale_Order_In_Transit_State = fields.Selection([('InTransit', 'In Transit'), ('Picked', 'Picked'),
                                                      ('RecievedinWarehouse', 'Recieved in Warehouse'),
                                                      ('shelved', 'Shelved'),
                                                      ('readyForDispatch', 'Ready For Dispatch'),
                                                      ('dispatched', 'Dispatched')],
                                                     track_visibility='onchange', string="In Transit",
                                                     help="In Transit Sale Order Status", store=True, index=True,
                                                     default="InTransit")


    x_Call_Center_Schedule_Time = fields.Selection(
        [('09:00 To 13:00', '09:00 To 13:00'), ('10:00 To 14:00', '10:00 To 14:00'),
         ('11:00 To 15:00', '11:00 To 15:00'), ('12:00 To 16:00', '12:00 To 16:00'),
         ('13:00 To 17:00', '13:00 To 17:00')], track_visibility='onchange',
        string="Schedule Time", help="Schedule Time", store=True, index=True, copy=True)
    x_call_center_reason = fields.Selection(
                                                [('NotReached', 'Not Reached'), ('NotReachedMobileSwitchedOff', 'Not Reached / Mobile Switched Off'),
                                                 ('FollowUp', 'Follow Up'),
                                                 ('CustomerWillCallBack', 'Customer Will Call Back'),
                                                 ('OrderRefused', 'Order Refused'),
                                                 ('ScheduleConfirmed', 'Schedule Confirmed')],
                                                track_visibility='onchange', string="Call Reason", help="Call Center Reason", store=True, index=True, copy=True)
    x_Sale_Order_Scheduled_State = fields.Selection([('none', 'None'), ('NotScheduled', 'Not Scheduled'), ('Scheduled', 'Scheduled')],
                                                    track_visibility='onchange', string="Scheduled", help="Scheduled Sale Order State", store=True, index=True,
                                                    default="none")

    x_Sale_Order_First_Call_State = fields.Selection([('none', 'None'), ('firstCall', '1st Call'),('secondCall', '2nd Call'),
                                                      ('thirdCall', '3rd Call'), ('fourthCall', '4th Call')],
                                                     track_visibility='onchange', string="First Call",
                                                     help="First Call Sale Order State",
                                                     store=True, index=True, default="none")

    x_Sale_Order_First_OFD_State = fields.Selection([('none', 'None'), ('firstOfd', '1st OFD'), ('firstRto', '1st RTO'),
                                                     ('secondOfd', '2nd OFD'), ('onHold', 'On Hold'),
                                                     ('readyToDispatchToSender',
                                                      'Ready To Dispatch To Sender'),
                                                     ('inTransitBackToSender', 'In Transit Back To Sender'),
                                                     ('returnToSender', 'Return To Sender')],
                                                    track_visibility='onchange', string="OFD",
                                                    help="OFD Sale Order State", store=True, index=True, default="none")

    x_Sale_Order_Req_For_Cancel_State = fields.Selection([('none', 'None'), ('requestForCancel', 'Request For Cancel'), ('readyToDispatch', 'Ready To Dispatch'),
                                                          ('cancelOrderInTransit', 'Cancel Order In Transit'), ('cancelOrderReturned',
                                                                                                           'Cancel Order Returned')],
                                                    track_visibility='onchange', string="Request For Cancel",
                                                    help="Request For Cancel Sale Order State", store=True, index=True, default="none")

    x_Sale_Order_Delivered_State = fields.Selection([('none', 'None'),('delivered', 'Delivered'),('notDelivered', 'Not Delivered')],
                                                    track_visibility='onchange',
                                                    string="Delivered", help="Delivered Sale Order State", store=True,
                                                    index=True, default="none")

    x_Sale_Order_Cash = fields.Monetary(string="Cash On Delivery", store=True, index=True, copy=True,
                                        help="Cash On Delivery")

    order_number = fields.Integer(string="Order Number", store=True, index=True,
                                  help="Client Order Number")

    x_Call_Center_Date = fields.Date(string="Scheduled Date", help="Scheduled Date", store=True, index=True, copy=True)

    amount_vat_tax = fields.Monetary(string='Amount Including VAT', help="14% VAT", store=True, readonly=True,
                                     index=True,
                                     track_visibility='always')

    vat_tax = fields.Monetary(string='VAT', help="VAT Amount",
                              index=True, store=True, readonly=True,
                              track_visibility='always')

    cod_fees = fields.Monetary(string='COD Fees', help="COD Fees", store=True, readonly=True, index=True,
                               track_visibility='always')

    order_fees_discount_percentage = fields.Float(string='Order Discount %', help="Order Discount %",
                                                  digits_compute=dp.get_precision('order_fees_discount_percentage'),
                                                  default=0.0)

    cod_fees_discount_percentage = fields.Float(string='COD Fees Discount %',
                                                help="COD Fees Discount %",
                                                digits_compute=dp.get_precision('cod_fees_discount_percentage'),
                                                default=0.0)

    delivery_repriced = fields.Monetary(string="Delivery Fees Repriced", store=True, index=True, copy=True,
                                        help="Delivery Fees Repriced",defaults=0.0)

    tax_repriced = fields.Monetary(string="Tax Repriced", store=True, index=True, copy=True,
                                         help="Tax Repriced", defaults=0.0)

    #product_temp = fields.Many2one('product.product', string='Product Temp')

    img_attach = fields.Html('Image', compute="_get_img_html")

    img_QR = fields.Html('Image', compute="_get_qr_img_html")

    google_map_partner = fields.Char(string="Map", store=True, index=True)

    #product_id = fields.Many2one('product.template', related='order_line.product_id', string='Product', store=True,
                                 #index=True)

    product_id = fields.Many2one('product.template', string='City', domain=[('sale_ok', '=', True),('is_courier_zone','=',True)],
                                 change_default=True, ondelete='restrict', store=True, index=True)

    # call_script = fields.Text('Call Script', compute='_get_img_html' )

    # x_date_from = fields.function(lambda *a,**k:{}, method=True, type='date',string="Date from")

    # s_date_to = fields.function(lambda *a,**k:{}, method=True, type='date',string="Date to")

    def _get_img_html(self):
        for elem in self:
            img_url = '/report/barcode/?type=EAN13&value=%s&width=300&height=50' % self.name
            elem.img_attach = '<img src="%s"/>' % img_url
            # elem.cr.execute('select  "x_Company_Call_Script" from res_partner where id = 7')
            # result = cr.dictfetchall()
            # _logger.debug(result)
            # elem.call_script = result[0]['x_Company_Call_Script']

    def _get_qr_img_html(self):
        for elem in self:
            img_url = '/report/barcode/?type=QR&value=%s&width=300&height=300' % self.name
            elem.img_attach = '<img src="%s"/>' % img_url


    def action_tree_view(self):

        return {
            'type': 'ir.actions.act_window',
            'name': 'All Orders',
            'res_model': 'sale.order',
            'res_id': self.id,
            'view_id':self.env.ref('courier-app.crm_unassigned_call_center_sale_order', False).id,
            'view_type': 'form',
            'view_mode': 'tree',
            'domain':[('x_Sale_order_Mobile_No','=',self.x_Sale_order_Mobile_No)],
            'target': 'new',
        }

    @api.one
    def _create_cod_order(self):

        self.env['sale.order.line'].create({
            'product_id': 'Cash On Delivery Fees',
            'product_qty': 1,
            'product_uom': 'Unit(s)',
        })

        return True

    @api.model
    def create(self, values):
        # Override the original create function for the res.partner model
        #_logger.debug('self._uid maged ! "%s"' % (str(self._uid)))
        user = self.env['res.users'].browse(self._uid)
        #_logger.debug('user maged ! "%s"' % (str(user)))
        self_partner_id = user[0]['partner_id']
        #_logger.debug('self_partner_id maged ! "%s"' % (str(self_partner_id)))
        partner = self.env['res.partner'].browse(int(self_partner_id))
        #_logger.debug('partner maged ! "%s"' % (str(partner)))
        partner_id = int(partner.commercial_partner_id)
        #_logger.debug('partner_id maged ! "%s"' % (str(partner_id)))
        sales_person_partner = self.env['res.partner'].browse(partner_id)
        sales_person = int(sales_person_partner[0]['user_id'])
        #_logger.debug('sales_person maged ! "%s"' % (str(sales_person)))

        values.update({'partner_id': partner_id})
        #values.update({'user_id': sales_person})

        if values.get('x_Sale_Order_Cash') > 0:
            values.update({'x_Sale_Order_COD': True})

        record = super(extend_sale_order, self).create(values)

        # Change the values of a variable in this super function

        try:
            results = self.env['res.partner'].search([('id', '=', int(record['partner_id']))])
            x_cod_fees_discount = results[0]['cod_fees_discount']
            x_order_fees_discount = results[0]['order_fees_customer_discount']
            cod_results = self.env['product.template'].search([('name', '=', 'COD')])
            x_cod_fees = cod_results[0]['list_price']

            record['order_fees_discount_percentage'] = x_order_fees_discount
            record['cod_fees_discount_percentage'] = x_cod_fees_discount

            update_cod_fees = 0
            update_amount_vat_tax = 0
            update_vat_tax = 0
            update_amount_total = 0
            update_tax = 0
            update_delivery_fees = 0
            order_fees_amount = record['amount_total']
            update_tax = record['amount_tax']
            update_delivery_fees = record['amount_untaxed']

            if record['x_Sale_Order_COD'] == True:

                if x_cod_fees_discount < 0.0:
                    update_cod_fees = float(x_cod_fees) - float((x_cod_fees * x_cod_fees_discount) / 100.0)
                elif x_cod_fees_discount >= 0.0:
                    update_cod_fees = float(x_cod_fees) - float((x_cod_fees * x_cod_fees_discount) / 100.0)

                if x_order_fees_discount < 0.0:
                    order_fees_amount = float(order_fees_amount) - float(
                        (order_fees_amount * x_order_fees_discount) / 100.0)
                    update_tax = float(update_tax) - float(
                        (update_tax * x_order_fees_discount) / 100.0)
                    update_delivery_fees = float(update_delivery_fees) - float(
                        (update_delivery_fees * x_order_fees_discount) / 100.0)
                elif x_order_fees_discount >= 0.0:
                    order_fees_amount = float(order_fees_amount) - float(
                        (order_fees_amount * x_order_fees_discount) / 100.0)
                    update_tax = float(update_tax) - float(
                        (update_tax * x_order_fees_discount) / 100.0)
                    update_delivery_fees = float(update_delivery_fees) - float(
                        (update_delivery_fees * x_order_fees_discount) / 100.0)

                update_amount_vat_tax = 1.14 * (order_fees_amount + update_cod_fees)
                update_vat_tax = 0.14 * (order_fees_amount + update_cod_fees)
                record['total_cash'] = record['x_Sale_Order_Cash']
                update_amount_total = record['x_Sale_Order_Cash'] - float(update_amount_vat_tax)


            else:
                update_cod_fees = x_cod_fees
                update_amount_vat_tax = 1.14 * (record['amount_total'] + update_cod_fees)
                update_vat_tax = 0.14 * (record['amount_total'] + update_cod_fees)
                update_amount_total = record['x_Sale_Order_Cash'] - float(update_amount_vat_tax)
                record['total_cash'] = record['x_Sale_Order_Cash']

            record['cod_fees'] = update_cod_fees
            record['amount_vat_tax'] = update_amount_vat_tax
            record['vat_tax'] = update_vat_tax
            record['amount_total'] = update_amount_total
            record['tax_repriced'] = update_tax
            record['delivery_repriced'] = update_delivery_fees
            record['user_id'] = sales_person

        except Exception as e:
            raise Exception(str(e))

        # record['passed_override_write_function'] = True
        # print 'Passed this function. passed_override_write_function value: ' + str(
        # record['passed_override_write_function'])

        # Return the record so that the changes are applied and everything is stored.
        return record

    # def __compute_amount_all(self):
    # for record in self:

    # return True

    @api.one
    def write(self, vals):
        res = super(extend_sale_order, self).write(vals)
        sale_order = self.env['sale.order'].search([('id', '=', self.id)])
        # _logger.debug('x_Sale_Order_First_Call_State maged ! "%s"' % (str(self.id)))
        #sale = self.env['sale.order']
        #sale = sale.browse(self.id)
        #_logger.debug('x_Sale_Order_First_Call_State maged ! "%s"' % (str(self.id)))
        if sale_order[0]['x_sale_order_schedule_confirmed'] == True and str(
                sale_order[0]['x_Sale_Order_Scheduled_State']) != 'Scheduled':
            vals['x_Sale_Order_Scheduled_State'] = 'Scheduled'
            vals['state'] = 'sale'

        res = super(extend_sale_order, self).write(vals)

            #_logger.debug('x_Sale_Order_First_Call_State maged ! 1_1')

        #if str(sale_order[0]['x_Sale_Order_First_Call_State']) == 'none' and sale_order[0]['x_Sale_Order_In_Transit_State'] != 'InTransit':
            #vals['first_call'] = True
            #vals['second_call'] = False
            #vals['third_call'] = False
            #vals['fourth_call'] = False
            #vals['x_Sale_Order_First_Call_State'] = 'firstCall'

        #elif str(sale_order[0]['x_Sale_Order_First_Call_State']) == 'firstCall' and str(
            #sale_order[0]['x_Sale_Order_Scheduled_State']) == 'Scheduled':
            #vals['first_call'] = True
            #vals['second_call'] = True
            #vals['third_call'] = False
            #vals['fourth_call'] = False
            #vals['x_Sale_Order_First_Call_State'] = 'secondCall'

        #elif str(sale_order[0]['x_Sale_Order_First_Call_State']) == 'secondCall' and str(
            #sale_order[0]['x_Sale_Order_Scheduled_State']) == 'Scheduled':
            #vals['first_call'] = True
            #vals['second_call'] = True
            #vals['third_call'] = True
            #vals['fourth_call'] = False
            #vals['x_Sale_Order_First_Call_State'] = 'thirdCall'

        #elif str(sale_order[0]['x_Sale_Order_First_Call_State']) == 'thirdCall' and str(
            #sale_order[0]['x_Sale_Order_Scheduled_State']) == 'Scheduled':
            #vals['first_call'] = True
            #vals['second_call'] = True
            #vals['third_call'] = True
            #vals['fourth_call'] = True
            #vals['x_Sale_Order_First_Call_State'] = 'fourthCall'

        #res = super(extend_sale_order, self).write(vals)

        return res

    total_cash = fields.Float(string="Total")

    def sale_order_cash_on_delivery_OnChange(self, cr, uid, ids, x_Sale_Order_Cash):
        total = self.amount_total + x_Sale_Order_Cash
        res = {
            'value': {
                # This sets the total price on the field standard_price.
                'total_cash': total
            }
        }
        # Return the values to update it in the view.
        return res

    def first_call_action(self):
        #sale_order = self.env['sale.order'].search([('id', '=', self.id)])
        if str(self.x_Sale_Order_First_Call_State) == 'none':
            self.first_call = True
            self.second_call = False
            self.third_call = False
            self.fourth_call = False
            self.x_Sale_Order_First_Call_State = 'firstCall'

    def second_call_action(self):
        #sale_order = self.env['sale.order'].search([('id', '=', self.id)])
        if str(self.x_Sale_Order_First_Call_State) == 'firstCall' and self.x_Sale_Order_Scheduled_State == 'Scheduled':
            self.first_call = True
            self.second_call = True
            self.third_call = False
            self.fourth_call = False
            self.x_Sale_Order_First_Call_State = 'secondCall'

    def third_call_action(self):
        #sale_order = self.env['sale.order'].search([('id', '=', self.id)])
        if str(self.x_Sale_Order_First_Call_State) == 'secondCall' and self.x_Sale_Order_Scheduled_State == 'Scheduled':
            self.first_call = True
            self.second_call = True
            self.third_call = True
            self.fourth_call = False
            self.x_Sale_Order_First_Call_State = 'thirdCall'

    def fourth_call_action(self):
        #sale_order = self.env['sale.order'].search([('id', '=', self.id)])
        if str(self.x_Sale_Order_First_Call_State) == 'thirdCall' and self.x_Sale_Order_Scheduled_State == 'Scheduled':
            self.first_call = True
            self.second_call = True
            self.third_call = True
            self.fourth_call = True
            self.x_Sale_Order_First_Call_State = 'fourthCall'

    @api.onchange('x_Sale_Order_COD')
    def sale_order_COD_OnChange(self):
        for elem in self:
            if elem.x_Sale_Order_COD == False:
                elem.x_Sale_Order_Cash = 0

    # @api.onchange('x_sale_order_schedule_confirmed')
    @api.one
    def sale_order_call_center_confirmation(self):
        # for rec in self.browse(cr, uid, ids, context=context):
        # if self.x_sale_order_schedule_confirmed:
        # sale_order = self.pool.get('sale.order').browse(cr, uid, rec.id, context=context)
        # sale_order_module = self.pool.get('sale.order')
        # values = {'x_Sale_Order_Scheduled_State': 'Scheduled'}
        # sale_order_module.write(cr, sale_order, values)
        if self.x_sale_order_schedule_confirmed and self.x_Sale_Order_Scheduled_State != 'Scheduled':
            sale_order = self.env['sale.order']
            sale_order = sale_order.browse(self.id)
            sale_order.x_Sale_Order_Scheduled_State = 'Scheduled'
            sale_order.state = 'sale'

        if self.x_Sale_Order_First_Call_State == 'None':
            sale_order = self.env['sale.order']
            sale_order = sale_order.browse(self.id)
            self.first_call = True
            self.second_call = False
            self.third_call = False
            self.fourth_call = False
            sale_order.x_Sale_Order_First_Call_State = 'firstCall'
        return True
        # if self.x_sale_order_schedule_confirmed == True:
        # self.x_Sale_Order_Scheduled_State = 'Scheduled'
        # self.env['sale.order'].write({'x_Sale_Order_Scheduled_State': 'Scheduled'})

    @api.one
    def sale_order_call_center_second_callconfirmation(self):
        if self.x_Sale_Order_First_Call_State == 'firstCall' and self.x_Sale_Order_Scheduled_State == 'Scheduled':
            sale_order = self.env['sale.order']
            sale_order = sale_order.browse(self.id)
            self.first_call = True
            self.second_call = True
            self.third_call = False
            self.fourth_call = False
            sale_order.x_Sale_Order_First_Call_State = 'secondCall'
        return True

    @api.one
    def sale_order_call_center_third_callconfirmation(self):
        if self.x_Sale_Order_First_Call_State == 'secondCall' and self.x_Sale_Order_Scheduled_State == 'Scheduled':
            sale_order = self.env['sale.order']
            sale_order = sale_order.browse(self.id)
            self.first_call = True
            self.second_call = True
            self.third_call = True
            self.fourth_call = False
            sale_order.x_Sale_Order_First_Call_State = 'thirdCall'
        return True

    @api.one
    def sale_order_call_center_fourth_callconfirmation(self):
        if self.x_Sale_Order_First_Call_State == 'thirdCall' and self.x_Sale_Order_Scheduled_State == 'Scheduled':
            sale_order = self.env['sale.order']
            sale_order = sale_order.browse(self.id)
            self.first_call = True
            self.second_call = True
            self.third_call = True
            self.fourth_call = True
            sale_order.x_Sale_Order_First_Call_State = 'fourthCall'
        return True

    @api.multi
    def cod_recieved(self):
        for record in self:
            if record.x_Sale_Order_COD_Done == False:
                record.x_Sale_Order_COD_Done = True
                # sale_order = record.env['sale.order']
                # sale_order = sale_order.browse(record.id)
                # sale_order.x_Sale_Order_COD_Done = True
        return True


#class extend_account_sale_order(models.Model):
    #_inherit = 'account.invoice'

    #cash_on_delivery = fields.Monetary(string="Cash On Delivery", help="Cash On Delivery", store=True, index=True,
                                       #copy=True, track_visibility='onchange')

    #invoice_validated = fields.Boolean(string="Invoice Validated", help="Invoice Validated", store=True, index=True,
                                       #copy=True, track_visibility='onchange', default=False)

    # total_cash = fields.Monetary(string="Total Cash",help="Total Cash",compute="_get_invoice_total_cash")

    #test_field = fields.Monetary(string="test", compute="_get_invoice_total_cash")

    #@api.one
    #def _get_invoice_total_cash(self):
        #for record in self:
            #results = record.env['sale.order'].search([('name', '=', record.origin)])
            #order_num = record.origin
            #_cashondelivery = results[0]['x_Sale_Order_Cash']
            #py_total = _cashondelivery + record.amount_total
            #self.test_field = _cashondelivery
            #if not record.invoice_validated:
                #self.env.cr.execute(
                    #"update account_invoice set cash_on_delivery = %f,amount_total = %f,amount_total_company_signed = %f,amount_total_signed = %f,residual = %f,residual_signed = %f,residual_company_signed = %f where origin = '%s' " % (
                        #_cashondelivery, py_total, py_total, py_total, py_total, py_total, py_total, order_num))
                #self.env.cr.execute(
                    #"update account_invoice set invoice_validated = True where origin = '%s'" % order_num)

        #return True

    #@api.one
    #def validate_invoice_amount(self):
        #for record in self:
            #results = record.env['sale.order'].search([('name', '=', record.origin)])
            #order_num = record.origin
            #_cashondelivery = results[0]['x_Sale_Order_Cash']
            #py_total = _cashondelivery + record.amount_total

            #if not record.invoice_validated:
                #self.env.cr.execute(
                    #"update account_invoice set cash_on_delivery = %f,amount_total = %f,amount_total_company_signed = %f,amount_total_signed = %f,residual = %f,residual_signed = %f,residual_company_signed = %f where origin = '%s' " % (
                        #_cashondelivery, py_total, py_total, py_total, py_total, py_total, py_total, order_num))
                #self.env.cr.execute(
                    #"update account_invoice set invoice_validated = True where origin = '%s'" % order_num)
                #self.env.cr.execute(
                    #'update sale_order set "x_Sale_Order_COD_Done" = True where name = "%s"' % order_num)

        #return True


class extend_account_sale_order(models.Model):
    _inherit = 'res.partner'

    order_fees_customer_discount = fields.Float(help="Order Fees Discount", string="Order Fees Discount", store=True,
                                                index=True,
                                                copy=True, track_visibility='onchange',
                                                digits_compute=dp.get_precision('order_fees_customer_discount'),
                                                default=0.0
                                                )

    cod_fees_discount = fields.Float(help="COD Fees Discount", string="COD Fees Discount", store=True, index=True,
                                     copy=True, track_visibility='onchange',
                                     digits_compute=dp.get_precision('cod_fees_discount'),
                                     default=0.0)

    first_kilo_fees_discount = fields.Float(help="1st Kilo Fees Discount", string="1st Kilo Fees Discount", store=True,
                                            index=True,
                                            copy=True, track_visibility='onchange',
                                            digits_compute=dp.get_precision('first_kilo_fees_discount'),
                                            default=0.0)

    second_kilo_fees_discount = fields.Float(help="2nd Kilo Fees Discount", string="2nd Kilo Fees Discount", store=True,
                                             index=True,
                                             copy=True, track_visibility='onchange',
                                             digits_compute=dp.get_precision('second_kilo_fees_discount'),
                                             default=0.0)

    third_kilo_fees_discount = fields.Float(help="3rd Kilo Fees Discount", string="3rd Kilo Fees Discount", store=True,
                                            index=True,
                                            copy=True, track_visibility='onchange',
                                            digits_compute=dp.get_precision('third_kilo_fees_discount'),
                                            default=0.0)

    fourth_kilo_fees_discount = fields.Float(help="4th Kilo Fees Discount", string="4th Kilo Fees Discount", store=True,
                                             index=True,
                                             copy=True, track_visibility='onchange',
                                             digits_compute=dp.get_precision('fourth_kilo_fees_discount'),
                                             default=0.0)

    fifth_kilo_fees_discount = fields.Float(help="5th Kilo Fees Discount", string="5th Kilo Fees Discount", store=True,
                                            index=True,
                                            copy=True, track_visibility='onchange',
                                            digits_compute=dp.get_precision('fifth_kilo_fees_discount'),
                                            default=0.0)

    sunday_cod_report = fields.Boolean(string="Sunday COD Reports", help="Sunday COD Reports", index=True,
                                       store=True, track_visibility='onchange', default=False)

    monday_cod_report = fields.Boolean(string="Monday COD Reports", help="Monday COD Reports", index=True,
                                       store=True, track_visibility='onchange', default=False)

    tuesday_cod_report = fields.Boolean(string="Tuesday COD Reports", help="Tuesday COD Reports", index=True,
                                        store=True, track_visibility='onchange', default=False)

    wednesday_cod_report = fields.Boolean(string="Wednesday COD Reports", help="Wednesday COD Reports", index=True,
                                          store=True, track_visibility='onchange', default=False)

    thursday_cod_report = fields.Boolean(string="Thursday COD Reports", help="Thursday COD Reports", index=True,
                                         store=True, track_visibility='onchange', default=False)

    friday_cod_report = fields.Boolean(string="Friday COD Reports", help="Friday COD Reports", index=True,
                                       store=True, track_visibility='onchange', default=False)

    saturday_cod_report = fields.Boolean(string="Saturday COD Reports", help="Saturday COD Reports", index=True,
                                         store=True, track_visibility='onchange', default=False)

class extend_accounting_sales(models.Model):
    _name = 'account.sale.invoice'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Accounting Invoices for Sales Orders'
    _order = 'create_date desc'

    invoice_number = fields.Char(string="Invoice Number", help="Invoice Number",
                                 size=128, store=True, index=True,
                                 track_visibility='always')

    partner_id = fields.Many2one('res.partner', string='Customer', help="Customer Refrence",
                                 required=True, index=True, track_visibility='always')

    state = fields.Selection([('draft', 'Draft'), ('sent', 'Sent'),('approved','Approved'), ('paid', 'Paid')], string="Invoice Status",
                             help="Invoice Status", store=True, index=True,
                             track_visibility='always', default='draft')

    invoice_count = fields.Char(string="Invoice Count", help="Customer Invoicing Count", size=10, store=True,
                                index=True,
                                track_visibility='always', default='0')

    invoice_orders = fields.One2many('sale.order.invoice', 'invoice_id', string='Invoice Orders',help="Invoice Orders", copy=True)

    paid_amount_total = fields.Float(string='Total Paid Amount', help="Total Paid Amount", store=True, readonly=True, index=True,
                               track_visibility='always')

    cod_fees_total = fields.Float(string='Total Orders COD Fees', help="Total Orders COD Fees", store=True, readonly=True, index=True,
                               track_visibility='always')

    vat_tax_total = fields.Float(string='Total VAT Orders Tax', help="Total VAT Orders Tax", store=True, readonly=True, index=True,
                               track_visibility='always')

    amount_vat_tax_total = fields.Float(string='Total Order fees Including VAT', help="Total Order fees Including VAT", store=True, readonly=True, index=True,
                               track_visibility='always')

    orders_fees_total = fields.Float(string='Total Orders Fees', help="Total Orders Fees", store=True, readonly=True, index=True,
                                        track_visibility='always')

    order_cash_total = fields.Float(string='Total Orders Cash', help="Total Orders Cash", store=True, readonly=True, index=True,
                                        track_visibility='always')

    order_tax_total = fields.Float(string='Total 10% Orders Tax', help="Total 10% Orders Tax", store=True, readonly=True, index=True,
                                    track_visibility='always')

    user_id = fields.Many2one('res.users', string='User', index=True, track_visibility='onchange',
                              default=lambda self: self.env.user)

    # def _create_invoice_number(self):
    # now = datetime.datetime.now()
    # _logger.debug('This is my debug message ! "%s"' % (datetime.datetime.now().strftime('%Y%m%d')))
    # self.invoice_number = 'INV-"%s"' % (datetime.datetime.now().strftime('%Y%m%d'))
    # _logger.debug('This is my debug message ! "%s"' % (datetime.datetime.now().strftime('%Y%m%d')))
    # return True

    def action_client_invoice_approve(self):
        if self.state == "sent":
            self.state = "approved"

    def invoice_paid(self):
        if self.state == "approved":
            self.state = "paid"

    def scheduler_invoice(self):
        customers = self.env['res.partner'].search([('active', '=', True)
                                                       ,('employee','=',False)
                                                       ,('is_company','=',True)
                                                       ,('name','!=','Rocket Express')
                                                    ])

        #_logger.debug('Maged customers ! "%s"' % (str(customers)))

        for customer in customers:

            company = int(customer[0]['id'])
            email = customer[0]['partner_account_email']
            sunday_cod_report = customer[0]['sunday_cod_report']
            monday_cod_report = customer[0]['monday_cod_report']
            tuesday_cod_report = customer[0]['tuesday_cod_report']
            wednesday_cod_report = customer[0]['wednesday_cod_report']
            thursday_cod_report = customer[0]['thursday_cod_report']
            friday_cod_report = customer[0]['friday_cod_report']
            saturday_cod_report = customer[0]['saturday_cod_report']

            #_logger.debug('Maged sunday_cod_report ! "%s"' % (str(sunday_cod_report)))
            #_logger.debug('Maged monday_cod_report ! "%s"' % (str(monday_cod_report)))
            #_logger.debug('Maged tuesday_cod_report ! "%s"' % (str(tuesday_cod_report)))
            #_logger.debug('Maged wednesday_cod_report ! "%s"' % (str(wednesday_cod_report)))
            #_logger.debug('Maged thursday_cod_report ! "%s"' % (str(thursday_cod_report)))
            #_logger.debug('Maged friday_cod_report ! "%s"' % (str(friday_cod_report)))
            #_logger.debug('Maged saturday_cod_report ! "%s"' % (str(saturday_cod_report)))

            #_logger.debug('Maged email ! "%s"' % (str(email)))
            #_logger.debug('Maged company ! "%s"' % (str(company)))

            current_day = datetime.date.today().strftime("%A")

            #_logger.debug('Maged current_day ! "%s"' % (str(current_day)))

            if sunday_cod_report == True and current_day == "Sunday":
                company_id = self.env['account.sale.invoice'].create({
                    'partner_id': company,
                })
                self.env.cr.commit()
                mail_template = self.env['mail.template'].browse(22)
                mail_template.write({'email_to': email})

                if mail_template:
                    mail_template.send_mail(int(company_id), force_send=True, raise_exception=True)

            if monday_cod_report == True and current_day == "Monday":
                company_id = self.env['account.sale.invoice'].create({
                    'partner_id': company,
                })
                self.env.cr.commit()

                #_logger.debug('Maged company_id ! "%s"' % (str(company_id)))

                #_logger.debug('Maged company_id ! "%s"' % (str(int(company_id))))

                mail_template = self.env['mail.template'].browse(22)
                mail_template.write({'email_to': email})

                if mail_template:
                    mail_template.send_mail(int(company_id), force_send=True, raise_exception=True)
                    pdf = self.env['report'].sudo().get_pdf([int(company_id)], 'courier-app.report_order_invoice')
                    self.env['ir.attachment'].create({
                        'name': self.invoice_number + ".pdf",
                        'type': 'binary',
                        'datas': base64.encodestring(pdf),
                        'res_model': 'account.sale.invoice',
                        'datas_fname': self.invoice_number + ".pdf",
                        'res_id': int(company_id),
                        'mimetype': 'application/x-pdf'
                    })

            if tuesday_cod_report == True and current_day == "Tuesday":
                company_id = self.env['account.sale.invoice'].create({
                    'partner_id': company,
                })
                self.env.cr.commit()
                mail_template = self.env['mail.template'].browse(22)
                mail_template.write({'email_to': email})

                if mail_template:
                    mail_template.send_mail(int(company_id), force_send=True, raise_exception=True)
                    pdf = self.env['report'].sudo().get_pdf([int(company_id)], 'courier-app.report_order_invoice')
                    self.env['ir.attachment'].create({
                        'name': self.invoice_number + ".pdf",
                        'type': 'binary',
                        'datas': base64.encodestring(pdf),
                        'res_model': 'account.sale.invoice',
                        'datas_fname': self.invoice_number + ".pdf",
                        'res_id': int(company_id),
                        'mimetype': 'application/x-pdf'
                    })

            if wednesday_cod_report == True and current_day == "Wednesday":
                company_id = self.env['account.sale.invoice'].create({
                    'partner_id': company,
                })
                self.env.cr.commit()
                mail_template = self.env['mail.template'].browse(22)
                mail_template.write({'email_to': email})

                if mail_template:
                    mail_template.send_mail(int(company_id), force_send=True, raise_exception=True)
                    pdf = self.env['report'].sudo().get_pdf([int(company_id)], 'courier-app.report_order_invoice')
                    self.env['ir.attachment'].create({
                        'name': self.invoice_number + ".pdf",
                        'type': 'binary',
                        'datas': base64.encodestring(pdf),
                        'res_model': 'account.sale.invoice',
                        'datas_fname': self.invoice_number + ".pdf",
                        'res_id': int(company_id),
                        'mimetype': 'application/x-pdf'
                    })

            if thursday_cod_report == True and current_day == "Thursday":
                company_id = self.env['account.sale.invoice'].create({
                    'partner_id': company,
                })
                self.env.cr.commit()
                mail_template = self.env['mail.template'].browse(22)
                mail_template.write({'email_to': email})

                if mail_template:
                    mail_template.send_mail(int(company_id), force_send=True, raise_exception=True)
                    pdf = self.env['report'].sudo().get_pdf([int(company_id)], 'courier-app.report_order_invoice')
                    self.env['ir.attachment'].create({
                        'name': self.invoice_number + ".pdf",
                        'type': 'binary',
                        'datas': base64.encodestring(pdf),
                        'res_model': 'account.sale.invoice',
                        'datas_fname': self.invoice_number + ".pdf",
                        'res_id': int(company_id),
                        'mimetype': 'application/x-pdf'
                    })

            if friday_cod_report == True and current_day == "Friday":
                company_id = self.env['account.sale.invoice'].create({
                    'partner_id': company,
                })
                self.env.cr.commit()
                mail_template = self.env['mail.template'].browse(22)
                mail_template.write({'email_to': email})

                if mail_template:
                    mail_template.send_mail(int(company_id), force_send=True, raise_exception=True)
                    pdf = self.env['report'].sudo().get_pdf([int(company_id)], 'courier-app.report_order_invoice')
                    self.env['ir.attachment'].create({
                        'name': self.invoice_number + ".pdf",
                        'type': 'binary',
                        'datas': base64.encodestring(pdf),
                        'res_model': 'account.sale.invoice',
                        'datas_fname': self.invoice_number + ".pdf",
                        'res_id': int(company_id),
                        'mimetype': 'application/x-pdf'
                    })

            if saturday_cod_report == True and current_day == "Saturday":
                company_id = self.env['account.sale.invoice'].create({
                    'partner_id': company,
                })
                self.env.cr.commit()
                mail_template = self.env['mail.template'].browse(22)
                mail_template.write({'email_to': email})

                if mail_template:
                    mail_template.send_mail(int(company_id), force_send=True, raise_exception=True)
                    pdf = self.env['report'].sudo().get_pdf([int(company_id)], 'courier-app.report_order_invoice')
                    self.env['ir.attachment'].create({
                        'name': self.invoice_number + ".pdf",
                        'type': 'binary',
                        'datas': base64.encodestring(pdf),
                        'res_model': 'account.sale.invoice',
                        'datas_fname': self.invoice_number + ".pdf",
                        'res_id': int(company_id),
                        'mimetype': 'application/x-pdf'
                    })

        return True

    @api.model
    def create(self, values):

        record = super(extend_accounting_sales, self).create(values)

        try:
            # results = record.env['account.sale.invoice'].search([('partner_id', '=', values.get('partner_id'))],order='invoice_count desc', limit=1)
            self.env.cr.execute(
                'select max(CAST (invoice_count AS INTEGER)) from account_sale_invoice where partner_id = %d' % values.get('partner_id'))

            max_invoice_count = str(self.env.cr.fetchone()[0])

            if max_invoice_count != '0':

                max_invoice_count = str(int(max_invoice_count) + 1)
                # _logger.debug('This is my debug message ! "%s"' % (str(max_invoice_count)))
                record['invoice_count'] = max_invoice_count
                # _logger.debug(record['invoice_number'] + '-"%s"' %(max_invoice_count))
                record['invoice_number'] = 'INV-%s-%s-%s' % (datetime.datetime.now().strftime('%Y%m%d'),values.get('partner_id'), max_invoice_count)
            else:
                number_int = 1
                record['invoice_count'] = '1'
                record['invoice_number'] = 'INV-%s-%s-%s' % (
                    datetime.datetime.now().strftime('%Y%m%d'),values.get('partner_id'), str(number_int))

            paid_amount_total = 0
            cod_fees_total = 0
            vat_tax_total = 0
            amount_vat_tax_total = 0
            orders_fees_total = 0
            order_cash_total = 0
            order_tax_total = 0

            results = record.env['sale.order'].search([('partner_id', '=', values.get('partner_id')),('invoice_status','=','to invoice')],
                                                                order='invoice_count desc')

            for rec in results:

                paid_amount = 0

                if rec[0]['x_Sale_Order_Delivered_State'] == 'delivered':
                    res = self.env['sale.order.invoice'].search([('order_ref', '=', rec[0]['name'])])
                    if not res:
                        rec[0]['invoice_status'] = 'invoiced'
                        if rec[0]['x_Sale_Order_COD'] == True:
                            paid_amount = float(rec[0]['x_Sale_Order_Cash']) - float(rec[0]['amount_total'])
                        else:
                            paid_amount = float(rec[0]['amount_total'])

                        paid_amount_total = paid_amount_total + paid_amount
                        cod_fees_total = cod_fees_total + float(rec[0]['cod_fees'])
                        vat_tax_total = vat_tax_total + float(rec[0]['vat_tax'])
                        amount_vat_tax_total = amount_vat_tax_total + float(rec[0]['amount_vat_tax'])
                        orders_fees_total = orders_fees_total + float(rec[0]['amount_total'])
                        order_cash_total = order_cash_total + float(rec[0]['x_Sale_Order_Cash'])
                        #order_tax_total = order_tax_total + float(rec[0]['amount_tax'])
                        order_tax_total = order_tax_total + float(rec[0]['tax_repriced'])

                        self.env['sale.order.invoice'].create({
                            'invoice_number': record['invoice_number'],
                            'order_ref': rec[0]['name'],
                            'partner_id': int(rec[0]['partner_id']),
                            'amount_vat_tax': rec[0]['amount_vat_tax'],
                            'vat_tax': rec[0]['vat_tax'],
                            'cod_fees': rec[0]['cod_fees'],
                            'amount_total': rec[0]['amount_total'],
                            'order_cash': rec[0]['x_Sale_Order_Cash'],
                            'invoice_id': record['id'],
                            'paid_amount': paid_amount,
                            'order_tax': rec[0]['tax_repriced'],
                        })

                    self.env.cr.commit()

                    record['paid_amount_total'] = paid_amount_total
                    record['cod_fees_total'] = cod_fees_total
                    record['vat_tax_total'] = vat_tax_total
                    record['amount_vat_tax_total'] = amount_vat_tax_total
                    record['orders_fees_total'] = orders_fees_total
                    record['order_cash_total'] = order_cash_total
                    record['order_tax_total'] = order_tax_total

        except Exception as e:
            raise Exception(str(e))

        return record

    @api.multi
    def action_mail_invoice_send(self):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        self.ensure_one()

        invoice_id = int(self.id)
        #_logger.debug('self.partner_id maged ! "%s"' % (str(self.partner_id)))
        res_partner = self.env['res.partner'].browse(int(self.partner_id))
        email_to = res_partner[0]['partner_account_email']
        #_logger.debug('email_to maged ! "%s"' % (email_to))

        if email_to is not None and email_to != "":
            #ir_model_data = self.env['ir.model.data']
            #try:
                #template_id = ir_model_data.get_object_reference('sale', 'email_template_edi_sale')[1]
                #template_id = 22
            #except ValueError:
                #template_id = False
            #try:
                #compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
            #except ValueError:
                #compose_form_id = False
            #ctx = dict()
            #ctx.update({
                #'default_model': 'account.sale.invoice',
                #'default_res_id': self.ids[0],
                #'default_use_template': bool(template_id),
                #'default_template_id': template_id,
                #'default_composition_mode': 'comment',
                #'mark_so_as_sent': True,
                #'email_to':email_to,
                #'custom_layout': "courier-app.mail_template_invoice_orders"
            #})
            #return {
                #'type': 'ir.actions.act_window',
                #'view_type': 'form',
                #'view_mode': 'form',
                #'res_model': 'mail.compose.message',
                #'views': [(compose_form_id, 'form')],
                #'view_id': compose_form_id,
                #'target': 'new',
                #'context': ctx,
            #}
            mail_template = self.env['mail.template'].browse(22)
            mail_template.write({'email_to': email_to})

            if mail_template:
                mail_template.send_mail(self.id, force_send=True, raise_exception=True)
                if self.state == "draft":
                    self.state = "sent"

                pdf = self.env['report'].sudo().get_pdf([invoice_id], 'courier-app.report_order_invoice')
                self.env['ir.attachment'].create({
                    'name': self.invoice_number+".pdf",
                    'type': 'binary',
                    'datas': base64.encodestring(pdf),
                    'res_model': 'account.sale.invoice',
                    'datas_fname': self.invoice_number+".pdf",
                    'res_id': invoice_id,
                    'mimetype': 'application/x-pdf'
                })

        return True

class extend_sale_invoices(models.Model):

    _name = 'sale.order.invoice'
    _description = 'Sales Orders Under Account Invoice'
    _order = 'create_date desc'

    invoice_number = fields.Char(string="Invoice Number", help="Invoice Number",
                                 size=128, store=True, index=True,require=True,
                                 track_visibility='always')

    order_ref = fields.Char(string="Order Reference", help="Order Reference",
                            size=20, store=True, index=True, require=True,
                            track_visibility='always')

    partner_id = fields.Many2one('res.partner', string='Customer', help="Customer Refrence",
                                 required=True, index=True, track_visibility='always')

    amount_vat_tax = fields.Float(string='Amount Including VAT', help="14% VAT", store=True,
                                     index=True,
                                     track_visibility='always')

    vat_tax = fields.Float(string='VAT', help="VAT Amount",
                              index=True, store=True,
                              track_visibility='always')

    cod_fees = fields.Float(string='COD Fees', help="COD Fees", store=True, readonly=True, index=True,
                               track_visibility='always')

    amount_total = fields.Float(string='Total Amount', help="Total Amount", store=True, readonly=True, index=True,
                                   track_visibility='always')

    order_cash = fields.Float(string="Cash On Delivery", store=True, index=True, help="Cash On Delivery")

    #order_num = fields.Integer(string="Order Number", store=True, index=True,help="Client Order Number")

    invoice_id = fields.Integer(string="Invoice Id", store=True, index=True,readonly=True,help="Invoice Id")


    paid_amount = fields.Float(string='Paid Amount', help="Paid Amount", store=True, readonly=True, index=True,
                               track_visibility='always')

    order_tax = fields.Float(string='Order 10% Tax', help="Order 10% Tax", store=True, readonly=True, index=True,
                               track_visibility='always')

class extend_manual_order(models.Model):

    _name = 'create.manual.order'
    _description = 'Client Create Manual Order'
    _order = 'create_date desc'



    order_id = fields.One2many('sale.order', 'id', string='Orders',help="Orders", copy=True)


    @api.model
    def create(self, values):

        try:
            product_uom = self.env['uom.uom'].search([('name', '=', 'Unit(s)')])
            product_uom_id = int(product_uom[0]['id'])

            user = self.env['res.users'].search([('id', '=', int(self._uid))])
            partner = self.env['res.partner'].search([('id', '=', int(user[0]['partner_id']))])


            _logger.info('partner[0][commercial_partner_id] maged ! "%s"' % (str(partner[0]['commercial_partner_id'])))
            _logger.info('self._uid maged ! "%s"' % (str(self._uid)))
            _logger.info('partner_id maged ! "%s"' % (str(user[0]['partner_id'])))
            _logger.info('partner maged ! "%s"' % (str(partner)))
            _logger.info('user maged ! "%s"' % (str(user)))

            partner_id = int(partner[0]['commercial_partner_id'])

            values.update({'partner_id':partner_id})

            _logger.info('x_Sale_Order_Cash maged ! "%s"' % (str(values.get('x_Sale_Order_Cash'))))
            _logger.info('values maged ! "%s"' % (str(values)))
            _logger.info('values.get(order_id)[0][2][x_Sale_Order_COD] maged ! "%s"' % (str(values.get('order_id')[0][2]['x_Sale_Order_Cash'])))

            if values.get('order_id')[0][2]['x_Sale_Order_Cash'] > 0:
                values.update({'x_Sale_Order_COD': True})

            record = super(extend_manual_order, self).create(values)

            for data in values.get('order_id'):
                _logger.info('data maged ! "%s"' % (str(data)))
                _logger.info('data[2] maged ! "%s"' % (str(data[2])))
                new_order_id = self.env['sale.order'].search([('x_sale_order_shipping_address', '=', str(data[2]['x_sale_order_shipping_address'])),
                                                              ('x_Sale_Order_Cust_Prod', '=',
                                                               str(data[2]['x_Sale_Order_Cust_Prod'])),
                                                              ('x_Sale_Order_Customer_name', '=',
                                                               str(data[2]['x_Sale_Order_Customer_name'])),
                                                              ('partner_id', '=',
                                                               partner_id),
                                                              ('order_number', '=',
                                                               int(data[2]['order_number'])),
                                                              ('x_Sale_order_Mobile_No', '=',
                                                               str(data[2]['x_Sale_order_Mobile_No'])),
                                                              ('x_Sale_Order_COD', '=',
                                                               data[2]['x_Sale_Order_COD']),
                                                              ('x_Sale_Order_Cash', '=',
                                                               int(data[2]['x_Sale_Order_Cash'])),
                                                              ('reversed_order', '=',
                                                               data[2]['reversed_order']),
                                                              ('x_Sale_Order_Cust_Prod', '=',
                                                               str(data[2]['x_Sale_Order_Cust_Prod']))
                                                              ])
                new_id = int(new_order_id[0]['id'])
                #_logger.debug('Maged ! "%s"' % (str(data[2]['product_id'])))
                #_logger.debug('Maged ! "%s"' % (str(new_id)))
                output = self.env['sale.order.line'].create({
                    'product_uom': product_uom_id,
                    'product_uom_qty': 1,
                    'partner_id': partner_id,
                    'product_id': int(data[2]['product_id']),
                    'order_id':new_id,
                })

                self.env.cr.commit()

                #_logger.debug('Maged ! "%s"' % (str(output)))

                results = self.env['res.partner'].search([('id', '=', partner_id)])
                x_cod_fees_discount = results[0]['cod_fees_discount']
                #_logger.debug('Maged ! "%s"' % (str(x_cod_fees_discount)))
                x_order_fees_discount = results[0]['order_fees_customer_discount']
                #_logger.debug('Maged ! "%s"' % (str(x_order_fees_discount)))
                cod_results = self.env['product.template'].search([('name', '=', 'COD')])
                x_cod_fees = cod_results[0]['list_price']
                #_logger.debug('Maged ! "%s"' % (str(x_cod_fees)))

                results = self.env['sale.order'].search([('x_sale_order_shipping_address', '=', str(data[2]['x_sale_order_shipping_address'])),
                                                              ('x_Sale_Order_Cust_Prod', '=',
                                                               str(data[2]['x_Sale_Order_Cust_Prod'])),
                                                              ('x_Sale_Order_Customer_name', '=',
                                                               str(data[2]['x_Sale_Order_Customer_name'])),
                                                              ('partner_id', '=',
                                                               partner_id),
                                                              ('order_number', '=',
                                                               int(data[2]['order_number'])),
                                                              ('x_Sale_order_Mobile_No', '=',
                                                               str(data[2]['x_Sale_order_Mobile_No'])),
                                                              ('x_Sale_Order_COD', '=',
                                                               data[2]['x_Sale_Order_COD']),
                                                              ('x_Sale_Order_Cash', '=',
                                                               int(data[2]['x_Sale_Order_Cash'])),
                                                              ('reversed_order', '=',
                                                               data[2]['reversed_order']),
                                                              ('x_Sale_Order_Cust_Prod', '=',
                                                               str(data[2]['x_Sale_Order_Cust_Prod']))
                                                              ])

                order_line_res = self.env['sale.order.line'].search([('id', '=', int(output))])

                #_logger.debug('Maged ! "%s"' % (str(order_line_res)))

                _logger.info('results maged ! "%s"' % (str(results)))

                update_cod_fees = 0
                update_amount_vat_tax = 0
                update_vat_tax = 0
                update_amount_total = 0
                order_fees_amount = order_line_res[0]['price_total']

                #_logger.debug('Maged ! "%s"' % (str(order_fees_amount)))

                if results[0]['x_Sale_Order_COD'] == True:
                    _logger.info('results maged ! "%s"' % (str(results)))

                    if x_cod_fees_discount < 0.0:
                        update_cod_fees = float(x_cod_fees) - float((x_cod_fees * x_cod_fees_discount) / 100.0)
                    elif x_cod_fees_discount >= 0.0:
                        update_cod_fees = float(x_cod_fees) - float((x_cod_fees * x_cod_fees_discount) / 100.0)

                    if x_order_fees_discount < 0.0:
                        order_fees_amount = float(order_fees_amount) - float(
                            (order_fees_amount * x_order_fees_discount) / 100.0)
                    elif x_order_fees_discount >= 0.0:
                        order_fees_amount = float(order_fees_amount) - float(
                            (order_fees_amount * x_order_fees_discount) / 100.0)

                    update_amount_vat_tax = 1.14 * (order_fees_amount + update_cod_fees)
                    update_vat_tax = 0.14 * (order_fees_amount + update_cod_fees)
                    results.total_cash = results[0]['x_Sale_Order_Cash']
                    update_amount_total = results[0]['x_Sale_Order_Cash'] - float(update_amount_vat_tax)

                else:
                    update_cod_fees = x_cod_fees
                    update_amount_vat_tax = 1.14 * (order_fees_amount + update_cod_fees)
                    update_vat_tax = 0.14 * (results[0]['amount_total'] + update_cod_fees)
                    update_amount_total = results[0]['x_Sale_Order_Cash'] - float(update_amount_vat_tax)
                    results.total_cash = results[0]['x_Sale_Order_Cash']

                results.cod_fees = update_cod_fees
                results.amount_vat_tax = update_amount_vat_tax
                results.vat_tax = update_vat_tax
                results.amount_total = update_amount_total

        except Exception as e:
            raise Exception(str(e))

        return record

class extend_sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self, values):

        try:
            product_uom = self.env['uom.uom'].search([('name', '=', 'Unit(s)')])
            product_uom_id = int(product_uom[0]['id'])

            values.update({'product_uom':product_uom_id})
            values.update({'product_uom_qty': 1})
            record = super(extend_sale_order_line, self).create(values)

        except Exception as e:
            raise Exception(str(e))

        return record

class extend_res_users(models.Model):
    _inherit = 'res.users'

    x_client_portal_user = fields.Boolean(string="Client Portal User", help="Is Client Portal User Access ?",track_visibility='always'
                                          ,index=True,store=True,copy=True)

    x_is_courier = fields.Boolean(string="Courier", help="Is Courier ?",
                                          track_visibility='always'
                                          , index=True, store=True, copy=True)

class extend_res_partner(models.Model):
    _inherit = 'res.partner'

    partner_account_email = fields.Char(string="Report Email",help="Accounting Report Email",index=True,
                                        track_visibility='always',store=True)

    @api.multi
    def _invoice_total(self):
        #_logger.debug('self.id maged ! "%s"' % (str(self.commercial_partner_id)))
        #self.env.cr.execute(
            #'select sum(orders_fees_total) from account_sale_invoice where partner_id = 7')
        #_logger.debug('self.id maged ! "%s"' % (str(self.env.cr.fetchone())))
        #sum_invoices = float(self.env.cr.fetchone()[0])
        #_logger.debug('self.env.cr.fetchone()[0] maged ! "%s"' % (str(self.env.cr.fetchone()[0])))
        #self.total_invoiced = float(self.env.cr.fetchone()[0])

        account_invoice_report = self.env['account.sale.invoice']
        if not self.ids:
            self.total_invoiced = 0.0
            return True

        user_currency_id = self.env.user.company_id.currency_id.id
        all_partners_and_children = {}
        all_partner_ids = []
        for partner in self:
            # price_total is in the company currency
            all_partners_and_children[partner] = self.with_context(active_test=False).search(
                [('id', 'child_of', partner.id)]).ids
            all_partner_ids += all_partners_and_children[partner]

        # searching account.invoice.report via the orm is comparatively expensive
        # (generates queries "id in []" forcing to build the full table).
        # In simple cases where all invoices are in the same currency than the user's company
        # access directly these elements

        # generate where clause to include multicompany rules
        where_query = account_invoice_report._where_calc([
            ('partner_id', 'in', all_partner_ids)
            #, ('state', 'not in', ['draft', 'cancel'])
            #,
            #('type', 'in', ('out_invoice', 'out_refund'))
        ])
        account_invoice_report._apply_ir_rules(where_query, 'read')
        from_clause, where_clause, where_clause_params = where_query.get_sql()

        # price_total is in the company currency
        query = """
                          SELECT SUM(orders_fees_total) as total, partner_id
                            FROM account_sale_invoice account_sale_invoice
                           WHERE %s
                           GROUP BY partner_id
                        """ % where_clause
        self.env.cr.execute(query, where_clause_params)
        price_totals = self.env.cr.dictfetchall()
        for partner, child_ids in all_partners_and_children.items():
            partner.total_invoiced = sum(price['total'] for price in price_totals if price['partner_id'] in child_ids)


class product_template_extend(models.Model):
    _inherit = 'product.template'

    is_courier_zone = fields.Boolean(string="Is a Courier Zone", index=True, store=True, track_visibility='always', default=False)

class res_partner_extend(models.Model):
    _inherit = 'res.partner'

    x_Company_Call_Script = fields.Text(string="Call Script", store=True, index=True, track_visibility='always')