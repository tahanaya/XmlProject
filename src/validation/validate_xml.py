from lxml import etree

def validate_xml(xml_path, schema_path, is_dtd=True):
    try:
        xml_doc = etree.parse(xml_path)
        if is_dtd:
            dtd = etree.DTD(open(schema_path))
            valid = dtd.validate(xml_doc)
        else:
            schema_doc = etree.parse(schema_path)
            schema = etree.XMLSchema(schema_doc)
            valid = schema.validate(xml_doc)
        
        if valid:
            print(f"{xml_path} validates against {schema_path}")
        else:
            print(f"{xml_path} fails to validate against {schema_path}")
            print(dtd.error_log.filter_from_errors() if is_dtd else schema.error_log.filter_from_errors())
    except Exception as e:
        print(f"Validation error: {e}")

# Example usage
if __name__ == "__main__":
    # Paths need to be adjusted based on actual file locations
   # validate_xml('../../data/output/xml/Students_GInf2.xml', '../../data/schemas/Students.dtd')
   # validate_xml('../../data/output/xml/Students_GInf2.xml', '../../data/schemas/Students.xsd', is_dtd=False)
    # Add these lines to the existing script to test Modules validation
 #
 #  validate_xml('../../data/output/xml/Modules_GInf2.xml', '../../data/schemas/Modules.dtd')
  #validate_xml('../../data/output/xml/Modules_GInf2.xml', '../../data/schemas/Modules.xsd', is_dtd=False)
  # Example usage
   validate_xml('../../data/output/xml/Notes_GInf2.xml', '../../data/schemas/Notes.dtd')
   validate_xml('../../data/output/xml/Notes_GInf2.xml', '../../data/schemas/Notes.xsd', is_dtd=False)