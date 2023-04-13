$.ajax({
    url: 'js/영이공 근처 맛집.csv',
    dataType: 'text',
  }).done(successFunction);

function successFunction(data){
    var indexList = [];
    var result = [];
    var search_m = 0;

    for (var i = 0; i < data.length; i++){
        var a = data.charAt(i);
        
        if (search_m == 0){
            if (a == '"'){
                search_m = 1;
            } else if (a == ','){
                if (indexList.length == 0){
                    indexList.push(0);
                    indexList.push(i);
                } else{
                    indexList.push(indexList[indexList.length-1]+1);
                    indexList.push(i);
                }
                
            }
        } else{
            if (a == '"'){
                search_m = 0;
            }
        }
    }

    indexList.push(indexList[indexList.length-1]+1);
    indexList.push(data.length-1);
    
    for (var i = 0; i < indexList.length; i = i + 2){
        let d = data.substring(indexList[i], indexList[i+1]).replace('\r', '').replace('\n', '').replace(/"/g, '').trimLeft();
        result.push(d);
    }

    console.log(result);
}
