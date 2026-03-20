
def merge_by_id_new(list1, list2, key="id"):
    # Turn list2 into a fast lookup dictionary: id -> dict
    lookup = {row[key]: row for row in list2}
    merged = []

    for row in list1:
        # Find matching row in list2 by id (or {} if none found)
        match = lookup.get(row.get(key), {})

        # Copy row from list1 so we DON'T modify the original list1
        new_row = dict(row)

        # Add fields from match into new_row (skip the id field)
        for k, v in match.items():
            if k != key:
                new_row[k] = v

        merged.append(new_row)

    return merged


# -------------------------
# Example data (already defined)
# -------------------------
list1 = [
    {"id": 45, "pula": 20, "inaltime": 16},
    {"id": 46, "pula": 10, "inaltime": 12},
    {"id": 99, "pula": 1,  "inaltime": 5},   # this one has no match in list2
]

list2 = [
    {"id": 45, "varsta": 15},
    {"id": 46, "varsta": 20},
    {"id": 123, "varsta": 50},               # this one doesn't exist in list1 (won't show up)
]

# -------------------------
# Run merge + print results
# -------------------------
result = merge_by_id_new(list1, list2)

print("Original list1 (unchanged):")
print(list1)
print("\nOriginal list2:")
print(list2)
print("\nMerged result:")
print(result)