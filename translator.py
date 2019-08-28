from sly import Lexer, Parser

TablaCadenas = {}
globales = []
ebps = {}
nVar = 0
ambito = 1
Nif = 0
Nwhile = 0
Ndistinto = 0
Nor = 0
Nand = 0
Nigual = 0
Ndesigual = 0
Nmayor_igual = 0
Nmenor_igual = 0
Nmenor = 0
Nmayor = 0
Ncadenas = 0
NParamPrint = 0
NParamLlamaFuncion = 0

class Nodo():
    def escribe():
        pass

class nodoEpilogo(Nodo):
    def escribe(self):
        print('\nmovl %ebp, %esp')
        print('popl %ebp')
        print('ret\n')

class nodoPrologo(Nodo):
    def escribe(self,p1):
        print('.text')
        print('.globl ' + p1)
        print('.type ' + p1 + ', @function')
        print(p1 + ':\n')
        print('pushl %ebp')
        print('movl %esp, %ebp')
        
class nodoMayor(Nodo):
    def escribe(self):
        print('movl %eax, %ebx;\npopl %eax;\ncmpl %ebx,%eax;\njle falseMayor'+str(Nmayor)+'\nmovl $1,%eax\njmp finalMayor'+str(Nmayor)+'\nfalseMayor'+str(Nmayor)+':\nmovl $0,%eax\nfinalMayor'+str(Nmayor)+':')


class nodoMayorIgual(Nodo):
    def escribe(self):
        print('movl %eax, %ebx;\npopl %eax;\ncmpl %ebx,%eax;\njge ciertoMayor_Igual'+str(Nmayor_igual)+'\nmovl $0,%eax\njmp finalMayor_Igual'+str(Nmayor_igual)+'\nciertoMayor_Igual'+str(Nmayor_igual)+':\nmovl $1,%eax\nfinalMayor_Igual'+str(Nmayor_igual)+':')

class nodoMenorIgual(Nodo):
    def escribe(self):
        print('movl %eax, %ebx;\npopl %eax;\ncmpl %ebx,%eax;\njle ciertoMenor_Igual'+str(Nmenor_igual)+'\nmovl $0,%eax\njmp finalMenor_Igual'+str(Nmenor_igual)+'\nciertoMenor_Igual'+str(Nmenor_igual)+':\nmovl $1,%eax\nfinalMenor_Igual'+str(Nmenor_igual)+':')

class nodoMenor(Nodo):
    def escribe(self):
        print('movl %eax, %ebx;\npopl %eax;\ncmpl %ebx,%eax;\njge falseMenor'+str(Nmenor)+'\nmovl $1,%eax\njmp finalMenor'+str(Nmenor)+'\nfalseMenor'+str(Nmenor)+':\nmovl $0,%eax\nfinalMenor'+str(Nmenor)+':')

class nodoDesigual(Nodo):
    def escribe(self):
        print('movl %eax, %ebx;\npopl %eax;\ncmpl %ebx,%eax;\njne falseDESIGUAL'+str(Ndesigual)+'\nmovl $0,%eax\njmp finalDESIGUAL'+str(Ndesigual)+'\nfalseDESIGUAL'+str(Ndesigual)+':\n movl $1,%eax\nfinalIGUAL'+str(Ndesigual)+':')

class nodoIgual(Nodo):
    def escribe(self):
        print('movl %eax, %ebx;\npopl %eax;\ncmpl %ebx,%eax;\njne falseIGUAL'+str(Nigual)+'\nmovl $1,%eax\njmp finalIGUAL'+str(Nigual)+'\nfalseIGUAL'+str(Nigual)+':\n movl $0,%eax\nfinalIGUAL'+str(Nigual)+':')

class nodoSuma(Nodo):
    def escribe(self):
        print('movl %eax, %ebx;\npopl %eax;\naddl %ebx,%eax;\n')

class nodoResta(Nodo):
    def escribe(self):
        print('movl %eax, %ebx;\npopl %eax;\nsubl %ebx,%eax;\n')

