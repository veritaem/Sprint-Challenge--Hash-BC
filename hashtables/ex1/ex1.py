#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)
    for w in range(len(weights)):
        w_rem = limit - weights[w]
        result = hash_table_retrieve(ht, w_rem)
        if result != None:
            return (w, result)
        hash_table_insert(ht, weights[w], w)


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
