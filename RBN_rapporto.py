import os

from utils import get_args


def leggi_output_motore_mod3(directory):
    file_name = os.path.join(directory, "output_motore.txt")
    f = open(file_name, 'r')

    line = f.readline().split()
    nnodi = eval(line[1])
    ncond = eval(line[3])

    line = f.readline()

    per = []
    mat = []
    while line != "":
        tmp = []

        for el in line.split():
            tmp += [eval(el)]

        linetmp1 = tmp[:nnodi]
        linetmp2 = tmp[nnodi:]
        mat += [linetmp1]
        per += [linetmp2[0]]
        line = f.readline()

    f.close()

    return nnodi, ncond, mat, per


def confronta_vettori_int(v1, v2, n):
    for i in range(n):
        if v1[i] != v2[i]:
            return 0
    return 1


def stampa_file_vettore_int(f, v, n):
    for i in range(n):
        f.write(str(v[i]) + " ")


def stampa_rapporto(n_attr, nnodi, ncond, elenco, mat, per, bacini, directory):
    file_name = os.path.join(directory, "output_motore_rapporto.txt")
    f = open(file_name, 'w')
    f.write("Attrattori: " + str(n_attr) + "   geni: " + str(nnodi) + "\n")

    j = 0
    for i in range(ncond):
        if elenco[i]:
            stampa_file_vettore_int(f, mat[i], nnodi)
            calc = bacini[j] / float(ncond)
            calc2 = "{:.6f}".format(calc)
            del calc
            f.write(" " + str(per[i]) + " " + str(calc2) + "\n")
            j += 1
    f.close()


def rbn_rapporto(directory):
    nnodi, ncond, mat, per = leggi_output_motore_mod3(directory)

    # Alloco elenco
    elenco = []
    for i in range(ncond):
        elenco.append(1)

    # Elimino doppioni
    for i in range(ncond):
        if elenco[i]:
            for j in range(i + 1, ncond, 1):
                if elenco[j]:
                    if confronta_vettori_int(mat[i], mat[j], nnodi):
                        elenco[j] = 0

    # Calcolo numero attrattori
    n_attr = 0
    for i in range(ncond):
        if elenco[i]:
            n_attr += 1

    #print("Numero Attrattori: " + str(n_attr))

    k = 0
    # Alloco bacini
    bacini = []
    for i in range(n_attr):
        bacini.append(0)

    for i in range(ncond):
        if k < n_attr:
            bacini[k] = 1
        if elenco[i]:
            # Conto il numero di vettori uguali al vettore modello
            for j in range(i + 1, ncond, 1):
                if confronta_vettori_int(mat[i], mat[j], nnodi):
                    bacini[k] += 1
            k += 1

    if k > n_attr:
        print("ALLARME n_attrattori: " + str(n_attr) + " j: " + str(k) + "\n")

    #print("bacini attrazione:\n")
    #for i in range(n_attr):
        #print(bacini[i])
    #print("\n")

    stampa_rapporto(n_attr, nnodi, ncond, elenco, mat, per, bacini, directory)


def main():
    args = get_args()

    if args.agent:
        rbn_rapporto("agent")
        print("Rapporto attrattori agente calcolato")
    if args.env:
        rbn_rapporto("environment")
        print("Rapporto attrattori ambiente calcolato")
    if not args.agent and not args.env:
        print("Nessun parametro fornito. Usa -a e/o -e per calcolare il rapporto degli attrattori.")


if __name__=="__main__":
    main()
