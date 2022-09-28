function add(id){
    var now = document.getElementById("num_" + id)
    document.getElementById("num_" + id).value = Number(now.value) + 1
}

function sub(id){
    var now = document.getElementById("num_" + id)
    if(Number(now.value)>0)
        document.getElementById("num_" + id).value = Number(now.value) - 1
}

function change(id){
    document.getElementById("changeblock").style.display = 'block'
    document.getElementById("distable").style.display = 'none'
    document.getElementById('change_id').value = id
    document.getElementById('change_name').value = document.getElementById("name_" + id).innerHTML
    document.getElementById('change_describe').value = document.getElementById("describe_" + id).innerHTML
    document.getElementById('change_price').value = document.getElementById("price_" + id).value
}

function closewindow(){
    document.getElementById('change_name').value = ""
    document.getElementById('change_describe').value = ""
    document.getElementById('change_price').value = ""
    document.getElementById("changeblock").style.display = 'none'
    document.getElementById("distable").style.display = 'block'
}