function run(){
    var f_list=document.getElementById("list");

    readTextFile("Dataset.json", function(text){
        var data = JSON.parse(text);

        for(var i = 0; i < data.length; i++) {
            f_list.innerHTML+='<a href="https://github.com/'+data[i][0]+'"><img src="'+data[i][1]+'" alt="'+data[i][0]+'" style="height:50px;width:50px;"/></a>';
        }
        //console.log(data["Dark Mode"]);
    });
}

//
function readTextFile(file, callback) {
    var rawFile = new XMLHttpRequest();
    rawFile.overrideMimeType("application/json");
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function() {
        if (rawFile.readyState === 4 && rawFile.status == "200") {
            callback(rawFile.responseText);
        }
    }
    rawFile.send(null);
}
