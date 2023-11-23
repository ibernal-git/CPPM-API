from pyclearpass import *
from dotenv import dotenv_values
from utils.constants import *
from utils.filter import get_filter
from utils.menu import show_menu
import sys
import getpass
import json
import pandas as pd


# Manejo de excepciones
def read_file_safe(file_name):
    try:
        with open(file_name) as file:
            return file.read().splitlines()
    except FileNotFoundError as error:
        print(f"ERROR: {error}")
        sys.exit()


# Imprimir mensajes constantes
def print_separator():
    print("\n<---------------------------------------------------->\n")


def print_invalid_option():
    print("\nOpción inválida. Intente nuevamente.")


# Lectura de credenciales
def get_credentials():
    username = input("Escribe el usuario: ")
    try:
        password = getpass.getpass()
        return username, password
    except Exception as error:
        print(f"ERROR: {error}")
        sys.exit()


# Funcion para obtener valores de diccionario
def get_val(i, dict):
    for key, value in dict.items():
        if i == key:
            return value


def result_validation(result):
    if get_val("status", result) == 401:
        print("Error: credenciales invalidas")
        sys.exit()
    count_result = get_val("count", result)
    if count_result is None:
        print("No se han encontrado MACs en Clearpass\n")
        raise FileNotFoundError("No se han encontrado MACs en Clearpass")
    if count_result > 1000:
        print(f"Total MACs en CPPM: {count_result}\n")
        print(
            "El numero de MACs en Clearpass supera los 1000, reduce el numero de MACs en el fichero\n"
        )
        raise ValueError("El numero de MACs en Clearpass supera los 1000")

    if count_result:
        print(f"Total en CPPM: {count_result}\n")
        print_separator()


def print_results_not_found(items_not_found, filter_name, file_name=DETAILS_FILE_NAME):
    print(
        f"\nTotal de elementos no encontrados en CPPM ({filter_name}): {len(items_not_found)}"
    )
    print(f"Elementos no encontrados en CPPM ({filter_name}): {items_not_found}")
    print_separator()
    print(f"Detalles guardados en archivo {file_name}\n")


def check_results(result, filter, macs_array, file_name=DETAILS_FILE_NAME):
    embedded = get_val("_embedded", result).get("items")
    cppm_macs = extract_cppm_macs(embedded, filter)
    items_not_found = []
    json_data_list = create_json_data_list(
        cppm_macs, filter, macs_array, items_not_found
    )
    write_json_to_file(json_data_list, file_name)

    print_not_found_message(items_not_found, filter, file_name)

    option_not_found = input("¿Deseas guardar los elementos no encontrados? (s/n): ")
    if option_not_found == "s":
        file_name = input("Introduce el nombre del fichero: ")
        write_json_to_file(items_not_found, file_name)
        print(f"Detalles guardados en archivo {file_name}\n")


def extract_cppm_macs(embedded, filter):
    cppm_macs = []
    for elem in embedded:
        if filter == FILTER[ACTIVE_SESSION] or filter == FILTER[NAS_SESSION]:
            cppm_macs.append((get_val(CALLING_STATION_ID, elem), elem))
        else:
            if filter == FILTER[ENDPOINTS_ROLE]:
                cppm_macs.append((get_val("mac_address", elem), elem))
            else:
                cppm_macs.append((get_val(filter, elem), get_val("attributes", elem)))
    return cppm_macs


def create_json_data_list(cppm_macs, filter, macs_array, items_not_found):
    json_data_list = []

    for mac in macs_array:
        encontrado = False
        for tupla in cppm_macs:
            if mac in tupla[0]:
                json_data, encontrado = create_json_data(mac, filter, tupla)
                if json_data:
                    json_data_list.append(json_data)
                break
        if not encontrado:
            items_not_found.append(mac)
            print_not_found_data(mac, encontrado, filter)
    return json_data_list


def create_json_data(mac, filter, tupla):
    if filter == FILTER[ENDPOINTS_ROLE]:
        role = get_val("attributes", tupla[1]).get("Last Known User Role")
        json_data = {"mac": mac, "Role": role} if role is not None else None
        encontrado = role is not None
        print_found_data(mac, role, encontrado, filter)
    else:
        json_data = {"mac": mac, "details": tupla[1]}
        encontrado = True
        print_found_data(mac, tupla[1], encontrado, filter)
    return json_data, encontrado


def write_json_to_file(json_data_list, file_name):
    with open(file_name, "w") as f:
        json.dump(json_data_list, f, indent=2)


