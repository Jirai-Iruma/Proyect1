import os
import sys
import getpass
#getpass ya viene incluido en la libreria de Python
import msvcrt
#msvcrt ya viene incluido en la libreria de Python
from dotenv import load_dotenv  
#pip install python-dotenv
from datetime import date

def fechact():
    #Día actual
    fec = str(date.today()).split('-')
    return fec[2] + "-" + fec[1] + "-" + fec[0]

def dgpause(prompt='\n\tOprima cualquier tecla para continuar ...', ver=0):
    """
    Esta funcion simula la instruccion os.system('pause'). 

    Parametros:
    prompt: msg que se presenta para esperar que el usuario oprima una tecla
    
    Salida:
    str: tecla oprimida en formato Unicode
    """
    print("="*ancho)
    print(prompt,end='')
    c=msvcrt.getwch()
    if ver: print(f'{c}')
    return  c

def el_borra_pantalla(): #Definimos la función estableciendo el nombre que queramos
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")


def busca_producto(lista_productos,producto):
    for un_producto in lista_productos:
        if un_producto[0]==producto:
            return un_producto
    return []

def dgleerpass(clave, prompt, clearpant=True,retries=3, reminder='\n\tResponda de nuevo!'):
    pase=False
    totint=retries
    while True:
        if clearpant: el_borra_pantalla()
        if pase:
            totint-=1
            print(reminder, 'Te quedan ', totint, ' intentos')
        ok =getpass.getpass(f'\n\t{prompt}')
        if ok==clave:
            return True
        retries -=  1
        if retries == 0:
            return False
        pase=True


def dgcrear_arch_producto(nom_arch_prodcto):
    modo='a'
    with open(nom_arch_prodcto,modo) as arc:
        el_borra_pantalla
        producto=input('\tIndique el codigo del producto  [-1 para finalizar] ')
        while len(producto)>0 and producto!='-1':
            denominacion=input(f'\tIndique la denominacion del producto: ')
            precref= float(input(f'\tIndique la precio de referencia: '))
            descuento= float(input(f'\tIndique el descuento : '))
            excento=input(f'\tIndique si esta excento de iva (s/n): ').lower()
            reg=f'{producto},{denominacion},{precref},{descuento},{excento}\n'
            arc.write(reg)
            el_borra_pantalla
            producto=input('\tIndique el codigo del producto  [-1 para finalizar] ')

def dgcrear_arch_ref_BCV():
    f=fechact()
    el_borra_pantalla
    try:
        ref=float(input(f'\tIndique el precio del $ para el {f}? '))
    except:
        ref=0.0
    
    print()
    if ref==0.0:
        print(f'Se mantiene el mismo precio de referencia del dian de ayer !!!'.center(ancho))
        modo='r'
        with open(fecbcv,modo) as arc:
           fr= arc.read().split(',')
        ref=float(fr[1])

    modo='w'
    with open(fecbcv,modo) as arc:
        reg=f'{f},{ref}'
        arc.write(reg)
    return f,ref

def leer_acrchivo_lista_productos(nom_arch):
    try:
        modo='r'
        with open(nom_arch,modo) as arc:
            reg=arc.read().split('\n')
    
        if len(reg[len(reg)-1])==0:
            reg.pop()

        lista_producto=[]
        for nreg in reg:
            un_prod=nreg.split(',')
            lista_producto.append([un_prod[0],\
                                un_prod[1].strip(),\
                                float(un_prod[2]),\
                                float(un_prod[3]),\
                                un_prod[4]])

        return lista_producto
    except:
        return []
def menu():
        """
        Muestra el menú de opciones.
        """
        el_borra_pantalla()
        print(f"""{rsocial:=^{ancho}}{d[3]}
\t1. Actualizar lista de productos
\t2. Actualizar referencia del BCV
\t3. Usar balanza
\t4. Salir{d[0]}""")
        
def menuadmin():
        """
        Muestra el menú de opciones.
        """
        el_borra_pantalla()
        print(f"""{rsocial:=^{ancho}}{d[3]}
\t1. Agregar nuevos productos
\t2. Modificar un producto
\t3. Regresar{d[0]}""")


d = {1 :'\x1b[31m', #rojo
     2 :'\x1b[32m', #verde
     3 :'\x1b[33m', #amarillo
     4 :'\x1b[34m', #azul
     5 :'\x1b[35m', #morado
     6 :'\x1b[36m', #cian
     7 :'\x1b[37m', #blanco
     0 :'\x1b[0m'   #default
     }
