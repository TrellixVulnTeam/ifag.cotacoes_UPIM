/**
 * Efeito visual no campo de cotação quando conclui o envio para o servidor
 *
 * @param $el
 * @param result
 * @param msg
 */
function input_result($el, result, msg) {
    var color = result == 'OK' ? '#09a00e' : '#f00';
    $el.css({'backgroundColor': color})
        .animate({
            opacity: 0.4
        }, 300, 'linear', function () {
            $el.animate({
                opacity: 100
            }).css({'backgroundColor': '#fff'});
        });

    $el.nextAll('div').remove();

    if (result != 'OK') {
        $el.parent().append('<div style="color:red">' + msg + '</div>')
    }
}

/**
 * Metodo que trata o envio das informações de de cotação, é ativado
 * pelo evento onchange de cada campo de cotação
 *
 * @param el
 */
function send_quote(el) {
    var $el = jQuery(el);
    jQuery.post(window.location.href, {
        'date': jQuery('#id_date').val(),
        'city': $el.data('city'),
        'indicator': $el.data('indicator'),
        'source': $el.data('source'),
        'value': $el.val()
    }).success(function (data, textStatus) {
        var result = null;
        if (textStatus == "success" && data['status'] == 'OK') {
            result = 'OK';
        } else {
            result = 'FAIL';
        }

        var labels = {
            'source': 'Fonte',
            'indicator': 'Indicador',
            'city': 'Cidade',
            'date': 'Data',
            'value': 'Valor'
        };

        var msg = [];
        if (data['message']) {
            for (var i in data['message']) {
                msg = [].concat(
                    msg,
                    [labels[i] + ': ' + data['message'][i].join('<br>')]
                );
            }
            msg = msg.join('<br>')
        }
        input_result($el, result, msg);
    }).fail(function (event, textStatus, httpStatusText) {
        input_result($el, textStatus, httpStatusText);
    });
}

jQuery(document).ready(function () {
    /* Adiciona evento de onchange nos campos filtro */
    jQuery('#id_city,#id_date,#id_category').change(function () {
        jQuery('#search_form').submit();
    });

    /* Adiciona evento de onchange nos campos de cotação */
    jQuery('.quotationField').change(function () {
        send_quote(this)
    });

    /* Restringe as datas de seleção */
    var js_date = jQuery.datepicker.parseDate('yy-mm-dd', server_date);
    jQuery('#id_date').datepicker("option", {maxDate: js_date});
});
