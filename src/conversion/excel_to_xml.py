import pandas as pd
from lxml import etree
import os

def read_excel_to_xml(input_path, output_path, root_element, row_element):
    try:
        df = pd.read_excel(input_path)
        root = etree.Element(root_element)
        for _, row in df.iterrows():
            element = etree.SubElement(root, row_element)
            for col in df.columns:
                child = etree.SubElement(element, col.replace(' ', '_').replace('/', '_'))
                child.text = str(row[col] if not pd.isnull(row[col]) else '')
        tree = etree.ElementTree(root)
        tree.write(output_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        print(f"Successfully created {output_path}")
    except Exception as e:
        print(f"Failed to process {input_path}: {str(e)}")

def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    input_files = {
        'students': os.path.join(project_root, 'data/input/Students.xlsx'),
        'modules': os.path.join(project_root, 'data/input/Modules.xlsx'),
        'notes' : os.path.join(project_root, 'data/input/Notes.xlsx')
    }
    output_files = {
        'students': os.path.join(project_root, 'data/output/xml/Students_GInf2.xml'),
        'modules': os.path.join(project_root, 'data/output/xml/Modules_GInf2.xml'),
        'notes' : os.path.join(project_root, 'data/output/xml/Notes_GInf2.xml')
    }

    for key in input_files:
        read_excel_to_xml(input_files[key], output_files[key], 'Root', key.capitalize())

if __name__ == "__main__":
    main()
