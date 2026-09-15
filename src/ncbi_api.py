import json
import sys
import urllib.parse
import urllib.request


NCBI_GENE_URL = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
)


def search_gene(gene_symbol, organism="Escherichia coli"):
    """Search NCBI Gene for a gene symbol and organism."""
    params = urllib.parse.urlencode(
        {
            "db": "gene",
            "term": (
                f"{gene_symbol}[Gene Name] AND "
                f"{organism}[Organism]"
            ),
            "retmode": "json",
        }
    )

    url = f"{NCBI_GENE_URL}esearch.fcgi?{params}"

    with urllib.request.urlopen(url, timeout=30) as response:
        data = json.load(response)

    return data["esearchresult"]["idlist"]


def get_gene_summary(gene_id):
    """Retrieve structured information for an NCBI Gene ID."""
    params = urllib.parse.urlencode(
        {
            "db": "gene",
            "id": gene_id,
            "retmode": "json",
        }
    )

    url = f"{NCBI_GENE_URL}esummary.fcgi?{params}"

    with urllib.request.urlopen(url, timeout=30) as response:
        data = json.load(response)

    record = data["result"][str(gene_id)]

    genomic_info = record.get("genomicinfo", [])

    if genomic_info:
        genomic_record = genomic_info[0]
    else:
        genomic_record = {}

    organism = record.get("organism", {})

    return {
        "gene_id": record["uid"],
        "gene_symbol": record["name"],
        "description": record["description"],
        "organism": organism.get("scientificname"),
        "taxid": organism.get("taxid"),
        "chromosome_accession": genomic_record.get("chraccver"),
        "start": genomic_record.get("chrstart"),
        "stop": genomic_record.get("chrstop"),
        "summary": record.get("summary"),
    }


def get_gene_summaries(gene_ids):
    """Retrieve structured summaries for multiple NCBI Gene IDs."""
    if not gene_ids:
        return []

    params = urllib.parse.urlencode(
        {
            "db": "gene",
            "id": ",".join(gene_ids),
            "retmode": "json",
        }
    )

    url = f"{NCBI_GENE_URL}esummary.fcgi?{params}"

    with urllib.request.urlopen(url, timeout=30) as response:
        data = json.load(response)

    records = []

    for gene_id in gene_ids:
        record = data["result"].get(str(gene_id))

        if record is None:
            continue

        genomic_info = record.get("genomicinfo", [])

        if genomic_info:
            genomic_record = genomic_info[0]
        else:
            genomic_record = {}

        organism = record.get("organism", {})

        records.append(
            {
                "gene_id": record["uid"],
                "gene_symbol": record["name"],
                "description": record["description"],
                "organism": organism.get("scientificname"),
                "taxid": organism.get("taxid"),
                "chromosome_accession": genomic_record.get("chraccver"),
                "start": genomic_record.get("chrstart"),
                "stop": genomic_record.get("chrstop"),
                "summary": record.get("summary"),
            }
        )

    return records


def filter_by_taxid(records, taxid):
    """Return only records matching the requested NCBI Taxonomy ID."""
    return [
        record
        for record in records
        if record.get("taxid") == taxid
    ]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python -m src.ncbi_api "
            "<gene_symbol>"
        )
        sys.exit(1)

    gene_symbol = sys.argv[1]

    gene_ids = search_gene(gene_symbol)

    print(f"NCBI Gene IDs for {gene_symbol}:")
    print(gene_ids)

    if gene_ids:
        records = get_gene_summaries(gene_ids)

        matching_records = filter_by_taxid(
            records,
            511145,
        )

        print("\nMatching records for Taxonomy ID 511145:")

        for record in matching_records:
            print(json.dumps(record, indent=4))
