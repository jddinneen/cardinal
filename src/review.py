#!/usr/bin/env python
# coding:utf-8
"""
prepares a summary of the user's data
Todo:
    * Replace print with logging
    * Add runtime to transmit data
"""

from datetime import datetime
import collections

__author__ = "Jesse David Dinneen, Fabian Odoni"
__copyright__ = "Copyright 2015, JDD"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Jesse David Dinneen"
__email__ = "jesse.dinneen@mail.mcgill.ca"
__status__ = "Beta"


def score_reverser(rawscore):
    """
    Reverses the score from
    7 6 5 4 3 2 1
    to
    1 2 3 4 5 6 7
    """
    return [7, 6, 5, 4, 3, 2, 1][int(rawscore) - 1]


def nice_size_format(num):
    """ Formats the file size output """
    suffix = 'B'
    for unit in ['', 'K', 'M', 'G', 'Tera', 'Peta', 'Exa', 'Zeta']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def summarize(the_results):
    """
    Calculates some key figures to present to the user
    """
    startTime = datetime.now()

    summary = []

    unfiled_files = 0
    total_symlinks = 0
    total_folders = 0
    total_files = 0
    empty_folders = 0
    file_types = collections.defaultdict(int)
    file_sizes = {'sum': 0, 'number': 0, 'max_size': 0, 'max_extension': ''}
    filename_lengths = []
    folder_name_lengths = []
    files_per_folder = {'sum': 0, 'number': 0}
    max_folder_depths = 0
    nodes_analyzed = 0
    files_analyzed = 0

    # iterate over the nodes, make observations
    for node_list in the_results.node_lists:

        for node_id, node in node_list.items():
            nodes_analyzed += 1
            # print("Analyzing node #{}: {}".format(nodes_analyzed, node_id))

            len_node_file_list = len(node.file_list)

            if node.depth > max_folder_depths:
                max_folder_depths = node.depth

            if node_id == 1:
                unfiled_files += len_node_file_list

            total_folders += 1
            total_files += len_node_file_list
            total_symlinks += node.symlinks
            folder_name_lengths.append(node.name_length)

            files_per_folder['sum'] += len_node_file_list
            files_per_folder['number'] += 1

            if len_node_file_list < 1:
                empty_folders += 1

            for file_in_node in node.file_list:
                files_analyzed += 1
                # print("Analyzing file #{}: {}".format(files_analyzed, file_in_node))

                if len(file_in_node.extension) < 1:
                    current_name_length = file_in_node.full_name_length
                else:
                    current_name_length = file_in_node.full_name_length - len(file_in_node.extension) - 1
                    norm_extension = file_in_node.extension.lower()
                    file_types[norm_extension] += 1
                filename_lengths.append(current_name_length)

                file_sizes['sum'] += file_in_node.file_size if file_in_node.file_size > 0 else 0
                file_sizes['number'] += 1

                if file_in_node.file_size > file_sizes['max_size']:
                    file_sizes['max_size'] = file_in_node.file_size

                    if len(file_in_node.extension) < 1:
                        file_sizes['max_extension'] = "extensionless"
                    else:
                        file_sizes['max_extension'] = file_in_node.extension

    max_file_type = max(file_types.items(), key=lambda a: a[1])
    most_common_file_type = max_file_type[0]
    number_of_most_common_file_type = max_file_type[1]
    average_filesize = file_sizes['sum'] / file_sizes['number']
    average_files_in_folder = files_per_folder['sum'] / files_per_folder['number']

    # Prepare summary of observations
    summary.append("You manage {} files and {} folders.".format(total_files, total_folders))
    summary.append("Your files average {0} in size with the biggest being a {1} {2} file.".format(nice_size_format(average_filesize), nice_size_format(file_sizes['max_size']), file_sizes['max_extension']))
    summary.append("Your most common file type is {}, of which you have {}.\n".format(most_common_file_type, number_of_most_common_file_type))
    summary.append("The average number of files in each of your folders is {0:.2f}.".format(average_files_in_folder))
    summary.append("You have {} empty folders, {} unfiled files, and {} shortcuts (symlinks).".format(empty_folders, unfiled_files, total_symlinks))
    summary.append("Your deepest folder is {} levels deep within your folder tree.\n".format(max_folder_depths))

    summary.append("The average length of your file names is {0:.2f} characters, with the longest being {1}.".format(sum(filename_lengths)/len(filename_lengths), max(filename_lengths)))
    summary.append("The average length of your folder names is {0:.2f} characters, with the longest being {1}.\n".format(sum(folder_name_lengths)/len(folder_name_lengths), max(folder_name_lengths)))

    # 3. summarize personality and sense of direction
    spatial_ability = int(the_results.sod_results['q1'])
    spatial_ability += score_reverser(the_results.sod_results['q2'])
    spatial_ability += int(the_results.sod_results['q3'])
    spatial_ability += int(the_results.sod_results['q4'])
    spatial_ability += int(the_results.sod_results['q5'])
    spatial_ability += score_reverser(the_results.sod_results['q6'])
    spatial_ability += int(the_results.sod_results['q7'])
    spatial_ability += score_reverser(the_results.sod_results['q8'])
    spatial_ability += int(the_results.sod_results['q9'])
    spatial_ability += score_reverser(the_results.sod_results['q10'])
    spatial_ability += score_reverser(the_results.sod_results['q11'])
    spatial_ability += score_reverser(the_results.sod_results['q12'])
    spatial_ability += score_reverser(the_results.sod_results['q13'])
    spatial_ability += int(the_results.sod_results['q14'])
    spatial_ability += score_reverser(the_results.sod_results['q15'])
    summary.append("Your spatial ability was measured to be: {} (out of 105)\n".format(spatial_ability))

    extraversion = int(the_results.personality_results['q1'])

    # reverse this score
    extraversion += score_reverser(the_results.personality_results['q6'])

    # reverse this score
    agreeableness = (score_reverser(the_results.personality_results['q2']))
    agreeableness += int(the_results.personality_results['q7'])

    conscientiousness = int(the_results.personality_results['q3'])

    # reverse this score
    conscientiousness += score_reverser(the_results.personality_results['q8'])

    # reverse this score
    stability = score_reverser(the_results.personality_results['q4'])
    stability += int(the_results.personality_results['q9'])

    openness = int(the_results.personality_results['q5'])
    # reverse this score
    openness += score_reverser(the_results.personality_results['q10'])

    summary.append("Personality results (each out of 14): extraversion {}, agreeableness {}, conscientiousness {}, emotional stability {}, openness to new experiences {}.".format(extraversion, agreeableness, conscientiousness, stability, openness))

    runtime = datetime.now() - startTime

    print("Summarizing runtime: {}".format(runtime))
    return "\n".join(summary)
