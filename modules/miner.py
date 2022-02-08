import subprocess
from datetime import datetime


def run_selected_algorithm(parameter_tuple):

    project_name = parameter_tuple[1]
    min_sup = parameter_tuple[3]
    confidence = parameter_tuple[4]
    selected_algorithm = parameter_tuple[5]
    min_pattern_length = parameter_tuple[6]
    max_pattern_length = parameter_tuple[7]

    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")

    print('Frequent items sets evaluation for ' + project_name + ' started at: ' + str(current_time))

    command = ''

    # Set up custom smpf command using the selected algorithm.
    match selected_algorithm:
        # Run the Apriori algorithm
        case 'apriori':
            command_prefix = 'java -jar spmf.jar run'
            selected_algorithm = 'Apriori'
            item_sets = 'output/transaction_database/' + project_name + '_item_sets.txt'
            output = 'output/' + project_name + '_' + 'min_sup-' + str(min_sup) + '_' + selected_algorithm + '_' + 'min_pattern_length-' + str(min_pattern_length) + '_' + 'max_pattern_length-' + str(max_pattern_length) + '_output.txt'
            min_sup = str(min_sup) + '%'
            command = command_prefix + ' ' + selected_algorithm + ' ' + item_sets + ' ' + output + ' ' + min_sup + ' ' + str(max_pattern_length)
        case 'fp-growth':
            # Run the FP-Growth algorithm.
            command_prefix = 'java -jar spmf.jar run'
            selected_algorithm = 'FPGrowth_association_rules'
            item_sets = 'output/transaction_database/' + project_name + '_item_sets.txt'
            output = 'output/' + project_name + '_' + 'min_sup-' + str(min_sup) + '_' + 'confidence-' + str(confidence) + '_' + selected_algorithm + '_' + 'min_pattern_length-' + str(min_pattern_length) + '_' + 'max_pattern_length-' + str(max_pattern_length) + '_output.txt'
            min_sup = str(min_sup) + '%'
            confidence = str(confidence) + '%'
            command = command_prefix + ' ' + selected_algorithm + ' ' + item_sets + ' ' + output + ' ' + min_sup + ' ' + confidence + ' ' + str(min_pattern_length) + ' ' + str(max_pattern_length)

    subprocess.run(command, shell=True)

    print('Frequent items sets evaluation for ' + project_name + ' completed at: ' + str(current_time))
