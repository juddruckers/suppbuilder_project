var btnClassClick = function(e){
    console.log("Button clicked from class: "+e.currentTarget.id)
    
}

$('.btn-click-action').on('click', btnClassClick);