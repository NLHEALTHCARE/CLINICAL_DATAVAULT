"""
Maakt een boomstructuur voor hl7rim_enums gebaseerd op Nictiz XML bestanden.

    Gebruik:
    Maak een csv bestand van nictiz xml file(s) met nictiz_process.py. Doe dit iedere keer in gedeeltes door in
    xml_parser_nictiz.py de regel "xml_refs = parser.xml_refs[20:30]" aan te passen. Run nictiz_proces.
    Run daarna enum_maker_nictiz.py.
    Kopieer de gewenste boomstructuur (en plaats deze bijvoorbeeld in hl7rim_enums.py).
    Let hierbij op het volgende: door de opbouw van de xml bestanden komen sommige boomstructuren vaker voor, let dus
    op dubbelingen.
    Let verder op dat sommige "leafs" niet direct onder de default van hetzelfde niveau komen te staan maar
    onderbroken worden door een "stem" op dat zelfde niveau. Corrigeer dit dan handmatig.
    Voorbeeld:
            class GeneticobservationinterpretationAbstractTypes:
                default = '_GeneticObservationInterpretation'
                carrier = 'CAR'
                ...
                class AbnormalTypes:
                    default = 'A'
                ...
                normal = 'N'

    In bovenstaand voorbeeld moet de regel met "normal = 'N'" verplaatst worden naar direct onder "carier' = 'CAR'.
"""

import os
import csv
import re

os.chdir('C:/!OntwikkelDATA/nictiz')


def set_attribute_name(string):
    """
    Een attribute naam mag alleen maar kleine letters hebben, geen leestekens bevatten en ipv spaties worden underscores
    gebruikt.

    """
    string = string.lower()
    string = string.replace("-", "_")  # voor behoud van leesbaarheid
    string = string.replace(" ", "_")
    for k in string:
        if k.isalpha() or k == "_":
            pass
        else:
            string = string.replace(k, "")
    return string


def set_class_name(string):
    """
    Een class naam is camelcased en bevat geen leestekens.

    """
    string = string.capitalize()
    if " " in string:
        string = string.title()  # .title() Capitalizes each word

    for j in string:
        if j.isalpha():
            pass
        else:
            string = string.replace(j, "")  # verwijdert leestekens en spaties
    return string

with open('valuesets.csv', newline='', encoding='UTF-8') as f:
    """ Loopt door alle regels van valuesets.csv en print vervolgens een boomstructuur uit van classes en properties die voor hl7rim_enums gebruikt
    zouden kunnen worden.
    ! Let op de gegevens staan soms dubbel in een XML document en daardoor ook in de genereerde boomstructuur.
    """
    r = csv.reader(f)
    data = []
    headers = ['temp_id', 'temp_fk', 'level', 'type', 'code', 'displayName', 'codeSystem', 'id', 'valueset', 'ingangsdatum', 'codestatus']
    indent = 4  # Python indentatie
    current_base_class = ''
    for (i, line) in enumerate(r):

        tempstr = str(line)  # line is een string
        tempstr = tempstr.strip("['")  # verwijdert 1e deel string
        tempstr = tempstr.strip("']")  # verwijdert 2e deel string
        tempstr2 = tempstr.replace('"', '')  # verwijdert de " indien aanwezig in de string, want deze geeft later een error doordat dit bijvoorbeeld een '4' verandert in '"4'
        tempstr2 = tempstr2.replace("', '", ",")

        templst = re.split(r";", tempstr2)  # maakt van resultaat een list; kolommen hebben vaste volgorde.

        if i >= 1:  # hierdoor sla je de header regel over dit voorkomt dat er later een error optreedt.
            if templst[0] == '0':  # Abstract/Stem

                if templst[1] != 'L':   # data met level 0 en type "L" bevat geen hierarchie: kan dus geskipped worden.
                    if current_base_class != str(templst[6]):  # waarde van column 'valueset'
                        current_base_class = templst[6]
                        print('')
                        print('')
                        print("class {}: ".format(set_class_name(templst[6])))  # dit is de naam van de valueset waaruit deze boomstructuur wordt opgebouwd.
                    print('')
                    if templst[1] == 'A':  # waarde van column 'type'
                        new_class = "class {}AbstractTypes:".format(set_class_name(templst[3]))  # waarde van column 'DisplayName'
                        print(''.ljust(indent + indent*int(templst[0])) + new_class)  # waarde van column 'level'
                        default = "default = '{}'".format(templst[2])  # waarde van column 'code'
                        print(''.ljust(2*indent + indent*int(templst[0])) + default)
                    elif templst[1] == 'S':
                        new_class = "class {}Types:".format(set_class_name(templst[3]))
                        print(''.ljust(indent + indent*int(templst[0])) + new_class)
                        default = "default = '{}'".format(templst[2])
                        print(''.ljust(2*indent + indent*int(templst[0])) + default)

            else:

                if templst[1] != 'L':
                    if templst[6] == "ICPC-1-2000NL":  # deze valueset bevat alleen (level 0 type L) en (level 1 type L)?!
                        pass
                    else:
                        print('')
                        if templst[1] == 'A':
                            new_class = "class {}AbstractTypes:".format(set_class_name(templst[3]))  # indien het een "Abstract" betreft plak "AbstractTypes" achter de class name
                            print(''.ljust(indent + indent*int(templst[0])) + new_class)
                        elif templst[1] == 'S':
                            new_class = "class {}Types:".format(set_class_name(templst[3])) # indien het een "Stem" betreft plak "Types" achter de class name
                            print(''.ljust(indent + indent*int(templst[0])) + new_class)

                        default = "default = '{}'".format(templst[2])
                        print(''.ljust(2*indent + indent*int(templst[0])) + default)

                else:
                    if templst[6] == "ICPC-1-2000NL":
                        pass
                    else:
                        leaf = "{} = '{}'".format(set_attribute_name(templst[3]), templst[2])
                        print(''.ljust(indent+indent*int(templst[0])) + leaf)
