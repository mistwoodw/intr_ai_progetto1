import pysmile
import pysmile_license
from pathlib import Path
import random


def run_decision_network():
    # Caricamento rete
    percorso_file = Path(__file__).parent / "network1.xdsl" 
    net = pysmile.Network()
    net.read_file(str(percorso_file))
    
    net.clear_all_evidence()
    net.update_beliefs()

    # Esecuzione del processo decisionale
    ask_user_decision(net, "Ricerca_marketing")
    autochoose_outcome(net, "Risultato_ricerca")
    ask_user_decision(net, "Sviluppo_prototipo")
    autochoose_outcome(net, "Qualita_prodotto_2")
    ask_user_decision(net, "Avvio_produzione")
    print(f"Utilità attesa: {net.get_node_value('Utilita_totale')[0]:.2f}")



def autochoose_outcome(net, node_id): #scelta casuale basata sulle probabilità
    if net.get_node_type(node_id) != pysmile.NodeType.CPT:
        raise TypeError(f"'{node_id}' non è un nodo chance (CPT).")
 
 
    probs = net.get_node_value(node_id) 
    outcomes = [net.get_outcome_id(node_id, i) for i in range(net.get_outcome_count(node_id))]
    chosen_outcome = random.choices(outcomes, weights=probs)[0]
    net.set_evidence(node_id, chosen_outcome)
    net.update_beliefs()
    print(f"Il risultato di {net.get_node_name(node_id)} è stato campionato come: {net.get_evidence_id(node_id)}")
    return None


def ask_user_decision(net, node_id): #scelta manuale dell'utente basata su utilità
    if net.get_node_type(node_id) != pysmile.NodeType.DECISION:
        raise TypeError(f"'{node_id}' non è un nodo decisione.")
    
    print(f"Vuoi effettuare {net.get_node_name(node_id)}:")
    for i in range(net.get_outcome_count(node_id)):
        outcome = net.get_outcome_id(node_id, i)
        outcome_EU = net.get_node_value(node_id)[i]
        print(f"\t{i}: {outcome} (EU: {outcome_EU:.2f})")
    
    while True:
        try:
            choice = int(input("\tInserisci il numero dell'opzione scelta: "))
            if 0 <= choice < net.get_outcome_count(node_id):
                chosen_outcome = net.get_outcome_id(node_id, choice)
                net.set_evidence(node_id, chosen_outcome)
                net.update_beliefs()
                print(f"Hai scelto: {net.get_evidence_id(node_id)}")
                return
            else:
                print("Scelta non valida. Riprova.")
        except ValueError:
            print("Input non valido. Inserisci un numero.")

def print_node(net, node_id): #funzione di sviluppo per stampare informazioni sul nodo
    node_name = net.get_node_name(node_id)

    # Tipo di nodo
    node_type = net.get_node_type(node_id)
    if node_type == pysmile.NodeType.CPT:
        tipo = "Chance"
    elif node_type == pysmile.NodeType.DECISION:
        tipo = "Decision"
    elif node_type == pysmile.NodeType.UTILITY:
        tipo = "Utility"
    else:
        tipo = "Altro"

    node_value = net.get_node_value(node_id)
    print(f"Nodo: {node_id}, {node_name}, Tipo: {tipo}, Valore: {node_value}")
    if node_type == pysmile.NodeType.DECISION:
        for i in range(net.get_outcome_count(node_id)):
            outcome = net.get_outcome_id(node_id, i)
            print(f"   {outcome}: {node_value[i]:.2f} numero {i}")


if __name__ == "__main__":
    run_decision_network()
