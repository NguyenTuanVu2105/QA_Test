from constants import *

def get_url(prefix):
    return '{}{}'.format(HOST, prefix)

def get_auth(): 
    return EMAIL, PASSWORD

def read_file_by_lines(file_url):
    f = open(file_url, "r", encoding = "utf-8")
    lines = f.readlines()
    lines = [x.strip() for x in lines]
    f.close()
    return lines

# read_file_by_lines("products.txt")