class nodoMulti(Nodo):
    def escribe(self):
        print('movl %eax, %ebx;\npopl %eax;\nimull %ebx,%eax;\n')

class nodoDiv(Nodo):
    def escribe(self):
        print('movl %eax, %ebx;\npopl %eax;\ncdq;\nidivl %ebx,%eax;\n')

class nodoDistinto(Nodo):
    def escribe(self):
        print('\ncmpl $0, %eax')
        print('je distinto'+str(Ndistinto))
        print('movl $1, %eax')
        print('distinto'+str(Ndistinto)+':')


class nodoEntero(Nodo):
    def escribe(self):
        print('subl $4, %esp')

class nodoAsig(Nodo):
    def escribe(self,p1,p2):
        print('movl '+ str(p2) +','+str(ebps[p1])+'(%ebp);\n')

class nodoMueveToEax(Nodo):
    def escribe(self,p1):
        print('movl '+ str(p1) +',%eax\n')

class nodoPushEax(Nodo):
    def escribe(self):
        print('pushl %eax')

class nodoMueve(Nodo):
    def escribe(self,p1,p2):
        print('movl '+ str(p1) +','+str(p2) +';\n')

class nodoLlamaFuncion(Nodo):
    def escribe(self,p1,p2):
        print('\ncall '+p1+';\naddl '+'$'+p2+',(%esp)\n')
        
class nodoListaParametrosLlama(Nodo):
    def escribe(self,i):
        print('\nmovl '+str(ebps['temp'+str(i)])+'(%ebp),%eax')
        ebps.pop('temp'+str(i))
        print('addl $4,%esp')
        print('pushl %eax')

class nodoEmptyParamLlama(Nodo):
    def escribe(self):
        global NParamLlamaFuncion
        print('subl $4,%esp')
        nuevo = min(ebps.values()) - 4
        print('movl %eax, '+str(nuevo)+'(%ebp)')
        ebps['temp'+ str(NParamLlamaFuncion)] = nuevo
        NParamLlamaFuncion = NParamLlamaFuncion + 1

class nodoPrintf(Nodo):
    def escribe(self,p1):
        global Ncadenas
        print('movl $s'+p1+', %eax\npushl %eax\ncall printf;')
        i = NParamPrint +1
        print('addl '+'$'+str(i*4)+',(%esp)')
        Ncadenas = Ncadenas + 1
class nodoListaParamPrint(Nodo):
    def escribe(self,i):
        print('movl '+str(ebps['temp'+str(i)])+'(%ebp),%eax')
        print('addl $4,%esp')
        print('pushl %eax')

class nodoEmptyParamPrint(Nodo):
    def escribe(self):
        global NParamPrint
        print('subl $4,%esp')
        nuevo = min(ebps.values()) - 4
        print('movl %eax, '+str(nuevo)+'(%ebp)')
        ebps['temp'+ str(NParamPrint)] = nuevo
        NParamPrint = NParamPrint + 1

class nodoRestoParamPrint(Nodo):
    def escribe(self):
        global NParamPrint
        print('subl $4,%esp')
        nuevo = min(ebps.values()) - 4
        print('movl %eax, '+str(nuevo)+'(%ebp)')
        ebps['temp'+ str(NParamPrint)] = nuevo
        NParamPrint = NParamPrint + 1

class Lexer(Lexer):
    tokens = {ID, NUM, CADENA, PRINTF, WHILE, IF, ELSE, MAIN,VOID, CHAR, INT, FLOAT, IGUAL, DISTINTO, MENOR_IGUAL, MAYOR_IGUAL, AND_AND, OR_OR}
    ignore = ' \t'
    literals = { '}','{',';',',', '*', '(', ')', '+',"/","-","=",">","<","!"}

    # Regular expression rules for tokens
    ID            = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['char']    = CHAR
    ID['int']     = INT
    ID['float']   = FLOAT
    #ID['main']    = MAIN
    ID['void']    = VOID
    ID['if']      = IF
    ID['else']    = ELSE
    ID['while']    = WHILE
    ID['printf']  = PRINTF
    IGUAL         = r'=='
    DISTINTO      = r'!='
    MENOR_IGUAL   = r'<='
    MAYOR_IGUAL   = r'>='
    AND_AND       = r'&&'
    OR_OR         = r'%%'
    CADENA        = r'".*"'

    @_(r'\d+')
    def NUM(self, t):
        t.value = int(t.value)
        return t
    
    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
        
