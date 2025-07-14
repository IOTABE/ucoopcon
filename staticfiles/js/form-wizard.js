var FormWizard = function () {

    "use strict";

    VMasker($("#fone_fixo")).maskPattern('(99)9999-9999');
    VMasker($("#fone_cel")).maskPattern('(99)99999-9999');
    VMasker($("#cep")).maskPattern('99999-999');

    var wizardContent = $('#wizard');
    var wizardForm = $('#formCadastro');
    var form = $('#formCadastro');
    var numberOfSteps = $('.swMain > ul > li').length;

    var initWizard = function () {
        // function to initiate Wizard Form
        wizardContent.smartWizard({
            selected: 0,
            keyNavigation: false,
            onLeaveStep: leaveAStepCallback,
            onShowStep: onShowStep
        });
        var numberOfSteps = 0;
        animateBar();
        initValidator();
    };

    var animateBar = function (val) {
        if ((typeof val == 'undefined') || val == "") {
            val = 1;
        }
        ;

        var valueNow = Math.floor(100 / numberOfSteps * val);
        $('.step-bar').css('width', valueNow + '%');
    };

    var initValidator = function () {

        jQuery.validator.setDefaults({
            errorElement: "span", // contain the error msg in a span tag
            errorClass: 'help-block',
            errorPlacement: function (error, element) { // render error placement for each input type
                if (element.attr("type") === "radio" || element.attr("type") === "checkbox") { // for chosen elements, need to insert the error after the chosen container
                    error.insertAfter($(element).closest('.form-group').children('div').children().last());
                } else {
                    error.insertAfter(element);
                    // for other inputs, just perform default behavior
                }
            },
            ignore: ':hidden',
            
            rules: {
                cota: {
                    required: true
                },
                cpf_cnpj: {
                    required: true,
                    minlength: 14
                },
                rg_ie: {
                    required: true
                },
                nome_razao: {
                    required: true,
                    minlength: 5
                },
                cover_fantasia: {
                    required: true
                },
                nome_socio: {
                    required: true
                },
                dt_nasc_fund: {
                    required: true
                },
                sexo: {
                    required: true
                },
                naturaldiade: {
                    minlength: 5,
                    required: true
                },
                profissao: {
                    required: true
                },
                fone_cel: {
                    required: true
                },
                email: {
                    required: true,
                    email: true
                },
                logradouro: {
                    required: true
                },
                num_end: {
                    required: true
                },
                bairro: {
                    required: true
                },
                cep: {
                    minlength: 8,
                    required: true
                },
                select_uf: {
                    required: true
                },
                select_cidade: {
                    required: true
                },
                termos: {
                    required: true
                },
                cond_pgto: {
                    required: true
                }

            },
            messages: {
                cota: "Selecione uma opção",
                cond_pgto: "Selecione uma opção",
                fone_cel: "Obrigatório"
            },
            highlight: function (element) {
                $(element).closest('.help-block').removeClass('valid');
                // display OK icon
                $(element).closest('.form-group').removeClass('has-success').addClass('has-error').find('.symbol').removeClass('ok').addClass('required');
                // add the Bootstrap error class to the control group
            },
            unhighlight: function (element) { // revert the change done by hightlight
                $(element).closest('.form-group').removeClass('has-error');
                // set error class to the control group
            },
            success: function (label, element) {
                label.addClass('help-block valid');
                // mark the current input as valid and display OK icon
                $(element).closest('.form-group').removeClass('has-error').addClass('has-success').find('.symbol').removeClass('required').addClass('ok');
            }
        });
    };

    var onShowStep = function (obj, context) {
        if (context.toStep == numberOfSteps) {
            $('.anchor').children("li:nth-child(" + context.toStep + ")").children("a").removeClass('wait');
        }
        $(".next-step").unbind("click").click(function (e) {
            e.preventDefault();
            wizardContent.smartWizard("goForward");
        });
        $(".back-step").unbind("click").click(function (e) {
            e.preventDefault();
            wizardContent.smartWizard("goBackward");
        });
        $(".finish-step").unbind("click").click(function (e) {
            e.preventDefault();
            onFinish(obj, context);
        });
    };

    var leaveAStepCallback = function (obj, context) {
        return validateSteps(context.fromStep, context.toStep);
        // return false to stay on step and true to continue navigation
    };

    var onFinish = function (obj, context) {
        if (validateAllSteps()) {
            $('.anchor').children("li").last().children("a").removeClass('wait').removeClass('selected').addClass('done').children('.stepNumber').addClass('animated tada');           
            sendData();   
        }
    };

    var validateSteps = function (stepnumber, nextstep) {

        var isStepValid = false;


        if (numberOfSteps >= nextstep && nextstep > stepnumber) {

            // cache the form element selector
            if (wizardForm.valid()) { // validate the form
                wizardForm.validate().focusInvalid();
                for (var i = stepnumber; i <= nextstep; i++) {
                    $('.anchor').children("li:nth-child(" + i + ")").not("li:nth-child(" + nextstep + ")").children("a").removeClass('wait').addClass('done').children('.stepNumber').addClass('animated tada');
                }
                //focus the invalid fields
                animateBar(nextstep);
                isStepValid = true;
                return true;
            }
            ;
        } else if (nextstep < stepnumber) {
            for (i = nextstep; i <= stepnumber; i++) {
                $('.anchor').children("li:nth-child(" + i + ")").children("a").addClass('wait').children('.stepNumber').removeClass('animated tada');
            }

            animateBar(nextstep);
            return true;
        }
    };
    var validateAllSteps = function () {
        var isStepValid = true;
        // all step validation logic
        return isStepValid;
    };

    return {
        init: function () {
            initWizard();
        }
    };
}();

function sendData() {
    var FormCad = $('#formCadastro');
    var UrlSalvar = FormCad.attr('action');

    $('.preloader-wrap').css('display','block')

    $.ajax({
            type: 'POST',
                    url: UrlSalvar,
                    data: FormCad.serialize(),
                    dataType: 'json',
                    complete: function(res) {
                          $('.preloader-wrap').css('display','none')
                          ret = res.responseJSON;

                         if (ret.result === true) {

                            $('.animate').css('visibility','visible');

                            swal({
                            title: "PARABÉNS!",
                            text: "Seu cadastro foi efetivado com sucesso! <br/> Imprima os documentos gerados e dirija-se ao nosso escritório para confirmação do seu cadastro.",
                            type: "success",
                            html: true,
                            showCancelButton: false,
                            confirmButtonColor: '#2F377A',
                            confirmButtonText: 'Imprimir documentos e Sair',
                            cancelButtonText: 'Cancelar',
                            closeOnConfirm: true,
                            closeOnCancel: false
                                },
                                function (isConfirm) {
                                    if (isConfirm) {
                                        window.open(ret.dados.url_termo, '_blank');

                                        //Redirecionar
                                        window.location.href = ret.dados.url_ficha;
                                    } else {
                                        //swal("OK!", "Continuar", "success");
                                        //console.log('Cancelado');
                                    }
                                });
                            }else{
                                
                                wal("Ops!", "Ocorreu um erro inesperado ao cadastrar. Por favor tente novamente mais tarde.", "error")
                                
                            }
                        }
            });
}