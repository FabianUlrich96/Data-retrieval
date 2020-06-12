import pandas as pd
import sys
from UserSelection import UserSelection


def read_function(file_path):
    data = pd.read_csv(file_path)
    return data


# TRT = No. of mobile posts / Total No. of posts


def trt_function(mobile_number, total_number, save_path):
    try:
        try_1 = mobile_number['Number_count']
        try_2 = total_number['Number_count']
    except KeyError as key_error:
        print(sys.stderr, "Error: missing Keyword in column!")
        print(sys.stderr, "Exception: %s" % str(key_error))
        sys.exit(1)

    data_merged = pd.merge(mobile_number, total_number, on='Tags', how='inner', suffixes=['_1', '_2'])
    data_merged['Number_count'] = data_merged['Number_count_1'] / data_merged['Number_count_2']

    data_output = data_merged[['Tags', 'Number_count', 'Number_count_1']]
    header = ['Tags', 'TRT', 'Mobile_count']
    trt_save = save_path + "_TRT.csv"
    data_output = data_output.sort_values(by='Number_count', ascending=False)
    data_output.to_csv(trt_save, header=header, index=False)
    trt_file = pd.read_csv(trt_save)
    trt_file = trt_file[trt_file.TRT > 0.4]
    trt_file = trt_file[trt_file.TRT < 1]
    trt_file.to_csv(trt_save)
    print("File successfully generated as: " + trt_save)
    return trt_save
# TST = No. of mobile posts/ No. of mobile posts for the most popular tag


def tst_function(mobile_number, save_path):
    mobile_number = pd.read_csv(mobile_number)
    try:
        try_1 = mobile_number['Mobile_count']
    except KeyError as key_error:
        print(sys.stderr, "Error: missing Keyword in column!")
        print(sys.stderr, "Exception: %s" % str(key_error))
        sys.exit(1)
    # most popular tag = android
    popular_number_count = 27467

    i = 0
    tst_save = save_path + "_TST.csv"
    for index, row in mobile_number.iterrows():
        tags_row = row['Tags']
        number_row = row['Mobile_count']
        tst = number_row/popular_number_count
        related_columns = ['Tags', "TST"]

        temp_df = pd.DataFrame([[tags_row, tst]])

        if i == 0:
            empty_df = pd.DataFrame(data=None)
            empty_df.to_csv(tst_save, header=False)
            temp_df.to_csv(tst_save, mode='a', header=related_columns)
        else:
            temp_df.to_csv(tst_save, mode='a', header=False)
        i += 1

    sort_df = pd.read_csv(tst_save)
    sort_df = sort_df.sort_values(by='TST', ascending=False)
    sort_df.to_csv(tst_save)
    print("File successfully generated as: " + tst_save)


def main():
    input_prompt_1 = "Please select the file with count of MOBILE TAGS"
    selected_file_1 = UserSelection.user_input(input_prompt_1)
    input_prompt_2 = "Please select the file with the TOTAL count of tags"
    selected_file_2 = UserSelection.user_input(input_prompt_2)
    save_file = UserSelection.save_name()
    if UserSelection.check_input(selected_file_1) & UserSelection.check_input(selected_file_2):
        data_1 = read_function(selected_file_1)
        data_2 = read_function(selected_file_2)
        trt = trt_function(data_1, data_2, save_file)
        tst_function(trt, save_file)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
