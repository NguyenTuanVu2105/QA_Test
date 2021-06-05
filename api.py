import flask
from flask import request, jsonify, flash, request, redirect, url_for
from flask_cors import CORS, cross_origin
from db import *
from process import * 
from werkzeug.utils import secure_filename
import xlrd
import os 

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
UPLOAD_FOLDER = 'excel'
ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/v1/resources/products/all', methods=['GET'])
def products():
    all_products = get_product()
    return jsonify(all_products)

@app.route('/api/v1/resources/products/delete', methods=['GET'])
def _delete_product():
    delete_product()
    return jsonify({"success": True})

@app.route('/api/v1/sync_product', methods=['POST'])
def sync_product(): 
    products = get_all_product() 
    create_products(products)
    print(products)
    return jsonify({"success": True})

@app.route('/api/v1/create_product', methods=['GET'])
def create_product(): 
    products = [{'name': 'AOP Nose Fit Face Mask', 'sku': 'AFM02', 'image': 'https://storage.googleapis.com/printholo/product-list-thumbnail/aop_1c_face_mask.png', 'sides': ['FRONT']}, {'name': 'AOP Sleeveless Jersey Tank Top', 'sku': 'ASJT01', 'image': 'https://assets.printholo.com/product-list-thumbnail/v-neck_sleeveless_jersey_tank_top_1621240760830_3AA2Ef6238.png', 'sides': ['FRONT', 'BACK', 'BINDING']}]
    create_products(products)
    return jsonify({"success": True})

@app.route('/api/v1/create_product', methods=['GET'])
def 


@app.route('/api/v1/create_preview_mockup', methods=['POST'])
def create_preview_mockup(): 
    sides = {
        "Front": {
            "color": "black", 
            "artwork": "https://printholo.storage.googleapis.com/artworks/thumbnails/pexels_elijah_o_donnell_4173624_1605846726204_4fF8734fb7.jpg"
        }, 
        "Back": {
            "color": "white", 
            "artwork": "https://printholo.storage.googleapis.com/default_artworks/thumbnails/Front_1604031195402_Afd622cb55.png"
        }, 
        "Right Sleeve": {
            "color": "grey", 
            "artwork": None
        }, 
        "Left Sleeve": {
            "color": "gold", 
            "artwork": None
        }, 
        "Hood": {
            "color": "green", 
            "artwork": None
        }
    }
    sku = "AHD01"
    image_url = preview_mockup(sku, sides)
    return jsonify({"success": True, "image_url": image_url})

@app.route('/api/v1/check_store_price', methods=['POST'])
def check_store_price(): 
    testcase = {
        "product": "ATS01", 
        "prices": [
            {
                "attribute": "S",
                "value": "14"
            },
            {
                "attribute": "M",
                "value": "80"
            },
            {
                "attribute": "L",
                "value": "0"
            },
            {
                "attribute": "XL",
                "value": "78"
            },
                        {
                "attribute": "2XL",
                "value": "6"
            },
            {
                "attribute": "3XL",
                "value": "0"
            }
        ] 
    }
    result = check_store_price_process(testcase)
    return jsonify({"pass":result})

@app.route('/api/v1/testcase-infomation', methods=['POST'])
def testcase_infomation(): 
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No data"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": ""})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_url)
        wb = xlrd.open_workbook(file_url)
        sheet = wb.sheet_by_index(0)
        testcases = []
        testcase = {}
        for i in range(1, sheet.nrows): 
            sku = sheet.cell_value(i, 1)
            if sku != '':
                if 'product' in testcase:
                    testcases.append(testcase)
                    testcase = {}
                testcase["product"] = sku
                testcase["infos"] = [{
                    "attribute": sheet.cell_value(i, 2),
                    "base_cost": sheet.cell_value(i, 3),
                    "US_ship": sheet.cell_value(i, 4),
                    "US_ship_add": sheet.cell_value(i,5),
                    "EU_ship": sheet.cell_value(i, 6),
                    "EU_ship_add": sheet.cell_value(i, 7),
                    "ROW_ship": sheet.cell_value(i, 8),
                    "ROW_ship_add": sheet.cell_value(i, 9),
                }]
            else: 
                testcase["infos"].append({
                    "attribute": sheet.cell_value(i, 2),
                    "base_cost": sheet.cell_value(i, 3),
                    "US_ship": sheet.cell_value(i, 4),
                    "US_ship_add": sheet.cell_value(i,5),
                    "EU_ship": sheet.cell_value(i, 6),
                    "EU_ship_add": sheet.cell_value(i, 7),
                    "ROW_ship": sheet.cell_value(i, 8),
                    "ROW_ship_add": sheet.cell_value(i, 9),
                })
        # print(testcases)

        # result = False 
        # result = check_information_product_process(testcase)
        return jsonify(testcases)

@app.route('/api/v1/check_information_product', methods=['POST'])
def check_information_product(): 
    pass 

app.run()