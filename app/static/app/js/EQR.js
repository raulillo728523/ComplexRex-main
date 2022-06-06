function getUser() {
    name = document.getElementById('nameQR').value;
    console.log(name);
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$(document).on("change", '#nameQR', function (e) {
    var dir = $("#nameQR option:selected").data("qr")
    if (dir == "x") {
        $("#dirQR").hide()
        $("#dirQR").attr("src", "")
        $("#btnQR").prop( "disabled", true )
    } else if(dir != "") {
        $("#btnQR").prop( "disabled", false )
        $("#dirQR").show()
        $("#btnQR").text("Actualizar código")
        $("#dirQR").attr("src", "/static/accounts/login/" + dir)
    }else {
        $("#btnQR").prop( "disabled", false )
        $("#dirQR").hide()
        $("#btnQR").text("Generar código")
    }

});
function generarQR() {
    var dir = $("#nameQR option:selected").data("qr")
        const csrftoken = getCookie('csrftoken')
        nombre = $("#nameQR option:selected").val()
        casa = $("#nameQR option:selected").data("residencia")
        
        id = $("#nameQR option:selected").attr("id")
        $.ajax({
            type: "POST",
            dataType: 'json',
            headers: { 'X-CSRFToken': csrftoken },
            url: "http://localhost:8000/newQR/",
            data: { nombre: nombre,
                    casa: casa ,
                    id: id}
        }).done(function (data) {
            console.log(data)
            location.reload()
            alert("Código de ingreso generado correctamente")
        });
}


function getQR() {
    console.log("Si entra")
    // var name = document.getElementById('nameQR').value;
    // $.ajax({
    //     type: "POST",
    //     dataType: 'json',
    //     headers: {'X-CSRFToken': csrftoken},
    //     url: "http://localhost:8000/newQR/",
    //     data: { data: name}
    // }).done(function( o ) {
    //     console.log("Se ejecuto bien")
    // });
}