var checkbox1 = document.querySelector("#cursos");
checkbox1.addEventListener('change', function() {
    vagas = document.getElementsByClassName('vaga');
    for(let i = 0; i < vagas.length; i++){
         if(this.checked) {
            vagas[i].style.display = 'none';
        } else {
            vagas[i].style.display = ''
        }
    }
});

$('#vagas').click(function(){
    var is_checked = $('#vagas').is(':checked');
    var url_params = new URLSearchParams(window.location.search);
    var url = window.location.href;
    var has_filtro_vagas = url_params.has("vagas");
    if (is_checked == true){
        if (has_filtro_vagas == true){
            url_params.delete('vagas');
        }else{
            url_params.append('vagas', true);
        }
    }else{
        if (has_filtro_vagas == true){
            url_params.append('vagas', true);
        }else{
            url_params.delete('vagas');
        }
    }
    window.location = Array.from(url_params).length == 0 ? window.location.origin.toString() : window.location.origin.toString() + '/?' + url_params.toString();
});

$('#cursos').click(function(){
    var is_checked = $('#cursos').is(':checked');
    var url_params = new URLSearchParams(window.location.search);
    var url = window.location.href;
    var has_filtro_cursos = url_params.has("cursos");
    if (is_checked == true){
        if (has_filtro_cursos == true){
            url_params.delete('cursos');
        }else{
            url_params.append('cursos', true);
        }
    }else{
        if (has_filtro_cursos == true){
            url_params.append('vagas', true);
        }else{
            url_params.delete('vagas');
        }
        console.log(url_params.entries());
    }
    window.location = Array.from(url_params).length == 0 ? window.location.origin.toString() : window.location.origin.toString() + '/?' + url_params.toString();
});