import csv
import glob


def get_csv_data() -> list[dict[str, str]]:
    """Cette fonction lit des fichiers csv et copie les données
    dans une liste de dictionnaires

    Returns:
        list[dict[str, str]]: liste des dictionnaire extraites des fichiers csv
    """
    data = []
    files = glob.glob("data/*.csv")
    for file in files:
        with open(file) as f:
            dico = csv.DictReader(f)
            data.extend(list(dico))
    # tri des données
    data.sort(key=lambda row: (row["building_id"], row["lastname"]))
    return data


def display_data(data_to_display: list[dict[str, str]]) -> None:
    """Affiche les données sous forme de table

    Args:
        data_to_display (list[dict[str, str]]): liste de données à afficher
    """
    print(" ".join(data_to_display[0]))  # initialisation champs
    for row in data_to_display:
        print(" ".join(row.values()))


def get_field_and_value(valid_criteria: set[str]) -> tuple[str, str]:
    """Demande à l'utilisateur de choisir un critère et une valeur
    à rechercher dans la base de données.

    Args:
        valid_criteria (set[str]): champs autorisés

    Returns:
        tuple[str, str]: critère et valeur pour la recherche
    """
    criteria_message = "\nSur quel critère voulez-vous effectuer une recherche ?\n"
    field = input(criteria_message)
    # gestion erreur
    while field not in valid_criteria:
        print("Le critère n'est pas valable, choisissez un critère valable parmi :")
        print(" - ".join(sorted(valid_criteria)))
        field = input(criteria_message)

    value = input("\nQuelle valeur souhaitez vous rechercher ?\n")
    return field, value


if __name__ == "__main__":

    data = get_csv_data()

    # récupération des intitulés de colonnes
    keys = set(data[0])

    while True:
        # menu
        user_input = input(
            "\nTapez 1 pour afficher la liste des immeubles.\nTapez 2 pour effectuer une recherche.\n"
        )

        if user_input == "1":
            display_data(data)

        elif user_input == "2":
            field, value = get_field_and_value(keys)
            # filtre données
            filtered_data = [row for row in data if row[field] == value]

            if filtered_data:
                display_data(filtered_data)
            else:
                print(
                    "Cette valeur n'est pas présente dans la base de données.\n"
                )  # gestion erreur
        else:
            print("La valeur saisie n'est pas conforme.\n")  # gestion erreur
