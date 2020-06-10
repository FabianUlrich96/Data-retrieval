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
    filter_term = filter_csv[filter_column].str.contains(filter_select)
    filtered_python = filter_csv[filter_term]
    filter_file = filter_file + ".csv"
    if os.path.exists(filter_file):
        pass
    else:
        filtered_python.to_csv(filter_file)

    return filtered_python


def shorten_function(shorten_file, shorten_save):
    short_file = shorten_file[['Id', 'Tags']].copy()
    short_save = shorten_save + "_short.csv"
    short_file.to_csv(short_save)
    print("File successfully generated as: " + short_save)
    return short_save, shorten_file


def related_tag_function(related_shorten, related_save):
    related_shorten['Tags'] = related_shorten['Tags'].str.replace(">", "")
    split_date = related_shorten['Tags'].str.split("<")
    data = split_date.to_list()
    header = [1, 2, 3, 4, 5, 6]
    tag_df = pd.DataFrame(data, columns=header)
    new_df = tag_df[1].append(tag_df[2]).append(tag_df[3]).append(tag_df[4]).append(tag_df[5]).append(tag_df[6])
    col_name = ['Tags']
    total_tags_file = related_save + "_short.csv"
    new_df.to_csv(total_tags_file, header=col_name)
    CsvAction.delete_empty_rows(total_tags_file, "Tags")
    return total_tags_file


def count_total_function(file_path, new_path):
    data = pd.read_csv(file_path)
    header = ['Tags', 'Number_count']
    data['Tags'].value_counts().reset_index().to_csv(new_path, header=header)


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
    shorten_save, shorten_csv = shorten_function(csv_file, save_file)
    related_tag_function(shorten_csv, save_file)
    tag_combination = save_file + "_combination.csv"
    count_total_function(shorten_save, tag_combination)


if __name__ == "__main__":
    main()
