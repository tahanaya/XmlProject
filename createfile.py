import pandas as pd
import numpy as np

# List of student IDs
students = [
    "21010395", "21010278", "21011326", "21010358", "21010266", "20001758",
    "21010287", "21010482", "21009157", "21010356", "21010411", "21010476",
    "22012817", "21009110", "21011779", "20011005", "21002603", "21010261",
    "21011724", "21009025", "21010326", "21010299", "21009475", "21010439",
    "21010403", "21010379", "21010272", "21010324", "20007042", "21010274",
    "21010319", "19006658", "21010322", "22012491", "21010441", "21010423",
    "20007896", "17004026", "21011787", "21010306", "19005680", "21010320",
    "21010359", "21010334", "21010011", "21010368", "20009973", "21010231",
    "21011780", "20000927", "20000104", "21010740", "21010291", "21011784",
    "21010332", "20007695", "21010401", "21009322", "21011667", "21010348",
    "21010242", "21015477", "20001713", "21010255", "21011615", "21010409"
]

# Module elements based on the XML data provided
module_elements = {
    "GINF31 Programmation oriente objet et XML": ["Programation orientee objet en JAVA", "XML et Applications"],
    "GINF32 qualite et approche processus": ["assurance contrôle qualite", "cycle de vie logiciel", "maitrise et optimisation des processus"],
    "GINF33 modelisation oriente objet et IHM": ["modelisation UML", "interaction homme machine"],
    "GINF34 bases de donnees avancees 1": ["optimisation et qualite de base de donnees", "administration et securite des bases de donnees", "bases de donnees NOSQL"],
    "GINF35 administration et programmation sys": ["administration systeme", "programmation systeme"],
    "GINF36 langues et communication 2": ["espagnol 2 et allemand", "anglais pro", "technique de communication"],
    "GINF41 technologies distribuees": ["intro a JEE", "programmation C#"],
    "GINF42 bases de donnees avancees 2 et cloud": ["gestion des donnes complexes", "gestion des donnees distribuees", "cloud computing et infogerance"],
    "GINF43 traitement de l image": ["traitement d image", "vision numerique", "processus stochastique"],
    "GINF44 programmation declarative et TAV": ["programmation declarative", "technique algorithmique avancee"],
    "GINF45 securite et cryptographie": ["securite des systemes", "cryptographie"],
    "GINF46 management de l entreprise 2": ["economie et compta 2", "projets collectif et stages", "management de projet"]
}

# Set reproducibility
np.random.seed(0)

# Generate grades data with element-specific
grades_data = {
    'StudentID': [],
    'ModuleName': [],
    'ElementName': [],
    'Grade': []
}

for student in students:
    for module, elements in module_elements.items():
        for element in elements:
            grades_data['StudentID'].append(student)
            grades_data['ModuleName'].append(module)
            grades_data['ElementName'].append(element)
            grades_data['Grade'].append(np.random.randint(0, 21))  # Random grade between 0 and 20

# Creating a DataFrame
grades_df = pd.DataFrame(grades_data)

# Save to Excel without an index column
grades_df.to_excel('Notess.xlsx', index=False)
