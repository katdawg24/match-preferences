import numpy as np
from MatchingFunction import linear_sum_assignment
from itertools import product
import pprint

def create_preference_matrix(num_tasks, num_preferences, group_size, rankings, dummy_nodes):
    """
    Create a preference matrix based on the rankings provided.
    
    Parameters:
    - node_count: Number of nodes (tasks).
    - group_size: Number of people.
    - rankings: Dictionary with person indices as keys and their rankings as values.
    
    Returns:
    - preferences: Matrix of preferences.
    """

    preferences = np.zeros((group_size, group_size))
    for person in rankings:
        for j in range(num_tasks):
            if rankings[person].__contains__(j):
                for node in dummy_nodes[j]:
                    preferences[person][node] = (num_preferences - rankings[person].index(j)) / float(num_preferences)

    return preferences

def exact_assignment_setup(num_tasks, group_size, exact_asignment_counts):
    """
    Setup for the exact assignment problem.
    
    Parameters:
    - num_tasks: Number of tasks to be assigned.
    - rankings: Dictionary with person indices as keys and their rankings as values.
    - exact_asignment_counts: Dictionary with person indices as keys and their exact assignment counts as values.
    
    Returns:
    - preferences: Matrix of preferences.
    """

    if group_size != sum(exact_asignment_counts.values()):
        raise ValueError("The sum of exact assignment counts must equal the number of people.")
    
    dummy_nodes = {nodes: [] for nodes in range(num_tasks)}

    node_count = 0
    for task in range(num_tasks):
        dummy_nodes[task] = list(range(node_count, node_count + exact_asignment_counts[task]))
        node_count += exact_asignment_counts[task]

    print("Dummy nodes:", dummy_nodes)
    return dummy_nodes

def find_optimal_assignments(preferences, dummy_nodes):
    """
    Find the optimal assignments using the Hungarian algorithm.

    Parameters:
    - preferences: Matrix of preferences.
    - dummy_nodes: Dictionary with task indices as keys and their dummy node indices as values.

    Returns:
    - row_ix: Row indices of the optimal assignments.
    - converted_col_ix: Converted column indices of the optimal assignments.
    - maxsum: Maximum sum of preferences.

    """
    row_ix, col_ix = linear_sum_assignment(preferences,maximize=True)
    maxsum = preferences[row_ix,col_ix].sum()
    converted_col_ix = convert_assignment_column(col_ix, dummy_nodes)

    return row_ix, converted_col_ix, maxsum

def find_assignment_counts(num_tasks, group_size, assignment_count_ranges):
    """
    Find the assignment counts for each task.
    
    Parameters:
    - num_tasks: Number of tasks to be assigned.
    - group_size: Number of people.
    - assignment_count_ranges: Dictionary with person indices as keys and their assignment count ranges as values.
    
    Returns:
    - assignment_counts: Dictionary with possible assignment counts for each task.
    """

    ranges = [ list(range(assignment_count_ranges[task][0], assignment_count_ranges[task][1] + 1)) for task in range(num_tasks)]
    
    possible_counts = [list(comb) for comb in product(*ranges)]
    print("Possible counts:", possible_counts)

    valid_counts = [count for count in possible_counts if sum(count) == group_size]

    if valid_counts == []:
        raise ValueError("No valid assignment counts found that sum to the group size.")
    
    print("Valid counts:", valid_counts)
    return valid_counts

def try_assignment_counts(num_tasks, num_preferences, group_size, assignment_count, rankings):
    """
    Try to assign counts to tasks based on the rankings provided.
    
    Parameters:
    - num_tasks: Number of tasks to be assigned.
    - group_size: Number of people.
    - assignment_count: Dictionary with person indices as keys and their assignment counts as values.
    - rankings: Dictionary with person indices as keys and their rankings as values.
    
    Returns:
    - maxsum: Maximum sum of preferences.
    """

    assignment_count_object = {}
    for task in range(num_tasks):
        assignment_count_object[task] = assignment_count[task]

    dummy_nodes = exact_assignment_setup(num_tasks, group_size, assignment_count_object)
    preferences = create_preference_matrix(num_tasks, num_preferences, group_size, rankings, dummy_nodes)

    row_ix, col_ix = linear_sum_assignment(preferences,maximize=True)
    maxsum = preferences[row_ix,col_ix].sum()

    return maxsum

def assignment_ranges_setup(num_tasks, num_preferences, group_size, assignment_count_ranges, rankings):
    """
    Setup for the assignment ranges.
    
    Parameters:
    - num_tasks: Number of tasks to be assigned.
    - group_size: Number of people.
    - assignment_count_ranges: Dictionary with person indices as keys and their assignment count ranges as values.
    
    Returns:
    - preferences: Matrix of preferences.
    """

    valid_assignment_counts = find_assignment_counts(num_tasks, group_size, assignment_count_ranges)

    assignment_count_scores = {i: {} for i in range(len(valid_assignment_counts))}
    for assignment_count in valid_assignment_counts:
        maxsum = try_assignment_counts(num_tasks, num_preferences, group_size, assignment_count, rankings)
        assignment_count_scores[valid_assignment_counts.index(assignment_count)]["assignment_count"] = assignment_count
        assignment_count_scores[valid_assignment_counts.index(assignment_count)]["maxsum"] = maxsum

    print("Assignment count scores:", assignment_count_scores)

    max_score = max([assignment_count_scores[i]["maxsum"] for i in range(len(assignment_count_scores))])
    best_assignment_count = [assignment_count_scores[i]["assignment_count"] for i in range(len(assignment_count_scores)) if assignment_count_scores[i]["maxsum"] == max_score][0]

    assignment_count_object = {}
    for task in range(num_tasks):
        assignment_count_object[task] = best_assignment_count[task]

    return assignment_count_object

