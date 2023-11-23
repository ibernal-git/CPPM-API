import sys
from utils.constants import *


def print_menu():
    print("\n<---------------------------------------------------->\n")
    print("¿Qué desea hacer?")
    print("1. Buscar usuarios locales")
    print("2. Buscar endpoints")
    print("3. Buscar usuarios locales y endpoints")
    print("4. Buscar endpoints y comprobar roles asignados (atributo Last Known Role)")
    print("5. Buscar sesiones activas de dispositivos en mac.txt")
    print("6. Buscar sesiones activas en un Device (Introducir NAS IP)")
    print("7. Salir")


def get_user_choice():
    while True:
        opcion = input("Ingrese su opción[1/2/3/4/5/6/7]: ")
        if opcion.isdigit():
            return int(opcion)
        else:
            print("\nOpción inválida. Intente nuevamente.")


def show_menu():
    while True:
        print_menu()
        opcion = get_user_choice()

        if opcion == 1:
            return LOCAL_USERS
        elif opcion == 2:
            return ENDPOINTS
        elif opcion == 3:
            return None
        elif opcion == 4:
            return ENDPOINTS_ROLE
        elif opcion == 5:
            return ACTIVE_SESSION
        elif opcion == 6:
            return NAS_SESSION
        elif opcion == 7:
            sys.exit()
        else:
            print("\nOpción inválida. Intente nuevamente.")
