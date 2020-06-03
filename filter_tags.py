import pandas as pd
import glob
import os.path


def user_input():
    path = input("Please enter the directory the .csv file is stored in. E.g. C:/Users/.../csv")
    path.replace("\\", "/")
    data_directory = list(path)
    file_name = input("Please enter a file name:") + ".csv"
    return data_directory, file_name


def list_files(list_directory):
    list_directory.append("/*.csv")
    found_files = [os.path.basename(x) for x in glob.glob(''.join(list_directory))]
    list_directory.remove("/*.csv")
    print("Available Files: " + str(found_files))
    return found_files


def select_file(selected_directory):
    selected_input = input("Select a file by typing in the full file name plus extension (e.g. example.csv)\n")
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


def input_cols():
    input_string = input("Enter the columns to be extracted: ")
    print(input_string)
    return input_string


def input_filter():
    input_term = input("Enter the filter term: ")
    print(input_term)
    return input_term


def filter_function(filter_column, filter_select, filter_csv, filter_file):
    filter_term = filter_csv[filter_column].str.contains(filter_select)
    filtered_python = filter_csv[filter_term]
    #print(filtered_python)
    filtered_python.to_csv(filter_file)
    return filtered_python

def main():
    directory, save_file = user_input()
    list_files(directory)
    selected_file = select_file(directory)
    selected_columns = input_cols()
    selected_filter = input_filter()
    filtered_csv = pd.read_csv(selected_file)
    csv_file = filter_function(selected_columns, selected_filter, filtered_csv, save_file)

    tags = csv_file['Tags']
    print(tags)


if __name__ == "__main__":
    main()
