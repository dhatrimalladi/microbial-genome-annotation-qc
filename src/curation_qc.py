import csv
import sys


REQUIRED_COLUMNS = [
    "gene_id",
    "gene_symbol",
    "product",
    "feature_type",
    "organism",
    "evidence_source",
]


def load_curated_genes(csv_file):
    """Load curated gene records from a CSV file."""
    with open(csv_file, "r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def validate_curated_genes(csv_file):
    """Validate structure and required fields in a curated gene dataset."""
    errors = []

    with open(csv_file, "r", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            return {
                "is_valid": False,
                "record_count": 0,
                "errors": ["CSV file has no header"],
            }

        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if column not in reader.fieldnames
        ]

        if missing_columns:
            errors.append(
                f"Missing required columns: {', '.join(missing_columns)}"
            )

        if missing_columns:
            return {
                "is_valid": False,
                "record_count": 0,
                "errors": errors,
            }

        gene_ids = set()
        record_count = 0

        for line_number, row in enumerate(reader, start=2):
            record_count += 1

            for column in REQUIRED_COLUMNS:
                if not row[column].strip():
                    errors.append(
                        f"Line {line_number}: missing value in '{column}'"
                    )

            gene_id = row["gene_id"].strip()

            if gene_id:
                if gene_id in gene_ids:
                    errors.append(
                        f"Line {line_number}: duplicate gene ID "
                        f"'{gene_id}'"
                    )
                else:
                    gene_ids.add(gene_id)

            feature_type = row["feature_type"].strip()

            if feature_type not in {"gene", "pseudogene"}:
                errors.append(
                    f"Line {line_number}: unexpected feature type "
                    f"'{feature_type}'"
                )

    return {
        "is_valid": len(errors) == 0,
        "record_count": record_count,
        "errors": errors,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m src.curation_qc <curated_genes.csv>")
        sys.exit(1)

    csv_file = sys.argv[1]

    result = validate_curated_genes(csv_file)

    print("Curation QC")
    print("-----------")
    print(f"Records: {result['record_count']}")
    print(f"Valid: {result['is_valid']}")

    if result["errors"]:
        print("Errors:")

        for error in result["errors"]:
            print(f"- {error}")
