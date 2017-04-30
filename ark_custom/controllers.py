# -*- coding: utf-8 -*-
# © 2015 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# import email
# import datetime
# from openerp import fields
from openerp import http,fields
from openerp.http import request
import logging
import xmlrpclib
from datetime import datetime
_logger = logging.getLogger(__name__)


class Main(http.Controller):
    # test this with
    # curl -i -X POST -H "Content-Type: application/json" -d {} $URL
    @http.route('/ark_custom/transaction/json', type='json', auth='none')
    def transaction_json(self,**args):
		try:
			_logger.info('CONNECTION SUCCESSFUL')
			_logger.info(args)
			usernameFromJson = args.get('username',False)
			passwordFromJson = args.get('password',False)
			noWayBill = args.get('noWayBill')
			interntalRef = args.get('internalRefOID',False)
			serviceType = args.get('serviceType',False)
			cityDestination = args.get('cityDestination',False)
			cityOrigin = args.get('cityOrigin',False)	
			
			customer = args.get('customer')
			customerAccountName = customer['accountName']
			customerCode = customer['customerCode']
			customerName = customer['customerName']
			customerAddress = customer['address']
			customerPhone = customer['phone']
			contactPerson = customer['contactPerson']
			
			#Connect to ODOO XMLRPC
			url = 'http://localhost:8069'
			db = 'test' 
			username = usernameFromJson
			password = passwordFromJson
			
			
			
			common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
			_logger.info(common.version())
			uid = common.authenticate(db, username, password, {})
			models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
			
			#Check Customer Availability 
			recordsCustomer = request.env['res.partner'].sudo().search([('customerCode','=',customerCode)])
			
			if recordsCustomer:
			
				_logger.info('Customer Exist in database ')
				idCustomer = recordsCustomer['id']
				
			else:
			
				idContactPerson = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name': contactPerson,'phone':customerPhone}])
				idCustomer = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name': customerName,'child_ids':[(6,0,[idContactPerson])],'street':customerAddress,'customerCode':customerCode,'is_company':True,'customerAccountName':customerAccountName}])
			
			#For Product
			#Check Attribute Origin
			recordsProductAttributeOrigin = request.env['product.attribute'].sudo().search([('name','=','Origin')])
			if recordsProductAttributeOrigin:
				_logger.info('Theres Already Attribute Name Origin')
				_logger.info(recordsProductAttributeOrigin.read(['id','name']))
				_logger.info(recordsProductAttributeOrigin.mapped('name'))
				arrayIdAttrOrigin = recordsProductAttributeOrigin.mapped('id')
				for i in arrayIdAttrOrigin:
					idAttrOrigins = i
				
				_logger.info(idAttrOrigins)
				
				
			else :
				_logger.info('No Attribute Named Origin, Creating New One')
				##id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name': name,'email':email,'type':'service',''}])
				idAttrOrigins = models.execute_kw(db, uid, password, 'product.attribute', 'create', [{'name': 'Origin'}])
				_logger.info(idAttrOrigins)
			
			recordsProductAttributeDestination = request.env['product.attribute'].sudo().search([('name','=','Destination')])
			if recordsProductAttributeDestination:
				_logger.info('Theres Already Attribute Name Destination')
				_logger.info(recordsProductAttributeDestination.read(['id','name']))
				_logger.info(recordsProductAttributeDestination.mapped('name'))
				arrayIdAttrDestination = recordsProductAttributeDestination.mapped('id')
				for i in arrayIdAttrDestination:
					idAttrDest = i
				
				_logger.info(idAttrDest)
				
				
			else :
				_logger.info('No Attribute Named Origin, Creating New One')
				##id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name': name,'email':email,'type':'service',''}])
				idAttrDest = models.execute_kw(db, uid, password, 'product.attribute', 'create', [{'name': 'Destination'}])
				_logger.info(idAttrDest)
			
			##_logger.info(id);
			#record = request.env['res.partner'].create(partner_val)
			
			#idProduct = models.execute_kw(db, uid, password, 'product.template', 'create', [{'name': 'Standard','type':'service'}])
			#Untuk Output Jsonnya 
			recordsProductTempate = request.env['product.template'].sudo().search([('type','=','service'),('name','=',serviceType)])
			
			if recordsProductTempate:
					
				_logger.info(recordsProductTempate.mapped('name'))
				_logger.info('Standard Product Already in Databases')
				arrayId = recordsProductTempate.mapped('id')
				for i in arrayId:
					
					idProduct = i
				
			else :
				idProduct = models.execute_kw(db, uid, password, 'product.template', 'create', [{'name': serviceType,'type':'service'}])
			
			
			recordsProductAttrValueOrigins = request.env['product.attribute.value'].sudo().search([('name','=',cityOrigin),('attribute_id','=',idAttrOrigins)])
			if recordsProductAttrValueOrigins:
				_logger.info('Origin City Already In Database |'+cityOrigin)
				_logger.info(recordsProductAttrValueOrigins.mapped('name'))
				arrayIdValueOrigins = recordsProductAttrValueOrigins.mapped('id')
				for i in arrayIdValueOrigins:
					idValueOrigins = i
			else :
				_logger.info('Creating New Value For Origin City with |'+cityOrigin)
				idValueOrigins = models.execute_kw(db, uid, password, 'product.attribute.value', 'create', [{'name': cityOrigin,'attribute_id':idAttrOrigins}])
				
			
			recordsProductAttrValueDestination = request.env['product.attribute.value'].sudo().search([('name','=',cityDestination),('attribute_id','=',idAttrDest)])
			if recordsProductAttrValueDestination:
				
				_logger.info('Destination City Already In Database |'+cityDestination)
				_logger.info(recordsProductAttrValueDestination.mapped('name'))
				arrayIdValueDestination = recordsProductAttrValueDestination.mapped('id')
				for i in arrayIdValueDestination:
					idValueDestination = i
				
			else:
				_logger.info('Creating New Value For Destination City with |'+cityDestination)
				idValueDestination = models.execute_kw(db, uid, password, 'product.attribute.value', 'create', [{'name': cityDestination,'attribute_id':idAttrDest}])
				
			
	#		idValue = models.execute_kw(db, uid, password, 'product.attribute.value', 'create', [{'name': 'Bekasi','attribute_id':idAttrOrigins}])
			#idValue = 10
			#_logger.info((6,0,[idValue]))
			_logger.info('idProduk : '+str(idProduct))
			#models.execute_kw(db, uid, password, 'product.attribute.line', 'create', [{'product_tmpl_id': idProduct,'attribute_id':idAttrOrigins,'value_ids':(4,idValue)}])
			#models.execute_kw(db, uid, password, 'product.attribute.line', 'create', [{'product_tmpl_id': idProduct,'attribute_id':idAttr,'value_ids':[(6,0,[idValue])]}])
			
			
			#ngebuat record baru/update di product.attribute.line
			recordsProductAttributeLineOrigins = request.env['product.attribute.line'].sudo().search([('product_tmpl_id','=',idProduct),('attribute_id','=',idAttrOrigins)])
			_logger.info('RecordsAttributeLineOrigins')
			_logger.info(recordsProductAttributeLineOrigins.read([]))
			
			if recordsProductAttributeLineOrigins:
					
					_logger.info('Updating product.attribute.line for origins based on id :'+str(recordsProductAttributeLineOrigins['id'])+' and the value is Id Value Origins (value_ids) :'+str(idValueOrigins))
					
					recordResultValueOrigin = models.execute_kw(db, uid, password, 'product.attribute.line', 'write',[[recordsProductAttributeLineOrigins['id']],{'value_ids':[(4,idValueOrigins)]}])
							
			else:
				
				_logger.info('Creating product.attribute.line for origins')
				models.execute_kw(db, uid, password, 'product.attribute.line', 'create', [{'product_tmpl_id': idProduct,'attribute_id':idAttrOrigins,'value_ids':[(6,0,[idValueOrigins])]}])
			
			
			
			recordsProductAttributeLineDestination = request.env['product.attribute.line'].sudo().search([('product_tmpl_id','=',idProduct),('attribute_id','=',idAttrDest)])
			_logger.info('RecordsAttributeLineDestination')
			_logger.info(recordsProductAttributeLineDestination.read([]))
			if recordsProductAttributeLineDestination:
			
					_logger.info('Updating product.attribute.line for Destination')
					recordResultValueOrigin = models.execute_kw(db, uid, password, 'product.attribute.line', 'write',[[recordsProductAttributeLineDestination['id']],{'value_ids':[(4,idValueDestination)]}])
							
			else:
				
				_logger.info('Creating product.attribute.line for Destination')
				models.execute_kw(db, uid, password, 'product.attribute.line', 'create', [{'product_tmpl_id': idProduct,'attribute_id':idAttrDest,'value_ids':[(6,0,[idValueDestination])]}])
			
			
			
			
			
		#	recordResultValueDestination = models.execute_kw(db, uid, password, 'product.attribute.line', 'write',[[idAttrDest],{'value_ids':[(4,idValueDestination)]}])
			
			#buat Ngetrigger update product.template
			models.execute_kw(db,uid,password,'product.template','write',[[idProduct],{'active':True}])
			
			
			#_logger.info(recordResult)
				
			price = 0
			description = 'Pengiriman Dari '+str(cityOrigin)+' Ke '+str(cityDestination)+' Dengan Tipe '+str(serviceType)
			_logger.info(description)
		
			recordPriceList = request.env['product.pricelist'].sudo().search([('name','ilike','Tiputipu'),('active','=',True)])
			_logger.info(recordPriceList.read([]))
			idPriceListVersion = int(recordPriceList['version_id'])
			
			
			recordPriceVersion = request.env['product.pricelist.version'].sudo().search([('id','=',idPriceListVersion)])
			_logger.info(recordPriceVersion.read([]))
			idPriceListItem = int(recordPriceVersion['items_id'])
			
			recordProductCategoryServiceType = request.env['product.category'].sudo().search([('name','ilike',serviceType)])
			_logger.info(recordProductCategoryServiceType.read([]))
			idCategoryServiceType = recordProductCategoryServiceType['id']
			
			
			recordProductCategoryDestination = request.env['product.category'].sudo().search([('name','ilike',cityDestination),('parent_id','=',idCategoryServiceType)])
			_logger.info(recordProductCategoryDestination.read([]))
			idCategoryDestination=int(recordProductCategoryDestination['id'])
			_logger.info(idCategoryDestination)
			
			recordPriceVersionItem = request.env['product.pricelist.item'].sudo().search([('categ_id','=',idCategoryDestination)])
			_logger.info(recordPriceVersionItem.read([]))
			price = int(recordPriceVersionItem['price_surcharge'])
			
			
			#_logger.info(models.execute_kw(db, uid, password,'product.pricelist', 'search_read',[[['name', 'ilike', 'gramedia'],]],{'fields': ['name', 'country_id', 'version_id'], 'limit': 5}))
			

			
		#	_logger.info(models.execute_kw(db, uid, password, 'product.attribute.line', 'name_get', [[7]]))
			recordsProductVariant = request.env['product.product'].sudo().search([('product_tmpl_id','=',idProduct),('attribute_value_ids','=',idValueOrigins),('attribute_value_ids','=',idValueDestination)])
			idProductVariant = recordsProductVariant['id']
			_logger.info(idProductVariant)
			
			
		#	idSaleOrderLine = models.execute_kw(db, uid, password, 'sale.order.line', 'create', [{'name': description,'product_id':idProduct,'product_uom_qty':1,'price_unit':price}])
			idSaleOrder = models.execute_kw(db, uid, password, 'sale.order', 'create', [{'partner_id':idCustomer,'order_line':[(0,0,{'product_id':idProductVariant,'product_uom_qty':1,'name':description,'price_unit':price})]}])
			
		#	_logger.info(idSaleOrder)
			status = [{'status':'0','Description':'Success','idQuotation':idSaleOrder}]
			return status
		except Exception as e:
			status = [{'status':'3','Description':e}]
			return status