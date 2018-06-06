$(document).ready(function () {
    let li = $(".categories li");
    li.each(function (index) {
        let i = $(this);
        if(i.attr("disable") == 1)
            i.addClass("lead mybtn disabled");
        else i.addClass("lead mybtn");
    })

});