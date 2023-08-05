def steal(fname):  
    import numpy as np
    
    rr = open(fname,"r")
    
    coor = rr.readlines()
    rr.close()
    atomNum = coor[2].split()
    atomN = atomNum[0]
    atmn = int(atomN)
    
    index = 0
    for rw in coor[0:100]:
        if rw != "\n":
            atm = rw.split()[0]
        if atm == "Atoms":
            start = index+2
            break
        index +=1
        
    finish = start + int(atomN)
    
    ncol = 6
    
    atoms = np.zeros([atmn,ncol])
    
    for row in coor[start:finish]:
        atomd = row.split()[0]
        atomid = int(atomd)
        for j in range (ncol):
            if j != 5:
                atoms[atomid-1,j] = row.split()[j]
            else:
                rs = row.split()[j]
                real = float(rs)
                fake = str(real)
                atoms[atomid-1,j] = fake
    
    return atoms

def radius(n):

    import math
    
    pi = math.pi

    basepair = 4.6*10**6 #bp
    volume = 6.7*10**(-19) #m3
    bp_dens = basepair/volume #bp/m3
    realN = n*10 #my polymer bp
    sysVol = realN/bp_dens#bp/(bp/m3)
    sigma = 34*10**(-10) #1 sigma corresponds to 10 bp and 10bp length is 34 armstrong
    rreal = (3*sysVol/(16*pi))**(1/3) #2a^3 = m3, a = (m3/2)^(1/3)
    r = int(rreal/sigma+1)
    
    return r,sysVol

def boundtf(fname):
    
    
    import numpy as np
    
    atoms = steal(fname)
    
    nrow = len(atoms)
    n = nrow
    ncol = 6
    
    bound = np.zeros([int(nrow*3/20),ncol]) 
    
    i = 0
    for r in range(n-1):
        
        row = atoms[r]
        rowr = atoms[r+1]
        
        if (r+1)%20 == 1:
            bound[i]=[i+n+1,4,4,row[3]+0.6,row[4],row[5]]
            bound[i+1]=[i+n+2,5,5,row[3]+1.4,row[4],row[5]]
            bound[i+2]=[i+n+3,4,4,rowr[3]+0.6,rowr[4],rowr[5]]
            i +=3
            
    total = np.append(atoms,bound)
    nrow = int(len(total)/6)
    total = total.reshape(nrow,ncol)

    return total

def freetf(um,index,n):
    from random import random
    import numpy as np
    
    
    sap = 5
    typ = 3
    
    r,sysVol = radius(n)
    
    ttf = um
    avag = 6.022*(10**23) #avagdaro number mol
    m2l = 1000 #m^3 to liter
    m2u = 10**(-6) #meter to micrometer
    
    ftf = avag*m2l*m2u*sysVol*ttf #molarite to number
    
    ntf = int(ftf)
    
    kok2 = 2**(1/2)
    
    free = np.zeros([3*ntf,6])
    
    index = index+1
    for i in range (0,3*ntf,3):
        xcr = 4*r*random()-2*r
        ycr = 2*r*random()/kok2 -r/kok2
        zcr = 2*r*random()/kok2 -r/kok2
        
        free[i]=[index,typ,typ,xcr,ycr,zcr]
        free[i+1]=[index+1,sap,sap,xcr-0.66,ycr+0.56,zcr+0.61]
        free[i+2]=[index+2,typ,typ,xcr+0.33,ycr+0.67,zcr+0.48]
        index +=3
        
    return free

def cylinder(r,index,atom_type):

    import math
    import numpy as np
    typ = atom_type
    cyl = np.array([])
    
    pir = r*3.14159
    pr = int(pir)
    
    for xcr in range (-2*r,2*r+1):
        
        
        for x in range(-pr,pr+1):
    
            index +=1
            ycr = math.cos(x/r)*r
            zcr = math.sin(x/r)*r
            coor = [index,typ,typ,xcr,ycr, zcr]
            coor = np.array(coor)
            
            cyl = np.append(cyl,coor)
            
    
    ncol = 6
    row = len(cyl)/ncol
    nrow =  int(row)
    
    cyl = cyl.reshape(nrow,ncol)
    return cyl

def cap(r,index,atom_type):
    import math
    import numpy as np
    
    r = r
    if 1 == 1:
        pi = math.pi
        r = r
        gs = r
        angle_num=int(pi*gs/2)
        cap = np.array([])
        typ = atom_type
        ncol = 6
        
    for xl in range (0,angle_num+1):
    
        angle = (pi/2)*xl/angle_num
        xcr = gs*math.cos(angle)
    
    
        r_new = math.sqrt(gs**2-xcr**2)
        num = int (2*pi*r_new)
        
    
        for i  in range (0,num,2):
            index +=1
    
            zcr = math.cos(2*pi/num*i)*r_new
            ycr = math.sin(2*pi/num*i)*r_new
            
            coor = [index,typ,typ,xcr+2*r+0.5,ycr, zcr]
            coor = np.array(coor)
            cap = np.append(cap,coor)
    
    
    r = -r
    gs = r
    angle_num = int(pi*gs/2)
    for xl in range (0,angle_num-1,-1):
    
        angle = (pi/2)*xl/angle_num
        xcr = gs*math.cos(angle)
    
    
        r_new = math.sqrt(gs**2-xcr**2)
        num = int (2*pi*r_new)
        
    
        for i  in range (0,-num,-2):
            index +=1
    
            zcr = math.cos(2*pi/num*i)*r_new
            ycr = math.sin(2*pi/num*i)*r_new
            
            coor = [index,typ,typ,xcr+2*r-0.5,ycr, zcr]
            coor = np.array(coor)
            cap = np.append(cap,coor)
    
    row = len(cap)/6
    nrow = int(row)
    cap = cap.reshape(nrow,ncol)
    return cap

