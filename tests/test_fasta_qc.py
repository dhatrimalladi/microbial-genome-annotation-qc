from src.fasta_qc import read_fasta, calculate_gc, genome_statistics, validate_sequence

def test_read_fasta():
    sequences = read_fasta("src/data/example_genome.fasta")

    assert len(sequences) == 2
    assert "contig_1" in sequences
    assert "contig_2" in sequences


def test_calculate_gc():
    sequence = "ATGCATGC"

    assert calculate_gc(sequence) == 50.0


def test_genome_statistics():
    result = genome_statistics("src/data/example_genome.fasta")

    assert result["number_of_contigs"] == 2
    assert result["genome_length"] == 87
    assert result["gc_content"] == 49.43
def test_validate_sequence():
    valid_result = validate_sequence("ATGCATGC")
    assert valid_result["is_valid"] is True
    assert valid_result["invalid_bases"] == []

    invalid_result = validate_sequence("ATGCXYZ")
    assert invalid_result["is_valid"] is False
    assert invalid_result["invalid_bases"] == ["X", "Y", "Z"]