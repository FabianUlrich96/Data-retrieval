import xml.etree.ElementTree as ET
import csv
from UserSelection import UserSelection


def structure_file(structure_selected):
    tree = ET.parse(structure_selected)
    root = tree.getroot()
    tag = root.tag
    att = root.attrib
    print(root.tag)
    return root


def initialize_csv_file(search_file):
    data = open(search_file, 'w', encoding='utf8', newline='')
    writer = csv.writer(data)
    search_head = []
    return writer, data


def close_csv_file(csv_file):
    csv_file.close()


def input_rows():
    input_string = input("Enter search terms to be extracted:")
    terms = input_string.split()
    print(terms)
    return terms


def parse_file(parse_save, parse_writer, parse_search, parse_root):
    parse_writer.writerow(parse_search)
    value = []
    for child in parse_root:
        for i in range(0, len(parse_search)):
            attribute = child.attrib.get(parse_search[i])

            if attribute:
                value.append(attribute)
            else:
                value.append("Empty")
            length_search_terms = int(len(parse_search))
            if i == length_search_terms - 1:
                parse_writer.writerow(value)
                print(value)
                value = []
    print("File successfully generated as: " + parse_save)


def main():
    input_prompt = "Please enter the directory the DataDump is stored in. E.g. C:/Users/.../DataDump"
    selected_file, file = UserSelection.user_input(input_prompt)

    structure_root = structure_file(selected_file)
    csv_writer, data_file = initialize_csv_file(file)
    search_terms = input_rows()
    parse_file(file, csv_writer, search_terms, structure_root)
    close_csv_file(data_file)


if __name__ == "__main__":
    main()
