import os
from lxml import etree
from weasyprint import HTML

def get_available_modules(modules_xml_path):
    """
    Parse the Modules_GInf2.xml file and return a list of module names.

    Args:
        modules_xml_path (str): Path to Modules_GInf2.xml

    Returns:
        list: List of module names
    """
    try:
        print(f"Parsing {modules_xml_path}...")
        tree = etree.parse(modules_xml_path)
        root = tree.getroot()
        modules = root.findall('.//Modules/MODULENAME')
        module_names = [module.text for module in modules if module.text]
        print(f"Modules trouvés: {module_names}")
        return module_names
    except etree.XMLSyntaxError as e:
        print(f"Erreur de syntaxe XML dans {modules_xml_path}: {e}")
    except FileNotFoundError:
        print(f"Fichier non trouvé: {modules_xml_path}")
    except Exception as e:
        print(f"Erreur inattendue lors de la lecture de {modules_xml_path}: {e}")
    return []

def select_module(module_names):
    """
    Display a list of modules and prompt the user to select one.

    Args:
        module_names (list): List of module names

    Returns:
        str: Selected module name
    """
    if not module_names:
        print("Aucun module disponible pour la sélection.")
        return None

    print("\nModules Disponibles:")
    for idx, module in enumerate(module_names, start=1):
        print(f"{idx}. {module}")

    while True:
        try:
            choice = int(input("\nEntrez le numéro du module que vous souhaitez sélectionner: "))
            if 1 <= choice <= len(module_names):
                selected_module = module_names[choice - 1]
                print(f"Module sélectionné: {selected_module}")
                return selected_module
            else:
                print(f"Veuillez entrer un numéro entre 1 et {len(module_names)}.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un numéro.")

def apply_xslt(input_xml_path, xslt_path, module_filter):
    """
    Apply the XSLT transformation on the XML file with the provided filter.

    Args:
        input_xml_path (str): Path to the input XML file (Notes_GInf2.xml)
        xslt_path (str): Path to the XSLT file (GradesReport.xsl)
        module_filter (str): The module name to filter in the XSLT

    Returns:
        str: Generated HTML content as a string
    """
    try:
        print(f"Chargement du fichier XML: {input_xml_path}")
        dom = etree.parse(input_xml_path)
        print(f"Chargement du fichier XSLT: {xslt_path}")
        xslt = etree.parse(xslt_path)
        transform = etree.XSLT(xslt)

        print(f"Application de la transformation XSLT avec le filtre module: {module_filter}")
        new_dom = transform(dom, moduleFilter=etree.XSLT.strparam(module_filter))

        html_content = etree.tostring(new_dom, pretty_print=True, method='html').decode('utf-8')
        print("Transformation XSLT réussie.")
        return html_content

    except etree.XMLSyntaxError as e:
        print(f"Erreur de syntaxe XML: {e}")
    except etree.XSLTParseError as e:
        print(f"Erreur lors de l'analyse du XSLT: {e}")
    except etree.XSLTApplyError as e:
        print(f"Erreur lors de l'application du XSLT: {e}")
    except FileNotFoundError as e:
        print(f"Fichier non trouvé: {e}")
    except Exception as e:
        print(f"Erreur inattendue: {e}")
    return None

def generate_pdf_from_html(html_content, output_pdf_path):
    """
    Convert HTML content to PDF using WeasyPrint.

    Args:
        html_content (str): HTML content as a string
        output_pdf_path (str): Path to save the generated PDF
    """
    try:
        print(f"Génération du PDF à partir du HTML...")
        HTML(string=html_content).write_pdf(output_pdf_path)
        print(f"PDF généré avec succès : {output_pdf_path}")
    except Exception as e:
        print(f"Erreur lors de la génération du PDF: {e}")

def main():
    # Définir les chemins relatifs par rapport au script Python
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # XmlCourseProject/
    modules_xml = os.path.join(base_dir, 'data', 'output', 'xml', 'Modules_GInf2.xml')
    notes_xml = os.path.join(base_dir, 'data', 'output', 'xml', 'Notes_GInf2.xml')
    xslt_file = os.path.join(base_dir, 'src', 'publication', 'xslt', 'GradesReport.xsl')
    html_output_dir = os.path.join(base_dir, 'data', 'output', 'html')
    pdf_output_dir = os.path.join(base_dir, 'data', 'output', 'pdf')

    # Créer les répertoires de sortie s'ils n'existent pas
    os.makedirs(html_output_dir, exist_ok=True)
    os.makedirs(pdf_output_dir, exist_ok=True)

    # Récupérer les modules disponibles
    modules = get_available_modules(modules_xml)

    # Sélectionner un module
    selected_module = select_module(modules)
    if not selected_module:
        return

    # Définir le nom des fichiers de sortie HTML et PDF
    # Remplacer les espaces et caractères spéciaux dans le nom du module pour le nom de fichier
    safe_module_name = "".join(c if c.isalnum() else "_" for c in selected_module)
    output_html = os.path.join(html_output_dir, f"GradesReport_{safe_module_name}.html")
    output_pdf = os.path.join(pdf_output_dir, f"GradesReport_{safe_module_name}.pdf")

    # Appliquer la transformation XSLT pour générer le HTML
    html_content = apply_xslt(notes_xml, xslt_file, selected_module)
    if not html_content:
        print("La génération du HTML a échoué. Le PDF ne sera pas généré.")
        return

    # Enregistrer le rapport HTML
    try:
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"\nRapport HTML généré avec succès : {output_html}")
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier HTML : {e}")
        return

    # Convertir le HTML en PDF
    generate_pdf_from_html(html_content, output_pdf)

if __name__ == "__main__":
    main()
