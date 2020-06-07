import pandas as pd
import sys
from UserSelection import UserSelection


def merge_function(file_path, file_path_2, save_path):
    data_1 = pd.read_csv(file_path, index_col=0)
    data_2 = pd.read_csv(file_path_2, index_col=0)
    try:
        try_1 = data_1['Tags']
        try_2 = data_2['Tags']
    except KeyError as key_error:
        print(sys.stderr, "Error: missing Keyword in column!")
        print(sys.stderr, "Exception: %s" % str(key_error))
        sys.exit(1)

    data_merged = pd.merge(data_1, data_2, on='Tags', how='inner', suffixes=['_1', '_2'])
    data_merged['Number_count'] = data_merged['Number_count_1'] + data_merged['Number_count_2']
    data_output = data_merged[['Tags', 'Number_count']]
    save_path_csv = save_path + ".csv"
    data_output.to_csv(save_path_csv, header=True, index=False)
    print("File successfully generated as: " + save_path_csv)


def main():
    input_prompt_1 = "Please select the FIRST tag_count file to be merged"
    selected_file_1 = UserSelection.user_input(input_prompt_1)
    input_prompt_2 = "Please select the SECOND tag_count file to be merged"
    selected_file_2 = UserSelection.user_input(input_prompt_2)
    save_file = UserSelection.save_name()
    if UserSelection.check_input(selected_file_1) & UserSelection.check_input(selected_file_2):
        merge_function(selected_file_1, selected_file_2, save_file)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
