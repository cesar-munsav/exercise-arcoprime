"""This code was developed to solve statement No. 2
    of the Arcoprime technical test, to apply for
    the position of Senior Data Engineer. Pure Python was used
    without any external library (only the time library)

    Assumptions:
    -The DNA sequence file is a .txt and contains
     newline characters.
    -As the resources and time of the data science team are limited,
    the code will be optimized using list comprehension.
    -The use of strings / regex methods is not allowed
    -The answers to the questions will be return in a dictionary
    -The execution time will be in milliseconds (ms) with 3 decimal.
    """

import time


def parse_dna_str(sequence_dna_str: str) -> str:
    """ Delete the newline characters from a DNA sequence string """
    new_sequence_dna_str = ""
    for letter in sequence_dna_str:
        if letter != "\n":
            new_sequence_dna_str += letter
    return new_sequence_dna_str


def get_input_file(input_path: str) -> str:
    """ Get the DNA sequence file and reads it """
    with open(input_path, 'r', encoding="utf-8") as sequence_dna_file:
        return parse_dna_str(sequence_dna_file.read())


def get_len_sequence(sequence_dna_str: str) -> tuple[int, float]:
    """ Get the lenght of a DNA sequence string
        and the associated execution time """
    start_time = time.time()
    len_sequence = sum([1 for letter in sequence_dna_str])
    end_time = time.time()
    execution_time = round((end_time - start_time)*1000, 3)
    return len_sequence, execution_time


def get_len_subsequence(subsequence: str) -> int:
    """ Get the lenght of a DNA subsequence string """
    return sum([1 for letter in subsequence])


def get_num_nucleot(sequence_dna_str: str,
                    nucleotides: str) -> tuple[dict, float]:
    """ Get the count of nucleotide in a DNA sequence string
        and  the associated execution time """
    start_time = time.time()
    num_nucleot = {
        nuc: sum([1 for letter in sequence_dna_str if letter == nuc])
        for nuc in nucleotides}
    end_time = time.time()
    execution_time = round((end_time - start_time)*1000, 3)
    return num_nucleot, execution_time


def get_num_subseq_dna(sequence_dna_str: str,
                       len_sequence_dna: int,
                       subsequence: str) -> tuple[int, float]:
    """ Get the number of occurrences of a DNA subsequence string
        in a DNA sequence string and  the associated execution time """
    start_time = time.time()
    len_subsequence_dna = get_len_subsequence(subsequence)
    num_subsequence_in_dna = sum(
        [1 for i in range(len_sequence_dna - len_subsequence_dna + 1)
         if sequence_dna_str[i:i+len_subsequence_dna] == subsequence])
    end_time = time.time()
    execution_time = round((end_time - start_time)*1000, 3)
    return num_subsequence_in_dna, execution_time


def format_test_solution(info_len_sequence_dna: tuple,
                         info_num_nucleotides: tuple,
                         info_num_subseq_dna: tuple) -> dict:
    """ Compilation of the answers in a dictionary """
    test_solution = {"Q2.1": {"Largo_secuencia": info_len_sequence_dna[0],
                              "Tiempo_ejecucion(ms)": info_len_sequence_dna[1]
                              },
                     "Q2.2": {"Apariciones_nucleot": info_num_nucleotides[0],
                              "Tiempo_ejecucion(ms)": info_num_nucleotides[1]
                              },
                     "Q2.3": {"Apariciones_subseq": info_num_subseq_dna[0],
                              "Tiempo_ejecucion(ms)": info_num_subseq_dna[1]
                              }
                     }
    return test_solution


def solution_sequence_dna(input_path: str, subsequence: str,
                          nucleotides: str) -> str:
    """ Get the solution of the  statement No. 2 """
    sequence_dna_str = get_input_file(input_path)
    info_len_sequence_dna = get_len_sequence(sequence_dna_str)
    len_sequence_dna = info_len_sequence_dna[0]
    info_num_nucleotides = get_num_nucleot(sequence_dna_str,
                                           nucleotides)
    info_num_subseq_dna = get_num_subseq_dna(sequence_dna_str,
                                             len_sequence_dna,
                                             subsequence)
    test_solution = format_test_solution(info_len_sequence_dna,
                                         info_num_nucleotides,
                                         info_num_subseq_dna)
    print(test_solution)
    return test_solution


if __name__ == "__main__":
    input_path = "input_files/sequence_dna.txt"
    subsequence = "tgccag"
    nucleotides = "atcg"

    solution_sequence_dna(input_path, subsequence, nucleotides)
