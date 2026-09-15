from src.run_qc import run_qc, save_report


def test_run_qc():
    result = run_qc(
        "src/data/example_genome.fasta",
        "src/data/example_annotation.gff3",
    )

    assert result["fasta"]["genome_length"] == 87
    assert result["fasta"]["gc_content"] == 49.43
    assert result["gff3"]["total_features"] == 4
    assert result["gff3_validation"]["is_valid"] is True
    assert result["sequence_id_validation"]["is_valid"] is True


def test_save_report(tmp_path):
    result = run_qc(
        "src/data/example_genome.fasta",
        "src/data/example_annotation.gff3",
    )

    output_file = tmp_path / "qc_report.json"

    save_report(result, output_file)

    assert output_file.exists()
