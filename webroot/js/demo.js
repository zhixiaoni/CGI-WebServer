function add(id){
    var now = document.getElementById("num_" + id)
    document.getElementById("num_" + id).value = Number(now.value) + 1
}

function sub(id){
    var now = document.getElementById("num_" + id)
    if(Number(now.value)>0)
        document.getElementById("num_" + id).value = Number(now.value) - 1
}
