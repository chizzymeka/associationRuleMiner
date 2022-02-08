import json


def build_transaction_database(parameter_tuple):

    project_name = parameter_tuple[1]
    modified_files_data = parameter_tuple[2]

    # read file
    with open(modified_files_data, 'r') as json_file:
        data = json_file.read()

    # parse file
    commits = json.loads(data)

    item_sets = 'output/transaction_database/' + project_name + '_item_sets.txt'

    with open(item_sets, 'w') as transaction_database_file:

        for commit in commits:

            counter = 0
            modified_files = commit['modified_files']
            file_ids_set = set()

            for modified_file in modified_files:
                file_id = modified_file['file_id']
                file_ids_set.add(file_id)

            file_ids_sorted_set = sorted(file_ids_set)

            # Note that 'item' in the for-loop below represents file_id.
            for item in file_ids_sorted_set:
                # Write the file_id to file.
                transaction_database_file.write(str(item))

                # Insert a whitespace after every file_id except the last one.
                counter = counter + 1
                number_of_modified_files = len(modified_files)
                if counter < number_of_modified_files:
                    transaction_database_file.write(' ')

            # The if statement filters out commits that have no associated modified files. It ensures that no
            # empty lines are in the transaction database file (item_sets.txt).
            if modified_files:
                transaction_database_file.write('\n')
