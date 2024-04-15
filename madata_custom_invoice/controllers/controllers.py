# -*- coding: utf-8 -*-
# from odoo import http


# class AdematReport(http.Controller):
#     @http.route('/ademat_report/ademat_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ademat_report/ademat_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ademat_report.listing', {
#             'root': '/ademat_report/ademat_report',
#             'objects': http.request.env['ademat_report.ademat_report'].search([]),
#         })

#     @http.route('/ademat_report/ademat_report/objects/<model("ademat_report.ademat_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ademat_report.object', {
#             'object': obj
#         })
