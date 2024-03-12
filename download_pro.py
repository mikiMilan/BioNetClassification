import requests
import networkx as nx
from bs4 import BeautifulSoup


def get_protein_sequence(systematic_name):
    url = f"https://yeastgenome.org/search?q={systematic_name}&is_quick=true"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        sequence_element = soup.find("li", id="sequence_tab")
        if sequence_element is None:
            return "X", "kasnije popraviti"
        a_element = sequence_element.find("a")
        if a_element is not None:
            link = a_element["href"]
            url = f"https://yeastgenome.org/backend"+link+"_details"
            headers = {"accept": "application/json"}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                json_response = response.json()
                if len(json_response['protein']) > 0:
                    sequence = json_response['protein'][0]['residues']
                    id = link.split("/")
                    return id[2], sequence
                else:
                    return "X", "sequence not found"
            else:
                return "X", "response not found"
        else:
            return "X", "id_sys not found"
    else:
        return "X", "name not found"


file_path = "data/yeast/BioGRID.txt"
G = nx.Graph()
downloaded = []

with open('sequences.txt', 'r') as file:
    for line in file:
        line = line.strip()
        nodes = line.split(" ") # ili "\t"
        # print(nodes)
        downloaded.append(nodes[0])


with open(file_path, 'r') as file:
    for line in file:
        line = line.strip()
        nodes = line.split("\t") # ili "\t"
        # print(nodes)
        G.add_edge(nodes[0], nodes[1])
print(G)

for node in G.nodes():
    if node not in downloaded:
        print(node)
        sequence = get_protein_sequence(node)
        print(sequence)

        with open('sequences.txt', 'a') as file_seq:
            file_seq.write(node + " " + sequence[0] + " " + sequence[1] + "\n")