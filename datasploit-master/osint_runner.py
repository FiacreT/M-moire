import importlib
import os
import sys
import json
from glob import glob
from collections import OrderedDict
from datetime import datetime


def run(component, module_dir, m_input, output = None):
    datas = []
    dir_path = "%s/%s" % (os.path.dirname(os.path.abspath(__file__)), module_dir)
    #print("---------------------------------------------------------------------------------------")
    #print("dir name",dir_path)
    sys.path.insert(0, dir_path)
    domain_files = glob("%s/%s_*.py" % (dir_path, component))
    #print("file name",domain_files)
    active_modules = OrderedDict()
    for index, i in enumerate(domain_files):
        module_name = os.path.basename(os.path.splitext(i)[0])
        print("module name", module_name)
        x = importlib.import_module(module_name)
        print("lib", x)
        if not x.ENABLED:
            print ("[-] Skipping %s because it is marked as disabled." % module_name.split("_")[1].title())
        else:
            active_modules[os.path.basename(os.path.splitext(i)[0])] = x

    json_output = {}
    tab_modules = list(active_modules.iteritems())
    print("/////////////////////////////////////////////////////////////////////////")
    for i in range(len(tab_modules)):
        temp = str(tab_modules[i]).split(',')[0]
        temp = temp.replace("'", "")
        temp = temp.replace('(', '')
        tab_modules[i] = temp
        print(tab_modules[i])
    

    for name, x in active_modules.iteritems():
        #print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",x)

        if "banner" in dir(x):
            x.banner()
        data = x.main(m_input)
        #print ("*************************************************************", data)
        if data:
            x.output(data, m_input)
            for mod in tab_modules:
                if(mod in str(x)):
                    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",str(x))
                    datas.append({mod:data})
            
            #if any(ext in str(x) for ext in tab_modules):
                
            #print ("*************************************************************", data)
    
    if output and str(output).lower() == "text":
        try:
            if x.WRITE_TEXT_FILE:
                filename = "text_report_%s_%s_%s.txt" % (m_input, x.MODULE_NAME, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
                text_data = x.output_text(data)
                #print ("*************************************************************", data)
            fh = open(filename, "w")
            fh.write(text_data)
            fh.close()
            print ("[+] Text Report written to %s" % filename)
        except Exception as e:
            pass
    
    return datas
            
    
"""
        if output and str(output).upper() == "JSON":
            json_output[name] = data

    if output and str(output).upper() == "JSON":
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = "datasploit_%s_%s_%s.json" % (module_dir, m_input, timestamp)
        filepath = "reports/json"
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        file = "%s/%s" % (filepath, filename)
        with open(file, "w") as fh:
            json.dump(json_output, fh, indent=4, sort_keys=True)
        print "JSON report saved to %s/%s" % (filepath, filename)
"""
