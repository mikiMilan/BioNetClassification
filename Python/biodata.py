from Bio import Entrez, SeqIO
import networkx as nx
from unit import loading_graph


def get_protein_sequence(protein_id):
    try:
        Entrez.email = "milan.predojevic@pmf.unibl.org"
        Entrez.api_key = '35c656feaca92a9c9c18d84d38be9127e609'

        search_handle = Entrez.esearch(db="protein", term=protein_id)
        search_results = Entrez.read(search_handle)
        search_handle.close()

        if len(search_results["IdList"]) == 0:
            print("Nije pronađen protein s identifikatorom:", protein_id)
            return None

        protein_id_ncbi = search_results["IdList"][0]

        fetch_handle = Entrez.efetch(db="protein", id=protein_id_ncbi, rettype="fasta", retmode="text")
        record = SeqIO.read(fetch_handle, "fasta")
        fetch_handle.close()

        return record.seq
    except Exception as e:
        print("Greška pri dohvaćanju sekvence:", e)
        return None


# Primjer korištenja funkcije za dobivanje sekvence proteina
protein_id = "YNCL0033C"
protein_sequence = get_protein_sequence(protein_id)
print(protein_sequence)

# G = nx.Graph()
# loading_graph(G, "data/yeast/BioGRID_withoutLeaves.txt")
#
# protein_sequences = {}
# counter = 0
# for node in G.nodes:
#     protein_sequences[node] = get_protein_sequence(node)
#     with open('sequence.txt', "a") as file:
#         line = node + " " + str(protein_sequences[node]) + "\n"
#         file.write(line)
#     counter += 1
#     if counter%10 == 0:
#         print(counter/10)




