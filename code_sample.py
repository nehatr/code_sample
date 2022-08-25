"""
$ loading.py
Author: Neha Tripathi


This module is designed to read a file and convert it into an array of arrays
that will be used as the dataset. The load_file method loads the file line by line
and extracts the labels of each instance. The auxiliary check method helps to
convert the float values. The remaining methods support label conversion
to a boolean list. Additionally, they support the conversion of continuous range "labels".

"""
# Load a file line by line and extract the labels into a dictionary. The check
# module ensures that only valid items can be converted to float numbers.
# --Parameters--
# filename:  the file that contains the dataset
# separator: a feature used to split the text into a list (usually a comma)
# label_loc: the location of the label in the dataset (preset to the final index)

def load_file(filename,separator,label_loc = -1):
    data = list()
    labels = dict()
    with open(filename,'r') as file:
        for line in file:
            # Below, we strip the white space and convert the item type to 'float' if applicable:
            temp = [float(x.strip())  if check(x) else x.strip() for x in line.split(separator) ]
            if temp[label_loc] in labels:
                labels[temp[label_loc]] += 1
            else:
                labels[temp[label_loc]]= 1
            data.append(temp)

    return data,labels


# Convert both numerical and string labels to a boolean list.
# First, the labels are extracted from the keys of a labels dictionary.
# Next, we generate a list of zeroes (with the length of the total number of labels)
# Finally, we replace one zero with a '1' at the matching index from the list of keys.
# --Parameters--
# data:  the data we want to modify.
# labels_dict: the dictionary of labels.
# label_loc: the location of the index for each instance (Preset to -1).

def convert_labels(data,labels_dict,label_loc= -1):
    total_labels = len(labels_dict)
    labels = [x for x in labels_dict.keys()]

    data_copy = list(data)
    for instance in data_copy:
        label = instance.pop(label_loc)     # pop the numerical/string label
        blank_labels = [0] * total_labels   # create a list of zeroes
        blank_labels[labels.index(label)] = 1   # each new label has only one '1'
        instance.append(blank_labels)       # add the converted label to the instance.

    return data_copy


# Convert labels to a boolean list when the "labels" are determined by a
# continuous range rather than as discrete values.
# Additionally, this method generates a dictionary of labels that maps each
# range to an integer corresponding.
# --Parameters--
# data:  the data we want to modify.
# ranges: a list of tuples that describe the minimum and maximum range
#         that allows us to discriminate between each category.
# label_loc: the location of the index for each instance (Preset to -1).

def convert_ranged_labels(data,ranges,label_loc= -1):
    total_labels = len(ranges)
    labels = dict.fromkeys(ranges,0) # a dictionary for the integer keys
    labels_without_ranges = dict.fromkeys([x for x in range(total_labels)],0)
    data_copy = list(data)

    for instance in data_copy:
        label = instance[label_loc]
        blank_labels = [0]* total_labels      # create a list of zeroes
        for i in range(total_labels):
            # Check whether the label falls within any of the ranges provided
            if label >= ranges[i][0] and label <= ranges[i][1]:
                labels_without_ranges[i]+=1
                labels[ranges[i]]+=1
                blank_labels[i] = 1         # only one '1' for each instance
                break

        instance.append(blank_labels)

    return data_copy,labels,labels_without_ranges


# Update the labels dictionary in the event of a changing dataset.
# --Parameters--
# updated_data: the updated dataset
# labels: the previous dictionary used to extract the number of labels.

def update_labels_dict(updated_data,labels):
    length= [n for n in range(len(labels))]
    updated_labels = dict.fromkeys(length,0)

    for item in updated_data:

        if item[-1].index(1) in labels_updated:
            updated_labels[item[-1].index(1)] += 1
        else:
            updated_labels[item[-1].index(1)]= 1

    return updated_labels



# Check if an item can be converted to a float.
# --Parameters--
# item: the item we want to convert to a float value.

def check(item):
    try:
        float(item)
        return True
    except ValueError:

        return False
