import csv
import json
import sys

from src.ncbi_api import search_gene, get_gene_summaries, filter_by_taxid


TARGET_TAXID = 511145


def load_gene_symbols(csv_file):
    """Load gene symbols from a curated gene CSV file."""
    with open(csv_file, "r", newline="") as file:
        reader = csv.DictReader(file)

        return [
            row["gene_symbol"].strip()
            for row in reader
            if row["gene_symbol"].strip()
        ]


def validate_gene_against_ncbi(gene_symbol):
    """Check whether a curated gene has a matching NCBI Gene record."""
    gene_ids = search_gene(gene_symbol)

    if not gene_ids:
        return {
            "gene_symbol": gene_symbol,
            "ncbi_match": False,
            "gene_id": None,
        }

    records = get_gene_summaries(gene_ids)

    matching_records = filter_by_taxid(
        records,
        TARGET_TAXID,
    )

    if not matching_records:
        return {
            "gene_symbol": gene_symbol,
            "ncbi_match": False,
            "gene_id": None,
        }

    return {
        "gene_symbol": gene_symbol,
        "ncbi_match": True,
        "gene_id": matching_records[0]["gene_id"],
    }


def validate_curated_genes_against_ncbi(csv_file):
    """Validate all curated gene symbols against NCBI Gene."""
    gene_symbols = load_gene_symbols(csv_file)

    results = []

    for gene_symbol in gene_symbols:
        result = validate_gene_against_ncbi(
            gene_symbol
        )
        results.append(result)

    return {
        "taxonomy_id": TARGET_TAXID,
        "record_count": len(results),
        "matched_records": sum(
            result["ncbi_match"]
            for result in results
        ),
        "unmatched_records": sum(
            not result["ncbi_match"]
            for result in results
        ),
        "results": results,
    }


def save_validation_report(results, output_file):
    """Save NCBI validation results as a JSON report."""
    with open(output_file, "w") as file:
        json.dump(
            results,
            file,
            indent=4,
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python -m src.ncbi_curation "
            "<curated_genes.csv> [report.json]"
        )
        sys.exit(1)

    csv_file = sys.argv[1]

    results = validate_curated_genes_against_ncbi(
        csv_file
    )

    print("NCBI Curation Validation")
    print("------------------------")
    print(f"Records checked: {results['record_count']}")
    print(f"Matched records: {results['matched_records']}")
    print(f"Unmatched records: {results['unmatched_records']}")

    for result in results["results"]:
        print(
            f"{result['gene_symbol']}: "
            f"{result['gene_id'] or 'No match'}"
        )

    if len(sys.argv) > 2:
        output_file = sys.argv[2]

        save_validation_report(
            results,
            output_file,
        )

        print(f"JSON report saved to {output_file}")
