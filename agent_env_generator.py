import subprocess

from utils import read_file


# Controllore ammissibilità parametri
def check_parameters(use_agent_RBN, use_agent_condini, use_env_RBN, use_env_condini):
    if use_agent_RBN != "S" and use_agent_RBN != "N":
        raise ValueError("'usare agente già presente' diverso da 'S' o 'N'")
    if use_agent_condini != "S" and use_agent_condini != "N":
        raise ValueError("'usare condini agente già presenti' diverso da 'S' o 'N'")
    if use_env_RBN != "S" and use_env_RBN != "N":
        raise ValueError("'usare ambiente già presente' diverso da 'S' o 'N'")
    if use_env_condini != "S" and use_env_condini != "N":
        raise ValueError("'usare condini ambiente già presenti' diverso da 'S' o 'N'")


def main():

    parameters = read_file("agent_env_generator_input.txt")

    use_agent_RBN = parameters["usare agente già presente"]
    use_agent_condini = parameters["usare condini agente già presenti"]
    use_env_RBN = parameters["usare ambiente già presente"]
    use_env_condini = parameters["usare condini ambiente già presenti"]

    check_parameters(use_agent_RBN, use_agent_condini, use_env_RBN, use_env_condini)

    if use_agent_RBN == "N":
        subprocess.run(["python", "generator_RBN.py", "-a"])
    if use_agent_condini == "N":
        subprocess.run(["python", "generator_initconditions.py", "-a"])
    if use_env_RBN == "N":
        subprocess.run(["python", "generator_RBN.py", "-e"])
    if use_env_condini == "N":
        subprocess.run(["python", "generator_initconditions.py", "-e"])


if __name__ == "__main__":
    main()