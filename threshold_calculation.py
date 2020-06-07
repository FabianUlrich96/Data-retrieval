import pandas as pd
from filter_tags import user_input
from filter_tags import list_files
from filter_tags import select_file


def read_function(file_path):
    data = pd.read_csv(file_path)
    return data


# TRT = No. of mobile posts / Total No. of posts


def trt_function(mobile_number, total_number, save_path):
    data_merged = pd.merge(mobile_number, total_number, on='Tags', how='inner', suffixes=['_1', '_2'])
    data_merged['Number_count'] = data_merged['Number_count_1'] / data_merged['Number_count_2']
    data_output = data_merged[['Tags', 'Number_count']]
    header = ['Tags', 'TRT']
    data_output.to_csv(save_path + "_TRT.csv", header=header, index=False)


# TST = No. of mobile posts/ No. of mobile posts for the most popular tag


def tst_function(mobile_number, save_path):
    popular_number_count = mobile_number['Number_count'].argmax()
    popular_number = mobile_number.loc[[popular_number_count]]
    #header = ['Tags', 'TST']
    i = 0
    popular_number_count = popular_number['Number_count'].values[0]

    for index, row in mobile_number.iterrows():
        tags_row = row['Tags']
        number_row = row['Number_count']
        tst = number_row/popular_number_count
        related_columns = ['Tags', "TST"]

        temp_df = pd.DataFrame([[tags_row, tst]])

        if i == 0:
            empty_df = pd.DataFrame(data=None)
            empty_df.to_csv(save_path + "_TST.csv", header=False)
            temp_df.to_csv(save_path + "_TST.csv", mode='a', header=related_columns)
        else:
            temp_df.to_csv(save_path + "_TST.csv", mode='a', header=False)
        i += 1


def main():
    directory, save_name = user_input()
    list_files(directory)
    selected_file_1 = select_file(directory)
    selected_file_2 = select_file(directory)
    data_1 = read_function(selected_file_1)
    data_2 = read_function(selected_file_2)
    trt_function(data_1, data_2, save_name)
    tst_function(data_1, save_name)


if __name__ == "__main__":
    main()
