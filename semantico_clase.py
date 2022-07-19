import re
import csv  
import sys

# Programa del analizador semántico


class Clase_Semantica:

    def __init__(self,texto):
        self.estado = []
        self.texto = texto

    def getValor(self):
        return self.estado

    def errores(self,No):
        if No==1:
            self.estado.append("\nError por no iniciar con la numeración (X.-).")
        elif No==2:
            self.estado.append("\nError en secuencia lógica de la numeración.")
        elif No==3:
            self.estado.append("\nError en identificador/expresión.")
        elif No==4:
            self.estado.append("\nError en palabra reservada.")
        elif No==5:
            self.estado.append("\nSe esperaba una coma, o dejo un espacio en el identificador.")
        elif No==6:
            self.estado.append("\nEl identificador ya existe.")
        elif No==7:
            self.estado.append("\nEl identificador no existe.")
        elif No==8:
            self.estado.append("\nExiste información después de FIN, o está mal ubicado.")
        elif No==9:
            self.estado.append("\nExiste información entes de INICIO, o está mal ubicado.")
        elif No==10:
            self.estado.append("\nExiste una comilla pero falta la que cierra al STRING.")
        elif No==11:
            self.estado.append("\nExisten lineas en blanco antes de INICIO y/o después de FIN.")
        elif No==12:
            self.estado.append("\nNúmero de paréntesis desbalanceado.")
        elif No==13:
            self.estado.append("\nError en operador relacional.")
        elif No==14:
            self.estado.append("\nError en la expresión relacional, no se puede comparar el STRING.")
        elif No==15:
            self.estado.append("\nTodas las variables del for deben tener el mismo nombre.")
        elif No==16:
            self.estado.append("\nFalta instrucción FIN.")
        return


    def D(self,txt):
        if len(txt)!=0:
            if re.search('[0-9]',txt[0]):
                return self.D(txt[1:])
            else:
                return 0
        else:
            return 1
        
    def L(self,txt):
        if len(txt)!=0:
            if re.search('[_|a-z|A-Z]',txt[0]):
                return self.L(txt[1:])
            else:
                return 0
        else:
            return 1

    def Lid(self,txt):
        if len(txt)!=0:
            if re.search('[_|a-z]',txt[0]):
                return self.L(txt[1:])
            else:
                return 0
        else:
            return 1

    def ID(self,txt):
        if len(txt)==1:
            return self.Lid(txt[0])
        elif len(txt)>1: 
            return self.Lid(txt[0])*self.RI(txt[1:])
        else:
            return 1

    def RI(self,txt):
        if len(txt)==1:
            return  self.L(txt[0]) + self.D(txt[0]) 
        elif len(txt)>1: 
            return ( self.L(txt[0]) + self.D(txt[0]) )*self.RI(txt[1:])
        else:
            return 1


    def separa(self,txt):
        tex=""
        k=0
        for dato in txt:
            if dato=="*":
                tex=tex+" * "
            elif dato=="+":
                tex=tex+" + "
            elif dato=="-":
                tex=tex+" - "
            elif dato==",":
                tex=tex+" , "
            elif dato=="(":
                tex=tex+" ( "
            elif dato==")":
                tex=tex+" ) "
            elif dato=="/":
                tex=tex+" / "
            elif dato=="%":
                tex=tex+" % "
            elif dato=="^":
                tex=tex+" ^ "
            elif dato==">":
                tex=tex+"  > "
            elif dato=="<":
                tex=tex+"  < "
            elif dato=="=":
                if tex[len(tex)-2]=="=":
                    tex=tex[0:len(tex)-4]+" == "
                elif tex[len(tex)-2]==">":
                    tex=tex[0:len(tex)-4]+" >= "
                elif tex[len(tex)-2]=="<":
                    tex=tex[0:len(tex)-4]+" <= "
                else:
                    tex=tex+"  = "
            else:
                tex=tex+dato
            k=k+1
        return tex

    def lex(self,txt):
        if txt!="":
            if txt[0]=='"':
                try:
                    t=txt[1:].index('"')
                except:
                    t=-1         
                if t==-1:
                    self.errores(10)
                    return
                else:
                    return t+2
        t=0
        bandera=0
        for dato in txt:
            if dato!=" " and dato!="\n":
                t=t+1
            else:
                return t
        return t

    def iniciar(self):

        IDs=[]
        codigopython=[]
        txtpy=""
        txtespacios=""

        pila=['S']
        vectorR=[]
        vectorC=[]
        #Abriendo archivo CSV tabla de análisis predictivo

        file = open('tabla.csv')
        type(file)
        csvreader = csv.reader(file)
        header = []
        rows = []
        header = next(csvreader)
        rows.append(header)
        k=1
        for row in csvreader:
            rows.append(row)
            vectorC.append(row[0])
            k=k+1
            
        vectorR=rows[0]
        totlineas=0

        for linea in range(len(self.texto)):
            #self.estado.append(linea)
            txt=self.texto[linea]
            txt=txt.strip()
            bandera=0
            if txt=="":
                bandera=1
            suma=0
            for z in txt:
                if z=='(':
                    suma=suma+1
                elif z==')':
                    suma=suma-1
            if suma!=0:
                self.estado.append("")
                self.estado.append(linea)
                self.errores(12)          
                return   
            totlineas=totlineas+1             
        if bandera==1:
            self.errores(11)
            return
            
        
        
        self.estado.append(str(totlineas)+" Lineas a leer del pseudocódigo")


        STR=re.compile('/".*')
        NUL=re.compile('[0-9]*[\.][-] ')
        IDS=re.compile('[a-z|_][a-z|_|0-9]*')   #Identificadores
        NOI=re.compile('[0-9][0-9]*[0-9]*')   #Números enteros
        NOF=re.compile('[0-9][0-9]*[\.][0-9][0-9]*')    #Números flotantes
        OPR=re.compile('[<][=]|[>][=]|[=][=]|[!][=]|[<]|[>]')   #Operadores relacionales
        OPA=re.compile('[\+]|[\^][\-]|[\*]|[\/]|[\%]')         #Operadores aritmeticos 
        PAL=re.compile('[F][I][N][D][E][S][D][E]|[D][E][S][D][E]|[H][A][S][T][A]|[I][N][C][R][E][M][E][N][T][O][S]|[E][N]|[H][A][S][T][A][Q][U][E]|[F][I][N][H][A][S][T][A][Q][U][E]|[M][I][E][N][T][R][A][S][Q][U][E]|[F][I][N][M][I][E][N][T][R][A][S]|[E][N][T][O][N][C][E][S]|[S][I]|[I][N][I][C][I][O]|[F][I][N]|[P][E][D][I][R]|[H][A][C][E][R]|[M][O][S][T][R][A][R]|[S][I][N][O]') #Palabras reservadas
        OAS=re.compile('[\w][=][\w]|[ ][=][ ]')  #Operador de asignación
        SEP=re.compile('[\s][,]|[,][\s]|[,]')  #Operador de separación
        PAR=re.compile('[(].+[)]')  #Paréntesis
        TEX=re.compile('/".*/"')  #Texto

        numlinea=0  
        for x in range(len(self.texto)):
            self.estado.append("----------------------------------------------------------------------------------------------------------------")
            txt=self.texto[x]
            numlinea=numlinea+1
            x=0
            txt=txt.strip()
            revisando=list(txt)
            self.estado.append(txt+"\n")
            #Número de línea
            if NUL.search(txt):
                result=NUL.search(txt)
                result2=NUL.finditer(txt)
                for match in result2:
                    [inicio,fin]=match.span()
                    if inicio!=0:
                        self.errores(1)
                        return
                    elif numlinea!=int(txt[0:fin-3]):
                        self.errores(2)
                        return

            #self.estado.append("Lexema: ",txt[0:fin])
            txt=txt[fin:]
            todalalinea=txt
            todalalinea=todalalinea.strip()
            txt=self.separa(txt)
            
            #A partir de aqui el número de línea esta bien
            
            #self.estado.append(txt)
            txt=txt.strip()
            n=self.lex(txt)
            lexema_anterior="NADA"
            lexema="NADA"
            lexema_base=""
            while n>0:
                lexema_anterior=lexema
                lexema=txt[0:n]
                txt=txt[n:]
                txt=txt.strip()
                #self.estado.append("Lexema: ",lexema, "y sigue:",txt, len(txt))
                #self.estado.append("-----> Lexema que se obtuvo: "+lexema)
                if lexema=="PEDIR":
                    lexema_base="PEDIR"
                elif lexema=="HACER":
                    lexema_base="HACER"
                elif lexema=="MOSTRAR":
                    lexema_base="MOSTRAR"
                elif lexema=="=":
                    lexema_base="="
                elif lexema=="SI":
                    lexema_base="SI"
                elif lexema=="MIENTRAS":
                    lexema_base="MIENTRAS"
                elif lexema=="HASTAQUE":
                    lexema_base="HASTAQUE"
                elif lexema=="EN":
                    lexema_base="EN"
                elif lexema=="DESDE":
                    lexema_base="DESDE"
                elif lexema=="HASTA":
                    lexema_base="HASTA"
                elif lexema=="FIN":
                    lexema_base="FIN"
                elif lexema=="INICIO":
                    lexema_base="INICIO"
                elif lexema=="OR":
                    lexema_base="OR"
                elif lexema=="FINSI":
                    lexema_base="FINSI"

                #Verificamos si es una cadena de texto pero de una sola comilla
                if lexema[0:1]=='"':
                    #self.estado.append(txt,n, lexema)
                    txtpy=lexema
                    lexema="STRING"
                    
                #Veamos si es un identificador
                elif ( not PAL.search(lexema) ) and IDS.search(lexema):
                    #self.estado.append("Lexema",lexema)
                    if self.ID(lexema)==1:
                        agregarID=lexema
                        lexema="ID"
                    else:
                        self.errores(3)
                        return
                        
                #Verificamos si es un número entero o flotante
                elif NOI.search(lexema) or NOF.search(lexema):
                    lexema="CTE"

                #Verificamos si es un operador relacional
                elif OPR.search(lexema) :
                    txtpy=lexema
                    lexema="OR"

                #Python
                #self.estado.append(lexema_anterior)
                if lexema_base=="PEDIR" and lexema_anterior=="," and lexema=="ID":
                    txtpy=agregarID+' = float(input("Dame el valor de la variable '
                    txtpy=txtpy+agregarID
                    txtpy=txtpy+':"))'
                    codigopython.append(txtespacios+txtpy)
                elif lexema_base=="PEDIR" and lexema=="STRING":
                    cuenta=-1
                    for z in todalalinea:
                        if z=="N":
                            break
                        cuenta=cuenta+1
                    todalalinea2=todalalinea[cuenta+2:]
                    todalalinea2=todalalinea2.strip()                     
                    txtpy=todalalinea2+" = float(input("+txtpy+"))"
                    codigopython.append(txtespacios+txtpy)
                elif lexema_base=="PEDIR" and lexema=="ID":
                    txtpy=agregarID+' = float(input("Dame el valor de la variable '
                    txtpy=txtpy+agregarID
                    txtpy=txtpy+': "))'
                    codigopython.append(txtespacios+txtpy)
                if lexema_base=="HACER" and lexema=="ID":
                    txtpy=agregarID+txt
                    codigopython.append(txtespacios+txtpy)
                if lexema_base=="MOSTRAR" and lexema=="STRING" and len(txt)==0:
                    txtpy='print('+txtpy+')'
                    codigopython.append(txtespacios+txtpy)
                elif lexema_base=="MOSTRAR" and lexema=="ID" and len(txt)==0:
                    txtpy='print('+agregarID+')'
                    codigopython.append(txtespacios+txtpy)
                elif lexema_base=="MOSTRAR" and (lexema=="ID" or lexema=="STRING") and len(txt)>0:
                    txtz=""
                    todalalinea2=todalalinea[7:]
                    todalalinea2=todalalinea2.strip()
                    for z in todalalinea2:
                        if z=="+":
                            txtz=txtz+","
                        else:
                            txtz=txtz+z
                    txtpy='print('+txtz+')'
                    codigopython.append(txtespacios+txtpy)
                if lexema=="SI":
                    try:
                        t=txt.find("E")
                    except:
                        t=-1
                    if t>0:
                        txtpy="if "+txt[0:t]+":"
                        codigopython.append(txtpy)
                        txtespacios="    "
                if lexema=="MIENTRASQUE":
                    txtpy="while "+txt+":"
                    codigopython.append(txtpy)
                    txtespacios="    "
                if lexema=="HASTAQUE":
                    txtpy="while !("+txt+"):"
                    codigopython.append(txtpy)
                    txtespacios="    "
                if lexema=="FINSI" or lexema=="FINDESDE" or lexema=="FINMIENTRAS" or lexema=="FINHASTAQUE":
                    txtespacios=""
                if lexema=="SINO":
                    txtpy="else:"
                    codigopython.append(txtpy)
                if lexema=="DESDE":
                    cuenta=-1
                    for z in todalalinea:
                        if z=="S":
                            break
                        cuenta=cuenta+1
                    cuenta=cuenta+4
                    todalalinea2=todalalinea[cuenta:]
                    todalalinea2=todalalinea2.strip()
                    cuenta=-1
                    for z in todalalinea2:
                        if z=="=":
                            break
                        cuenta=cuenta+1
                    id1=todalalinea2[0:cuenta+1]
                    id1=id1.strip()
                    todalalinea2=todalalinea2[cuenta+2:]

                    cuenta=-1
                    for z in todalalinea2:
                        if z=="H":
                            break
                        cuenta=cuenta+1
                    id2=todalalinea2[0:cuenta+1]
                    id2=id2.strip()
                    todalalinea2=todalalinea2[cuenta+7:]

                    cuenta=-1
                    for z in todalalinea2:
                        if z=="=":
                            break
                        cuenta=cuenta+1
                    id3=todalalinea2[0:cuenta+1]
                    id3=id3.strip()
                    todalalinea2=todalalinea2[cuenta+2:]

                    cuenta=-1
                    for z in todalalinea2:
                        if z=="I":
                            break
                        cuenta=cuenta+1
                    id4=todalalinea2[0:cuenta+1]
                    id4=id4.strip()
                    todalalinea2=todalalinea2[cuenta+12:]
                    
                    cuenta=-1
                    for z in todalalinea2:
                        if z=="=":
                            break
                        cuenta=cuenta+1
                    id5=todalalinea2[0:cuenta+1]
                    id5=id5.strip()
                    todalalinea2=todalalinea2[cuenta+2:]
                    cuenta=-1
                    for z in todalalinea2:
                        if z=="+":
                            break
                        cuenta=cuenta+1
                    id6=todalalinea2[0:cuenta+1]
                    id6=id6.strip()
                    id7=todalalinea2[cuenta+1:]
                    id7=id7.strip()
                    if id1!=id3 and id3!=id5 and id5!=id6:
                        self.errores(15)
                        return
                    id4=str(int(id4)+1)
                    if id7[0]=="+":
                        id7=id7[1:]
                    txtpy='for '+id1+' in range('+id2+','+id4+','+id7+'):'
                    codigopython.append(txtespacios+txtpy)
                    txtespacios="    "
                    
                self.estado.append("El lexema es: "+lexema+"  texto restante -->"+txt)
                #Posibles errores
                if lexema_anterior=="ID" and lexema=="ID":
                    self.errores(5)
                    return
                    
                if (lexema_anterior=="EN" or lexema_anterior=="PEDIR" ) and lexema=="ID":
                    #self.estado.append("Debemos agregar el identificador:",agregarID," pero verificamos si no se repite")
                    for z in IDs:
                        if z==agregarID:
                            self.errores(6)
                            return
                    IDs.append(agregarID)

                if (lexema_anterior=="DESDE" or lexema_anterior=="HACER") and lexema=="ID":
                    #self.estado.append("Debemos agregar el identificador:",agregarID," pero verificamos si no se repite")
                    bandera=0
                    for z in IDs:
                        if z==agregarID:
                            bandera=1
                    if bandera==0:
                        IDs.append(agregarID)

                if lexema_base=="PEDIR" and lexema_anterior=="," and lexema=="ID":
                    #self.estado.append("Debemos agregar el identificador:",agregarID," pero verificamos si no se repite")
                    for z in IDs:
                        if z==agregarID:
                            self.errores(6)
                            return
                    IDs.append(agregarID)

                if (lexema_anterior=="HASTA" or lexema_base=="HASTAQUE" or lexema_base=="MIENTRASQUE" or lexema_base=="SI" or lexema_base=="MOSTRAR")and lexema=="ID":
                    #self.estado.append("Debemos verificar que ya exista el identificador:",agregarID)
                    bandera=0
                    for z in IDs:
                        if z==agregarID:
                            bandera=1
                    if bandera==0:
                        self.errores(7)
                        return

                if lexema_base=="=" and lexema=="ID":
                    #self.estado.append("Debemos verificar que ya exista el identificador:",agregarID)
                    bandera=0
                    for z in IDs:
                        if z==agregarID:
                            bandera=1
                    if bandera==0:
                        self.errores(7)
                        return

                if lexema_anterior=="OR" and lexema=="OR":
                    self.errores(13)
                    return

                if lexema_base=="SI" and lexema=="STRING":
                    self.errores(14)
                    return
                    
                if lexema_anterior=="STRING" and lexema=="OR":
                    self.errores(14)
                    return

                if lexema_base=="FIN" and totlineas>numlinea:                
                    self.errores(8)
                    return

                if numlinea==1 and lexema_base!="INICIO" :                
                    self.errores(9)
                    return
                
                sigue=pila.pop()
                self.estado.append("\nSiguiente arriba: "+str(sigue))
                try:
                    nr=vectorC.index(sigue)
                except:
                    nr = -1
                while nr>=0:
                    try:
                        nc=vectorR.index(lexema)
                    except:
                        nc=-1
                        
                    txtrev=rows[nr+1][nc]
                    txtrev=txtrev.strip()
                    self.estado.append("nr = {}, sigue en pila = {}, nc = {}, lexema = [{}]".format(nr,sigue,nc,lexema))
                    if nc>=0:
                        if rows[nr+1][nc]=="":
                            self.estado.append("\nnr = {}, sigue en pila = {}, nc ={}, lexema = [{}]".format(nr,sigue,nc,lexema))
                            self.estado.append("Error en la instrucción: CTE, ID, Operador, fuera de lugar.")
                            return
                        else:
                            lexema2=rows[nr+1][nc]
                            lexema2=lexema2.strip()
                            pila2=[]
                            n=self.lex(lexema2)
                            while n>0:
                                lexema3=lexema2[0:n]
                                pila2.append(lexema3)
                                lexema2=lexema2[n:]
                                lexema2=lexema2.strip()
                                n=self.lex(lexema2)
                            for k in range(len(pila2)-1,-1,-1):
                                if pila2[k]!="?":
                                    pila.append(pila2[k])

                    else:
                        self.errores(4)
                        return
                        
                    sigue=pila.pop()
                    self.estado.append("Siguiente abajo: "+str(sigue))
                    try:
                        nr=vectorC.index(sigue)
                    except:
                        nr = -1

                if sigue!=lexema:
                    self.estado.append("\nError en la instrucción: "+sigue+ " diferente de "+ lexema)
                    return
                n=self.lex(txt)
        
            self.estado.append("\nEstado de la pila: "+str(pila))

        self.estado.append("")

        if len(pila)==0:
            self.estado.append("El pseudocódigo está bien escrito.")
            self.estado.append("----------------------------------------------------------------------------------------------------------------")
            self.estado.append("Identificadores creados:\n")
            idx=1
            for z in IDs:
                self.estado.append(str(idx)+".- "+str(z))
                idx=idx+1
            self.estado.append("----------------------------------------------------------------------------------------------------------------")
            self.estado.append("En código python que se guardó fue:\n")
            lineantes=""
            with open("progpython.py", "w") as archivo_salida:
                for linea in codigopython:
                    if lineantes!=linea:
                        archivo_salida.write(linea + "\n")
                        lineantes=linea
                        self.estado.append(linea+"\n")
        else:
            self.errores(16)
            return
            

#self.estado.append("")
#self.estado.append("Identificadores creados")
#for z in IDs:
#    self.estado.append(z)

