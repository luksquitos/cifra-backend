(function($) { // O Django Admin geralmente usa jQuery
    $(document).ready(function() {
        // Seletor para os botões de submit do Django Admin
        var saveButtons = $('input[type="submit"][name="_save"], input[type="submit"][name="_addanother"], input[type="submit"][name="_continue"]');

        saveButtons.on('click', function() {
            var clickedButton = $(this);
            // Desabilita todos os botões de salvar para evitar confusão
            saveButtons.prop('disabled', true);
            // Opcional: Mudar o texto
            clickedButton.val('Salvando...');
        });

        // Se o formulário tiver erros e a página recarregar, reabilitar os botões
        if ($('.errorlist').length > 0) {
            saveButtons.prop('disabled', false);
        }
    });
})(django.jQuery);
