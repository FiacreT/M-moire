
function select_tools(id_entities, id_tools){

    var domain_tools = {'Automater':'automater','Datasploit':'datasploit','DnsRecon':'dnsRecon','TheHarvester':'theHarvester','Recon-ng':'recon-ng'};
    var ip_tools = {'Automater':'automater','Datasploit':'datasploit','Recon-ng':'recon-ng'};
    var email_tools = {'Datasploit':'datasploit','Recon-ng':'recon-ng'};
    var username_tools = {'Datasploit':'datasploit','Recon-ng':'recon-ng'};
    var recon = {'Recon-ng':'recon-ng'};
    //alert("hello")
    var select_entities = document.getElementById(id_entities);
    var select_tools_ = document.getElementById(id_tools);
    var entities_selected = select_entities.options[select_entities.selectedIndex].value;
    //alert(entities_selected);
    switch(entities_selected){
        case 'email':
            /*alert(select_tools_.options.length)*/
            select_tools_.options.length = 0;
            /*
            for(index in email_tools){
                var op = document.createElement("option");
                op.value = email_tools[index];
                op.text = index;
                select_tools_.appendChild(op);
                select_tools_.selectpicker("refresh");
            }
            */
            break;
        case 'domain':
            select_tools_.options.length = 0;
            for(index in domain_tools){
                var op = document.createElement("option");
                op.value = domain_tools[index];
                op.text = index;
                select_tools_.appendChild(op);
            }
            break;
        case 'username':
            select_tools_.options.length = 0;
            for(index in username_tools){
                var op = document.createElement("option");
                op.value = username_tools[index];
                op.text = index;
                select_tools_.appendChild(op);
            }
            break;
        case 'ip':
            select_tools_.options.length = 0;
            for(index in ip_tools){
                var op = document.createElement("option");
                op.value = ip_tools[index];
                op.text = index;
                select_tools_.appendChild(op);
            }
            break;
        case 'company':
            select_tools_.options.length = 0;
            for(index in recon){
                var op = document.createElement("option");
                op.value = recon[index];
                op.text = index;
                select_tools_.appendChild(op);
            }
            break;
        case 'host':
            select_tools_.options.length = 0;
            for(index in recon){
                var op = document.createElement("option");
                op.value = recon[index];
                op.text = index;
                select_tools_.appendChild(op);
            }
            break;
        case 'contact':
            select_tools_.options.length = 0;
            for(index in recon){
                var op = document.createElement("option");
                op.value = recon[index];
                op.text = index;
                select_tools_.appendChild(op);
            }
            break;
        case 'location':
            select_tools_.options.length = 0;
            for(index in recon){
                var op = document.createElement("option");
                op.value = recon[index];
                op.text = index;
                select_tools_.appendChild(op);
            }
            break;

    }


}


