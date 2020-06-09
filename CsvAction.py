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