import pandas as pd
import os.path
import sys
import re
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
    short_file['Tags'] = short_file['Tags'].str.replace(">", "")
    split_date = short_file['Tags'].str.split("<")
    data = split_date.to_list()
    header = [1, 2, 3, 4, 5, 6]
    tag_df = pd.DataFrame(data, columns=header)
    new_df = tag_df[1].append(tag_df[2]).append(tag_df[3]).append(tag_df[4]).append(tag_df[5]).append(tag_df[6])
    col_name = ['Tags']
    total_tags_file = short_save
    new_file = new_df.to_csv(total_tags_file, header=col_name)

    print("File successfully generated as: " + short_save)
    return short_save


def related_function(related_shorten, related_file):
    related_shorten = pd.read_csv(related_shorten)

    dropped_df = related_shorten.drop_duplicates(keep="first", inplace=False)
    dropped_df = dropped_df.drop(dropped_df.index[0:1])
    col_name = ['Tags']
    related_tags_file = related_file + "_related_tags.csv"
    dropped_df.to_csv(related_tags_file, header=True)

    print("File successfully generated as: " + related_tags_file)

    return related_tags_file


def number_function(related_save, related_tags):
    related_csv = pd.read_csv(related_save + ".csv")
    related_output = related_save + "_related_number"
    related_output_csv = related_output + ".csv"
    header = ["Index", "Tags"]
    related_tag_df = pd.DataFrame(related_csv, columns=header)
    column_related = header[1]

    tags_file = pd.read_csv(related_tags)
    tags_file_df = pd.DataFrame(tags_file, columns=header)
    i = 0
    for index, row in tags_file_df.iterrows():
        filter_related = re.escape(str(row['Tags']))
        related_df = filter_function(column_related, filter_related, related_tag_df, related_output)
        related_rows = related_df['Tags'].value_counts()
        related_columns = ['Tags', "Number_count"]
        temp_df = pd.DataFrame([[filter_related, related_rows]])

        if i == 0:
            empty_df = pd.DataFrame(data=None)
            empty_df.to_csv(related_output_csv, header=False)
            temp_df.to_csv(related_output_csv, mode='a', header=related_columns)
        else:
            temp_df.to_csv(related_output_csv, mode='a', header=False)
        i += 1

    print("File successfully generated as: " + related_output_csv)


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
    short_save = shorten_function(csv_file, save_file)
    CsvAction.delete_empty_rows(short_save, "Tags")
    related_tags_file = related_function(short_save, save_file)
    number_function(save_file, related_tags_file)


if __name__ == "__main__":
    main()