/*
function selectVille(idCountry, idCity){ //Charge les villes du pays selectioné


var v_cam = {'douala':'334','yaounde': '333','garoua':'335','bamenda':'336','maroua':'337','bafoussam':'338','ngaoundere':'339','bertoua':'340','ebolowa':'341','buea':'342','kumba':'343','edea':'344','nkongsamba':'345','foumban':'346','limbe':'556','tiko':'557','kribi':'813','mbalmayo':'952','batouri':'954','bafia':'958','abong-mbang':'962','bandjoun':'965','sangmelima':'1058','bafang':'1156','bangangte':'1175','dschang':'1205'};
  var v_congo_b = {'brazzaville':'347','pointe-noire':'348'};
  var v_congo_k = {'kinshasa':'349','lubumbashi':'350','kolwezi':'351','mbuji-mayi':'352','kisangani':'353','kananga':'354','likasi':'355','boma':'356','tshikapa':'357','bukavu':'358','goma':'951'};
  var v_cote_iv = {'abidjan':'359','yamoussoukro':'360','bouake':'361','korhogo':'362','san-pedro':'363','grand-bassam':'364','agboville':'365','touba':'366','tieme':'367','daloa':'1206','gagnoa':'1207'};
  var v_sene = {'dakar':'483','pikine':'484','touba':'485','guediawaye':'486','thies':'487','kaolack':'488','mbour':'489','saint-louis':'490','rufisque':'491','ziguinchor':'492','diourbel':'493','louga':'494','tambacounda':'495','mbacke':'496','kolda':'497','autreville':'1187','saly':'1190','bargny':'1192','fatick':'1194','saint':'1197','ragiondethias':'1198','tivaouane':'1202'};
  var v_gabon = {'libreville':'618','port-gentil':'619','masuku':'620','oyem':'621','moanda':'622','mouila':'623','lambarene':'624','tchibanga':'625','koulamoutou':'626'};
  var v_tchad = {'ndjamena':'1208','moundou':'1209','sarh':'1210','abeche':'1211','kelo':'1212','koumra':'1213','pala':'1214','am-timan':'1215','bongor':'1216','mongo':'1217'};
  var v_benin = {'cotonou':'1227','ouidah':'1218','mallanville':'1219','bohicon':'1220','kandi':'1221','tchaourou':'1222','abomey-calavi':'1223','pobe':'1224','porto-novo':'1225','lokossa':'1226','djougou':'1228','aplahoue':'1229','dassa-zoume':'1230','parakou':'1231','allada':'1232','natitingou':'1233'};
  var v_centrafique = {'bangui':'1249','birao':'1234','baboua':'1235','bossongoa':'1236','n-dele':'1237','bangassou':'1238','alindao-1':'1239','bria':'1240','bambari':'1241','sibut':'1242','carnot':'1243','bozoum':'1244','kaga-bandoro':'1245','berberati':'1246','mbaiki':'1247','bimbo':'1248'};
  var v_togo = {'lome':'1250','sokode':'1251','kara':'1252','kpalime':'1253','atakpame':'1254','bassar':'1255','tsevie':'1256','aneho':'1257','dapaong':'1258','mango':'1259','tchamba':'1260','niamtougou':'1261','bafilo':'1262','notse':'1263','sotouboua':'1264','vogan':'1265','badou':'1266','biankouri':'1267'};
  var v_mali = {'bamako':'1268','sikasso':'1269','mopti':'1270','koutiala':'1271','kayes':'1272','segou':'1273','nioro-du-sahel-1':'1274','markala':'1275','niono-1':'1276','kolondieba-1':'1277','kati-1':'1278','gao':'1279','kolokani':'1280','menaka':'1281','bougouni':'1282','niafunke':'1283','banamba':'1284','tombouctou':'1285','macina':'1286'};
  var v_niger = {'niamey':'1287','zinder':'1288','maradi':'1289','agadez':'1290','tahoua':'1291','arlit':'1292','dosso':'1293','birninkonni':'1264','tessaoua':'1295'};
  var v_burkina = {'ouagadougou':'1296','bobo-dioulasso':'1297','koudougou':'1298','banfora':'1299','ouahigouya':'1300'};
  var v_burundi = {'bujumbura':'1301','muyinga':'1302','gitega':'1303','ngozi':'1304'};
  var v_guinee = {'conakry':'1305','kankan':'1306','kindia':'1307','nzerekore':'1308','labe':'1309'};
  
    var select = document.getElementById(idCountry);
    var selectVille = document.getElementById(idCity);
  
    var numVille = select.options[select.selectedIndex].value;
    switch(numVille){
      case '43'://cote d'ivoire
      selectVille.options.length = 0;
      var i=0;
      for(index in v_cote_iv){
        var op = document.createElement("option");
        op.value = v_cote_iv[index];
        op.text = index;
        selectVille.appendChild(op);
      }
  
        break;
      case '40'://cameroun
      selectVille.options.length = 0;
      var i=0;
      for(index in v_cam){
        var op = document.createElement("option");
        op.value = v_cam[index];
        op.text = index;
        selectVille.appendChild(op);
      }
  
        break;
      case '55'://senegal
      selectVille.options.length = 0;
      for(index in v_sene){
        var op = document.createElement("option");
        op.value = v_sene[index];
        op.text = index;
        selectVille.appendChild(op);
      }
        break;
      case '70'://Bénin
      selectVille.options.length = 0;
      for(index in v_benin){
        var op = document.createElement("option");
        op.value = v_benin[index];
        op.text = index;
        selectVille.appendChild(op);
      }
        break;
      case '42'://Congo Kinshasa
      selectVille.options.length = 0;
      for(index in v_congo_k){
        var op = document.createElement("option");
        op.value = v_congo_k[index];
        op.text = index;
        selectVille.appendChild(op);
      }
        break;
      case '68'://Gabon
      selectVille.options.length = 0;
      for(index in v_gabon){
        var op = document.createElement("option");
        op.value = v_gabon[index];
        op.text = index;
        selectVille.appendChild(op);
      }
        break;
      case '41'://Congo Brazza
      selectVille.options.length = 0;
      for(index in v_congo_b){
        var op = document.createElement("option");
        op.value = v_congo_b[index];
        op.text = index;
        selectVille.appendChild(op);
      }
        break;
      case '73'://Mali
      selectVille.options.length = 0;
      for(index in v_mali){
        var op = document.createElement("option");
        op.value = v_mali[index];
        op.text = index;
        selectVille.appendChild(op);
      }
        break;
      case '69'://Tchad
      selectVille.options.length = 0;
      for(index in v_tchad){
        var op = document.createElement("option");
        op.value = v_tchad[index];
        op.text = index;
        selectVille.appendChild(op);
      }
        break;
      case '71'://Centrafrique
      selectVille.options.length = 0;
      for(index in v_centrafique){
        var op = document.createElement("option");
        op.value = v_centrafique[index];
        op.text = index;
        selectVille.appendChild(op);
      }
  
        break;
      case '72'://Togo
      selectVille.options.length = 0;
      for(index in v_togo){
        var op = document.createElement("option");
        op.value = v_togo[index];
        op.text = index;
        selectVille.appendChild(op);
      }
  
        break;
      case '75'://Burquina Faso
      selectVille.options.length = 0;
      for(index in v_burkina){
        var op = document.createElement("option");
        op.value = v_burkina[index];
        op.text = index;
        selectVille.appendChild(op);
      }
        break;
      case '74'://Niger
      selectVille.options.length = 0;
      for(index in v_niger){
        var op = document.createElement("option");
        op.value = v_niger[index];
        op.text = index;
        selectVille.appendChild(op);
      }
  
        break;
      case '76'://Burundi
      selectVille.options.length = 0;
      for(index in v_burundi){
        var op = document.createElement("option");
        op.value = v_burundi[index];
        op.text = index;
        selectVille.appendChild(op);
      }
        break;
      case '77'://Guinee
      selectVille.options.length = 0;
      for(index in v_guinee){
        var op = document.createElement("option");
        op.value = v_guinee[index];
        op.text = index;
        selectVille.appendChild(op);
      }
  
        break;
    }
    
  
  }

//*/