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
    """Validate basic GFF3 structure and coordinates."""
    errors = []

    with open(gff3_file, "r") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split("\t")

            # GFF3 records must contain 9 columns
            if len(parts) != 9:
                errors.append(
                    f"Line {line_number}: expected 9 columns, found {len(parts)}"
                )
                continue

            start = parts[3]
            end = parts[4]

            # Coordinates must be integers
            try:
                start = int(start)
                end = int(end)
            except ValueError:
                errors.append(
                    f"Line {line_number}: start and end must be integers"
                )
                continue

            # Start coordinate must not be greater than end
            if start > end:
                errors.append(
                    f"Line {line_number}: start coordinate is greater than end"
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