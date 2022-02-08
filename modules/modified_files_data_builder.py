# The main for-loop which traverses a given repository resides inside a for-loop that loops twice, as in 'range(2)'.
# The idea is that on the first iteration, that is, 'i == 0', it build file IDs that will be used in the JSON file
# and the transaction database. On the second iteration, the function then builds the aforementioned JSON file.

from datetime import datetime
from pydriller import Repository

import json


def build_modified_files_data(parameter_tuple):

    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")

    counter = 0
    path = ''
    commits = []
    filepath_id_map = {}
    repo_url = parameter_tuple[0]
    project_name = parameter_tuple[1]
    modified_files_data = parameter_tuple[2]

    for i in range(2):

        if i == 0:
            print('File ID generation for ' + project_name + ' started at: ' + str(current_time))
        elif i == 1:
            print('"Modified Files Data" file building for ' + project_name + ' started at: ' + str(current_time))

        # You can use the commented-out for-loop below if you want to limit the traversal, maybe for test purposes.
        # for commit in Repository(repo_url, since=datetime(2020, 12, 31, 17, 0, 0)).traverse_commits():

        for commit in Repository(repo_url).traverse_commits():

            modified_files_list = []

            for modified_file in commit.modified_files:

                counter = counter + 1
                change_type = modified_file.change_type.name

                match change_type:

                    # If the modification type is an ADDITION, then use the new path as the filepath could not have
                    # existed before the file was created.
                    case 'ADD':
                        path = modified_file.new_path

                    # If the modification type is a DELETION, then use the old path before the file was deleted.
                    case 'DELETE':
                        path = modified_file.old_path

                    # If the modification type is a MODIFICATION, then use the old path because it is still the
                    # same file.
                    case 'MODIFY':
                        path = modified_file.old_path

                    # If the modification type is a RENAMING, then use the new path that the file has been
                    # renamed to.
                    case 'RENAME':
                        path = modified_file.new_path

                assert path != ''

                if i == 0:
                    if path not in filepath_id_map:
                        filepath_id_map[path] = counter
                elif i == 1:
                    # Look up previously-generated file ID.
                    file_id = filepath_id_map[path]

                    modified_files_map = {
                        'file_id': file_id,
                        'filepath': path,
                        'change_type': change_type
                    }

                    # Collect the details of all modified files under current commit.
                    modified_files_list.append(modified_files_map)

            if i == 1:
                commit_details_map = {
                    'commit_hash': commit.hash,
                    'commit_message': commit.msg,
                    'modified_files': modified_files_list
                }

                commits.append(commit_details_map)

        if i == 1:
            # Create JSON data.
            with open(modified_files_data, 'w') as json_file:
                json.dump(commits, json_file)

        if i == 0:
            print('File ID generation for ' + project_name + ' completed at: ' + str(current_time))
        elif i == 1:
            print('"Modified Files Data" building for ' + project_name + ' completed at: ' + str(current_time))