def print_found_data(mac, data, encontrado, filter):
    if encontrado:
        print(f"{mac} encontrado en Clearpass")
        if filter != FILTER[ACTIVE_SESSION]:
            print(f"Detalles: {data}")
        print_separator()


def print_not_found_data(mac, encontrado, filter):
    if not encontrado:
        print(f"{mac} <NO> encontrado en Clearpass")
        print_separator()


def print_not_found_message(items_not_found, filter, file_name):
    if filter == FILTER[LOCAL_USERS]:
        print_results_not_found(items_not_found, "usuarios locales", file_name)
    elif filter == FILTER[ENDPOINTS]:
        print_results_not_found(items_not_found, "endpoints", file_name)
    elif filter == FILTER[ENDPOINTS_ROLE]:
        print_results_not_found(items_not_found, "roles", file_name)
    elif filter == FILTER[ACTIVE_SESSION]:
        print("\nDetalles guardados en archivo %s\n" % file_name)
        print(
            "MACS sin sesiones encontradas en CPPM: %s\n %s\n"
            % (len(items_not_found), items_not_found)
        )
    elif filter == FILTER[NAS_SESSION]:
        print("\nDetalles guardados en archivo %s" % file_name)


def read_file(file_name):
    try:
        with open(file_name) as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print(f"Fichero no encontrado: {file_name}")
        sys.exit()


# Bucle principal
def main():
    config = dotenv_values(".env")
    if not config or not config.get("SERVER") or not config.get("CLIENT_ID"):
        print("Fichero .env no encontrado o incompleto")
        sys.exit()

    SERVER = config["SERVER"]
    CLIENT_ID = config["CLIENT_ID"]

    username, password = get_credentials()
    login = ClearPassAPILogin(
        server=SERVER,
        granttype="password",
        username=username,
        password=password,
        clientid=CLIENT_ID,
        verify_ssl=True,
    )

    while True:
        menu_option = show_menu()
        print_separator()
        macs_array = read_file_safe(FILE_NAME)
        if menu_option in [LOCAL_USERS, ENDPOINTS, ENDPOINTS_ROLE]:
            print(f"\nTotal de elementos en Archivo <{FILE_NAME}>: {len(macs_array)}\n")

            print(f"Buscando en CPPM...\n")
            api_result = (
                ApiIdentities.get_local_user(
                    login,
                    get_filter(macs_array, menu_option),
                    calculate_count="true",
                    limit=1000,
                )
                if menu_option == LOCAL_USERS
                else ApiIdentities.get_endpoint(
                    login,
                    get_filter(macs_array, menu_option),
                    calculate_count="true",
                    limit=1000,
                )
            )
            result_validation(api_result)
            if menu_option == ENDPOINTS_ROLE:
                check_results(api_result, FILTER[ENDPOINTS_ROLE], macs_array)
            else:
                check_results(api_result, FILTER[menu_option], macs_array)

        elif menu_option == None:
            print("Buscando usuarios locales y endpoints...\n")
            api_result_local = ApiIdentities.get_local_user(
                login,
                get_filter(macs_array, LOCAL_USERS),
                calculate_count="true",
                limit=1000,
            )
            api_result_endpoints = ApiIdentities.get_endpoint(
                login,
                get_filter(macs_array, ENDPOINTS),
                calculate_count="true",
                limit=1000,
            )
            result_validation(api_result_local)
            check_results(
                api_result_local, FILTER[LOCAL_USERS], macs_array, "local_users.json"
            )
            print_separator()
            result_validation(api_result_endpoints)
            check_results(
                api_result_endpoints, FILTER[ENDPOINTS], macs_array, "endpoints.json"
            )

        elif menu_option == ACTIVE_SESSION:
            print(f"\nTotal de elementos en Archivo <{FILE_NAME}>: {len(macs_array)}\n")
            print("Buscando Logs de sesiones...\n")

            api_result = ApiSessionControl.get_session(
                login,
                get_filter(macs_array, ACTIVE_SESSION),
                calculate_count="true",
                limit=1000,
                sort="-acctsessionid",
            )
            result_validation(api_result)
            check_results(api_result, FILTER[ACTIVE_SESSION], macs_array)

        elif menu_option == NAS_SESSION:
            nasipaddress = input("Introduce la IP del NAS: ")
            print("Buscando Logs de sesiones...\n")

            api_result = ApiSessionControl.get_session(
                login,
                get_filter(macs_array, NAS_SESSION, nasipaddress),
                calculate_count="true",
                limit=1000,
                sort="-acctsessionid",
            )
            result_validation(api_result)
            check_results(api_result, FILTER[NAS_SESSION], macs_array)


# Punto de entrada del programa
if __name__ == "__main__":
    main()
