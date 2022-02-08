from pathlib import Path

from modules import miner, transaction_database_builder, modified_files_data_builder
import csv
from datetime import datetime

if __name__ == '__main__':

    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")

    rows = []
    with open('input_file.csv', 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            try:
                repo_url = row[0].strip()

                # The if-statement below is a disabling mechanism that skip repos that start with '-' in the input csv
                # file. So, if you do not want the program to analyse a repo, just put a '-' in front of it.
                if repo_url.startswith('-'):
                    continue

                min_sup = float(row[1].strip())
                confidence = int(row[2].strip())
                selected_algorithm = str(row[3].strip())
                min_pattern_length = int(row[4].strip())
                max_pattern_length = int(row[5].strip())

                assert isinstance(repo_url, str)
                assert isinstance(min_sup, float)
                assert isinstance(confidence, int)
                assert isinstance(selected_algorithm, str)
                assert isinstance(min_pattern_length, int)
                assert isinstance(max_pattern_length, int)

                # Split string once by the last '/' delimiter.
                repo_url_components = repo_url.rsplit("/", 1)

                # Given 'https://github.com/apache/accumulo.git';
                # 'repo_url_components[0]' represents 'https://github.com/apache';
                # 'repo_url_components[1]' represents 'accumulo.git'.

                project_name = repo_url_components[1].split('.git')[0]
                modified_files_data = 'output/modified_files_data/' + project_name + '_modified_files_data.json'

                parameter_tuple = (
                    repo_url,
                    project_name,
                    modified_files_data,
                    min_sup,
                    confidence,
                    selected_algorithm,
                    min_pattern_length,
                    max_pattern_length
                )

                json_file = Path(modified_files_data)

                if json_file.is_file():
                    print(project_name + '_modified_files_data.json already exists.')
                    transaction_database_builder.build_transaction_database(parameter_tuple)
                    miner.run_selected_algorithm(parameter_tuple)
                else:
                    modified_files_data_builder.build_modified_files_data(parameter_tuple)
                    transaction_database_builder.build_transaction_database(parameter_tuple)
                    miner.run_selected_algorithm(parameter_tuple)

                print('')
                print('Completed ' + project_name + ' at ' + str(current_time))
                print('')
            except OSError as error:
                print('Error encountered...')
                print(error)
                print('Skipping ' + project_name + '...')
                continue
