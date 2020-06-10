import pandas as pd
from UserSelection import UserSelection
from CsvAction import CsvAction


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
    CsvAction.shorten_function(selected_csv, save_file)
    CsvAction.delete_empty_rows(save_file + "_short.csv", "Tags")
    CsvAction.count_values(save_file + "_short.csv", "Tags", save_file + "_count.csv")


if __name__ == "__main__":
    main()
