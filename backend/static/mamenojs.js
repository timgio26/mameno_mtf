// function myFunction() {
//     var x = document.getElementById("mySelect").value;
    
//   }

// var changedText = document.getElementById('changed');
document.getElementById("type").onchange = listQ;
function listQ(){
    var x = document.getElementById("type").value;
    // console.log(x)
    if(x=='Nota Bersama'){
        // console.log('notabersama')
        document.getElementById("demo").innerHTML = "Masukin Kode Divisi";
        document.getElementById("divinp").style.display = "flex"; 
    }else{
        // console.log('bukan nota bersama')
        document.getElementById("divinp").style.display = "none";
    }
    
    // 
}
