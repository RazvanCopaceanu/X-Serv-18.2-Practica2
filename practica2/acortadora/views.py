from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from acortadora.models import Urls


FORMULARIO = """
 <form action="" method="POST">
  URL a acortar:<br>
  <input type="text" name="URL" value=""><br>
  <input type="submit" value="Acortar URL">
 </form>
"""

@csrf_exempt
def barra(request):
    lista_urls = Urls.objects.all()
    if request.method == "POST":
        nombre = request.POST['nombre']
        if nombre.startswith('http://') or nombre.startswith('https://'):
            url_guardada = nombre
            respuesta = "La pagina guardada es " + url_guardada
        else:
            url_guardada = "http://" + nombre
            respuesta = "La pagina guardada es " + url_guardada

        if nombre in lista_urls:
            url_corta = "/" + " " + nombre.id
        else:
            url = Urls(nombre=nombre)
            url.save()
            url_corta = Urls.objects.get(nombre=nombre).id
            respuesta = (str(url_corta) + "Es la url acortada que proviene de la url: " + nombre)
    elif request.method == "GET":
        if Urls.objects.all().exists():
            respuesta = "Las URLs acortadas son: "
            for url in lista_urls:
                respuesta += str(url.id) + "   es la   " + url.nombre + " ; "
        else:
            respuesta = "No hay URLs acortadas"
        respuesta += FORMULARIO
    else:
        return HttpResponse("Este método no está permitido")
    return HttpResponse(respuesta)

def redireccion(request, url_corta):
    try:
        nombre = Urls.objects.get(id=url_corta).nombre
        return HttpResponseRedirect(nombre)
    except Urls.DoesNotExist:
        respuesta = "Este recurso no existe"
        return HttpResponse(respuesta)
