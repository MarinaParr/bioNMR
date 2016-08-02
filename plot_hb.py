def plotting():
#!/usr/bin/python

    import re
    import os

    chids="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuv"

    def get_gp_script(header,chain):
        from subprocess import PIPE, Popen
    
        def replacement(s):
            idd = int(s.group(0)[1:])
            return "-"+str((idd-1)%76+1)+":"
  
        script="""

    set terminal png size 1024,1080
    set output "img/hb_trace.%d.png"



    set ylabel '%s'
    set xlabel 'time, ns'
    #set ylabel '\Large{}'
    set grid mxtics mytics xtics ytics
    set key top right

    # test
    # set style fill solid 1.0 border 0
    set border 0
    set ytics 0,0,0
    # set arrow from first 390, graph 0 to first 390, graph 1 nohead
    %s
    plot  [0:2020][0.5:%d-0.5] 'img/hb_trace.dat.%d.dat' using 1:(1.0):(10.0):(0.1):((255-$2)*256*256+(255-$2)*256+255) with boxxyerrorbars lc rgb variable lt 5 notitle fs solid  %s

    """%(
        chain,
        "chain %s (mol #%02d)"%(chids[chain], chain),
        "".join([ "set ytics add ('%s' %d)\n" %( h, i+1) for i,h in enumerate(header)] ),
        len(header)+1,
        chain,
        "".join([ ", '' using 1:(%d.0):(10.0):(0.1):((255-$%d)*256*256+(255-$%d)*256+255) with boxxyerrorbars lc rgb variable lt 5 notitle fs solid "%(i+1,i+2,i+2) for i in range(1,len(header))])
   
        )
        print >> open("tmp.gp","w"), script
        p = Popen(["gnuplot"], stdin=PIPE, stdout=PIPE, bufsize=1)
        p.communicate(script)
    
        print chain, len(header)


    for interested_chain in range(48):
        with open("img/hb_trace.dat."+str(interested_chain)+".dat","r") as f:
            strings = f.readlines()
            names = strings[0]
            header = names.split(" ")
        get_gp_script([ header[j] for j in range(len(header))],interested_chain)
