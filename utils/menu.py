import sys
from utils.constants import *
def show_menu():
  while True:
    print("\n<---------------------------------------------------->\n")
    print("¿Qué desea hacer?")
    print("1. Buscar usuarios locales")
    print("2. Buscar endpoints")
    print("3. Buscar usuarios locales y endpoints")
    print("4. Salir")
    
    opcion = input("Ingrese su opción[1/2/3/4]: ")
    
    if opcion == "1":
        return LOCAL_USERS
    elif opcion == "2":
        return ENDPOINTS
    elif opcion == "3":
        return None
    elif opcion == "4":
        sys.exit()
    else:
        print("\nOpción inválida. Intente nuevamente.")