class Parser(Parser):
    tokens = Lexer.tokens

    def __init__(self):
        self.names = { }

    @_('funcion entrada')
    def entrada(self,p):
    	pass

    @_('')
    def entrada(self,p):
    	pass

    @_('tipo ID igualNum ";"')
    def funcion(self,p):
        globales.append(p.ID)

    @_(' "=" NUM')
    def igualNum(self,p):
        pass

    @_('')
    def igualNum(self,p):
        pass



    @_('tipo ID  "(" emptyLocal parametrosFuncion ")" "{" instruccion "}" emptyGlobal')
    def funcion(self,p):
        nE = nodoEpilogo()
        nE.escribe()
        global ambito
        ambito = 1
    
    @_('tipo ID emptyParametros restoParam')
    def parametrosFuncion(self,p):
        global nVar
        nVar = 0

    @_('')
    def emptyParametros(self,p):
        global nVar
        nVar = nVar + 1
        ebps[p[-1]] = (nVar + 1)*4

    @_('')
    def parametrosFuncion(self,p):
        pass

    @_(' "," tipo ID emptyParametros restoParam')
    def restoParam(self,p):
    	pass

    
    @_('')
    def restoParam(self,p):
        pass

    
    @_('')
    def emptyGlobal(self,p):
        global ambito
        ambito = 1

    @_('')
    def emptyLocal(self,p):
        global ambito,nVar
        ambito = -1
        nVar = 0
        nP = nodoPrologo()
        nP.escribe(str(p[-2]))
        
        #ebps = {}

    @_('')
    def instruccion(self, p):
        pass

    @_('')
    def funcion(self,p):
        pass


    #---------INCIO DEFINICIONES--------------
    #Empties usados: 1,2,3,4,5
    @_('definicion instruccion')
    def instruccion(self, p):
        pass

    @_('tipo lista ";"')
    def definicion(self, p):
        pass
    
    @_('INT')
    def tipo(self,p):
        return "int"
    
    @_('CHAR')
    def tipo(self, p):
        return "char"

    @_('FLOAT')
    def tipo(self, p):
        return "float"
  
    @_(' empty1 elm resto')
    def lista(self,p):
        pass

    #Declaracion simple, int a = 2; ó int a = 2 + 9
    @_(' empty1 elm "=" arit_log empty2B resto')
    def lista(self,p):
        pass

    @_('')
    def empty1(self,p):
        ne = nodoEntero()
        ne.escribe()
        global nVar
        nVar = nVar + 1

    @_('')
    def empty2B(self,p):
        no = nodoAsig()
        no.escribe(p[-3],p[-1])
        return p[-5]

    @_(' "," empty3 elm resto')
    def resto(self,p):
        pass

    #Declaracion simple, int a = 2, b , c = 3;
    @_(' "," empty3 elm "=" arit_log empty4B resto')
    def resto(self,p):
        pass

    @_('')
    def empty3(self,p):
        ne = nodoEntero()
        ne.escribe()
        global nVar
        nVar = nVar + 1

    @_('')
    def empty4B(self,p):
        no = nodoAsig()
        no.escribe(p[-3],p[-1])

    @_(' ')
    def resto(self,p):
        pass

    @_(' "*" elm ')
    def elm(self,p):
        return p.elm

    @_(' ID ')
    def elm(self,p):
        ebps[p.ID] = ambito*(nVar)*4
        return p.ID
    #------------FIN DEFINICIONES-----------------
    #Empties usados: 1,2,3,4,5


    #------------SENTENCIAS CONDICIONALES---------



    #------------INCIO ARITMÉTICA-----------------
    #Empties usados: 
    @_(' arit_log ";" instruccion')
    def instruccion(self, p):
        pass

    @_('prioridad0')
    def arit_log(self,p):
        return '%eax'

    @_('prioridad0 emptyOR OR_OR prioridad1')
    def prioridad0(self,p):
        global Nor
        Nor = Nor + 1
        print('finalOR_OR'+str(p.emptyOR)+':')

    @_('')
    def emptyOR(self,p):
        global Nor
        print('cmpl $0, %eax')
        print('jne finalOR'+str(Nor)) 
        return Nor

    @_('prioridad1')
    def prioridad0(self,p):
        pass


    @_('prioridad1 emptyAND AND_AND prioridad2')
    def prioridad1(self,p):
        global Nand
        Nand = Nand + 1
        print('finalAND_AND'+str(p.emptyAND)+':')

    @_('')
    def emptyAND(self,p):
        global Nand
        print('cmpl $0, %eax')
        print('je final'+str(Nand)+':')
        return Nand

    @_('prioridad2ymedio')
    def prioridad1(self,p):
        pass

    @_('prioridad2ymedio emptyMENORIGUAL MENOR_IGUAL prioridad2')
    def prioridad2ymedio(self,p):
        nM = nodoMenorIgual()
        nM.escribe()

    @_('')
    def emptyMENORIGUAL(self,p):
        nP = nodoPushEax()
        nP.escribe()
        global Nmenor_igual
        Nmenor_igual = Nmenor_igual + 1

    
    @_('prioridad2ymedio emptyMAYORIGUAL MAYOR_IGUAL prioridad2')
    def prioridad2ymedio(self,Nmayor_igual):
        nM = nodoMayorIgual()
        nM.escribe()

    @_('')
    def emptyMAYORIGUAL(self,p):
        nP = nodoPushEax()
        nP.escribe()
        global Nmayor_igual
        Nmayor_igual = Nmayor_igual + 1

    @_('prioridad2ymedio emptyMENOR "<" prioridad2')
    def prioridad2ymedio(self,p):
        nM = nodoMenor()
        nM.escribe()
        
    @_('')
    def emptyMENOR(self,p):
        nP = nodoPushEax()
        nP.escribe()
        global Nmenor
        Nmenor = Nmenor + 1

    @_('prioridad2ymedio emptyMAYOR ">" prioridad2')
    def prioridad2ymedio(self,p):
        nM = nodoMayor()
        nM.escribe()

    @_('')
    def emptyMAYOR(self,p):
        nP = nodoPushEax()
        nP.escribe()
        global Nmayor
        Nmayor = Nmayor + 1

    @_('prioridad2')
    def prioridad2ymedio(self,p):
        pass

    @_('prioridad2 emptyDESIGUAL DISTINTO prioridad3')
    def prioridad2(self,p):
        nD = nodoDesigual()
        nD.escribe()

    @_('')
    def emptyDESIGUAL(self,p):
        nP = nodoPushEax()
        nP.escribe()
        global Ndesigual
        Ndesigual = Ndesigual + 1

    @_('prioridad2 emptyIGUAL IGUAL prioridad3')
    def prioridad2(self,p):
        nI = nodoIgual()
        nI.escribe()
            
    @_('')
    def emptyIGUAL(self,p):
        nP = nodoPushEax()
        nP.escribe()
        global Nigual
        Nigual = Nigual + 1

    @_('prioridad3')
    def prioridad2(self,p):
        pass

    @_('prioridad3 emptyP3 "+" prioridad4')
    def prioridad3(self,p):
        nS = nodoSuma()
        nS.escribe()
        
    
    @_('prioridad3 emptyP3 "-" prioridad4')
    def prioridad3(self,p):
        nR = nodoResta()
        nR.escribe()

    @_('')
    def emptyP3(self,p):
        nP = nodoPushEax()
        nP.escribe()

    @_('prioridad4')
    def prioridad3(self,p):
        pass
    
    @_('prioridad4 emptyP4 "*" prioridad5')
    def prioridad5(self,p):
        nM = nodoMulti()
        nM.escribe()

    @_('prioridad4 emptyP4 "/" prioridad5')
    def prioridad5(self,p):
        nD = nodoDiv()
        nD.escribe()

    @_('')
    def emptyP4(self,p):
        print('pushl %eax')

    @_('prioridad5')
    def prioridad4(self,p):
        pass
    
    @_('"!" prioridad5')
    def prioridad5(self,p):
        global Ndistinto
        Ndistinto = Ndistinto + 1
        nD = nodoDistinto()
        nD.escribe()

    @_('prioridad6')
    def prioridad5(self,p):
        return p.prioridad6

    @_('NUM')
    def prioridad6(self,p):
        nM = nodoMueveToEax()
        nM.escribe('$'+str(p.NUM))
        return p.NUM

    @_('elmA')
    def prioridad6(self,p):
        return p.elmA

    @_(' "(" arit_log ")"')
    def prioridad6(self,p):
        return p.arit_log

    @_(' ID ')
    def elmA(self,p):
        nM = nodoMueveToEax()
        if str(p.ID) in ebps:
         nM.escribe(str(ebps[p.ID])+'(%ebp)')
        else: 
            if str(p.ID) in globales:
                nM.escribe(p.ID)

    
    #------------FIN ARITMÉTICAS---------------- 

    

    #------------INCIO ASIGNACIONES---------------
    #Empties usados: 
    @_('asignacion ";" instruccion')
    def instruccion(self,p):
        pass

    @_('elmAsig restoAsig')
    def asignacion(self,p):
        pass
    #Antes de incluir cambiar el contenido de la variable en TablaValores habría que mirar que existe en TablaTipo
    @_('"=" elmAsig restoAsig')
    def restoAsig(self,p):
        nM = nodoMueve()
        nM.escribe(str(p.elmAsig),str(p[-4]))

    @_('"=" NUM')
    def restoAsig(self,p):
        nM = nodoMueve()
        nM.escribe('$'+str(p.NUM),str(p[-1]))

    #La variable elmAsig debe existir ya en TablaAsig
    @_('"=" elmAsig')
    def restoAsig(self,p):
        nM = nodoMueve()
        nM.escribe(str(p.elmAsig),str(p[-1]))      

    @_('"=" llamaFuncion')
    def restoAsig(self,p):
        nM = nodoMueve()
        nM.escribe(str('%eax'),str(p[-3]))

    @_('"=" arit_log')
    def restoAsig(self,p):
        nM = nodoMueve()
        nM.escribe(str('%eax'),str(p[-3]))

    @_('* elmAsig')
    def elmAsig(self,p):
        return p.elmAsig

    @_('ID')
    def elmAsig(self,p):
        if p.ID in ebps:
            return str(ebps[p.ID])+'(%ebp)'
        else:
            if p.ID in globales:
                return '$'+p.ID

    #------------FIN ASIGNACIONES---------------

    #------------INICIO FUNCIONES---------------
    @_('llamaFuncion ";" instruccion')
    def instruccion(self,p):
        pass

    @_('ID "(" listaParametrosLlamaFuncion ")"')
    def llamaFuncion(self,p):
        global NParamLlamaFuncion
        Nl = nodoLlamaFuncion()
        Nl.escribe(p.ID,str(NParamLlamaFuncion*4))
        NParamLlamaFuncion = 0

    @_('')
    def listaParametrosLlamaFuncion(self,p):
        pass

    @_('llamaFuncion emptyParamLlamaFuncion restoParametrosLlamaFuncion')
    def listaParametrosLlamaFuncion(self,p):
        global NParamLlamaFuncion
        i = NParamLlamaFuncion - 1
        nl = nodoListaParametrosLlama() 
        while(i>=0):
            nl.escribe(i)
            i = i - 1

    @_('arit_log emptyParamLlamaFuncion restoParametrosLlamaFuncion')
    def listaParametrosLlamaFuncion(self,p):
        global NParamLlamaFuncion
        i = NParamLlamaFuncion - 1
        nl = nodoListaParametrosLlama() 
        while(i>=0):
            nl.escribe(i)
            i = i - 1

    @_('')
    def emptyParamLlamaFuncion(self,p):        
        nE = nodoEmptyParamLlama()
        nE.escribe()

    
    @_('"," arit_log emptyParamLlamaFuncion restoParametrosLlamaFuncion')
    def restoParametrosLlamaFuncion(self,p):
        pass

    @_('"," llamaFuncion emptyParamLlamaFuncion restoParametrosLlamaFuncion')
    def restoParametrosLlamaFuncion(self,p):
        pass

    @_('')
    def restoParametrosLlamaFuncion(self,p):
        pass

    @_('PRINTF "(" CADENA emptyCADENA listaParametrosPrint ")"')
    def llamaFuncion(self,p):
        nP = nodoPrintf()
        nP.escribe(p.emptyCADENA)

        

    @_('')
    def emptyCADENA(self,p):
        global Ncadenas,TablaCadenas
        TablaCadenas[Ncadenas] = str(p[-1])
        return str(Ncadenas)

    @_('')
    def listaParametrosPrint(self,p):
        pass

    @_('"," arit_log emptyParamPrint restoParametrosPrint')
    def listaParametrosPrint(self,p):
        global NParamPrint
        i = NParamPrint - 1
        nLP = nodoListaParamPrint()
        while(i>=0):
            nLP.escribe(i)
            i = i - 1

    @_('')
    def emptyParamPrint(self,p):
        nEPP = nodoEmptyParamPrint()
        nEPP.escribe()

    @_('"," arit_log')
    def restoParametrosPrint(self,p):
        nRPP = nodoRestoParamPrint()
        nRPP.print()

    @_('')
    def restoParametrosPrint(self,p):
        pass

    #---------------------------INICIO SENTENCIAS CONDICIONALES-------------------

    @_('IF_ELSE instruccion')
    def instruccion(self, p):
        pass

    @_('')
    def IF_ELSE(self, p):
        pass

    @_('IF "(" arit_log ")" emptyIF_INICIO "{" instruccion "}" inicioELSE')
    def IF_ELSE(self, p):
        print('finalIf'+str(p.emptyIF_INICIO)+':\n')


    @_('ELSE emptyELSE_INICIO "{" instruccion "}"')
    def inicioELSE(self,p):
        pass
        #print('finalIf'+str(p[-4])+':')

    @_('')
    def inicioELSE(self,p):
        print('jmp finalIf'+str(p[-4])+'\n')
        print('false'+str(p[-4])+':')
        
    @_('')
    def emptyELSE_INICIO(self,p):
        print('jmp finalIf'+str(p[-5]))
        print('false'+str(p[-5])+":")

    @_('')
    def emptyIF_INICIO(self,p):
        global Nif
        print('cmp $0, %eax')
        Nif = Nif + 1
        etiq = 'false'+str(Nif)
        print('jne '+ etiq)
        etLevel = Nif
        return etLevel
    
    #---------------------------FIN SENTENCIAS CONDICIONALES------------------

    #---------------------------INICIO WHILE-------------------
    @_('bucle_while instruccion')
    def instruccion(self, p):
        pass

    @_(' WHILE emptyStartWhile "(" arit_log ")" emptyWhile "{" instruccion "}" ')
    def bucle_while(self, p):
        print('jmp start'+str(p.emptyWhile))
        print('finalWhile'+str(p.emptyWhile)+':')

    @_('')
    def bucle_while(self, p):
    	pass

    @_('')
    def emptyStartWhile(self,p):
        global Nwhile
        print('start'+str(Nwhile+1)+':')

    @_('')
    def emptyWhile(self,p):
    	print('cmpl $0, %eax')
    	
    	global Nwhile
    	Nwhile = Nwhile + 1
    	e = Nwhile

    	print('je finalWhile'+str(Nwhile))
    	return e
    #---------------------------FIN WHILE----------------------

    

if __name__ == '__main__':
    lexer = Lexer()
    parser = Parser()

    f = open("CodigoC.c")
    try:
        text = f.read()
    except EOFError:
        print("Ha ocurrido un error")
    if text: 
        parser.parse(lexer.tokenize(text))
    #print(TablaTipos)
    #print(TablaValores)
    print(ebps)
    print(globales)

