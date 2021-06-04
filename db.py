import sqlite3 

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_product():
    conn = sqlite3.connect('testcase.db', 10)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    products = cur.execute('SELECT * FROM Product;').fetchall()
    conn.close()
    return products

def delete_product():
    conn = sqlite3.connect('testcase.db', 10)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute("Delete from Product;")
    cur.execute("Delete from ProductSide;")
    cur.execute("Delete from SideMockupSampleTestcase;")
    cur.execute("Delete from SizePriceSampleTestcase;")
    cur.execute("Delete from MockupSampleTestcase;")
    cur.execute("Delete from PriceSampleTestcase;")
    conn.commit()
    conn.close()
    return products

def create_products(products):
    conn = sqlite3.connect('testcase.db', 10)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    sql_insert = "INSERT INTO Product VALUES "
    sql_insert_sides = "INSERT INTO ProductSide(name, product_id) VALUES "
    values = ""
    sides_value = ""
    for i in range(len(products)):
        product = products[i]
        value = "({}, '{}', '{}', '{}')".format(i+1, product['name'], product['sku'], product['image'])
        values = values + value + ','
        for side in product['sides']: 
            side_value = "('{}', {})".format(side, i+1)
            sides_value = sides_value + side_value + ','
    values = values[:-1] 
    sides_value = sides_value[:-1]
    sql_insert = sql_insert + values +  ";"
    sql_insert_sides = sql_insert_sides + sides_value + ";"
    print(sql_insert)
    print(sql_insert_sides)
    cur.execute(sql_insert)
    cur.execute(sql_insert_sides)
    conn.commit()
    conn.close()
    return True

