from src import ncbi_curation


def test_load_gene_symbols(tmp_path):
    csv_file = tmp_path / "genes.csv"

    csv_file.write_text(
        "gene_id,gene_symbol,product,feature_type,organism,evidence_source\n"
        "gene1,thrL,protein,gene,E. coli,NCBI RefSeq\n"
        "gene2,thrA,enzyme,gene,E. coli,NCBI RefSeq\n"
    )

    result = ncbi_curation.load_gene_symbols(csv_file)

    assert result == ["thrL", "thrA"]


def test_validate_gene_against_ncbi(monkeypatch):
    def mock_search_gene(gene_symbol):
        assert gene_symbol == "thrA"
        return ["945803"]

    def mock_get_gene_summaries(gene_ids):
        assert gene_ids == ["945803"]

        return [
            {
                "gene_id": "945803",
                "gene_symbol": "thrA",
                "organism": (
                    "Escherichia coli str. "
                    "K-12 substr. MG1655"
                ),
                "taxid": 511145,
            }
        ]

    monkeypatch.setattr(
        ncbi_curation,
        "search_gene",
        mock_search_gene,
    )

    monkeypatch.setattr(
        ncbi_curation,
        "get_gene_summaries",
        mock_get_gene_summaries,
    )

    result = ncbi_curation.validate_gene_against_ncbi(
        "thrA"
    )

    assert result == {
        "gene_symbol": "thrA",
        "ncbi_match": True,
        "gene_id": "945803",
    }


def test_validate_gene_without_ncbi_match(monkeypatch):
    monkeypatch.setattr(
        ncbi_curation,
        "search_gene",
        lambda gene_symbol: [],
    )

    result = ncbi_curation.validate_gene_against_ncbi(
        "unknown_gene"
    )

    assert result == {
        "gene_symbol": "unknown_gene",
        "ncbi_match": False,
        "gene_id": None,
    }


def test_validate_gene_wrong_taxid(monkeypatch):
    monkeypatch.setattr(
        ncbi_curation,
        "search_gene",
        lambda gene_symbol: ["123456"],
    )

    monkeypatch.setattr(
        ncbi_curation,
        "get_gene_summaries",
        lambda gene_ids: [
            {
                "gene_id": "123456",
                "gene_symbol": "thrA",
                "organism": "Escherichia coli",
                "taxid": 562,
            }
        ],
    )

    result = ncbi_curation.validate_gene_against_ncbi(
        "thrA"
    )

    assert result == {
        "gene_symbol": "thrA",
        "ncbi_match": False,
        "gene_id": None,
    }


def test_validate_curated_genes_against_ncbi(monkeypatch, tmp_path):
    csv_file = tmp_path / "genes.csv"

    csv_file.write_text(
        "gene_id,gene_symbol,product,feature_type,organism,evidence_source\n"
        "gene1,thrA,enzyme,gene,E. coli,NCBI RefSeq\n"
        "gene2,thrB,enzyme,gene,E. coli,NCBI RefSeq\n"
    )

    def mock_validate(gene_symbol):
        return {
            "gene_symbol": gene_symbol,
            "ncbi_match": gene_symbol == "thrA",
            "gene_id": "945803" if gene_symbol == "thrA" else None,
        }

    monkeypatch.setattr(
        ncbi_curation,
        "validate_gene_against_ncbi",
        mock_validate,
    )

    result = ncbi_curation.validate_curated_genes_against_ncbi(
        csv_file
    )

    assert result["taxonomy_id"] == 511145
    assert result["record_count"] == 2
    assert result["matched_records"] == 1
    assert result["unmatched_records"] == 1


def test_save_validation_report(tmp_path):
    output_file = tmp_path / "report.json"

    results = {
        "taxonomy_id": 511145,
        "record_count": 1,
        "matched_records": 1,
        "unmatched_records": 0,
        "results": [
            {
                "gene_symbol": "thrA",
                "ncbi_match": True,
                "gene_id": "945803",
            }
        ],
    }

    ncbi_curation.save_validation_report(
        results,
        output_file,
    )

    assert output_file.exists()

    saved_data = output_file.read_text()

    assert '"taxonomy_id": 511145' in saved_data
    assert '"gene_symbol": "thrA"' in saved_data
