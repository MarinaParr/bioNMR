def all_interactions(filename, n):
    import re
    with open(filename, "r") as data:
        strings = data.readlines()
        length = (len(strings)-1)//n
        int_names = strings[0].split(" ")
        int_names.remove(int_names[-1])
        l = []
        for int_name in int_names:
            inf = re.split('~|::|--', int_name)
            num_mol_f = str((int(inf[1]))//76)
            num_res_f = str(int(inf[1])%76)
            num_mol_s = str((int(inf[4]))//76)
            num_res_s = str(int(inf[4])%76)
            name = inf[0]+num_res_f+"~"+num_mol_f+"::"+inf[2]+"--"+inf[3]+num_res_s+"~"+num_mol_s+"::"+inf[5]
            l.append(name)
        d = dict()
        for elem in l:
            d[elem] = []
        for string in strings[1:]:
            string = string.split(" ")
            i = 0
            for elem in string[:len(string)-1]:
                d[l[i]].append(int(elem))
                i += 1
        for key in d:
            st = []
            k = 0
            while k != (len(d[key])//n):
                st.append(str(int((255-sum(d[key][k*n:k*n+n])*255/n))))
                k += 1
            d[key] = st
        l_inn = []
        l_out = []
        for key in d:
            name_elements = re.split('~|::|--', key)
            name = name_elements[0]+"_"+name_elements[2]+"_"+name_elements[3]+"_"+name_elements[5]
            if name_elements[1] == name_elements[4]:
                if name not in l_inn:
                    l_inn.append(name)
            else:
                if name not in l_out:
                    l_out.append(name)
        all_inner = []
        for i in range(48):#Number_of_molecules
            for element in l_inn:
                items = element.split("_")
                inn_int = items[0]+"~"+str(i)+"::"+items[1]+"--"+items[2]+"~"+str(i)+"::"+items[3]
                if inn_int in d:
                    all_inner.append(inn_int+"\t"+"\t".join(d[inn_int]))
                else:
                    all_inner.append(inn_int+"\t"+"\t".join([str(0) for x in range(length)]))
        all_outer = []
        for i in range(48):#Number_of_molecules
            for elem in l_out:
                items = elem.split("_")
                out_int_d = items[0]+"~"+str(i)+"::"+items[1]+"--"+items[2]+"~"+"?"+"::"+items[3]
                out_int_ac = items[0]+"~"+"?"+"::"+items[1]+"--"+items[2]+"~"+str(i)+"::"+items[3]
                iis = re.split('~|::|--', out_int_d)
                iiss = re.split('~|::|--', out_int_ac)
                q = 0
                for key in d:
                    if len(re.findall(iis[0]+"\~"+iis[1]+"::"+iis[2]+"--"+iis[3]+"\~"+"\d+"+"::"+iis[5],key)) != 0:
                        all_outer.append(key+"\t"+"\t".join(d[key]))
                        q = 1
                if q == 0:
                    all_outer.append(out_int_d+"\t"+"\t".join([str(0) for x in range(length)]))
                p = 0
                for key in d:
                    if len(re.findall(iiss[0]+"\~"+"\d+"+"::"+iiss[2]+"--"+iiss[3]+"\~"+iiss[4]+"::"+iiss[5],key)) != 0:
                        all_outer.append(key+"\t"+"\t".join(d[key]))
                        p = 1
                if p == 0:
                    all_outer.append(out_int_ac+"\t"+"\t".join([str(0) for x in range(length)]))
        return(all_inner, all_outer)

def interesting_interactions(list_of_interesting_residues, all_inner, all_outer):
    import re
    import os
    interesting_interaction = []
    res_one_letter = {"ALA": "A",
        "ARG": "R",
        "ASN": "N",
        "ASP": "D",
        "CYS": "C",
        "GLU": "E",
        "GLN": "Q",
        "GLY": "G",
        "HIS": "H",
        "HIE": "H",
        "ILE": "I",
        "LEU": "L",
        "LYS": "K",
        "MET": "M",
        "PHE": "F",
        "PRO": "P",
        "SER": "S",
        "THR": "T",
        "TRP": "W",
        "TYR": "Y",
        "VAL": "V",}
    for string in all_inner:
        elems = string.split("\t")
        name = re.split('~|::|--', elems[0])
        if (name[0] in list_of_interesting_residues) or (name[3] in list_of_interesting_residues):
            interesting_interaction.append(string)
    for string in all_outer:
        elems = string.split("\t")
        name = re.split('~|::|--', elems[0])
        if (name[0] in list_of_interesting_residues) or (name[3] in list_of_interesting_residues):
            interesting_interaction.append(string)
    if (not os.path.isdir("img")):
        os.mkdir("img")
    for elem in list_of_interesting_residues:
        for i in range(48):
            with open("img/hb_trace.dat."+str(i)+".dat", "w") as f:
                intss = []
                for element in interesting_interaction:
                    name = element.split("\t")[0]
                    items = re.split('~|::|--', name)
                    if elem+str(i) == items[0]+items[1] or elem+str(i) == items[3]+items[4]:
                        data = element.split("\t")
                        intss.append(data)
                length = len(intss[0])
                for ints in intss:
                        name = ints[0]
                        ne = re.split('~|::|--', name)
                        acid_1 = res_one_letter[ne[0][0:3]]
                        num_1 = ne[0][3:5]
                        acid_2 = res_one_letter[ne[0][0:3]]
                        num_2 = ne[0][3:5]
                        name_2 = "["+ne[1]+"]"+acid_1+"-"+num_1+":"+ne[2]+"---"+"["+ne[4]+"]"+acid_2+"-"+num_2+":"+ne[5]
                        f.write(name_2+" ")
                f.write("\n")
                time = 10
                for j in range(1, length):
                    f.write(str(time)+" ")
                    for ints in intss:
                        f.write(ints[j]+" ")
                    time += 20
                    f.write("\n")