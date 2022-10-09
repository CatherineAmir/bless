# -*- coding: utf-8 -*-
# from odoo import http


# class Bless(http.Controller):
#     @http.route('/bless/bless/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bless/bless/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bless.listing', {
#             'root': '/bless/bless',
#             'objects': http.request.env['bless.bless'].search([]),
#         })

#     @http.route('/bless/bless/objects/<model("bless.bless"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bless.object', {
#             'object': obj
#         })
