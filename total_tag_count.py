import pandas as pd
from filter_tags import user_input
from filter_tags import list_files
from filter_tags import select_file
from filter_tags import shorten_function


def total_tags_function(count_shorten, count_name):
    count_shorten['Tags'] = count_shorten['Tags'].str.replace(">", "")
    split_date = count_shorten['Tags'].str.split("<")
    data = split_date.to_list()
    header = [1, 2, 3, 4, 5, 6]
    tag_df = pd.DataFrame(data, columns=header)
    new_df = tag_df[1].append(tag_df[2]).append(tag_df[3]).append(tag_df[4]).append(tag_df[5]).append(tag_df[6])
    col_name = ['Tags']
    total_tags_file = count_name + "_short.csv"
    new_df.to_csv(total_tags_file, header=col_name)

    return total_tags_file


def delete_empty_rows(file_path):
    data = pd.read_csv(file_path)
    data.dropna(subset=["Tags"], inplace=True)
    tag_names = data[data['Tags'] == 'Empty'].index
    data.drop(tag_names, inplace=True)
    data = data[['Tags']]
    data.to_csv(file_path, header=True)


def count_total_function(file_path, new_path):
    data = pd.read_csv(file_path)
    header = ['Tags', 'Number_count']
    data['Tags'].value_counts().reset_index().to_csv(new_path, header=header)


def main():
    directory, save_name = user_input()
    list_files(directory)
    selected_file = select_file(directory)
    print(selected_file)
    selected_csv = pd.read_csv(selected_file)
    short_csv = shorten_function(selected_csv, save_name)
    total_tags_function(short_csv, save_name)
    delete_empty_rows(save_name + "_short.csv")

    count_total_function(save_name + "_short.csv", save_name + "_count.csv")


if __name__ == "__main__":
    main()
