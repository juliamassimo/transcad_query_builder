import csv
file = open('test_query_simple1.csv')

csvreader = csv.reader(file, delimiter=';') #put -- , delimiter=';' -- if csv file is not separated by ,

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
output_file = open("echange+transit.qry","w")
#create functions to define recurrent statements
def xmlhead():
  output_file.write('<?xml version="1.0"?>')
  output_file.write("\n")
  output_file.write("<critical_link_queries>")
  output_file.write('\n ')

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

  output_file.write('\t\t\t'+texte)

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
  output_file.write('\t\t\t'+texte1+texte2+texte3) #première sortie = il ne peut pas avoir entré ou sorti du perimètre avant

def printquerytransit(injecteur_entree,injecteur_sortie): #dernière entrée et première sortie
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
  output_file.write('\t\t\t'+texte+texte1+texte2+texte3)

def printquery_entree_connecteur(injecteur_entree, connecteur_destination):
  global entree
  ei = injecteur_entree[1]
  ci = connecteur_destination[1]
  notent = [' and not Link'+sens+'('+ej+')' for ej,sens in entree if ej != ei]
  texte = 'Link'+injecteur[2]+'('+ei+')'
  texte2 = ' and EndLink'+connecteur_destination[2]+'(' + ci + ')'
  for i in notent:
    texte = texte+i
  output_file.write('\t\t\t'+texte+texte2)

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
  output_file.write('\t\t\t'+texte1+texte2+texte3) #première sortie = il ne peut pas avoir entré ou sorti du perimètre avant

def debutquery():
  output_file.write('\n ')
  output_file.write('\t<query>')
  output_file.write('\n ')
  output_file.write("\t\t<name>"+" "+"Inj"+str(injecteur[0])+" "+"</name>")
  output_file.write('\n ')
  output_file.write("\t\t<text>")
  output_file.write('\n ')

def debutqueryt(injecteur_entree,injecteur_sortie):
  output_file.write('\n ')
  output_file.write('\t<query>')
  output_file.write('\n ')
  output_file.write("\t\t<name>"+" "+"Inj"+str(injecteur_entree[0])+"-"+"Inj"+str(injecteur_sortie[0])+" "+"</name>")
  output_file.write('\n ')
  output_file.write("\t\t<text>")
  output_file.write('\n ')

def finquery():
  output_file.write('\n ')
  output_file.write("\t\t</text>")
  output_file.write('\n ')
  output_file.write('\t</query>')
  output_file.write('\n')

def printtale():
  output_file.write('</critical_link_queries>')

########################################################################################
#assemble the different functions
xmlhead()
#for last entry in the perimeter :
for injecteur in rows:
    if injecteur[4] == '1': #Column entrée
      debutquery()
      printqueryentr(injecteur)
      finquery()
    else:
      pass
output_file.write('\n ')

#for first exit from the perimeter :
for injecteur in rows:

    if injecteur[5] == '1': #Column sortie
      debutquery()
      printquerysort(injecteur)
      finquery()
    else:
      pass
output_file.write('\n ')

#for only transit through the perimeter
for injecteur_entree in rows_entree:
  for injecteur_sortie in rows_sortie:
    debutqueryt(injecteur_entree,injecteur_sortie)
    printquerytransit(injecteur_entree,injecteur_sortie)
    finquery()
output_file.write('\n ')

printtale()
