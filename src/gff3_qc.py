def read_gff3(gff3_file):
    """Read GFF3 annotations and return valid feature records."""

    features = []

    with open(gff3_file, "r") as file:
        for line_number, line in enumerate(file, start=1):

            line = line.strip()

            # Ignore comments and empty lines
            if not line or line.startswith("#"):
                continue

            columns = line.split("\t")

            # GFF3 should contain 9 columns
            if len(columns) != 9:
                continue

            feature = {
                "line_number": line_number,
                "seqid": columns[0],
                "source": columns[1],
                "type": columns[2],
                "start": int(columns[3]),
                "end": int(columns[4]),
                "score": columns[5],
                "strand": columns[6],
                "phase": columns[7],
                "attributes": columns[8],
            }

            features.append(feature)

    return features


def count_features(features):
    """Count annotation features by type."""

    counts = {}

    for feature in features:
        feature_type = feature["type"]

        counts[feature_type] = counts.get(feature_type, 0) + 1

    return counts


def find_invalid_coordinates(features):
    """Find features where start/end coordinates are invalid."""

    invalid = []

    for feature in features:

        if feature["start"] <= 0:
            invalid.append(feature)

        elif feature["end"] < feature["start"]:
            invalid.append(feature)

    return invalid


def find_duplicate_ids(features):
    """Find duplicate feature IDs in GFF3 attributes."""

    seen_ids = set()
    duplicate_ids = set()

    for feature in features:

        attributes = feature["attributes"]

        for item in attributes.split(";"):

            if item.startswith("ID="):

                feature_id = item.split("=", 1)[1]

                if feature_id in seen_ids:
                    duplicate_ids.add(feature_id)

                seen_ids.add(feature_id)

    return sorted(duplicate_ids)


if __name__ == "__main__":
    print("GFF3 QC module loaded successfully.")
