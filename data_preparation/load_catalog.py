import xml.etree.ElementTree as ET
import pandas as pd

def xml_to_csv(xml_file, csv_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    rows = []
    for product in root.findall('.//product'):
        row = {'id': product.attrib['id']}
        for attr in product:
            tag = attr.tag
            text = attr.text.strip() if attr.text else ''
            row[tag] = text
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(csv_file, index=False, encoding = 'utf-8')

xml_to_csv('/Users/polina/PycharmProjects/Prefix-Search-Ranking/data/catalog_products_new.xml', '/Users/polina/PycharmProjects/Prefix-Search-Ranking/data/catalog_products.csv')
