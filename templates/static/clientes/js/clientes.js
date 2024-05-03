function add_carro() {
    container = document.getElementById('form-carro')

    html = "<br>  <div class='row'> <div class='col-md'> <input type='text' placeholder='carro' class='form-control' name='carro' > </div> <div class='col-md'><input type='text' placeholder='Placa' class='form-control' name='placa' ></div> <div class='col-md'> <input type='number' placeholder='ano' class='form-control' name='ano'> </div> </div>"

    container.innerHTML += html
}

// função para apresentar o formulario que aparece para o cliente se é de add ou att
function exibir_form(tipo) {

    add_cliente = document.getElementById('adicionar-cliente')
    att_cliente = document.getElementById('atualizar_cliente')

    if (tipo == "1") {
        att_cliente.style.display = "none"
        add_cliente.style.display = "block"

    } else if (tipo == "2") {
        add_cliente.style.display = "none";
        att_cliente.style.display = "block"
    }

}

function dados_cliente() {
    cliente = document.getElementById('cliente-select')
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    id_cliente = cliente.value

    data = new FormData()
    data.append('id_cliente', id_cliente)
    //fetch faz requisição ao banco da informação
    fetch("/clientes/atualiza_cliente/", {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        //console.log(data)



        document.getElementById('form-att-cliente').style.display = 'block'
        id = document.getElementById('id')
        id.value = data['cliente_id']

        document.getElementById('nome').value = data['cliente']['nome']
        document.getElementById('sobrenome').value = data['cliente']['sobrenome']
        document.getElementById('cpf').value = data['cliente']['cpf']
        document.getElementById('email').value = data['cliente']['email']

        div_carros = document.getElementById('carros')
        //Isso é feito para não incrementar quando troca o cliente
        div_carros.innerHTML = ""

        for (i = 0; i < data['carros'].length; i++) {

            div_carros.innerHTML += "<form action='/clientes/update_carro/" + data['carros'][i]['id'] + "' method='POST'>\
            <div class='row'>\
                <div class='col-md'>\
                    <input class='form-control' type='text' name='carro' value='"+ data['carros'][i]['fields']['carro'] + "'>\
                </div>\
                <div class='col-md'>\
                    <input class='form-control' type='text' name='placa' value='"+ data['carros'][i]['fields']['placa'] + "'>\
                </div>\
                <div class='col-md'>\
                    <input class='form-control' type='integer' name='ano' value='"+ data['carros'][i]['fields']['ano'] + "'>\
                </div>\
                <div class='col-md'>\
                    <input class='btn btn-lg btn-success' type='submit' value='Salvar'>\
                </div>\
                </form>\
                <div class='col-md'>\
                        <a href='/clientes/excluir_carro/"+ data['carros'][i]['id'] + "' class='btn btn-lg btn-danger'>EXCLUIR</a>\
                    </div>\
                </div><br>"
        }

    })
}

function update_cliente() {
    nome = document.getElementById('nome').value
    sobrenome = document.getElementById('sobrenome').value
    email = document.getElementById('email').value
    cpf = document.getElementById('cpf').value
    id = document.getElementById('id').value

    fetch('/clientes/update_cliente/' + id, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({
            nome: nome,
            sobrenome: sobrenome,
            email: email,
            cpf: cpf,
        })
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        div_alert = document.getElementById('alert')
        div_alert.innerHTML = ""


        if (data['status'] == 200) {
            nome = data['nome']
            sobrenome = data['sobrenome']
            email = data['email']
            cpf = data['cpf']
            div_alert.innerHTML += "<div class='alert alert-success' role='alert'>\
            Alteração salva com sucesso\
          </div>"
            console.log('Dados salvo com sucesso')
        } else {
            div_alert = document.getElementById('alert')
            div_alert.innerHTML += "<div class='alert alert-danger' role='alert'>\
            Ocorreu um erro\
          </div>"
            console.log('Ocorreu um erro')
        }
    })
}