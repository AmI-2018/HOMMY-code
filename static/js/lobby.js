var SERVER = "http://192.168.0.65:5000";
$(document).ready(function () {
    $.getJSON(SERVER+"/playMusic", function (data){});
});