if __name__=="__main__":
    # Cargar las variables del archivo .env  
    if not load_dotenv():
        el_borra_pantalla
        print(f'\tNo se encuentra el archivo de ambiente')
        print(f'\tEl ATM se detendrá. Cre de nuevo el archivo ') 
        quit()

    # Acceder a las variables de entorno  
    secret_key = os.getenv('SECRET_KEY')  
    debug = os.getenv('DEBUG') == 'True'  
    arc_producto=os.getenv('ARC_PRODUCTO')
    fecbcv=os.getenv("ARC_FECBCV")
    ancho=int(os.getenv("ANCHO"))
    auto=os.getenv("AUTO") == 'True'
    rsocial=os.getenv("RAZONSOCIAL")

    admin=True
    if len(sys.argv)>1:
        if sys.argv[1]=='admin':
            ok =getpass.getpass(f'\n\tIngrese su clave de administrdo ')
            admin=ok==secret_key
    # Usar las variables de entorno  
    if  debug:
        print(f'Archivo de productos: {arc_producto}')   
        print(f'Archivo de BCV: {fecbcv}') 

        print(f'Secret Key: {secret_key}')  
        print(f'Debug Mode: {debug}')
        print(f'Admin: {admin}') 
        print(f'Ancho: {ancho}') 
        print(f'Auto: {auto}') 
        print(f'Banco: {rsocial}') 
        dgpause()
    

    productos=leer_acrchivo_lista_productos(arc_producto)
    nohaydatos=len(productos)==0
    if nohaydatos:
        opcion="1"
    else:
        menu()
        opcion = input(f'\n\t{d[4]}Ingrese una opción: {d[0]}')
    
    while (opcion != "4"):
        if opcion == "1" :
            if nohaydatos:
                el_borra_pantalla()
                print(f'Para poder arrancar el sistema debe agregar productos al archivo de Productos')
                dgpause()

            if nohaydatos or dgleerpass(secret_key,"Indique su clave de acceso "):
                if nohaydatos:
                    opc="1"
                else:
                    menuadmin()
                    opc = input(f'\n\t{d[4]}Ingrese una opción: {d[0]}')

                while (opc != "3"):
                    if opc == "1":
                        el_borra_pantalla()
                        dgcrear_arch_producto(arc_producto)
                        productos=leer_acrchivo_lista_productos(arc_producto)
                        nohaydatos=len(productos)==0
                        if nohaydatos:
                            print(f'\n\t{d[1]}Al no agregar datos se supone que no desea inicializar el sistema.{d[0]}')
                            quit()

                    if opc == "2":
                        productos=leer_acrchivo_lista_productos(arc_producto)
                        nohaydatos=len(productos)==0
                    
                    menuadmin()
                    opc = input(f'\n\t{d[4]}Ingrese una opción: {d[0]}')

                dgpause()
                print(1)
            else:
                el_borra_pantalla()
                print(f'{ancho*"="}')
                print(f'   acceso no autorizado '.center(ancho,'='))
                print(f'{ancho*"="}')
                dgpause()
                quit()
        if opcion == "2":
            f,ref=dgcrear_arch_ref_BCV()

            dgpause()
        if opcion == "3":
            el_borra_pantalla()
            nombre_del_producto = input("\tBIENVENIDO\n\tIndique el código o nombre del producto: ").strip()
            prod = busca_producto(productos, nombre_del_producto)
            if not prod:
                print(f"\n\t{d[1]}Producto no encontrado.{d[0]}")
                dgpause()
            else:
                try:
                    peso = float(input(f"\tIngrese el peso en kg: "))
                    if prod[4]:
                        valor = prod[2] * peso * (1 - prod[3])
                        valor_con_iva = valor * 1.16
                        print(f"El valor a pagar por {peso} kg de {prod[1]} es: {valor_con_iva}")
                    else:
                        valor = (prod[2] * peso * (1 - prod[3]))
                        print(f"El valor a pagar por {peso} kg de {prod[1]} es: {valor}")
                except Exception as e:
                    print(f"\n\t{d[1]}Error en el peso proseso.")
                dgpause()

        menu()
        opcion = input(f'\n\t{d[4]}Ingrese una opción: {d[0]}')