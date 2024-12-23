import os
from lxml import etree

def apply_xslt(input_xml, xslt_path, output_html, module_filter):
    """
    Apply the XSLT transformation on the XML file with the provided filter.

    Args:
        input_xml (str): Path to the input XML file.
        xslt_path (str): Path to the XSLT file.
        output_html (str): Path to the output HTML file.
        module_filter (str): The module name to filter in the XSLT.
    """
    # Construct full paths using the base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Navigate to project root
    input_xml_path = os.path.join(base_dir, input_xml)
    xslt_path_full = os.path.join(base_dir, xslt_path)
    output_html_path = os.path.join(base_dir, output_html)
    students_xml_path = os.path.join(base_dir, 'data/output/xml/Students_GInf2.xml')
    
    # Debug prints
    print(f"Base directory: {base_dir}")
    print(f"Input XML path: {input_xml_path}")
    print(f"XSLT path: {xslt_path_full}")
    print(f"Output HTML path: {output_html_path}")
    print(f"Students XML path: {students_xml_path}")
    print(f"Module filter: {module_filter}")

    # Load the XML and XSLT
    try:
        dom = etree.parse(input_xml_path)
        print("XML loaded successfully.")

        xslt = etree.parse(xslt_path_full)
        print("XSLT loaded successfully.")

        transform = etree.XSLT(xslt)
        print("XSLT transformer created successfully.")

        # Apply the transformation with the parameters
        new_dom = transform(dom, 
                            moduleFilter=etree.XSLT.strparam(module_filter),
                            studentsFile=etree.XSLT.strparam(students_xml_path))
        print("Transformation applied successfully.")

        # Write the output HTML
        with open(output_html_path, 'wb') as f:
            f.write(etree.tostring(new_dom, pretty_print=True, method='html'))
        print(f"HTML report successfully generated at: {output_html_path}")

    except etree.XMLSyntaxError as e:
        print(f"XML Syntax Error: {e}")
    except etree.XSLTParseError as e:
        print(f"XSLT Parse Error: {e}")
    except etree.XSLTApplyError as e:
        print(f"XSLT Apply Error: {e}")
    except FileNotFoundError as e:
        print(f"File Not Found Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    apply_xslt(
        'data/output/xml/Notes_GInf2.xml',  # Input XML path
        'src/publication/xslt/GradesReport.xsl',  # XSLT path
        'data/output/html/GradesReport_GInf2.html',  # Output HTML path
        'GINF35 administration et programmation sys'  # Module filter
    )
