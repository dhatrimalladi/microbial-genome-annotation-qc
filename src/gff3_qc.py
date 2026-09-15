import sys


def parse_gff3(gff3_file):
    """Parse a GFF3 file and return feature counts and types."""
    features = {}
    total_features = 0

    with open(gff3_file, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split("\t")

            if len(parts) >= 9:
                feature_type = parts[2]
                features[feature_type] = features.get(feature_type, 0) + 1
                total_features += 1

    return {
        "total_features": total_features,
        "feature_types": features
    }


def validate_gff3(gff3_file):
    """Validate basic GFF3 structure, coordinates, and feature IDs."""
    errors = []
    feature_ids = {}

    with open(gff3_file, "r") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split("\t")

            if len(parts) != 9:
                errors.append(
                    f"Line {line_number}: expected 9 columns, found {len(parts)}"
                )
                continue

            start = parts[3]
            end = parts[4]
            attributes = parts[8]

            try:
                start = int(start)
                end = int(end)
            except ValueError:
                errors.append(
                    f"Line {line_number}: start and end must be integers"
                )
                continue

            if start > end:
                errors.append(
                    f"Line {line_number}: start coordinate is greater than end"
                )

            attribute_dict = {}

            for attribute in attributes.split(";"):
                if "=" in attribute:
                    key, value = attribute.split("=", 1)
                    attribute_dict[key] = value

            if "ID" not in attribute_dict:
                errors.append(
                    f"Line {line_number}: missing feature ID"
                )
            else:
                feature_id = attribute_dict["ID"]

                is_pseudo = (
                    attribute_dict.get("pseudo") == "true"
                )

                has_ribosomal_slippage = (
                    attribute_dict.get("exception")
                    == "ribosomal slippage"
                )

                if feature_id in feature_ids:
                    previous_is_pseudo, previous_has_slippage = (
                        feature_ids[feature_id]
                    )

                    if not (
                        (is_pseudo and previous_is_pseudo)
                        or (
                            has_ribosomal_slippage
                            and previous_has_slippage
                        )
                    ):
                        errors.append(
                            f"Line {line_number}: duplicate feature ID "
                            f"'{feature_id}'"
                        )
                else:
                    feature_ids[feature_id] = (
                        is_pseudo,
                        has_ribosomal_slippage
                    )

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }


def validate_sequence_ids(fasta_file, gff3_file):
    """Check that GFF3 sequence IDs exist in the FASTA file."""
    fasta_ids = set()

    with open(fasta_file, "r") as file:
        for line in file:
            line = line.strip()

            if line.startswith(">"):
                sequence_id = line[1:].split()[0]
                fasta_ids.add(sequence_id)

    errors = []

    with open(gff3_file, "r") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split("\t")

            if len(parts) != 9:
                continue

            sequence_id = parts[0]

            if sequence_id not in fasta_ids:
                errors.append(
                    f"Line {line_number}: sequence ID "
                    f"'{sequence_id}' not found in FASTA"
                )

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        results = parse_gff3(sys.argv[1])
        validation = validate_gff3(sys.argv[1])

        print(results)
        print(validation)
    else:
        print("Please provide a GFF3 file path.")
