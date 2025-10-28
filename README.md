## Generatore RBN

**`generator_RBN.py`** genera una **RBN** basandosi sui parametri forniti da `input_generatore.txt`. \
Il file `grafo_default.txt` contiene il grafo generato.

## Generatore condizioni iniziali

**`generator_initconditions.py`** genera le **condizioni iniziali** basandosi sui parametri forniti da `input_gen_cond.txt`. \
Il file `cond_default.txt` contiene le condizioni iniziali generate.

## Simulatore RBN

**`simulator.py`** simula il comportamento di una RBN partendo dalle condizioni iniziali, basandosi sui parametri forniti da `input_motore.txt`. \
Il risultato delle simulazioni viene stampato nel file `output_motore.txt`. La scelta del formato dell'output dipende dal valore del parametro *mode*:
- **mode = 1**: stampa solo lo stato finale
- **mode = 2**: stampa tutti gli stati passo per passo
- **mode = 3**: stampa il record maggiore dell'attrattore, il periodo e quanti passi sono stati necessari per trovarlo

## Rapporto attrattori

**`RBN_rapporto.py`** calcola quante volte è presente un record (l'attrattore) nel file `output_motore.txt`, generato in *mode 2*, e la sua percentuale di presenza.
Il risultato viene scritto nel file `output_motore_rapporto.txt`.

## Espandi attrattori

**`espandi_attrattori.py`** genera 2 file usando come input `output_motore_rapporto.txt`:
- `attrattori_espansi.txt`: mostra passo per passo come si sviluppa la RBN nel periodo
- `attrattori_espansi_media.txt`: valori medi dei nodi nel periodo

## Generatore interazione agente-ambiente

**`agent_env_generator.py`** genera le RBN e le condizioni iniziali dell'agente e dell'ambiente a seconda dei parametri forniti nel file `agent_env_generator_input.txt`.

## Simulatore interazione agente-ambiente

**`agent_env_interaction.py`** simula il comportamento di due RBN (**agente** e **ambiente**) che interagiscono tra loro, basandosi sui parametri forniti da `input_AG_AMB.txt`. \
Il risultato delle simulazioni viene stampato nei file `output_interaction.txt`. La scelta del formato dell'output dipende dal valore del parametro *mode*:
- **mode = 1**: stampa solo lo stato finale
- **mode = 2**: stampa tutti gli stati passo per passo, stampa ogni stato al cambiamento sul file `output_interaction_mode3.txt` e calcola il benessere dell'agente.
- **mode = 3**: stampa ogni stato al cambiamento

Nei file `variazione_nodi.txt` vengono stampati i valori dei:
- nodi sensori per l'agente
- nodi su cui hanno effetto gli effettori per l'ambiente

Nelle colonne a sinistra sono stampati i valori attuali dei nodi, nelle colonne a destra vengono stampati i valori che i nodi avrebbero senza l'interazione agente-ambiente.

## Calcolo benessere

**`benessere_calculator.py`** calcola il **benessere** dell'agente basandosi sui parametri forniti da `input_benessere.txt` e dagli stati dell'agente presenti nel file `output_interaction_mode3.txt`. 
File generabile solamente simulando l'interazione agente-ambiente in *mode 2*. \
Il valore del benessere per ogni condizione iniziale, viene salvato nel file `benessere_agent.txt`.

## Gestore interazione agente-ambiente e calcolo benessere

**`benessere_interaction_simulator.py`** gestisce l'interazione agente-ambiente e calcola il benessere a seguito della modifica delle funzioni booleane dei nodi essenziali dell'agente, letti dal file `input_benessere.txt`.
Si basa sui parametri forniti dal file `benessere_interaction_simulator_input.txt`, dove viene specificato il numero di interazioni da effettuare e la modalità:
- **mode = a**: usa sempre le stesse condizioni iniziali
- **mode = b**: le nuove condizioni iniziali saranno l'ultimo stato in cui mi trovavo nella precedente interazione

Nel file `benessere_interaction_simulator_output.txt` viene salvato il benessere dell'agente, con le funzioni booleane dei nodi essenziali.

Le condizioni iniziali di partenza sono scelte con la seguente procedura:
1. Genero nuove condizioni iniziali
2. Trovo gli attrattori
3. Scelgo il primo record dal file `attrattori_espansi.txt`
4. Modifico il file `input_benessere.txt` fissando omega=periodo, e il valore ideale dei nodi essenziali dal file `attrattori_espansi_media.txt`

## Lanci multipli di "Gestore interazione agente-ambiente e calcolo benessere"

**`benessere_interaction_launcher.py`** lancia N volte il file `benessere_interaction_simulator.py` e memorizza i risultati dei vari lanci nella cartella `risultati_lanci`. \
Nel file `benessere_interaction_launcher_input.txt` è contenuto:
- il nome da dare alla cartella contenente i diversi lanci (se esiste già una cartella con lo stesso nome, aggiunge al nome della cartella un numero incrementale)
- il numero di lanci da effettuare
- l'omega con cui il benessere deve essere calcolato

Prima di ogni lancio esegue `agent_env_generator.py`, che, leggendo il file di input `agent_env_generator_input.txt`, eventualmente ricrea le RBN e le condizioni iniziali.

Nella cartella contenente i diversi lanci verrà creato il file `sintesi.xlsx` che contiene:
- il benessere e la funzione booleana dei nodi effettori di ogni simulazione, presi dal file `benessere_interaction_simulator_output.txt`
- il profilo (il valore ideale dei nodi essenziali) di ogni lancio

## Evoluzione agente

**`evolution.py`** gestisce l'evoluzione dell'agente e memorizza le varie generazioni nella cartella `risultati_evoluzione`. \
Legge i parametri forniti dal file `evolution_input.txt`:
- il nome da dare alla cartella contenente le diverse generazioni (se esiste già una cartella con lo stesso nome, aggiunge al nome della cartella un numero incrementale)
- il numero massimo di generazioni da creare
- l'omega con cui il benessere deve essere calcolato
- la probabilità che a cambiare sia un nodo effettore
- la probabilità che a cambiare sia il nodo dell'ambiente su cui agisce un nodo effettore

Inizialmente genera il padre G0 (tramite `benessere_interaction_simulator.py`), dei tentativi fatti prende quello con il benessere migliore. Quelle saranno le funzioni booleane di partenza del figlio G1. \
Questo procedimento verrà effettuato ogni volta che viene generato un nuovo figlio. \
Genera il figlio con le nuove funzioni booleane, e in modo casuale, verranno cambiati o i nodi dell'ambiente su cui agiscono i nodi effettori o i nodi effettori.
- se il nuovo figlio generato avrà un benessere migliore o uguale a quello del padre, la prossima generazione verrà creata a partire dal figlio.
- se il nuovo figlio generato avrà un benessere peggiore di quello del padre, la prossima generazione verrà ricreata a partire dal padre.

La generazione termina quando il benessere diventa 0 oppure quando viene raggiunto il limite massimo di generazioni imposto dal file di input.

Nella cartella contenente le diverse generazioni verrà creato il file `sintesi.xlsx` (ogni riga equivale a una generazione) che contiene:
- il benessere migliore tra quelli calcolati
- i nodi effettori
- i nodi dell'ambiente su cui agiscono i nodi effettori
- la funzione booleana dei nodi effettori che hanno portato al benessere migliore
- il profilo (il valore ideale dei nodi essenziali) 
- S/N: indica se abbiamo trovato un figlio migliore del padre

## Lanci multipli di "Evoluzione agente"

**`evolution_launcher.py`** lancia N volte il file `evolution.py` e memorizza i risultati dei vari lanci nella cartella `risultati_lanci_evoluzione`. \
Nel file `evolution_launcher_input.txt` è contenuto:
- il nome da dare alla cartella contenente i diversi lanci (se esiste già una cartella con lo stesso nome, aggiunge al nome della cartella un numero incrementale)
- il numero di lanci da effettuare

Nella cartella contenente i diversi lanci verrà creato il file `sintesi.xlsx` che contiene l'esito di tutte le evoluzioni eseguite.