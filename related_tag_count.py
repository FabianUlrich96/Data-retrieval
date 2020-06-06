import pandas as pd
from filter_tags import user_input
from filter_tags import list_files
from filter_tags import select_file


def merge_function(file_path, file_path_2, save_path):
    data_1 = pd.read_csv(file_path, index_col=0)
    data_2 = pd.read_csv(file_path_2, index_col=0)
    data_merged = pd.merge(data_1, data_2, on='Tags', how='inner', suffixes=['_1', '_2'])
    data_merged['Number_count'] = data_merged['Number_count_1'] + data_merged['Number_count_2']
    data_output = data_merged[['Tags', 'Number_count']]
    data_output.to_csv(save_path + ".csv", header=True, index=False)


def main():
    directory, save_name = user_input()
    list_files(directory)
    selected_file_1 = select_file(directory)
    selected_file_2 = select_file(directory)

    merge_function(selected_file_1, selected_file_2, save_name)


if __name__ == "__main__":
    main()