def convert_assignment_column(col_ix, dummy_nodes):
    """
    Convert the assignment column to the original task indices.
    
    Parameters:
    - col_ix: Column indices from the assignment.
    - dummy_nodes: Dictionary with task indices as keys and their dummy node indices as values.
    
    Returns:
    - converted_col_ix: Converted column indices.
    """

    converted_col_ix = []
    for i in range(len(col_ix)):
        for task in dummy_nodes:
            if col_ix[i] in dummy_nodes[task]:
                converted_col_ix.append(task)
                break

    return converted_col_ix

def solve_one_to_one(num_tasks, num_preferences, rankings):

    dummy_nodes = {task: [task] for task in range(num_tasks)}
    preferences = create_preference_matrix(num_tasks, num_preferences, len(rankings), rankings, dummy_nodes)

    print("Preferences matrix:\n", preferences)

    row_ix, converted_col_ix, maxsum = find_optimal_assignments(preferences, dummy_nodes)

    results = {int(person): converted_col_ix[person] for person in row_ix}

    print("Total preference:", maxsum)
    print("Results:")  
    pprint.pprint(results)

    return results, maxsum

def solve_exact_assignment(num_tasks, num_preferences, exact_asignment_counts, rankings):
    dummy_nodes = exact_assignment_setup(num_tasks, len(rankings), exact_asignment_counts)
    preferences = create_preference_matrix(num_tasks, num_preferences, len(rankings), rankings, dummy_nodes)

    print("Preferences matrix:\n", preferences)

    row_ix, converted_col_ix, maxsum = find_optimal_assignments(preferences, dummy_nodes)

    results = {int(person): converted_col_ix[person] for person in row_ix}

    print("Total preference:", maxsum)
    print("Results:")  
    pprint.pprint(results)

    return results, maxsum

def exact_assignment_counts_example():
    num_tasks = 3
    num_preferences = 3
    rankings = {
        0: [0, 1, 2],
        1: [1, 2, 0],
        2: [0, 2, 1],
        3: [1, 2, 0],
        4: [0, 1, 2],
        5: [0, 2, 1],
        6: [2, 0, 1],
        7: [1, 0, 2],
        8: [0, 1, 2],
        9: [1, 2, 0],
        10: [0, 2, 1],
        11: [1, 0, 2],
        12: [0, 1, 2],
        13: [2, 0, 1],
        14: [1, 2, 0]
    }

    exact_asignment_counts = {
        0: 5,
        1: 5,
        2: 5
    }

    dummy_nodes = exact_assignment_setup(num_tasks, len(rankings), exact_asignment_counts)
    preferences = create_preference_matrix(num_tasks, num_preferences, len(rankings), rankings, dummy_nodes)

    print("Preferences matrix:\n", preferences)

    row_ix, converted_col_ix, maxsum = find_optimal_assignments(preferences, dummy_nodes)

    results = {int(person): converted_col_ix[person] for person in row_ix}

    print("Total preference:", maxsum)
    print("Results:")  
    pprint.pprint(results)

def solve_assignment_with_ranges(num_tasks, num_preferences, assignment_count_ranges, rankings):
    best_assignment_count = assignment_ranges_setup(num_tasks, num_preferences, len(rankings), assignment_count_ranges, rankings)
    print("Best assignment count:", best_assignment_count)

    dummy_nodes = exact_assignment_setup(num_tasks, len(rankings), best_assignment_count)
    preferences = create_preference_matrix(num_tasks, num_preferences, len(rankings), rankings, dummy_nodes)

    print("Preferences matrix:\n", preferences)

    row_ix, converted_col_ix, maxsum = find_optimal_assignments(preferences, dummy_nodes)

    results = {int(person): converted_col_ix[person] for person in row_ix}

    print("Total preference:", maxsum)
    print("Results:")  
    pprint.pprint(results)

    return results, maxsum

def assignment_ranges_example():
    num_tasks = 3
    num_preferences = 3
    group_size = 15
    rankings = {
        0: [0, 1, 2],
        1: [1, 2, 0],
        2: [0, 2, 1],
        3: [1, 2, 0],
        4: [0, 1, 2],
        5: [0, 2, 1],
        6: [2, 0, 1],
        7: [1, 0, 2],
        8: [0, 1, 2],
        9: [1, 2, 0],
        10: [0, 2, 1],
        11: [1, 0, 2],
        12: [0, 1, 2],
        13: [2, 0, 1],
        14: [1, 2, 0]
    }

    assignment_count_ranges = {
        0: (5,7),
        1: (5,5),
        2: (2,5)
    }

    best_assignment_count = assignment_ranges_setup(num_tasks, num_preferences, group_size, assignment_count_ranges, rankings)
    print("Best assignment count:", best_assignment_count)

    dummy_nodes = exact_assignment_setup(num_tasks, len(rankings), best_assignment_count)
    preferences = create_preference_matrix(num_tasks, num_preferences, len(rankings), rankings, dummy_nodes)

    print("Preferences matrix:\n", preferences)

    row_ix, converted_col_ix, maxsum = find_optimal_assignments(preferences, dummy_nodes)

    results = {int(person): converted_col_ix[person] for person in row_ix}

    print("Total preference:", maxsum)
    print("Results:")  
    pprint.pprint(results)

if __name__ == "__main__":
    assignment_ranges_example()
    # exact_assignment_counts_example()

