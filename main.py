import json

import numpy as np
import pandas as pd

cursos=pd.read_csv("Cursos.csv")
cursos.id=cursos.id.astype(str)

with open("profile.json") as my_file:
    profile=json.load(my_file)

def simple_menu(promt: str,options: dict):
    '''
     Display a list of options and return a array with the option selected
 Arguments:
     promt: str
        a String to display the instructions
     options: list
        an Array with Strings wich will be used as options
 Returns:
     an integer of the selected option's position 
    '''
    op=0
    #Mientras que el usuario no ingrse s
    while True:
        print(promt)
        #Imprime las opciones y muestra el numero de opción
        for key,value in options.items():
            print(f"({key}):  {value}")
        op=input('Ingrese el numero de opción: ')
        if op in options:
            return op

def menu_multiple_opcion(promt: str,options: list):
    '''
     Display a list of options and return a array with all the options selected
 Arguments:
     promt: str
        a String to display the instructions
     options: list
        an Array with Strings wich will be used as options
 Returns:
     An array with the Strings selected by the user
    '''
    op=0
    #crea un dict y luego lo popula con cada opción disponible y setea los valores en False
    choices={}
    for option in options:
        choices[option]=False
    #Mientras que el usuario no ingrse s
    while op!="S":
        print(promt)
        #Imprime las opciones y muestra el numero de opción
        for contador,value in enumerate(options):
            emoji = "\U00002714" if choices[value] else "\U0000274C"
            print(f"({emoji}){contador}:  {value}")
        op=input('Presione "S" para continuar')
        #la respuesta no será case-sensitive y si es un número ingresado, cambia el valor del atributo 
        op=op.upper()
        if op.isnumeric():
            op=int(op)
            #Revisa que este dentro del rango de opciones
            if op in range(0,len(options)):
                choices[options[op]]= not choices[options[op]]
    #Al terminar el while se crea una variable output y se agrega cada valor en True
    output=[]
    for key in choices:
        if choices[key]:
            output.append(key)
    return output

def input_numerico(promt: str):
    '''
     Ask for a number and stop asking only when a valid number is recived
 Arguments:
     promt: str
        a String to display the instructions
 Returns:
     A numeric value ingresed by the user
    '''
    while True:
        i=input(f"{promt}\n")
        if i.isnumeric():
            return int(i)

def input_bool(promt: str):
    '''
     Ask for a number and stop asking only when 0 or 1 is recived, 
     then it return True if the input is 1, False otherwise
 Arguments:
     promt: str
        a String to display the instructions
 Returns:
     A boolean value given by the user
    '''
    while True:
        i=input(f"{promt}\n(1)Sí\n(0)No")
        if i in ["0","1"]:
            return i=="1"

def select_orientation():
    '''
     Let the user change their interests and update their profile
    '''
    profile["temas"]=menu_multiple_opcion("¿Qué tema te interesa?",list(cursos["categoria"].unique()))
    #Sobreescribimos el perfil
    with open('profile.json', 'w') as file:
        json.dump(profile, file, indent=4)

def recomendar_curso(cursos, profile):
#Si no hay temas seleccionados, ir al panel de selección de temas y guardar la configuración
    if profile["temas"]==[]:
        select_orientation()

#Buscar los cursos en las categorias de interes
    disponible = cursos[cursos["categoria"].isin(profile["temas"])]

#Filtrar los cursos terminados
    disponible= disponible[~(disponible["id"].isin(profile["completo"]))]

#Filtrar por los cursos que cumplen con los requisitos de estudio
    completado = profile["completo"]
    completado.append("inicial")
    requisito = disponible.dependencia.apply(lambda x: set(x.split("-")).issubset(set(completado)))
    disponible=disponible[requisito]

#Filtrar por el tiempo disponible
    minutes=input_numerico("¿Cuantos minutos tiene?")
    disponible=disponible[disponible["minutos"]<minutes]

    metodo = menu_multiple_opcion("¿Cómo quieres estudiar?",["lectura", "video", "audio", "interactivo"])
    final=pd.DataFrame()
    for forma in metodo:
        final=pd.concat([final,disponible[disponible[forma]]])
    final = final[final.duplicated()]
    if final.empty:
        print("No hay cursos disponibles que cumplan con los requisitos.\nCambie los criterios de busqueda")
    else:
        print(final["id","nombre","categoria","minutos","link","lectura","video","audio", "interactivo"])

    _=input("Presione enter para salir")


op=0
while True:
    op=simple_menu("Bienvenido a Voluntad 101 \U0001f600\n",{
    "1": "Cambiar mis intereses",
    "2": "Recomendar un Curso",
    "3": "Terminar un curso (en desarrollo)",
    "Salir": "Salir de la aplicación"
    })
    if op=="1":
        select_orientation()
    if op=="2":
        recomendar_curso(cursos,profile)
    if op=="3":
        print("No implementado. Cambiar directamente profile.json con los id correspondientes")
    if op=="Salir":
        print("Gracias por usar Voluntad 101")
        break




# recomendar_curso(cursos, profile)