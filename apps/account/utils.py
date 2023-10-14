import random


def slugify(value: str):

    elements = (".", "-", "_", "/", "@")
    random_elements_list = [elements[random.randint(0, 4)] for i in range(0, len(value))]

    array = list(range(0, len(value)))
    random.shuffle(array)

    slugify_value_list = [value[i] for i in array]
    slugify_value_list = list(zip(slugify_value_list, random_elements_list))
    result = "".join(["".join(pair) for pair in slugify_value_list])
    return result
