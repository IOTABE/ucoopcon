jQuery(document).ready(function ($) {

    serachProfisoes();
    preencheUf();
    
    //Plano autoselecionado
    var PlanoInicial = $("#planoInicial").val();
    
    //se tiver selecionado ao carregar
    //Preencher as condições de pagamento para o plano selecionado
    if(PlanoInicial > 0){
        var ctSelec = getRadioVal(document.getElementById('formCadastro'), 'cota' );
        seachCondPgtoPl(ctSelec);
    }
    
    VMasker($("#iput_data")).maskPattern('99/99/9999');
    $('#iput_data').attr("placeholder", "dd/mm/yyyy");

    if ($("input:radio[name='tipo_pessoa']:checked").val() == "Fisica") {
        VMasker($("input[name=cpf_cnpj]")).maskPattern('999.999.999-99');
        $("#area_nome_socio").css("display", "none");
    } else {
        VMasker($("input[name=cpf_cnpj]")).maskPattern('99.999.999/9999-99');
        $("#cpf_cnpj").attr("placeholder", "Informe o CNPJ");
        $("#lb_cpf_cnpj").html('CNPJ <span class="symbol required"></span>');
        $("#lb_rg_ie").html('RG <span class="symbol required"></span>');
        $("#area_nome_socio").css("display", "block");
    }

    $("input[name=tipo_pessoa]:radio").change(function () {
        $('input[name=cpf_cnpj]').val("");//Limpar o campo

        if ($(this).val() === "Fisica") {//Acaso seja CPF
            VMasker($("input[name=cpf_cnpj]")).maskPattern('999.999.999-99');
            $("#cpf_cnpj").attr("placeholder", "Informe o CPF");
            $("#lb_cpf_cnpj").html('CPF <span class="symbol required"></span>');

            $("#rg_ie").attr("placeholder", "Informe o RG");
            $("#lb_rg_ie").html('RG <span class="symbol required"></span>');

            $(".group_org_exped").css("display", "block");
            $(".group_uf_org_exped").css("display", "block");
            $("#area_nome_socio").css("display", "none");

        } else {//Acaso seja Cnpj
            VMasker($("input[name=cpf_cnpj]")).maskPattern('99.999.999/9999-99');
            $("#cpf_cnpj").attr("placeholder", "Informe o CNPJ");
            $("#lb_cpf_cnpj").html('CNPJ <span class="symbol required"></span>');

            $("#rg_ie").attr("placeholder", "Informe a IE");
            $("#lb_rg_ie").html('Inscrição Estadual <span class="symbol required"></span>');

            $(".group_org_exped").css("display", "none");
            $(".group_uf_org_exped").css("display", "none");

            $("#area_nome_socio").css("display", "block");

            $("#area_nome_socio").validate({
                rules: {
                    nome_socio: "required"
                }
            });


        }
    });
    
    //Ao navegar entre ufs, preencher as cidades da mesma
    $('#select_uf').change(function () {
        serachCidadades($('#select_uf').val());
    });
    
    //Ao sair do campo verificar o docuemnto
    $('#cpf_cnpj').blur(function () {
        var doc = $('#cpf_cnpj').val().replace(/[^\d]+/g, '');
        if (doc !== '' || doc.length >= 11) {
            verifiCpfCnpj(doc);
        }
    });
    
    //preencher as condições de pagamento
    $('#formCadastro').on('change', 'input[name=cota]:radio', function (e) {
        var cotaSelecionada = getRadioVal( document.getElementById('formCadastro'), 'cota' );
        seachCondPgtoPl(cotaSelecionada);
    });
    
});


function preencheUf() {
    var optionsUf = '';
    $.get(
            base_url_var + "utilitarios/util/loadUfs",
            function (data) {
                $.each(data.dados, function (x, u) {
                    optionsUf = '<option value="' + u.id_uf + '">' + u.cigla_uf + '</option>';
                    $('#select_uf').append(optionsUf);
                });
            }
    );
}

function serachCidadades(UF) {
    var optionsCid = '';
    var selecione = '<option value="">.: Selecione :.</option>';
    $('#select_cidade').find('option').remove().end();
    $.get(
            base_url_var + "utilitarios/util/loadCidadesUF/" + UF,
            function (data) {
                $('#select_cidade').append(selecione);
                $.each(data.dados, function (i, c) {
                    optionsCid = '<option value="' + c.id_cidade + '">' + c.nome_cidade + '</option>';
                    $('#select_cidade').append(optionsCid);
                });
            });
}
;

function serachProfisoes() {

    var optionProfissao = '';
    //$('#profissao').find('option').remove().end();
    $.get(
            base_url_var + "utilitarios/util/loadProfissoes",
            function (data) {
                $.each(data.dados, function (i, p) {
                    optionProfissao = '<option value="' + p.id_prof + '">' + p.nome_prof + '</option>';
                    $('#profissao').append(optionProfissao);
                });
            });
}
;

function verifiCpfCnpj(DOC) {
    $.get(
            base_url_var + "cooperado/verifiCpfCnpj/" + DOC,
            function (data) {
                if (data.result === true) {
                    swal({
                        title: "ATENÇÃO",
                        text: "O " + data.tipo + " - " + data.dados.cpf_cnpj_pes + " já está em uso!",
                        type: "warning",
                        showCancelButton: false,
                        confirmButtonColor: '#2F377A',
                        confirmButtonText: 'Informar outro ' + data.tipo,
                        cancelButtonText: 'Cancelar',
                        closeOnConfirm: true,
                        closeOnCancel: true
                    },
                            function (isConfirm) {
                                if (isConfirm) {
                                    //window.open(data.responseJSON.url, '_blank');
                                    //limpar campo
                                    $('#cpf_cnpj').val("");
                                } else {
                                    //swal("OK!", "Continuar", "success");
                                    //console.log('Cancelado');
                                }
                            });
                }
            });
}

function getRadioVal(form, name) {
    var val;
    // Buscar os raidios pelo nome específico
    var radios = form.elements[name];

    // Percorre os radios
    for (var i = 0, len = radios.length; i < len; i++) {
        if (radios[i].checked) { // radio checked?
            val = radios[i].value; // se estiver selecionado, pegar o seu valor
            break; // parar o loop
        }
    }
    return val; // retorna o valor do radio selecionado ou undefined se nenhum estiver selecionado
}

function seachCondPgtoPl(PlanoID) {
    
    var listCondPgto = '';

    $('#tb_cond_pgto').find('tr').remove().end();

    $.get(
            base_url_var + "cooperado/loadCondPagamentoPlano/" + PlanoID,
            function (data) {
                if(data.result === true){
                    $.each(data.dados, function (i, cp) {
                        
                        listCondPgto = '<tr>\n\
                            <td>\n\
                                 <input type="radio" id="cond_pgto_radio" name="cond_pgto" value="'+cp.id_cdpg_pl+'">\n\
                                 <label for="cond_pgto">'+ cp.nome_cdpg_pl+'</label>\n\
                            </td>\n\
                            <td><i class="fa '+cp.icon_fpgt+'"></i> '+ cp.nome_fpgt+'</td>\n\
                            <td>'+ cp.num_parcela_cdpg_pl+'</td>\n\
                            <td><b>R$ '+ cp.vlr_parcela_cdpg_pl+'</b></td>\n\
                            <td><b> R$ '+ cp.vlr_total_cdpg_pl+'</b></td>\n\
                        </tr>';
                        
                        $('#tb_cond_pgto').append(listCondPgto);
                    });
                }else{
                    console.log(data.msg);
                }
            });
}