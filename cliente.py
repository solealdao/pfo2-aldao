import requests

BASE_URL = "http://localhost:5000"

def registrar():
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    data = {"usuario": usuario, "contraseña": contraseña}
    r = requests.post(f"{BASE_URL}/registro", json=data)
    print(r.json()['mensaje'])

def login():
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    data = {"usuario": usuario, "contraseña": contraseña}
    r = requests.post(f"{BASE_URL}/login", json=data)
    print(r.json()['mensaje'])
    return usuario if r.status_code == 200 else None

def agregar_tarea(usuario):
    descripcion = input("Descripción de la tarea: ")
    data = {"usuario": usuario, "descripcion": descripcion}
    r = requests.post(f"{BASE_URL}/tareas", json=data)
    print(r.json()['mensaje'])

def listar_tareas(usuario):
    r = requests.get(f"{BASE_URL}/tareas/{usuario}")
    if r.status_code == 200:
        tareas = r.json().get('tareas', [])
        if tareas:
            print(f"Tareas de {usuario}:")
            for t in tareas:
                print(f"- [{t['id']}] {t['descripcion']}")
        else:
            print("No hay tareas.")
    else:
        print(r.json()['mensaje'])

def menu():
    usuario_logueado = None
    while True:
        print("\nMenú:")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Agregar tarea")
        print("4. Listar tareas")
        print("5. Salir")
        opcion = input("Elegí una opción: ")

        if opcion == '1':
            registrar()
        elif opcion == '2':
            usuario_logueado = login()
        elif opcion == '3':
            if usuario_logueado:
                agregar_tarea(usuario_logueado)
            else:
                print("Primero iniciá sesión.")
        elif opcion == '4':
            if usuario_logueado:
                listar_tareas(usuario_logueado)
            else:
                print("Primero iniciá sesión.")
        elif opcion == '5':
            print("Adiós!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
