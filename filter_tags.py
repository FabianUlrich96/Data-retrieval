import pandas as pd
import glob
import os.path
import re


def user_input():
    path = input("Please enter the directory the .csv file is stored in. E.g. C:/Users/.../csv")
    path.replace("\\", "/")
    data_directory = list(path)
    file_name = input("Please enter a file name:")
    return data_directory, file_name


def list_files(list_directory):
    list_directory.append("/*.csv")
    found_files = [os.path.basename(x) for x in glob.glob(''.join(list_directory))]
    list_directory.remove("/*.csv")
    print("Available Files: " + str(found_files))
    return found_files


def select_file(selected_directory):
    selected_input = input("Please select a posts file plus extension (e.g. posts.csv)\n")
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
    new_file = shorten_file[['Id', 'Tags']].copy()
    new_file.to_csv(shorten_save + "_short.csv")
    return new_file


def related_function(related_shorten, related_file, tag_identifier):
    related_shorten['Tags'] = related_shorten['Tags'].str.replace(">", "")
    split_data = related_shorten["Tags"].str.split("<")
    data = split_data.to_list()
    header = [1, 2, 3, 4, 5, 6]
    tag_df = pd.DataFrame(data, columns=header)
    new_df = tag_df[1].append(tag_df[2]).append(tag_df[3]).append(tag_df[4]).append(tag_df[5]).append(tag_df[6])

    dropped_df = new_df.drop_duplicates(keep="first", inplace=False)
    dropped_df = dropped_df.drop(dropped_df.index[0:1])
    col_name = ['Tags']
    related_tags_file = related_file + "_" + tag_identifier + "_tags.csv"
    dropped_df.to_csv(related_tags_file, header=col_name)

    return related_tags_file


def number_function(related_save, related_tags, number_identifier):
    related_csv = pd.read_csv(related_save + ".csv")
    related_output = related_save + "_" + number_identifier + "_number"
    header = ["Index", "Tags"]
    related_tag_df = pd.DataFrame(related_csv, columns=header)
    column_related = header[1]

    tags_file = pd.read_csv(related_tags)
    tags_file_df = pd.DataFrame(tags_file, columns=header)
    i = 0
    for index, row in tags_file_df.iterrows():
        filter_related = re.escape(str(row['Tags']))
        related_df = filter_function(column_related, filter_related, related_tag_df, related_output)
        related_rows = related_df.count()
        related_columns = ['Tags', "Number_count"]
        temp_df = pd.DataFrame([[filter_related, related_rows['Tags']]])

        if i == 0:
            empty_df = pd.DataFrame(data=None)
            empty_df.to_csv(related_output + ".csv", header=False)
            temp_df.to_csv(related_output + ".csv", mode='a', header=related_columns)
        else:
            temp_df.to_csv(related_output + ".csv", mode='a', header=False)
        i += 1


def main():
    directory, save_file = user_input()
    list_files(directory)
    selected_file = select_file(directory)
    selected_columns = "Tags"
    selected_filter = input_filter()
    filtered_csv = pd.read_csv(selected_file)
    csv_file = filter_function(selected_columns, selected_filter, filtered_csv, save_file)
    shorten_csv = shorten_function(csv_file, save_file)

    related = "related"
    related_tags_file = related_function(shorten_csv, save_file, related)
    number_function(save_file, related_tags_file, related)


if __name__ == "__main__":
    main()
