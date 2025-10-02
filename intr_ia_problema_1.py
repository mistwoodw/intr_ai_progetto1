import pysmile
import pysmile_license
from pathlib import Path
import random


def run_decision_network():
    # Caricamento rete
    percorso_file = Path(__file__).parent / "network1.xdsl" 
    net = pysmile.Network()
    net.read_file(str(percorso_file))
    
    # Eventuale evidenza: Ricerca marketing = Effettuare o Non_effettuare
    net.clear_all_evidence()
    net.update_beliefs()

    ask_user_decision(net, "Ricerca_marketing")
    autochoose_outcome(net, "Risultato_ricerca")
    ask_user_decision(net, "Sviluppo_prototipo")
    autochoose_outcome(net, "Qualita_prodotto_2")
    ask_user_decision(net, "Avvio_produzione")
    autochoose_outcome(net, "Domanda_mercato")
    autochoose_outcome(net, "Profitto")

    # Calcolo delle credenze a posteriori
    net.update_beliefs()


def autochoose_outcome(net, node_id):
    if net.get_node_type(node_id) != pysmile.NodeType.CPT:
        raise TypeError(f"'{node_id}' non è un nodo chance (CPT).")
#    if not check_parents_evidence(net, node_id):
#        raise ValueError(f"Non puoi campionare; tutte le evidenze dei genitori del nodo {net.get_node_name(node_id)} devono essere impostate")
    
 
    probs = net.get_node_value(node_id) 
    outcomes = [net.get_outcome_id(node_id, i) for i in range(net.get_outcome_count(node_id))]
    chosen_outcome = random.choices(outcomes, weights=probs)[0]
    net.set_evidence(node_id, chosen_outcome)
    net.update_beliefs()
    print(f"Il risultato di {net.get_node_name(node_id)} è stato campionato come: {chosen_outcome}")
    return None

"""
def check_parents_evidence(net, node_id):
    print(node_id)
    parents = net.get_parent_ids(node_id)
    for parent in parents:
        print(f"parent: {parent}")
        if not net.is_evidence(parent):
            return False
    return True
"""
def ask_user_decision(net, node_id):
    if net.get_node_type(node_id) != pysmile.NodeType.DECISION:
        raise TypeError(f"'{node_id}' non è un nodo decisione.")
    
    print(f"Vuoi effettuare {net.get_node_name(node_id)}:")
    for i in range(net.get_outcome_count(node_id)):
        outcome = net.get_outcome_id(node_id, i)
        outcome_EU = net.get_node_value(node_id)[i]
        print(f"{i}: {outcome} (EU: {outcome_EU:.2f})")
    
    while True:
        try:
            choice = int(input("Inserisci il numero dell'opzione scelta: "))
            if 0 <= choice < net.get_outcome_count(node_id):
                chosen_outcome = net.get_outcome_id(node_id, choice)
                net.set_evidence(node_id, chosen_outcome)
                net.update_beliefs()
                print(f"Hai scelto: {chosen_outcome}")
                return
            else:
                print("Scelta non valida. Riprova.")
        except ValueError:
            print("Input non valido. Inserisci un numero.")

def print_node(net, node_id):
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


    # NOTA: pysmile non supporta get_decision, quindi non è possibile stampare le decisioni ottimali direttamente



if __name__ == "__main__":
    run_decision_network()
