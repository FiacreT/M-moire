
$('.selectpicker').selectpicker();
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
    $('#tools').prop('disabled', false);
    switch(entities_selected){
        case 'email':
            $("#tools").empty();
            for(index in email_tools){
              var option = $('<option></option>').attr("value", email_tools[index]).text(index);
              $("#tools").append(option);
              $('.selectpicker').selectpicker('refresh');
            }
            /*
            var option = $('<option></option>').attr("value", "option value").text("Text");
            $("#tools").empty().append(option);
            $('.selectpicker').selectpicker('refresh')
            
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
            $("#tools").empty();
            for(index in domain_tools){
              var option = $('<option></option>').attr("value", domain_tools[index]).text(index);
              $("#tools").append(option);
              $('.selectpicker').selectpicker('refresh');
            }
            /*
            select_tools_.options.length = 0;
            for(index in domain_tools){
                var op = document.createElement("option");
                op.value = domain_tools[index];
                op.text = index;
                select_tools_.appendChild(op);
            }
            */
            break;
        case 'username':
            $("#tools").empty();
            for(index in username_tools){
              var option = $('<option></option>').attr("value", username_tools[index]).text(index);
              $("#tools").append(option);
              $('.selectpicker').selectpicker('refresh');
            }
            /*
            select_tools_.options.length = 0;
            for(index in username_tools){
                var op = document.createElement("option");
                op.value = username_tools[index];
                op.text = index;
                select_tools_.appendChild(op);
            }
            */
            break;
        case 'ip':
            $("#tools").empty();
            for(index in ip_tools){
              var option = $('<option></option>').attr("value", ip_tools[index]).text(index);
              $("#tools").append(option);
              $('.selectpicker').selectpicker('refresh');
            }
            /*
            select_tools_.options.length = 0;
            for(index in ip_tools){
                var op = document.createElement("option");
                op.value = ip_tools[index];
                op.text = index;
                select_tools_.appendChild(op);
            }
            */
            break;
        case 'company':
            $("#tools").empty();
            for(index in recon){
              var option = $('<option></option>').attr("value", recon[index]).text(index);
              $("#tools").append(option);
              $('.selectpicker').selectpicker('refresh');
            }
            /*
            select_tools_.options.length = 0;
            for(index in recon){
                var op = document.createElement("option");
                op.value = recon[index];
                op.text = index;
                select_tools_.appendChild(op);
            }
            */
            break;
        case 'host':
            $("#tools").empty();
            for(index in recon){
              var option = $('<option></option>').attr("value", recon[index]).text(index);
              $("#tools").append(option);
              $('.selectpicker').selectpicker('refresh');
            }
            /*
            select_tools_.options.length = 0;
            for(index in recon){
                var op = document.createElement("option");
                op.value = recon[index];
                op.text = index;
                select_tools_.appendChild(op);
            }
            */
            break;
        case 'contact':
            $("#tools").empty();
            for(index in recon){
              var option = $('<option></option>').attr("value", recon[index]).text(index);
              $("#tools").append(option);
              $('.selectpicker').selectpicker('refresh');
            }
            /*
            select_tools_.options.length = 0;
            for(index in recon){
                var op = document.createElement("option");
                op.value = recon[index];
                op.text = index;
                select_tools_.appendChild(op);
            }
            */
            break;
        case 'location':
            $("#tools").empty();
            for(index in recon){
              var option = $('<option></option>').attr("value", recon[index]).text(index);
              $("#tools").append(option);
              $('.selectpicker').selectpicker('refresh');
            }
            /*
            select_tools_.options.length = 0;
            for(index in recon){
                var op = document.createElement("option");
                op.value = recon[index];
                op.text = index;
                select_tools_.appendChild(op);
            }
            */
            break;

    }


}


