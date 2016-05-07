'''
Created on Dec 9, 2015

@author: Adam Horea-Marius
============================================================
=Nume: Adam Horea-Marius                                   =
=Grupa: 211                                                =
=Specializare: Informatica Romana, anul I                  =
============================================================
'''
class InputException(Exception):
    pass

class Number():
    '''
    Clasa ce incapsuleaza un numar intr-o baza oarecare, precum si operatiile obisnuite
    '''
    def __init__(self, sir_cifre, baza):
        '''
        Primeste in constructor sirul cifrelor format din numere intregi pozitive < 15
        si o baza oarecare >= 2 si <= 16
        Suporta operatiile arimetice de baza
        '''
        self.__sir_cifre =sir_cifre[::-1]
        self.__baza = baza
            
    def __add__(self, ot):
        '''
        Adunarea a doua numere intr-o baza oarecare, memorate prin sirul cifrelor
        post: returneaza suma sub forma unui obiect de tip Number
        '''
        if len(self.__sir_cifre) <= len(ot.__sir_cifre): k = len(self.__sir_cifre)
        else: k = len(ot.__sir_cifre)
        t = 0
        rez = []
        for i in range(0, k):
            rez.append((self.__sir_cifre[i] + ot.__sir_cifre[i] + t) % self.__baza)
            t = (self.__sir_cifre[i] + ot.__sir_cifre[i] + t) // self.__baza
        for i in range(k, len(self.__sir_cifre)):
            rez.append((self.__sir_cifre[i] + 0 + t) % self.__baza)
            t = (self.__sir_cifre[i] + 0 + t) // self.__baza
        for i in range(k, len(ot.__sir_cifre)):
            rez.append((0 + ot.__sir_cifre[i] + t) % self.__baza)
            t = (0 + ot.__sir_cifre[i] + t) // self.__baza
        if t == 1: rez.append(1)
        return Number(rez[::-1], self.__baza)
    
    def __lt__(self, ot):
        '''
        ot : Number
        Aceasta metoda este apelata oridecate ori are loc comparatia n1 < n2, unde n1, n2 
        sunt 2 obiecte de tip Number
        Returneaza True daca n1 < n2 si False in caz contrar
        '''
        a = self.__sir_cifre[::-1]
        b = ot.__sir_cifre[::-1]
        while len(a) > 1 and a[0] == 0: a.pop(0)
        while len(b) > 1 and b[0] == 0: b.pop(0)
        if len(a) < len(b): return True
        if len(a) > len(b): return False
        for i in range(len(a)):
            if a[i] == b[i]: continue
            elif a[i] < b[i]: return True
            else: return False
        return False
    
    def __eq__(self, ot):
        '''
        Returneaza True daca 2 obiecte de tip Number sunt egale,
        iar false in caz contrar
        '''
        for cifra in self.__sir_cifre:
            if cifra != ot.__sir_cifre[0]: return False
        return True
    
    def __ne__(self, ot):
        '''
        Returneaza True daca 2 obiecte de tip Number sunt diferite,
        iar false in caz contrar
        '''
        return not self == ot
    
    def __sub__(self, ot):
        '''
        Preconditii : Descazutul >= scazatorul
        Returneaza diferenta a doua numere scrise intr-o baza oarecare
        '''
        t = 0
        rez = []
        if len(ot.__sir_cifre) < len(self.__sir_cifre): lg_max = len(ot.__sir_cifre)
        else: lg_max = len(self.__sir_cifre)
        for i in range(0, lg_max):
            if self.__sir_cifre[i] + t >= ot.__sir_cifre[i]:
                rez.append(self.__sir_cifre[i] + t - ot.__sir_cifre[i])
                t = 0
            else:
                rez.append(self.__baza + self.__sir_cifre[i] + t - ot.__sir_cifre[i])
                t = -1
        i += 1
        while i < len(self.__sir_cifre):
            if self.__sir_cifre[i] + t >= 0:
                rez.append(self.__sir_cifre[i] + t - 0)
                t = 0
            else:
                rez.append(self.__baza + self.__sir_cifre[i] + t - 0)
                t = -1
            i += 1
        return Number(rez[::-1], self.__baza)
    
    def mul(self, c):
        '''
        Inmulteste un numar intr-o baza oarecare cu o cifra din baza respectiva
        Returneaza rezultatul inmultirii in baza respectiva
        '''
        rez = []
        t = 0
        for i in range(0, len(self.__sir_cifre) ):
            rez.append((self.__sir_cifre[i] * c + t) % self.__baza)
            t = (self.__sir_cifre[i] * c + t) // self.__baza
        rez.append(t)
        return Number(rez[::-1], self.__baza)
    
    def __integer_division(self, c):
        '''
        Returneaza o pereche ce contine catul si restul impartirii unui numar scris 
        intr-o baza oarecare la o cifra din aceeasi baza
        '''
        if c == 0: raise ZeroDivisionError("Impartirea la zero este imposibila!")
        t = 0
        sir = self.__sir_cifre[::-1]
        cat = []
        for i in range(len(sir)):
            cat.append((t * self.__baza + sir[i]) // c)
            t = (t * self.__baza + sir[i]) % c
        return (Number(cat, self.__baza), Number([t], self.__baza))
    
    def div(self, c):
        '''
        Retuneaza catul impartirii a unui obiect de tip Number la cifra c
        '''
        rez = self.__integer_division(c)
        return rez[0]
    
    def mod(self,c):
        '''
        Retuneaza restul impartirii unui obiect de tip Number la cifra c
        '''
        rez = self.__integer_division(c)
        return rez[1]
    
    def get_sir_cifre(self):
        return self.__sir_cifre
    
    def conversie(self, new_base):
        '''
        pre: 2 <= new_base: int <= 16
        Returneaza numarul convertit in noua baza, folosind dupa caz,
        conversia prin impartiri succesive, conversia prin substitutie
        '''
        if self.__baza == new_base: return self, str(self)
        elif new_base > self.__baza: return self.conv_prin_substitutie(new_base)
        else: return self.conv_prin_impartiri(new_base)

    def conv_prin_substitutie(self, new_base):
        '''
        Algoritmul de conversie prin substitutie generala a unui dintr-o baza oareacare
        intr-o alta baza oarecare
        Primeste noua baza ca parametru si returneaza un tuplu format din un obiect
        de tip Number si un string ce reprezinta modul in care s-a realizat conversia
        '''
        dict_cifre = {0: "0", 1: "1", 2: "2", 3: "3", 
                      4: "4", 5: "5", 6: "6", 7: "7", 
                      8: "8", 9: "9", 10: "A", 11: "B",
                      12: "C", 13: "D", 14: "E", 15: "F"}
        rez = Number([0], new_base)
        prev = Number([1], new_base)
        exemplu = ""
        for i in range (0, len(self.__sir_cifre)):
            exemplu += dict_cifre[self.__sir_cifre[i]]+" * "+dict_cifre[self.__baza]+" ^ "+str(i)+" + "
            rez = rez + prev.mul(self.__sir_cifre[i])
            prev = prev.mul(self.__baza)
        exemplu = "("+exemplu[:-3]+")("+str(new_base)+")"
        return rez, exemplu
    
    def conv_prin_impartiri(self, new_base):
        '''
        Algoritmul de conversie prin impartiri succesive a unui dintr-o baza oareacare
        intr-o alta baza oarecare
        Primeste noua baza ca parametru si returneaza un tuplu format din un obiect
        de tip Number si un string ce reprezinta modul in care s-a realizat conversia
        '''
        dict_cifre = {0: "0", 1: "1", 2: "2", 3: "3", 
                      4: "4", 5: "5", 6: "6", 7: "7", 
                      8: "8", 9: "9", 10: "A", 11: "B",
                      12: "C", 13: "D", 14: "E", 15: "F"}
        rez = []
        exemplu = ""
        cat = self.div(new_base)
        rest = self.mod(new_base)
        exemplu += str(self)+" : "+dict_cifre[new_base]+" = "+str(cat)+" rest "+str(rest)+"\n"
        rez.append(rest.__sir_cifre[0])
        zero = Number([0], self.__baza)
        while cat != zero:
            rest = cat.mod(new_base)
            old_cat = cat
            cat = cat.div(new_base)
            exemplu += str(old_cat)+" : "+dict_cifre[new_base]+" = "+str(cat)+" rest "+str(rest)+"\n"
            rez.append(rest.__sir_cifre[0])
        return Number(rez[::-1], new_base), exemplu
    
    def __2to4(self, new_base):
        '''
        Conversia unui numar din baza 2 in baza 4 folosind faptul ca 1 cifra in 
        baza 4 poate fi reprezentata cu 2 cifre din baza 2
        '''
        dict_cifre = {"00": 0, "01": 1, "10": 2, "11": 3}
        nr_caractere_de_sters = 2 + len(str(self.__baza))
        nr = str(self)[:-nr_caractere_de_sters]
        if len(nr) % 2 != 0: nr = "0" + nr
        lista_cifre = [nr[i:i+2] for i in range(0, len(nr), 2)]
        rez = []
        ex = ""
        for cifra in lista_cifre:
            if cifra in dict_cifre:
                rez.append(dict_cifre[cifra])
                ex += cifra + " "
        return Number(rez, new_base), ex[:-1]
    
    def __2to8(self, new_base):
        '''
        Conversia unui numar din baza 2 in baza 8 folosind faptul ca 1 cifra in 
        baza 8 poate fi reprezentata cu 3 cifre din baza 2
        '''
        dict_cifre = {"000": 0, "001": 1, "010": 2, "011": 3,
                      "100": 4, "101": 5, "110": 6, "111": 7}
        nr_caractere_de_sters = 2 + len(str(self.__baza))
        nr = str(self)[:-nr_caractere_de_sters]
        if len(nr) % 3 == 1: nr = "00" + nr
        elif len(nr) % 3 == 2: nr = "0" + nr
        lista_cifre = [nr[i:i+3] for i in range(0, len(nr), 3)]
        rez = []
        ex = ""
        for cifra in lista_cifre:
            if cifra in dict_cifre:
                rez.append(dict_cifre[cifra])
                ex += cifra + " "
        return Number(rez, new_base), ex[:-1]
    
    def __2to16(self, new_base):
        '''
        Conversia unui numar din baza 2 in baza 16 folosind faptul ca 1 cifra in 
        baza 16 poate fi reprezentata cu 4 cifre din baza 2
        '''
        dict_cifre = {"0000": 0, "0001": 1, "0010": 2, "0011": 3,
                      "0100": 4, "0101": 5, "0110": 6, "0111": 7,
                      "1000": 8, "1001": 9, "1010": 10, "1011": 11,
                      "1100": 12, "1101": 13, "1110": 14, "1111": 15}
        nr_caractere_de_sters = 2 + len(str(self.__baza))
        nr = str(self)[:-nr_caractere_de_sters]
        if len(nr) % 4 == 1: nr = "000" + nr
        elif len(nr) % 4 == 2: nr = "00" + nr
        elif len(nr) % 4 == 3: nr = "0" + nr
        lista_cifre = [nr[i:i+4] for i in range(0, len(nr), 4)]
        rez = []
        ex = ""
        for cifra in lista_cifre:
            if cifra in dict_cifre:
                rez.append(dict_cifre[cifra])
                ex += cifra + " "
        return Number(rez, new_base), ex[:-1]
    
    def __16to2(self, new_base):
        '''
        Conversia unui numar din baza 16 in baza 2 folosind faptul ca 4 cifre 
        binare corespund unei cifre hexa
        '''
        dict_cifre = {'0' : [0, 0, 0, 0] , '1' : [0, 0, 0, 1] ,'2' : [0, 0, 1, 0] ,'3' : [0, 0, 1, 1] ,
                      '4' : [0, 1, 0, 0] , '5' : [0, 1, 0, 1] ,'6' : [0, 1, 1, 0] , '7' : [0, 1, 1, 1] ,
                      '8' : [1, 0, 0, 0] , '9' : [1, 0, 0, 1] , 'A' : [1, 0, 1, 0] , 'B' : [1, 0, 1, 1] ,
                      'C' : [1, 1, 0, 0] , 'D' : [1, 1, 0, 1] , 'E' : [1, 1, 1, 0] , 'F' : [1, 1, 1, 1] ,}
        nr_caractere_de_sters = 2 + len(str(self.__baza))
        nr = str(self)[:-nr_caractere_de_sters]
        lista_cifre = [nr[i:i+1] for i in range(0, len(nr), 1)]
        rez = []
        ex = ""
        for cifra in lista_cifre:
            if cifra in dict_cifre:
                rez += dict_cifre[cifra]
                ex += cifra + " "
        return Number(rez, new_base), ex[:-1]
    
    def __8to2(self, new_base):
        '''
        Conversia unui numar din baza 8 in baza 2 folosind faptul ca 3 cifre 
        binare corespund unei cifre octal
        '''
        dict_cifre = {'0' : [0, 0, 0] , '1' : [0, 0, 1] ,'2' : [0, 1, 0] ,'3' : [0, 1, 1] ,
                      '4' : [1, 0, 0] ,  '5' : [1, 0, 1] , '6' : [1, 1, 0] , '7' : [1, 1, 1]}
        nr_caractere_de_sters = 2 + len(str(self.__baza))
        nr = str(self)[:-nr_caractere_de_sters]
        lista_cifre = [nr[i:i+1] for i in range(0, len(nr), 1)]
        rez = []
        ex = ""
        for cifra in lista_cifre:
            if cifra in dict_cifre:
                rez += dict_cifre[cifra]
                ex += cifra + " "
        return Number(rez, new_base), ex[:-1]
    
    def __4to2(self, new_base):
        '''
        Conversia unui numar din baza 4 in baza 2 folosind faptul ca 2 cifre 
        binare corespund unei cifre in baza 4
        '''
        dict_cifre = {'0' : [0, 0] , '1' : [0, 1] ,'2' : [1, 0] ,'3' : [1, 1]}
        nr_caractere_de_sters = 2 + len(str(self.__baza))
        nr = str(self)[:-nr_caractere_de_sters]
        lista_cifre = [nr[i:i+1] for i in range(0, len(nr), 1)]
        rez = []
        ex = ""
        for cifra in lista_cifre:
            if cifra in dict_cifre:
                rez += dict_cifre[cifra]
                ex += cifra + " "
        return Number(rez, new_base), ex[:-1]
    
    def conv_rapide(self, new_base):
        '''
        Alege algoritmul de conversii rapide in functie de baza initiala
        si baza destinatie
        '''
        if self.__baza == 2 and new_base == 4: return self.__2to4(new_base)
        elif self.__baza == 2 and new_base == 8: return self.__2to8(new_base)
        elif self.__baza == 2 and new_base == 16: return self.__2to16(new_base)
        elif self.__baza == 16 and new_base == 2: return self.__16to2(new_base)
        elif self.__baza == 8 and new_base == 2: return self.__8to2(new_base)
        elif self.__baza == 4 and new_base == 2: return self.__4to2(new_base)
        elif self.__baza == 2 and new_base == 2: return self, str(self)[:-3]
        
    def __str__(self):
        '''
        functie folosita la afisarea unui numar intr-o baza oareare
        '''
        return self.__repr__()
    
    def __repr__(self):
        '''
        functie ce este apelata cand este folosita funcia str(numar)
        returneaza reprezentarea unui obiect de tip Number
        '''
        rez = ""
        dict_cifre = {10 : "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"}
        i = 0
        sir = self.__sir_cifre[::-1]
        while len(sir) > 1 and sir[0] == 0: sir.pop(0)
        for cnt in range(i, len(sir)):
            cifra = sir[cnt]
            if cifra < 10: rez += str(cifra)
            else: rez += dict_cifre[cifra]
        return rez + "(" + str(self.__baza) + ")"
#End of number class definition
             
def make_int_list(sir):
    '''
    Primeste un sir de caractere si retunreaza o lista de numere intregi, 
    Fiecare element al listei reprezentand cifra corespunzatoare fiecarui caracter
    Daca a fost introdus un caracter care nu este cifra se va semnala eroarea
    '''
    dict_cifre = {"0": 0, "1": 1, "2": 2, "3": 3, 
                  "4": 4, "5": 5, "6": 6, "7": 7,
                  "8": 8, "9": 9, "A" : 10, "B": 11,
                  "C": 12, "D": 13, "E": 14, "F": 15,
                  "a" : 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15} 
    if sir == "": raise InputException("Ati introdus un numar invalid!")
    rez = []
    for cifra in sir:
        if not cifra in dict_cifre: raise InputException("Ati introdus un numar invalid!")
        else: rez.append(dict_cifre[cifra])
    while len(rez) > 1 and rez[0] == 0: rez.pop(0)
    return rez

def validate(sir, baza):
    '''
    Ridica InputException daca sirul nu poate reprezenta un 
    numar scris in baza transmisa ca parametru
    '''
    for el in sir:
        if el < 0 or el >= baza: raise InputException("Ati introdus in numar invalid!")

def read_base():
    '''
    Returneaza o baza citita de la tastatura
    Daca baza introdusa este incorecta se ridica InputException
    '''
    baza = input("> ") 
    try:
        baza = int(baza) 
        if baza < 2 or baza > 16: raise InputException("Baza poate sa fie un numar intreg din intervalul [2, 16]")     
    except ValueError: raise InputException("Baza poate sa fie un numar intreg din intervalul [2, 16]")
    return baza

def afisare_procedeu_substitutie(nr, baza_initiala, baza_finala):
    '''
    nr : obiect de tip Number()
    baza_intiala, baza_finala : int
    Afiseaza pasii prin care are loc conversia prin substitutie a 
    numarului nr din baza initiala in baza finala
    '''
    print("Conversie prin substitutie din baza "+str(baza_initiala)+" in baza "+str(baza_finala)+": ")
    conv = nr.conversie(baza_finala)
    print(nr,"=",conv[1],"=",conv[0])
    print("---------------------------------------------------------")
 
def afisare_procedeu_impartire(nr, baza_initiala, baza_finala):
    '''
    nr : obiect de tip Number()
    baza_intiala, baza_finala : int
    Afiseaza pasii prin care are loc conversia prin impartiri 
    succesive a numarului nr din baza initiala in baza finala
    '''
    print("Conversie prin impartiri din baza "+str(baza_initiala)+" in baza "+str(baza_finala)+": ")
    conv = nr.conversie(baza_finala)
    print(conv[1])
    print("Luand resturile in ordine inversa avem:",nr,"=",conv[0])
    print("---------------------------------------------------------") 
    
def sub_menu_1():
    '''
    Realizeaza interfata cu uilizatorul in cadrul primului submeniu si gestioneaza 
    modul in care este prezentata adunarea a doua numere intr-o baza oarecare
    '''
    print("Introduceti baza primului numar: ")
    baza1 = read_base()
    n1 = input("Introduceti primul numar:\n>")
    n1 = make_int_list(n1)
    validate(n1, baza1)
    print("Introduceti baza celui de-al doilea numar: ")
    baza2 = read_base()
    n2 = input("Introduceti al doilea numar:\n>")
    n2 = make_int_list(n2)
    validate(n2, baza2)
    print("Introduceti baza in care doriti sa fie efectuate calculele: ")
    baza_finala = read_base()
    n1 = Number(n1, baza1)
    n2 = Number(n2, baza2)
    n1_conversion = n1.conversie(baza_finala)
    n2_conversion = n2.conversie(baza_finala)
    if baza1 <= baza_finala: afisare_procedeu_substitutie(n1, baza1, baza_finala)
    else: afisare_procedeu_impartire(n1, baza1, baza_finala)
    if baza2 <= baza_finala: afisare_procedeu_substitutie(n2, baza2, baza_finala)
    else: afisare_procedeu_impartire(n2, baza2, baza_finala)
    print(str(n1_conversion[0])+" + "+str(n2_conversion[0])+" = "+str(n1_conversion[0] + n2_conversion[0]) + "\n")

def sub_menu_2():
    '''
    Realizeaza interfata cu uilizatorul in cadrul celui de-al doilea submeniu si gestioneaza 
    modul in care este prezentata scaderea a doua numere intr-o baza oarecare
    '''
    print("Introduceti baza descazutului: ")
    baza1 = read_base()
    n1 = input("Introduceti descazutul:\n>")
    n1 = make_int_list(n1)
    validate(n1, baza1)
    print("Introduceti baza scazatorului: ")
    baza2 = read_base()
    n2 = input("Introduceti scazatorul:\n>")
    n2 = make_int_list(n2)
    validate(n2, baza2)
    print("Introduceti baza in care doriti sa fie efectuate calculele: ")
    baza_finala = read_base()
    n1 = Number(n1, baza1)
    n2 = Number(n2, baza2)
    n1_conversion = n1.conversie(baza_finala)
    n2_conversion = n2.conversie(baza_finala)
    if n1_conversion[0] < n2_conversion[0]:
        raise InputException("Scazatorul nu poate fi mai mare decat descazutul!")
    if baza1 <= baza_finala: afisare_procedeu_substitutie(n1, baza1, baza_finala)
    else: afisare_procedeu_impartire(n1, baza1, baza_finala)
    if baza2 <= baza_finala: afisare_procedeu_substitutie(n2, baza2, baza_finala)
    else: afisare_procedeu_impartire(n2, baza2, baza_finala)
    print(str(n1_conversion[0])+" - "+str(n2_conversion[0])+" = "+str(n1_conversion[0] - n2_conversion[0]) + "\n")

def sub_menu_3():
    '''
    Realizeaza interfata cu uilizatorul in cadrul celui de-al treilea submeniu si gestioneaza 
    modul in care este prezentata inmultirea unui numar intr-o baza oarecare cu o cifra
    '''
    print("Introduceti baza in care doriti sa efectuati operatia (intreg din [2, 16]):") 
    baza = read_base()    
    n1 = input("Introduceti numarul de inmultit:\n>")
    n1 = make_int_list(n1)
    validate(n1, baza)
    cif = input("Introduceti o cifra din baza "+ str(baza)+ ":\n>")
    cif = make_int_list(cif)
    validate(cif, baza)
    if len(cif) > 1:
        raise InputException("Ati introdus o cifra incorecta!")
    n1 = Number(n1, baza)
    print(str(n1)+" * "+str(Number(cif, baza))+" = "+str(n1.mul(cif[0])) + "\n")
     
def sub_menu_4():
    '''
    Realizeaza interfata cu uilizatorul in cadrul submeniului 4 si gestioneaza 
    modul in care este prezentata impartirea unui numar intr-o baza oarecare cu o cifra
    '''
    print("Introduceti baza in care doriti sa efectuati operatia (intreg din [2, 16]):") 
    baza = read_base()
    n1 = input("Introduceti numarul de impartit:\n>")
    n1 = make_int_list(n1)
    validate(n1, baza)
    cif = input("Introduceti o cifra din baza "+ str(baza)+ ":\n>")
    cif = make_int_list(cif)
    validate(cif, baza)
    if len(cif) > 1:
        raise InputException("Ati introdus o cifra incorecta!")
    n1 = Number(n1, baza)
    print(str(n1)+" : "+str(Number(cif, baza))+" = "+str(n1.div(cif[0])) + " rest "+ str(n1.mod(cif[0]))+ "\n")

def sub_menu_5():
    '''
    Realizeaza interfata cu uilizatorul in cadrul submeniului 5 si gestioneaza 
    modul in care este prezentata coversia unui numar dintr-o baza oareacare intr-o alta baza 
    oarecare folosind o alta baza intermerdiara
    '''
    print("Introduceti baza numarului de convertit: ")
    baza1 = read_base()
    n1 = input("Introduceti numarul:\n>")
    n1 = make_int_list(n1)
    validate(n1, baza1)
    print("Introduceti baza destinatie: ")
    baza2 = read_base()
    print("Introduceti baza intermerdiara: ")
    baza_inter = read_base()
    n1 = Number(n1, baza1)
    n1_conversion = n1.conversie(baza_inter)
    n2 = n1_conversion[0]
    if baza1 <= baza_inter: afisare_procedeu_substitutie(n1, baza1, baza_inter)
    else: afisare_procedeu_impartire(n1, baza1, baza_inter)
    if baza_inter <= baza2: afisare_procedeu_substitutie(n2, baza_inter, baza2)
    else: afisare_procedeu_impartire(n2, baza_inter, baza2)
    
def sub_menu_6():
    '''
    Realizeaza interfata cu uilizatorul in cadrul submeniului 6 si gestioneaza 
    modul in care sunt prezentate conversiile rapide intre bazele 2, 4, 8 sau 16
    '''
    domeniu = [2, 4, 8, 16]
    print("Introduceti baza numarului de convertit(2, 4, 8 sau 16): ")
    baza1 = read_base()
    if not baza1 in domeniu:
        raise InputException("Baza trebuie sa fie o putere a lui 2")
    n1 = input("Introduceti numarul:\n>")
    n1 = make_int_list(n1)
    validate(n1, baza1)
    n1 = Number(n1, baza1)
    if baza1 == 2:
        print("Introduceti baza destinatie(4, 8 sau 16): ")
        baza2 = read_base()
        if not baza2 in domeniu:
            raise InputException("Baza trebuie sa fie o putere a lui 2")
        print(n1, "=", n1.conv_rapide(baza2)[1]+"("+str(baza1)+")", "=", n1.conv_rapide(baza2)[0])
    else: 
        baza2 = 2
        n2 = n1.conversie(2)[0]
        print(n1, "=", n1.conv_rapide(baza2)[1]+"("+str(baza1)+")", "=", 
              n2.conv_rapide(baza1)[1]+"("+str(baza2)+")", "=", n1.conv_rapide(baza2)[0])
    
def sub_menu_7():
    '''
    Realizeaza interfata cu uilizatorul in cadrul submeniului 7 si gestioneaza 
    modul in care este prezentata conversia unui numar dintr-o baza oarecare intr-o alta 
    baza folosind, dupa caz, conversia prin substituie sau conversia prin imaprtirii succesive
    '''
    print("Introduceti baza numarului de convertit: ")
    baza1 = read_base()
    n1 = input("Introduceti numarul:\n>")
    n1 = make_int_list(n1)
    validate(n1, baza1)
    print("Introduceti baza destinatie: ")
    baza2 = read_base()
    n1 = Number(n1, baza1)
    if baza1 <= baza2: afisare_procedeu_substitutie(n1, baza1, baza2)
    else: afisare_procedeu_impartire(n1, baza1, baza2)

def menu():
    '''
    Afiseaza meniul principal
    '''
    print("Meniu: ")
    print("      0 < - > Iesire")
    print("      1 < - > Aduna 2 numere intr-o baza oarecare")
    print("      2 < - > Scade 2 numere intr-o baza oarecare")
    print("      3 < - > Inmulteste un numar intr-o baza oarecare cu o cifra")
    print("      4 < - > Imparte un numar intr-o baza oarecare cu o cifra")
    print("      5 < - > Converteste un numar utilizand o baza intermediara")
    print("      6 < - > Conversii rapide")
    print("      7 < - > Converteste un numar intr-o baza oarecare")
    
def run():
    '''
    Gestionaza in mare parte interactiunea cu utilizatorul in cadrul consolei prin 
    folosirea unui ciclu repetitiv si a unui dicitionar de comenzi
    '''
    cmd = {"1": sub_menu_1, "2": sub_menu_2, "3": sub_menu_3, "4": sub_menu_4,
           "5": sub_menu_5, "6": sub_menu_6, "7": sub_menu_7}
    print('''
    ==============================================
    =Nume: Adam Horea-Marius                     =
    =Grupa: 211                                  =
    =Specializare: Informatica Romana, anul I    =
    ==============================================
        ''')
    while True:
        try:
            menu()
            c = input("Introduceti optiunea: ")
            if c == "0":
                print("Iesire...")
                break
            option = cmd[c]
            option()
        except KeyError: print("Optiune incorecta! Incercati din nou!\n")
        except InputException as ie: print(ie, "\n")
        except ZeroDivisionError as ze: print(ze)
        except: print("A aparut o eroare neasteptata! Va rog incercati din nou!\n")
run()
