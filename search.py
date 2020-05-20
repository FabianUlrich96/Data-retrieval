import xml.etree.ElementTree as ET
import csv
import glob
import os.path


def user_input():
    path = input("Please enter the directory the DataDump is stored in. E.g. C:/Users/.../DataDump")
    path.replace("\\", "/")
    data_directory = list(path)
    file_name = input("Please enter a file name:") + ".csv"
    return data_directory, file_name


def list_files(list_directory):
    list_directory.append("/*.xml")
    found_files = [os.path.basename(x) for x in glob.glob(''.join(list_directory))]
    list_directory.remove("/*.xml")
    print("Available Files: " + str(found_files))
    return found_files


def select_file(selected_directory):
    selected_input = input("Select a file by typing in the full file name plus extension (e.g. example.xml)\n")
    selected_directory.append("/" + selected_input)
    selected_append = ''.join(selected_directory)
    print(selected_append)
    selected_directory.remove("/" + selected_input)
    try:
        open(selected_append, "r")
    except FileNotFoundError:
        selected_append = False
        print("File does not exist")

    return selected_append


def structure_file():
    tree = ET.parse(selected_file)
    root = tree.getroot()
    tag = root.tag
    att = root.attrib
    print(root.tag)
    return root


def initialize_csv_file(search_file):
    # file for writing csv
    data = open(search_file, 'w', encoding='utf8', newline='')

    # csv writer object
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


def parse_file():
    csv_writer.writerow(search_terms)
    value = []
    for child in structure_root:
        for i in range(0, len(search_terms)):
            attribute = child.attrib.get(search_terms[i])

            if attribute:
                value.append(attribute)
            else:
                value.append("Empty")
            length_search_terms = int(len(search_terms))
            if i == length_search_terms - 1:
                csv_writer.writerow(value)
                print(value)
                value = []
    print("File successfully generated as: " + file)


directory, file = user_input()
available_files = list_files(directory)
selected_file = select_file(directory)

if selected_file is False:
    selected_file = select_file(directory)
else:
    structure_root = structure_file()
    print("Valid file selected")
csv_writer, data_file = initialize_csv_file(file)
search_terms = input_rows()
parse_file()
close_csv_file(data_file)
