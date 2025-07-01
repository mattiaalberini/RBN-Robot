## Generatore RBN e 

**`generator_RBN.py`**

Crea una **RBN** basandosi sui parametri forniti nei file **`input_generatore_SEMPLICE.txt`** e **`input_generatore_PIUCOMPLICATO.txt`**. \
La scelta del file da utilizzare come input dipende dal valore dalla variabile booleana *generatore_semplice*:
- **generatore_semplice = False** (default): **`input_generatore_SEMPLICE.txt`**
- **generatore_semplice = True**: **`input_generatore_PIUCOMPLICATO.txt`**
    
Il file **`grafo_default.txt`** contiene il grafo generato

## Generatore condizioni iniziali

**`generator_initconditions.py`**
    
Genera le **Condizioni iniziali** basandosi sui parametri forniti nel file **`input_gen_cond.txt`**. \
Il file **`cond_default.txt`** contiene le condizioni iniziali generate.


## Simulatore RBN

**`simulator.py`**
    
Simula il comportamento di una RBN partendo dalle condizioni iniziali, basandosi sui parametri nel file **`input_motore.txt`**. \
Il risultato delle simulazioni viene stampato nel file **`output_motore.txt`**. La scelta del formato dell'output dipende dal valore del parametro *mode*:
- **mode = 1**: stampa solo lo stato finale
- **mode = 2**: stampa tutti gli stati passo per passo

## Simulatore interazione agente-ambiente

**`agent_env_interaction.py`**

Simula il comportamento di due RBN (**agente** e **ambiente**) che interagiscono tra loro basandosi sui parametri nel file **`input_AG_AMB.txt`**. \
Il risultato delle simulazioni viene stampato nei file **`output_interaction.txt`**. La scelta del formato dell'output dipende dal valore del parametro *mode*:
- **mode = 1**: stampa solo lo stato finale
- **mode = 2**: stampa tutti gli stati passo per passo
- **mode = 3**: stampa ogni stato al cambiamento