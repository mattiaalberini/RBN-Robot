## Generatore RBN

**`generator_RBN.py`** genera una **RBN** basandosi sui parametri forniti da **`input_generatore.txt`**. \
Il file **`grafo_default.txt`** contiene il grafo generato.

## Generatore condizioni iniziali

**`generator_initconditions.py`** genera le **condizioni iniziali** basandosi sui parametri forniti da **`input_gen_cond.txt`**. \
Il file **`cond_default.txt`** contiene le condizioni iniziali generate.


## Simulatore RBN

**`simulator.py`** simula il comportamento di una RBN partendo dalle condizioni iniziali, basandosi sui parametri forniti da **`input_motore.txt`**. \
Il risultato delle simulazioni viene stampato nel file **`output_motore.txt`**. La scelta del formato dell'output dipende dal valore del parametro *mode*:
- **mode = 1**: stampa solo lo stato finale
- **mode = 2**: stampa tutti gli stati passo per passo

## Simulatore interazione agente-ambiente

**`agent_env_interaction.py`** simula il comportamento di due RBN (**agente** e **ambiente**) che interagiscono tra loro, basandosi sui parametri forniti da **`input_AG_AMB.txt`**. \
Il risultato delle simulazioni viene stampato nei file **`output_interaction.txt`**. La scelta del formato dell'output dipende dal valore del parametro *mode*:
- **mode = 1**: stampa solo lo stato finale
- **mode = 2**: stampa tutti gli stati passo per passo, stampa ogni stato al cambiamento sul file **`output_interaction_mode3.txt`** e calcola il benessere dell'agente.
- **mode = 3**: stampa ogni stato al cambiamento

Nei file **`variazione_nodi.txt`** vengono stampati i valori dei:
- nodi sensori per l'agente
- nodi su cui hanno effetto gli effettori per l'ambiente

Nelle colonne a sinistra sono stampati i valori attuali dei nodi, nelle colonne a destra vengono stampati i valori che i nodi avrebbero senza l'interazione agente-ambiente.

## Calcolo benessere
**`benessere_calculator.py`** calcola il **benessere** dell'agente basandosi sui parametri forniti da **`input_benessere.txt`** e dagli stati dell'agente presenti nel file **`output_interaction_mode3.txt`**. 
File generabile solamente simulando l'interazione agente-ambiente in *mode 2*. \
Il valore del benessere per ogni condizione iniziale, viene salvato nel file **`benessere_agent.txt`**.