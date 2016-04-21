from django.shortcuts import render
from models import Url
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def acortador(request, recurso):

    formulario = '<form action="" method="POST">'
    formulario += 'Acortar url: <input type="text" name="valor">'
    formulario += '<input type="submit" value="Enviar">'
    formulario += '</form>'

    urls = Url.objects.all()

    if request.method == "GET":
        if recurso == "":

            respuesta = "<html><body>" + formulario + "</body></html>"

            for url in urls:
                respuesta += str(url.valor) + " = " + url.url + "<br>"
        else:
            try:
                recurso = int(recurso)
                objeto = Url.objects.get(valor=recurso) #Si esta el objeto

                respuesta = "<html><body><meta http-equiv='refresh'content='1 url="\
                        + objeto.url + "'>" + "</p>" + "</body></html>"

            except Url.DoesNotExist:
                respuesta = "<html><body> Error: Recurso no encontrado </body></html>"

    elif request.method == "POST":
        cuerpo = request.body.split("=", 1)[1]

        if cuerpo.find("http%3A%2F%2F") >= 0:
            cuerpo = cuerpo.split('http%3A%2F%2F')[1]

        cuerpo = "http://" + cuerpo
        try:
            objeto = Url.objects.get(url=cuerpo)
            respuesta = "<html><body> Ya tengo esta valor guardado," + objeto.url + " = " + str(objeto.valor) + "</body></html>"

        except Url.DoesNotExist:
            valor = len(urls) + 1
            nuevo_objeto = Url(url = cuerpo, valor = valor)
            nuevo_objeto.save()

            respuesta = "<html><body>Nuevo valor guardado: " + nuevo_objeto.url + " = " + str(nuevo_objeto.valor) + "</body></html>"

    return HttpResponse(respuesta)
