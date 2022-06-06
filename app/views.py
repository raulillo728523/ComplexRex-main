from django.shortcuts import render, redirect
from .models import Producto, UserComplex
from django.contrib.auth.decorators import login_required

from django.db import connection
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from dynamic_db_router import in_database
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import cryptocode
import cv2 as cv
import webbrowser
import qrcode

# Clave secreta para encriptar y desencriptar

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# Create your views here.
# Prueba de cambios 
class newQR(APIView):
    @action(detail=True, methods=['POST']) 
    def post(self, request, format=None):
        try:
            # print(clave)
            # print(des)
            nombre = request.data["nombre"]
            casa = request.data["casa"]
            id = request.data["id"]
            data = id+'_'+casa
            info = cryptocode.encrypt(data,"cmpx")
            print (info)
            save_path = "app/static/app/img/QRS/"
            completeName = save_path+casa+'_'+nombre+'.png'
            UserComplex.objects.filter(id = id).update(QR = completeName[11:])
            img = qrcode.make(info)
            img.save(completeName)
            
            return Response({
                        'data':id,
                        'status':'1',
                        'message': 'Correcto'
                    },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                        'data':'',
                        'status':'2',
                        'message': 'No se pudo obtener la informacion: '+ str(e)
                    },status=status.HTTP_400_BAD_REQUEST)

class getQR(APIView):
    @action(detail=True, methods=['POST']) 
    def post(self, request, format=None):
        try:
            dato= request.data["data"]
            return Response({
                        'data':dato,
                        'status':'1',
                        'message': 'Correcto'
                    },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                        'data':'',
                        'status':'2',
                        'message': 'No se pudo obtener la informacion: '+ str(e)
                    },status=status.HTTP_400_BAD_REQUEST)

def home(request):
    products = Producto.objects.all()
    data = {
        'products': products
    }
    return render(request, 'app/home.html', data)

def logIn(request):
    return redirect('/accounts/login')
@login_required
def dashboard(request):
    return redirect('/admin/')

def galeria(request):
    return render(request, 'app/galeria.html')

@login_required
def contacto(request):
    return render(request, 'app/contacto.html') 


@login_required
def LQR(request):
    usuarios = UserComplex.objects.all()
    data = {
        'usuarios' : usuarios
        }
    print(request)
    return render(request, 'app/LQR.html', data)



    # img = qrcode.make('Hola')
    # img.save('QR.png')


@login_required
def EQR(request):
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(request.user)
    usuarios = UserComplex.objects.all()
    data = {
        'usuarios' : usuarios,
        'token' : token
        }
    return render(request, 'app/EQR.html', data)


@login_required
def logOutReedirect(request):
    return redirect('/accounts/logout/')



def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("Select * from auth_user")
        row = dictfetchall(cursor)
    return row

def getComplexUser():
    with connection.cursor() as cursor:
        cursor.execute("Select * from auth_user")
        row = dictfetchall(cursor)
    return row

class getUrl(APIView):

    @action(detail=True, methods=['GET'])
    def get(self, request, format=None):
        #vId = request.GET.get('name','')
        try:
            connections.databases["con"] = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            }
            with connections["con"].cursor() as cursor:
                cursor.execute("Select * from auth_user ")
                row = dictfetchall(cursor)
            response = {'suc_intelisis':row,'status':'0','message':'OK'}
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                        'data':'',
                        'status':'2',
                        'message': 'No se pudo hacer la peticion: '+ str(e)
                    },status=status.HTTP_400_BAD_REQUEST)

@login_required
def showLectorQR(request):
    ResultQR = ""
    cap = cv.VideoCapture(0)
    detector = cv. QRCodeDetector()
    while True:
        _,img=cap.read()
        data,one,_= detector.detectAndDecode(img)
        if data:
            a=data
            break
        cv.imshow("Muestre el codigo a leer",img)
        if cv.waitKey(1)==ord('q'):
            break
    #b = webbrowser.open(str(a))
    cap.release()
    cv.destroyAllWindows()
    try:

        if data != "" :
            for dat in a:
                ResultQR += dat
            des = cryptocode.decrypt(ResultQR, "cmpx")
            usuarios = UserComplex.objects.all()
            temp = des.split("_")
            id=int(temp[0])-1
            qrData = "Acceso : "+usuarios[id].nombre+" "+usuarios[id].apellidos+" del domicilio "+usuarios[id].residencia
            data = {
                'usuarios' : usuarios,
                'QR': qrData,
                }
            
            return render(request, 'app/LQR.html', data)
        else:
            usuarios = UserComplex.objects.all()
            data = {
                'usuarios' : usuarios,
                'QR' : "Lectura cancelada",
                }
        return render(request, 'app/LQR.html', data)
    except:
        usuarios = UserComplex.objects.all()
        data = {
            'usuarios' : usuarios,
            'QR' : "El código no corresponde a ningún usuario registrado",
            }
        return render(request, 'app/LQR.html', data)

    



