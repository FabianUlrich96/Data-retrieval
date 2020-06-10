import pandas as pd


class CsvAction:
    @staticmethod
    def delete_empty_rows(file_path, row):
        data = pd.read_csv(file_path)
        data.dropna(subset=[row], inplace=True)
        tag_names = data[data[row] == 'Empty'].index
        data.drop(tag_names, inplace=True)
        data = data[[row]]
        data.to_csv(file_path, header=True)

    @staticmethod
    def count_values(file_path, column, new_path):
        data = pd.read_csv(file_path)
        header = ['Tags', 'Number_count']
        data['Tags'].value_counts().sort_values(ascending=False).reset_index().to_csv(new_path, header=header)

        print("File successfully generated as: " + new_path)

    @staticmethod
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
        new_df.to_csv(total_tags_file, header=col_name)

        print("File successfully generated as: " + short_save)
        return short_save
