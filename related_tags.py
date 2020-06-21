import pandas as pd
import os.path
import sys
from UserSelection import UserSelection
from CsvAction import CsvAction



def input_filter():
    input_term = input("Enter the filter term: ")
    print(input_term)
    return input_term


def filter_function(filter_column, filter_select, filter_csv, filter_file):
    filter_select = "<" + filter_select + ">"
    filter_term = filter_csv[filter_column].str.contains(filter_select)
    filtered_python = filter_csv[filter_term]
    print(filtered_python)
    filter_file = filter_file + ".csv"
    if os.path.exists(filter_file):
        pass
    else:
        filtered_python.to_csv(filter_file)

    return filtered_python


def related_function(related_shorten, related_file):
    related_shorten = pd.read_csv(related_shorten)
    dropped_df = related_shorten.drop_duplicates(subset='Tags', keep="first", inplace=False)
    dropped_df = dropped_df.drop(dropped_df.index[0:1])
    related_tags_file = related_file + "_related_tags.csv"
    dropped_df.to_csv(related_tags_file, header=True)

    print("File successfully generated as: " + related_tags_file)

    return related_tags_file


def main():
    input_prompt = "Please enter the directory the .csv file is stored in. E.g. C:/Users/.../csv"
    selected_file = UserSelection.user_input(input_prompt)
    if UserSelection.check_input(selected_file):
        selected_filter = input_filter()
        save_file = UserSelection.save_name()
        selected_columns = "Tags"
        filtered_csv = pd.read_csv(selected_file)
    else:
        sys.exit(1)
    csv_file = filter_function(selected_columns, selected_filter, filtered_csv, save_file)
    csv_file[['Id', 'Tags']].to_csv("test1234.csv")
    short_save = CsvAction.shorten_function(csv_file, save_file)
    CsvAction.delete_empty_rows(short_save, "Tags")
    related_function(short_save, save_file)
    CsvAction.count_values(save_file + "_short.csv", "Tags", save_file + "_related_count.csv")


if __name__ == "__main__":
    main()
