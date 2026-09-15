import csv

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


if __name__ == "__main__":
    csv_file = "src/data/curated_genes.csv"

    gene_symbols = load_gene_symbols(csv_file)

    print("Curated gene symbols:")
    for gene_symbol in gene_symbols:
        print(f"- {gene_symbol}")
