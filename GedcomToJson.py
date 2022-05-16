from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser
import re


def get_element_name(element):
    (first, last) = element.get_name()
    return first + " " + last


def get_element_id(element):
    return int(element.get_pointer().split('I')[1].split('@')[0])


def get_element_gender(element):
    if element.get_gender() == 'M':
        gender = 'male'
    else:
        gender = 'female'
    return gender


def get_element_short_name(element):
    (first, last) = element.get_name()
    return first[0] + last[0]


class GedcomToJsonParser:
    json = []

    def __init__(self, file_path):
        self.gedcom_parser = Parser()
        self.gedcom_parser.parse_file(file_path)

    def get_json(self):
        root_child_elements = self.gedcom_parser.get_root_child_elements()

        for element in root_child_elements:
            if isinstance(element, IndividualElement):
                person = {}
                person.update({'id': get_element_id(element)})
                pids = self.get_element_spouses_ids(element)
                if pids:
                    person.update({'pids': pids})
                person.update({'cids': self.get_element_children(element)})
                person.update({'name': get_element_name(element)})
                person.update({'gender': get_element_gender(element)})
                person.update({'shortname': get_element_short_name(element)})
                self.json.append(person)

        for element in root_child_elements:
            if isinstance(element, IndividualElement):
                self.add_parents(element)

        for person in self.json:
            person.pop('cids')

        return self.json



    def get_element_spouses_ids(self, element):
        spouses_ids = []
        for family in self.gedcom_parser.get_families(element):
            gedcom_string = family.to_gedcom_string(recursive=True)
            spouse = ''
            if element.get_gender() == 'M':
                spouse = gedcom_string.split('WIFE @I')[1].split('@')[0]
                # print(gedcom_string.split('WIFE @I')[1].split('@')[0])
            if element.get_gender() == 'F':
                spouse = gedcom_string.split('HUSB @I')[1].split('@')[0]
                # print(gedcom_string.split('HUSB @I')[1].split('@')[0])
            spouses_ids.append(int(spouse))
        return spouses_ids

    def get_element_mother_id(self, element):
        mother = ''
        element_id = get_element_id(element)
        for family in self.gedcom_parser.get_families(element):
            family_children = self.get_element_children(family)
            if element_id in family_children:
                gedcom_string = family.to_gedcom_string(recursive=True)
                mother = gedcom_string.split('WIFE @I')[1].split('@')[0]
        return mother

    def get_element_children(self, element):
        children = []
        for family in self.gedcom_parser.get_families(element):
            gedcom_string = family.to_gedcom_string(recursive=True)
            children += [int(child) for child in re.findall(r'(?<=CHIL @I)\d+', gedcom_string)]
        return children

    def add_parents(self, element):
        for child_id in self.get_element_children(element):
            if element.get_gender() == 'M':
                self.json[child_id - 1].update({'fid': get_element_id(element)})
            if element.get_gender() == 'F':
                self.json[child_id - 1].update({'mid': get_element_id(element)})





