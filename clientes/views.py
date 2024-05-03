from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Cliente, Carro 
from django.http import JsonResponse
import re
#converte o objeto em json
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

def clientes(request):  
    if request.method == 'GET':
        clientes_list = Cliente.objects.all() 
        return render(request, 'clientes.html', {'clientes':clientes_list})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        carros = request.POST.getlist('carro')
        placas = request.POST.getlist('placa')
        anos = request.POST.getlist('ano')

        cliente = Cliente.objects.filter(cpf=cpf)

        if cliente.exists():
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'carros': zip(carros, placas, anos) })
        
        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf, 'carros': zip(carros, placas, anos)})

        cliente = Cliente(
            nome = nome,
            sobrenome = sobrenome,
            email = email,
            cpf = cpf
        )

        cliente.save()

        for carro, placa, ano in zip(carros, placas, anos):
            car = Carro(
                carro = carro,
                placa = placa,
                ano = ano,
                cliente = cliente
            )
            car.save()

        return redirect(reverse('clientes'))

#requisição no banco de dados    
def att_cliente(request):
    id_cliente = request.POST.get('id_cliente')
    cliente = Cliente.objects.filter(id=id_cliente)
    carros = Carro.objects.filter(cliente=cliente[0])#acessa o cliente na posição 0

    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
    cliente_id = json.loads(serializers.serialize('json', cliente))[0]['pk']
    carros_json = json.loads(serializers.serialize('json', carros))
    carros_json = [{'fields': carro['fields'], 'id':carro['pk']} for carro in carros_json]
    print(carros_json)
    data = {'cliente':cliente_json, 'carros':carros_json, 'cliente_id':cliente_id}
    return JsonResponse(data)

#isso permite que quando mando a requisição não é necessaria a chave csrf
@csrf_exempt
def update_carro(request, id):
    nome_carro = request.POST.get('carro')
    placa = request.POST.get('placa')
    ano = request.POST.get('ano')

    carro = Carro.objects.get(id=id)
    list_carros = Carro.objects.filter(placa=placa).exclude(id=id)
    if list_carros.exists():
        return HttpResponse('Placa existente')
    carro.carro = nome_carro
    carro.placa = placa
    carro.ano = ano
    carro.save()

    return HttpResponse('teste')

def excluir_carro(request, id):
    try:
        carro = Carro.objects.get(id=id)
        carro.delete()
        return redirect(reverse('clientes')+f'')
    except:
        return redirect(reverse('clientes'))

def update_cliente(request, id):
    #necessario converter para JSON pois vem como bytes
    body = json.loads(request.body)
    nome = body['nome']
    sobrenome = body['sobrenome']
    email = body['email']
    cpf = body['cpf']

    cliente = get_object_or_404(Cliente, id=id)

    try:
        cliente.nome = nome
        cliente.sobrenome = sobrenome
        cliente.email = email
        cliente.cpf = cpf
        cliente_email = Cliente.objects.filter(email=cliente.email).exclude(id=id)
        if cliente_email.exists():
            return HttpResponse('Esse email já existe')
        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf})
        cliente.save()
        return JsonResponse({'status':'200','nome':nome, 'sobrenome':sobrenome, 'email':email, 'cpf':cpf})
    except:
        return JsonResponse({'status':'500'})

    return JsonResponse({'teste':'teste'})
