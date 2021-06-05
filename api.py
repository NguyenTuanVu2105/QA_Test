import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from db import *
from process import * 

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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
    print(products)
    return jsonify({"success": True})

@app.route('/api/v1/create_product', methods=['GET'])
def create_product(): 
    products = [{'name': 'AOP Nose Fit Face Mask', 'sku': 'AFM02', 'image': 'https://storage.googleapis.com/printholo/product-list-thumbnail/aop_1c_face_mask.png', 'sides': ['FRONT']}, {'name': 'AOP Sleeveless Jersey Tank Top', 'sku': 'ASJT01', 'image': 'https://assets.printholo.com/product-list-thumbnail/v-neck_sleeveless_jersey_tank_top_1621240760830_3AA2Ef6238.png', 'sides': ['FRONT', 'BACK', 'BINDING']}]
    create_products(products)
    return jsonify({"success": True})

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

@app.route('/api/v1/check_information_product', methods=['POST'])
def check_information_product(): 
    testcase = {
        "product": "ATS01", 
        "infos": [
            {
                "attribute": "S",
                "base_cost": "8",
                "US_ship": "5.4",
                "US_ship_add": "5.4",
                "EU_ship": "8.9",
                "EU_ship_add": "8.9",
                "ROW_ship": "12.86",
                "ROW_ship_add": "12.86",

            },
            {
                "attribute": "M",
                "base_cost": "8",
                "US_ship": "5.4",
                "US_ship_add": "5.4",
                "EU_ship": "8.9",
                "EU_ship_add": "8.9",
                "ROW_ship": "12.86",
                "ROW_ship_add": "12.86",
            },
            {
                "attribute": "L",
                "base_cost": "8",
                "US_ship": "5.4",
                "US_ship_add": "5.4",
                "EU_ship": "10.9",
                "EU_ship_add": "10.9",
                "ROW_ship": "14.71",
                "ROW_ship_add": "14.71",
            },
            {
                "attribute": "XL",
                "base_cost": "8",
                "US_ship": "5.4",
                "US_ship_add": "5.4",
                "EU_ship": "10.9",
                "EU_ship_add": "10.9",
                "ROW_ship": "14.71",
                "ROW_ship_add": "14.71",
            },
            {
                "attribute": "2XL",
                "base_cost": "8",
                "US_ship": "5.4",
                "US_ship_add": "5.4",
                "EU_ship": "10.9",
                "EU_ship_add": "10.9",
                "ROW_ship": "14.71",
                "ROW_ship_add": "14.71",
            },
            {
                "attribute": "3XL",
                "base_cost": "8",
                "US_ship": "5.4",
                "US_ship_add": "5.4",
                "EU_ship": "10.9",
                "EU_ship_add": "10.9",
                "ROW_ship": "14.71",
                "ROW_ship_add": "14.71",
            }
        ] 
    }
    result = check_information_product_process(testcase)
    return jsonify({"pass":result})

app.run()