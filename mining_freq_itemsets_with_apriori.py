from itertools import combinations
# Use sets not hashtables

# Load data into input_list
input_list = []
with open('categories.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        line = line.split(";")
        input_list.append(line)

# Create current set
patterns = set()
# Create global set
final_patterns = set()

hash_table = {}
for category in input_list:
    for srs in category:
        hash_table[srs] = 1 + hash_table.get(srs, 0)

freq_one_itemset = []
freq_one_itemset_categories = []

for k, v in hash_table.items():
    if v > 771:
        freq_one_itemset_categories.append(k)
        pattern_line = str(v) + ':' + k + "\n"
        p = str(v) + ':' + k
        # print(pattern_line)
        freq_one_itemset.append(pattern_line)
        patterns.add(p)

# print(patterns)

def get_candidates(item_set, length):
    # Extract the relevant parts from the item set
    extracted_lines = set()
    temp = []
    for item in item_set:
        parts = item.split(":")
        temp.append(parts[1].strip())

    # Make extracted_lines only contain one item in each string
    temp_list_set = []
    for item in temp:
        if ";" in item:
            place = item.split(";")
            temp_list_set.append(set(place))
            for ele in place:
                extracted_lines.add(ele)
        else:
            extracted_lines.add(item)


    temp_set = set(temp)
    # Generate candidate pairs of the desired length
    candidate_list = []
    for combination in combinations(extracted_lines, length):
        # Create a candidate key from the combination
        candidate = set()
        has_freq_subset = False
        # temp_str = ""
        for ele in combination:
            candidate.add(ele)
            # if len(temp_str) > 0:
            #     temp_str += ";" + ele
            # else:
            #     temp_str += ele

# This next line only checks if the generated candidate exists in list of subsets
# However, the generated candidate might not match the order that the temp list holds it as
# In the validate_candidates function, we use sets to compare
        for c in combinations(candidate, length - 1):
            if len(c) <= 1:
                if candidate.issubset(temp_set):
                    has_freq_subset = True
            elif set(c) in (temp_list_set):
                has_freq_subset = True
           
            # if temp_str not in temp and temp_str not in list(extracted_lines):
            #     if temp_str.count(";") == length - 1:
            #         continue
            #     has_freq_subset = False
        
        if (has_freq_subset):
            candidate_list.append(candidate)

    return candidate_list



# def get_valid_candidates(item_list, min_sup):
#     result_list = [';'.join(sorted(sublist)) for sublist in input_list]
#     # print(item_list)
#     better_item_list = [f"{';'.join(sorted(s.split(';')))}" for s in item_list]
#     for item in better_item_list:
#         x = result_list.count(item)
#         if x > min_sup:
#             print(x)
#     return -1

"""
Given a list of sets, return all candidates with a support > min_sup
"""

def validate_candidates(candidate_set, min_sup):
    temp_hash = {}
    # print(candidate_set)
    # now we have a list of sets that contain the categories of each place

    # Transform database into a list of sets
    list_of_sets = [set(sublist) for sublist in input_list]
    # print(list_of_sets)
    for s1 in list_of_sets:
        for s2 in candidate_list:
            if s2.issubset(s1):
                s = ";".join(s2)
                temp_hash[s] = 1 + temp_hash.get(s, 0)
                # print(s1)
                # print(s2)
    ret_set = set()
    for k,v in temp_hash.items():
        if v > min_sup:
            ret_set.add(str(v) + ":" + k)
    return ret_set

def get_valid_candidates(item_list, min_sup):
    temp_hash = {}
    print(item_list)
    for input_line in input_list:
        for category in item_list:
            # print("category: ")
            # print(category)
            # print("")
            parts = category.split(";")
        
            is_in_input_line = True
            # print("parts: ")
            # print(parts)
            # print("")
            # print("input_line: ")
            # print(input_line)
            # print("")
            for ele in parts:
                if ele not in input_line:
                    # print(ele)
                    # print(" is not in ")
                    # print(input_line)
                    is_in_input_line = False
            # print(category)
            # print(list(reversed(parts)))
            # reversed_category = ";".join(list(reversed(parts)))
            # print(reversed_category)
            # and (reversed_category not in temp_hash)
            if (is_in_input_line == True):
                # print(category)
                parts.sort()
                cat = ";".join(parts)
                # print(cat)
                temp_hash[cat] = 1 + temp_hash.get(cat, 0)
                # print("added ")
                # print(category)
                # print(" to hashtable, with support of ")
                # print(temp_hash[category])

    ret_set = set()
    for key, value in temp_hash.items():
        if value > min_sup:
            ret_set.add(str(value) + ":" + key)

    return ret_set

k = 2

while (patterns):

    #Add patterns to final set
    final_patterns = final_patterns.union(patterns)
    # patterns.clear()

    # Generate candidates
    candidate_list = get_candidates(patterns, k)
    print("\n\n\n")
    # print(candidate_set)


    # Validate candidates
    # Put valid candidates in patterns
    patterns = validate_candidates(candidate_list, 771)
    # patterns = get_valid_candidates(candidate_list, 771)
    # print(patterns)
    
    k += 1

with open("patterns.txt", "w") as f:
    for s in list(final_patterns):
        f.write(f'{s}\n')

print(final_patterns)