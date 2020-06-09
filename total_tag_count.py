import pandas as pd
from UserSelection import UserSelection
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

    print("File successfully generated as: " + new_path)


def main():
    input_prompt = "Please enter the directory the .csv file is stored in. E.g. C:/Users/.../csv"
    selected_file = UserSelection.user_input(input_prompt)
    save_file = UserSelection.save_name()
    print(selected_file)
    selected_csv = pd.read_csv(selected_file)
    short_csv = shorten_function(selected_csv, save_file)
    total_tags_function(short_csv, save_file)
    delete_empty_rows(save_file + "_short.csv")

    count_total_function(save_file + "_short.csv", save_file + "_count.csv")


if __name__ == "__main__":
    main()
