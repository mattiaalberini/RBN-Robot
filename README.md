## Generatore RBN

**`generator_RBN.py`** genera una **RBN** basandosi sui parametri forniti da un file di input. La scelta del file da utilizzare come input dipende dal valore dalla variabile booleana *generatore_semplice*:
- **generatore_semplice = False** (default): **`input_generatore_PIUCOMPLICATO.txt`**
- **generatore_semplice = True**: **`input_generatore_SEMPLICE.txt`**
    
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
- **mode = 2**: stampa tutti gli stati passo per passo
- **mode = 3**: stampa ogni stato al cambiamento