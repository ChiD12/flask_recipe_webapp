
//add more forms for ingredients/steps
$(document).on("click", ".moreIng", function(){
    var row = $(".anotherIng").eq(0).clone().show();
    $(".ingredientDiv").append(row);
    window.scrollBy(0, 100);
})

$(document).on("click", ".removeIng", function(){
    var remaining = $(".anotherIng");
    if (remaining.length >1){
        var index = $(".removeIng").index(this);
        $(".anotherIng").eq(index).remove();
    }
    //window.scrollBy(0, -50);
})

//add more forms for ingredients/steps
$(document).on("click", ".moreStep", function(){
    var row = $(".anotherStep").eq(0).clone().show();
    $(".stepDiv").append(row);
    window.scrollBy(0, 100);
})

$(document).on("click", ".removeStep", function(){
    
    var remaining = $(".anotherStep");
    if (remaining.length >1){
        var index = $(".removeStep").index(this);
        $(".anotherStep").eq(index).remove();
    }
    //window.scrollBy(0, -50);
})