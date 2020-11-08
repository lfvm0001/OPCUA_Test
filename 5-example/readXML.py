import re

def read_file(server,file):

    nameSpaces = []
    objects    = []
    variables  = []
    
    searchfile = open(file, "r")
    for line in searchfile:
        if "<Uri>" in line: 
            nameS = re.sub('</Uri>|<Uri>','',line)
            nameS = nameS.strip()

            nsIndex = server.get_namespace_index(nameS)
            dict_nameS = {"name": nameS, "index": nsIndex}
            nameSpaces.append(dict_nameS)
            
        if "<UAObject" in line:
            obj = re.sub('.*BrowseName="|".*','',line)
            obj = obj.strip()
            obj = re.split(":",obj)
            
            id = re.sub('.*NodeId="ns=\d;i=*|".*','',line)
            id = id.strip()
            
            dict_objs = {"i":int(obj[0])-1, "name":obj[1], "id":id}
            objects.append(dict_objs)
            
        if "<UAVariable" in line:
            var = re.sub('.*BrowseName="|".*','',line)
            var = var.strip()
            var = re.split(":",var)
            
            id = re.sub('.* NodeId="ns=\d;i=*|".*','',line)
            id = id.strip()
            
            parentid = re.sub('.*ParentNodeId="ns=\d;i=*|".*','',line)
            parentid = parentid.strip()
            
            dict_vars = {"i":int(var[0])-1, "name":var[1], "id":id, "parentid":parentid}
            variables.append(dict_vars)
     
    searchfile.close()
    
    for dicO in objects:
        dicO["ns"] = nameSpaces[dicO["i"]]["index"]
        for dicVar in variables:
            dicVar["ns"] = nameSpaces[dicVar["i"]]["index"]
            if dicVar["parentid"] == dicO["id"]:
                dicVar["parentName"] = dicO["name"]
                
    response = []
    response.append(nameSpaces)
    response.append(objects)
    response.append(variables)
    
    return response