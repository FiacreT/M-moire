$('.selectpicker').selectpicker();


function createCapteur(){
    var type = {'1' : 'Préssion','2' : 'Température','3' : 'Humidité','4' : 'Vent','5' : 'Thermique'};
    var typeCapt = document.getElementById("typeCapteur");
    
    //alert(typeCapt.value);

    var ports = $('.selectpicker').val();
   var lesPorts ="";
   for(var i=0; i<ports.length; i++){
    lesPorts = lesPorts + ports[i];
    if(i!=ports.length-1){
        lesPorts = lesPorts +',';
    }
   }
   //alert(lesPorts);
   //$("#"+displayId ).append( "<td>"+lesPorts+"</td>" );
   //document.getElementById(displayId).lastChild.append("<td>"+lesPorts+"</td>");
   
    var displayId = 'capteur'+typeCapt.value;
    var portId = "port"+typeCapt.value;
    document.getElementById('bodyTable').style.display = 'block';
    document.getElementById('headTable').style.display = 'block';
    document.getElementById(portId).innerHTML = lesPorts;
    document.getElementById(displayId).style.display = 'block';
    //$('#typeCapteur').find('option').remove().end();
    $("#typeCapteur option[value='"+typeCapt.value+"']").remove();
    
   
   
  

}


function createSelectOption(){

    var type = {'1' : 'Préssion','2' : 'Température','3' : 'Humidité','4' : 'Vent','5' : 'Thermique'};
    var capteurNonPresent = {'1' : 'Préssion','2' : 'Température','3' : 'Humidité','4' : 'Vent','5' : 'Thermique'};
    var capteursPresent = document.getElementsByClassName("typeCapteurs");
    var capteur = document.getElementsByClassName("capteur");
    //alert(document.getElementById('capteur1').style.display === 'none');
    for(var i=0; i<capteursPresent.length; i++){
        //alert(document.getElementById('capteur'+(i+1)).style.display === 'none');

        if(document.getElementById('capteur'+(i+1)).style.display !== 'none'){
            var typeC = capteursPresent[i].textContent;
            typeC = typeC.replace(/\s/g,'');
            //alert(typeC.length);
            if(typeC=='Préssion'){
                //capteurNonPresent['1'] = 'Préssion';
                delete capteurNonPresent["1"];
            }
            if(typeC=='Température'){
                //capteurNonPresent['2'] = 'Température';
                delete capteurNonPresent["2"];
            }
            if(typeC=='Humidité'){
                //capteurNonPresent['3'] = 'Humidité';
                delete capteurNonPresent["3"];
            }
            if(typeC=='Vent'){
                //capteurNonPresent['4'] = 'Vent';
                delete capteurNonPresent["4"];
            }
            if(typeC=='Thermique'){
                //capteurNonPresent['5'] = 'Thermique';
                delete capteurNonPresent["5"];
            }
        }
     

    } 
     
    var optionString = {};
    //var option = '<option value="foo">foo</option>';
    $('#typeCapteur').find('option').remove().end();
    var k = 0;
    for(var key in capteurNonPresent){
        //alert(''+key);
        //alert(capteurNonPresent[key]);
        optionString[k] = '<option value="'+key+'">'+capteurNonPresent[key]+'</option>';

        $('#typeCapteur').append(optionString[k]);
        
    }
}
