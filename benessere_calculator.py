import os


# Lettore parametri da file
def read_file(file_name):
    parameters_app = {}

    with open(file_name, "r", encoding="utf-8") as file:
        next_read = ""

        for line in file:
            if ":" in line:
                next_read = ""
                parameters_app[line.split(":")[0].strip()] = line.split(":")[1].strip()
            elif "ESSENZIALI" in line:
                next_read = "essenziali"
                parameters_app["essenziali"] = {}


            if next_read == "essenziali":
                parts = line.split()
                if len(parts) == 2:
                    nodo = int(parts[0])
                    val = float(parts[1])
                    parameters_app["essenziali"][nodo] = val

    return parameters_app


def read_states(file_name):
    states = {}

    with open(file_name, "r", encoding="utf-8") as file:
        first_line = file.readline().split()
        # second_line = file.readline().split() # init_condition

        n_cond = int(first_line[3])

        for index, line in enumerate(file):
            state = [int(x) for x in line.split()]
            states[index] = state

    return n_cond, states


def calculate_benessere(states, omega):
    for i, s in enumerate(states, start=1):
        if i % omega == 0:
            print(str(i))
            print(states[s])



def main():
    parameters = read_file("input_benessere.txt")

    omega = int(parameters["omega"])

    # ID NODO AGENTE - Valore ideale
    essenziali = parameters["essenziali"]

    n_cond, states = read_states(os.path.join("agent", "output_interaction_mode3.txt"))

    calculate_benessere(states, omega)


if __name__ == "__main__":
    main()