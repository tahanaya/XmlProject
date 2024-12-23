import os
from lxml import etree

def get_available_modules(modules_xml_path):
    """
    Parse the Modules_GInf2.xml file and return a list of module names.

    Args:
        modules_xml_path (str): Path to Modules_GInf2.xml

    Returns:
        list: List of module names
    """
    try:
        tree = etree.parse(modules_xml_path)
        root = tree.getroot()
        modules = root.findall('.//Modules/MODULENAME')
        module_names = [module.text for module in modules if module.text]
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

def apply_xslt(input_xml_path, xslt_path, output_html_path, module_filter):
    """
    Apply the XSLT transformation on the XML file with the provided filter.

    Args:
        input_xml_path (str): Path to the input XML file (Notes_GInf2.xml)
        xslt_path (str): Path to the XSLT file (GradesReport.xsl)
        output_html_path (str): Path to the output HTML file
        module_filter (str): The module name to filter in the XSLT
    """
    try:
        # Charger le XML et le XSLT
        dom = etree.parse(input_xml_path)
        xslt = etree.parse(xslt_path)
        transform = etree.XSLT(xslt)

        # Appliquer la transformation avec le paramètre moduleFilter
        new_dom = transform(dom, moduleFilter=etree.XSLT.strparam(module_filter))

        # Écrire le résultat dans le fichier HTML
        with open(output_html_path, 'wb') as f:
            f.write(etree.tostring(new_dom, pretty_print=True, method='html'))

        print(f"\nRapport HTML généré avec succès : {output_html_path}")

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

def main():
    # Définir les chemins relatifs par rapport au script Python
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # XmlCourseProject/
    modules_xml = os.path.join(base_dir, 'data', 'output', 'xml', 'Modules_GInf2.xml')
    notes_xml = os.path.join(base_dir, 'data', 'output', 'xml', 'Notes_GInf2.xml')
    xslt_file = os.path.join(base_dir, 'src', 'publication', 'xslt', 'GradesReport.xsl')
    html_output_dir = os.path.join(base_dir, 'data', 'output', 'html')

    # Créer le répertoire de sortie HTML s'il n'existe pas
    os.makedirs(html_output_dir, exist_ok=True)

    # Récupérer les modules disponibles
    modules = get_available_modules(modules_xml)

    # Sélectionner un module
    selected_module = select_module(modules)
    if not selected_module:
        return

    # Définir le nom du fichier de sortie HTML
    # Remplacer les espaces et caractères spéciaux dans le nom du module pour le nom de fichier
    safe_module_name = "".join(c if c.isalnum() else "_" for c in selected_module)
    output_html = os.path.join(html_output_dir, f"GradesReport_{safe_module_name}.html")

    # Appliquer la transformation XSLT
    apply_xslt(notes_xml, xslt_file, output_html, selected_module)

if __name__ == "__main__":
    main()