def membrane(r,index,atom_type):
    import numpy as np
    
    cyl = cylinder(r,index,atom_type)
    index += len(cyl)
    
    cap1 = cap(r,index,atom_type)
    
    memb = np.append(cyl,cap1)
    memb = np.array(memb)
    ncol = 6
    nrow = int(len(memb)/ncol)
    memb = memb.reshape(nrow,ncol)
    return memb

def bonder(n,um):

    import numpy as np


    clps = int(n/20*23)
    free = freetf(um,clps,n)
    fr = int(len(free)/3)
    btf = int(clps/23)
    
    ntyp = 1
    
    tfs = btf +fr
    
    num_bonds = n+tfs*2
    bonds = np.zeros([num_bonds,4])
    index = 0
    
    ntyp = 1
    for i in range(n):
        index +=1
        if index < n:
            bonds[i] = [index,ntyp,index,index+1]
        elif index == n:
            bonds[i] = [index,ntyp,index,1]
            
    
    tftyp = 2
    indx = n
    b = 0
    for index in range(n+1,n+tfs*3+1,3):
        ilk = index
        iki = index+1
        uc = index+2
        bonds[indx] = [index+b,tftyp,ilk,iki]
        indx +=1
        bonds [indx] = [index+b+1,tftyp,iki,uc]
        indx +=1
        b-=1
    
    return bonds

def angler(n,um):

    import numpy as np
    
    clps = (n/20*23)
    
    
    free = freetf(um,clps,n)
    
    fr = int(len(free)/3)
    btf = int(clps/23)
    
    ntyp = 1
    
    tfs = btf +fr
    
    
    num_angles = n+tfs
    angles = np.zeros([num_angles,5])
    index = 0
    
    for i in range(n):
        index += 1
        
        if i<n-2:
            angles[i]=[index,ntyp,index,index+1,index+2]
        elif i==n-2:
            angles[i]=[index,ntyp,index,index+1,1]
        elif i==n-1:
            angles[i]=[index,ntyp,index,1,2]
    
    tftyp = 2
    indx = index +1
    for j in range(tfs):
        index = index +1
        angles[n+j]=[index,tftyp,indx+j,indx+j+1,indx+j+2]
        indx = indx +2
        
    return angles

def buildNwrite(um,filetoread,filetowrite):

    import numpy as np
    
    pos =  boundtf(filetoread)
    ps = len(pos)
    n = int(ps/23*20)
    r,sysVol = radius(n)
    
    ftf = freetf(um,ps,n)
    ft = len(ftf) 
    index = ft + ps
    
    mem = membrane(r,index,6)
    angles = angler(n,um)
    bonds = bonder(n,um)
    
    atoms1 = np.append(pos,ftf)
    atoms =np.append(atoms1,mem)
    
    boy = len(atoms)
    ncol = 6
    nrow = int(boy/ncol)
    
    atoms = atoms.reshape(nrow,ncol)
    
    
    ll = open(filetowrite,"w")
    
    ll.write("\n\n")
    
    num_atoms = str(nrow)
    ll.write(num_atoms+" atoms\n")
    ll.write("6 atom types\n")
    bnds = str(len(bonds))
    ll.write(bnds+" bonds\n")
    ll.write("2 bond types\n")
    angls = str(len(angles))
    ll.write(angls+" angles\n")
    ll.write("2 angle types\n\n")
    
    x = 5.2324242
    ll.write(str(-3*r-x)+" "+str(3*r+x)+" xlo xhi\n")
    ll.write(str(-r-x)+" "+str(r+x)+" ylo yhi\n")
    ll.write(str(-r-x)+" "+str(r+x)+" zlo zhi\n\n")
    
    ll.write("Masses\n\n")
    ll.write("1 1\n")   
    ll.write("2 1\n")
    ll.write("3 2\n")
    ll.write("4 2\n")
    ll.write("5 2\n")
    ll.write("6 1\n\n")
    
    ll.write("Pair Coeffs # lj/cut\n\n")
    
    ll.write("1 12 1\n")   
    ll.write("2 12 1\n")
    ll.write("3 12 1\n")
    ll.write("4 12 1\n")
    ll.write("5 12 1\n")
    ll.write("6 12 1\n\n")
    
    ll.write("Bond Coeffs # fene\n\n")
    
    ll.write("1 30 1.5 1 1\n")   
    ll.write("2 30 2.0 1.3 1.3\n\n")
    
    ll.write("Angle Coeffs # harmonic\n\n")
    
    ll.write("1 1 180.0\n")
    ll.write("2 12 40\n\n")
    
    ll.write("Atoms # angle\n\n")
    
    for row in atoms:
        for i in range (6):
            if i<3:
                ii = int(row[i])
                ll.write(str(ii)+" ")
            else:
                ll.write(str(row[i])+" ")
        ll.write("\n")
    
    ll.write("\nBonds\n\n")
    
    for row in bonds:
        for i in range (4):
                ii = int(row[i])
                ll.write(str(ii)+" ")
        ll.write("\n")
    
    ll.write("\nAngles\n\n")
    for row in angles:
        for i in range (5):
                ii = int(row[i])
                ll.write(str(ii)+" ")
        ll.write("\n")
    return
