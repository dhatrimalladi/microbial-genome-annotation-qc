import sys


def read_fasta(fasta_file):
    """Read a FASTA file and return sequences as a dictionary."""
    sequences = {}
    current_id = None
    current_sequence = []

    with open(fasta_file, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):
                if current_id is not None:
                    sequences[current_id] = "".join(current_sequence)

                current_id = line[1:].split()[0]
                current_sequence = []
            else:
                current_sequence.append(line)

        if current_id is not None:
            sequences[current_id] = "".join(current_sequence)

    return sequences


def validate_sequence(sequence):
    """Validate that a DNA sequence contains only valid nucleotide characters."""
    sequence = sequence.upper()
    valid_bases = set("ATGC")

    invalid_bases = set(sequence) - valid_bases

    return {
        "is_valid": len(invalid_bases) == 0,
        "invalid_bases": sorted(invalid_bases),
    }


def calculate_gc(sequence):
    """Calculate GC percentage for a DNA sequence."""
    sequence = sequence.upper()
    gc_count = sequence.count("G") + sequence.count("C")

    if len(sequence) == 0:
        return 0.0

    return (gc_count / len(sequence)) * 100


def genome_statistics(fasta_file):
    """Calculate basic statistics for a FASTA genome."""
    sequences = read_fasta(fasta_file)
    total_length = sum(len(seq) for seq in sequences.values())

    if total_length == 0:
        gc_content = 0.0
    else:
        total_gc = sum(
            calculate_gc(seq) * len(seq) / 100
            for seq in sequences.values()
        )
        gc_content = (total_gc / total_length) * 100

    contig_lengths = sorted(
        (len(seq) for seq in sequences.values()),
        reverse=True
    )

    half_genome = total_length / 2
    cumulative_length = 0
    n50 = 0

    for length in contig_lengths:
        cumulative_length += length

        if cumulative_length >= half_genome:
            n50 = length
            break

    return {
        "number_of_contigs": len(sequences),
        "genome_length": total_length,
        "gc_content": round(gc_content, 2),
        "n50": n50,
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        stats = genome_statistics(sys.argv[1])
        print(stats)
    else:
        print("Please provide a FASTA file path.")