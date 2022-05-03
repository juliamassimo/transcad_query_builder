import csv
file = open('test_query_simple1.csv')

csvreader = csv.reader(file)

headers = next(csvreader)

rows = []
rows_entree = []
rows_sortie = []
connecteur = []
entree = []
sortie = []
for row in csvreader:
  rows.append(row)
  if row[4] == '1': #entree
    rows_entree.append(row)
    entree.append((row[1],row[2]))
  elif row[5] == '1': #sortie
    rows_sortie.append(row)
    sortie.append((row[1],row[2]))
  else:
    connecteur.append(row)

file.close()

#create functions to define recurrent statements
def xmlhead():
  print('<?xml version="1.0"?>')
  print("\n")
  print("<critical_link_queries>")

def printqueryentr(injecteur):
  global entree
  global sortie
  ei = injecteur[1]
  notent = [' and not Link'+sens+'('+ej+')' for ej,sens in entree if ej != ei]
  notsort = [' and not Link'+sens+'('+sj+')' for sj,sens in sortie ]
  texte = 'Link'+injecteur[2]+'('+ei+')'
  for i in notent:
    texte = texte+i
  for i in notsort:
    texte = texte+i

  print('\t\t\t'+texte)

def printquerysort(injecteur):
  global entree
  global sortie
  si = injecteur[1]
  notent = [' and not Link'+sens+'('+ej+')' for ej,sens in entree]
  notsort = [' and not Link'+sens+'('+sj+')' for sj,sens in sortie if sj != si]
  texte1 = ''
  texte2 = ''
  texte3 = ' and Link'+injecteur[2]+'('+si+')'
  for i in notent:
    texte1 = texte1+i
  for i in notsort:
    texte2 = texte2+i
  texte1 = texte1[5:]
  print('\t\t\t'+texte1+texte2+texte3) #première sortie = il ne peut pas avoir entré ou sorti du perimètre avant

def printquerytransit(injecteur_entree,injecteur_sortie): #dernière entrée et dernière sortie
  global entree
  global sortie
  ei = injecteur_entree[1]
  si = injecteur_sortie[1]
  notent = [' and not Link' + sens + '(' + ej + ')' for ej, sens in entree if ej != ei]
  notsort = [' and not Link' + sens + '(' + sj + ')' for sj, sens in sortie if sj != si]
  texte1 = ''
  texte2 = ''
  texte3 = ' and Link' + injecteur_sortie[2] + '(' + si + ')'
  texte = 'Link' + injecteur_entree[2] + '(' + ei + ')'
  for i in notent:
    texte1 = texte1 + i
  for i in notsort:
    texte2 = texte2 + i
  print('\t\t\t'+texte+texte1+texte2+texte3)

def printquery_entree_connecteur(injecteur_entree, connecteur_destination):
  global entree
  ei = injecteur_entree[1]
  ci = connecteur_destination[1]
  notent = [' and not Link'+sens+'('+ej+')' for ej,sens in entree if ej != ei]
  texte = 'Link'+injecteur[2]+'('+ei+')'
  texte2 = ' and EndLink'+connecteur_destination[2]+'(' + ci + ')'
  for i in notent:
    texte = texte+i
  print('\t\t\t'+texte+texte2)

def printquery_connecteur_sortie(connecteur_origine, injecteur_sortie):
  global sortie
  si = injecteur_sortie[1]
  ci = connecteur_origine[1]
  notsort = [' and not Link'+sens+'('+sj+')' for sj,sens in sortie if sj != si]
  texte1 = 'StartLink'+connecteur_origine[2]+'(' + ci + ')'
  texte2 = ''
  texte3 = ' and Link'+injecteur_sortie[2]+'('+si+')'
  for i in notsort:
    texte2 = texte2+i
  print('\t\t\t'+texte1+texte2+texte3) #première sortie = il ne peut pas avoir entré ou sorti du perimètre avant

def debutquery():
  print('\t<query>')
  print("\t\t<name>"+" "+"Inj"+str(injecteur[0])+" "+"<\\name>")
  print("\t\t<text>")

def debutqueryt(injecteur_entree,injecteur_sortie):
  print('\t<query>')
  print("\t\t<name>"+" "+"Inj"+str(injecteur_entree[0])+"-"+"Inj"+str(injecteur_sortie[0])+" "+"<\\name>")
  print("\t\t<text>")

def finquery():
  print("\t\t<\\text>")
  print('\t<\\query>')
  print('\n')

def printtale():
  print('<\\critical_link_queries>')

########################################################################################
#assemble the different functions
#for last entry in the perimeter :
xmlhead()
for injecteur in rows:
    if injecteur[4] == '1': #Column entrée
      debutquery()
      printqueryentr(injecteur)
      finquery()
    else:
      pass
printtale()
print('\n ******************************end of file*********************************')
print('\n ')

#for first exit from the perimeter :
xmlhead()
for injecteur in rows:

    if injecteur[5] == '1': #Column sortie
      debutquery()
      printquerysort(injecteur)
      finquery()
    else:
      pass
printtale()
print('\n ******************************end of file*********************************')
print('\n ')

#for only transit through the perimeter
xmlhead()
for injecteur_entree in rows_entree:
  for injecteur_sortie in rows_sortie:
    debutqueryt(injecteur_entree,injecteur_sortie)
    printquerytransit(injecteur_entree,injecteur_sortie)
    finquery()
printtale()
print('\n ******************************end of file*********************************')
print('\n ')

#for O-D entry
xmlhead()
for injecteur_entree in rows_entree:
  for connecteur_destination in connecteur:
    debutqueryt(injecteur_entree,connecteur_destination)
    printquery_entree_connecteur(injecteur_entree,connecteur_destination)
    finquery()
printtale()
print('\n ******************************end of file*********************************')
print('\n ')

#for O-D exit
xmlhead()
for injecteur_sortie in rows_sortie:
  for connecteur_origine in connecteur:
    debutqueryt(connecteur_origine, injecteur_sortie)
    printquery_connecteur_sortie(connecteur_origine, injecteur_sortie)
    finquery()
printtale()
print('\n ******************************end of file*********************************')
print('\n ')