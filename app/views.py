from django.http import Http404 ,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from .form import ServiceForm,IntForm,FloatForm,StringForm
from .models import Services,MetaData, Int,Float, String,Date,semantic_rules
from django.db.models.query_utils import Q
from django.core.mail import mail_admins
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core.files.base import ContentFile
# Create your views here.
from django.http import HttpResponse
from django.core.mail import send_mail
import csv
import pandas as pd
import numpy as np
import re
import os
import xml.etree.ElementTree as et
from collections import defaultdict
import json
import zipfile
from PIL import Image
from PIL.ExifTags import TAGS
from io import BytesIO
import datetime
from io import StringIO
def extract(fichier):
    data = []
    with zipfile.ZipFile(fichier, "r") as f:
    #boucler sur le contenu
        for name in f.namelist():
        #lire le contenu
            d = []
            #name
            d.append(name)
            #extension
            ext = name.split('.')[-1]
            d.append(ext)
            image_data = f.read(name)
            image = Image.open(BytesIO(image_data))

            #extraire metadata
            exif_data = image.getexif()
            width, height = image.size
            #height width
            d.append(height)
            d.append(width)
            out = BytesIO()
            image.save(out, format=image.format)
            taille = round(out.tell()/1024,2)
            #size
            d.append(taille)
            values = f.getinfo(name).date_time
            newdate = datetime.datetime(*map(int, values))
            #date creation
            d.append(newdate)
            #datemod
            d.append(datetime.datetime.now())  
            #datemod is today
            #lastly
            data.append(d)
    df = pd.DataFrame(data, columns = ['Name', 'format','hauteur','largeur','taille','date_creation','date_modification'])
    return df
def flatten_json(nested_json, exclude=['']):
    out = {}

    def flatten(x, name='', exclude=exclude):
        if type(x) is dict:
            for a in x:
                if a not in exclude: flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out

def flatten_xml(node, key_prefix=()):
    """
    Walk an XML node, generating tuples of key parts and values.
    """

    # Copy tag content if any
    text = (node.text or '').strip()
    if text:
        yield key_prefix, text

    # Copy attributes
    for attr, value in node.items():
        yield key_prefix + (attr,), value

    # Recurse into children
    for child in node:
        yield from flatten_xml(child, key_prefix + (child.tag,))


def dictify_key_pairs(pairs, key_sep='.'):
    """
    Dictify key pairs from flatten_xml, taking care of duplicate keys.
    """
    out = {}

    # Group by candidate key.
    key_map = defaultdict(list)
    for key_parts, value in pairs:
        key_map[key_sep.join(key_parts)].append(value)

    # Figure out the final dict with suffixes if required.
    for key, values in key_map.items():
        if len(values) == 1:  # No need to suffix keys.
            out[key] = values[0]
        else:  # More than one value for this key.
            for suffix, value in enumerate(values, 1):
                out[f'{key}{key_sep}{suffix}'] = value

    return out







def evaluer(request):
    form=ServiceForm()
    col_names = []
    sheets = []
    nbli = 0
    if request.method=='POST':
        #get the file
        form=ServiceForm(request.POST , request.FILES)
        if form.is_valid() :
            #read the file
            paramFile=request.FILES['fichier']
            if re.search('.zip',str(paramFile)):
                #save the zip file and send to new page (create 3 for each type) hare we create a form of metadata (of said type) then evaluate 
                my_file =  Services.objects.create(nom=request.POST.get('nom'),domaine=request.POST.get('domaine'),nblignes=0,nbcolonnes=0,fichier=paramFile)
                request.session['fileID'] = my_file.id
                return redirect('http://127.0.0.1:8000/multimedia/')

            if re.search('.csv',str(paramFile)):
                df = pd.read_csv(paramFile,error_bad_lines=False, warn_bad_lines=True)
                df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
                col_names = list(df.columns)
                nbli = len(df.index)
                #save to database
            elif re.search('.xml',str(paramFile)):
                tree = et.parse(paramFile).iter()
                rows = [dictify_key_pairs(flatten_xml(row)) for row in tree]
                df = pd.DataFrame(rows)
                df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
                col_names = list(df.columns)
                nbli = len(df.index)
            elif re.search('.json',str(paramFile)):
                this_dict = json.load(paramFile)
                df = pd.DataFrame([flatten_json(x) for x in this_dict[list(this_dict.keys())[0]]])
                df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
                col_names = list(df.columns)
                nbli = len(df.index)
            my_file =  Services.objects.create(nom=request.POST.get('nom'),domaine=request.POST.get('domaine'),nblignes=nbli,nbcolonnes=len(col_names),fichier=paramFile)
            #save the file to session
            request.session['fileID'] = my_file.id
            request.session['col_names'] = col_names
            #send to another page
            return redirect('http://127.0.0.1:8000/parametrage/')

    else:
        form=ServiceForm()

    return render(request,'app/evaluer.html',{'form':form})


def multimedia(request):
    file_id = request.session['fileID']
    return render(request,'app/multimedia.html')

def display(request):
    file_id = request.session['fileID']
    fich = Services.objects.get(pk=file_id)
    if re.search('.csv',str(fich.fichier)):
        df = pd.read_csv(fich.fichier,error_bad_lines=False, warn_bad_lines=True)
        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    elif re.search('.xml',str(fich.fichier)):
        tree = et.parse(fich.fichier).iter()
        rows = [dictify_key_pairs(flatten_xml(row)) for row in tree]
        df = pd.DataFrame(rows)
        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    elif re.search('.json',str(fich.fichier)):
        this_dict = json.load(fich.fichier)
        df = pd.DataFrame([flatten_json(x) for x in this_dict[list(this_dict.keys())[0]]])
        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    elif re.search('.zip',str(fich.fichier)):
        df = extract(fich.fichier)
    
    geeks_object = df.to_html()
    return HttpResponse(geeks_object)

def dimensionss(request):
    file_id = request.session['fileID']
    if request.method=='POST':
        rules = []
        request.session['formatss'] = request.POST.getlist('format')
        
        #exact
        request.session['hauteurmin'] = request.POST.get('hauteurmin')
        request.session['hauteurmax'] = request.POST.get('hauteurmax')
        
        #exact
        request.session['largeurmin'] = request.POST.get('largeurmin')
        request.session['largeurmax'] = request.POST.get('largeurmax')
        
        #exact
        request.session['taillemin'] = request.POST.get('taillemin')
        request.session['taillemax'] = request.POST.get('taillemax')
        
        #exact
        request.session['datecmin'] = request.POST.get('datecmin')
        request.session['datecmax'] = request.POST.get('datecmax')
        
        #exact
        request.session['datemin'] = request.POST.get('datemin')
        request.session['datemax'] = request.POST.get('datemax')
        

    return render(request,'app/dimensionss.html')

def evalMul(request):
    file_id = request.session['fileID']
    obj = Services.objects.get(pk=file_id)
    dimeC = 0
    dimeE = 0
    dimeV = 0
    dimeU = 0
    #nom type regle
    if request.method=='POST':
         #enregistrer les regles semaniques ici
        dim = request.POST.getlist('type')
        seuC = request.POST.get('poids1')
        seuE = request.POST.get('poids2')
        seuV = request.POST.get('poids3')
        seuU = request.POST.get('poids4')
        for t in dim:
            if t == 'comp':
                dimeC = 1
            if t == 'Exactitude':
                dimeE = 1
            if t == 'Vali':
                dimeV = 1
            if t == 'cohh':
                dimeU = 1
    
    valErr = []
    exactErr = []
    complErr = []
    coErr = []
    val = 0
    coh = 0
    comp = 0
    exa = 0
    data = []
    with zipfile.ZipFile(obj.fichier, "r") as f:
    #boucler sur le contenu
        for name in f.namelist():
        #lire le contenu
            d = []
            #name
            d.append(name)
            #extension
            ext = name.split('.')[-1]
            d.append(ext)
            image_data = f.read(name)
            image = Image.open(BytesIO(image_data))

            #extraire metadata
            exif_data = image.getexif()
            width, height = image.size
            #height width
            d.append(height)
            d.append(width)
            out = BytesIO()
            image.save(out, format=image.format)
            taille = round(out.tell()/1024,2)
            #size
            d.append(taille)
            values = f.getinfo(name).date_time
            newdate = datetime.datetime(*map(int, values))
            #date creation
            d.append(newdate)
            #datemod
            d.append(datetime.datetime.now())  
            #datemod is today
            #lastly
            data.append(d)
    df = pd.DataFrame(data, columns = ['Name', 'format','hauteur','largeur','taille','date_creation','date_modification'])
    

    formatss = request.session['formatss']


    hauteurmin = request.session['hauteurmin']
    hauteurmax = request.session['hauteurmax']

    largeurmin = request.session['largeurmin']
    largeurmax = request.session['largeurmax']
    taillemin = request.session['taillemin']
    taillemax = request.session['taillemax']
    datecmin = request.session['datecmin']
    datecmax = request.session['datecmax']
    datemin = request.session['datemin']
    datemax = request.session['datemax']
    with zipfile.ZipFile(obj.fichier, "r") as f:
        index = 0 
        nbelem = len(f.namelist())
        for name in f.namelist():
        #lire le contenu
            #extension
            ext = image.format
            if formatss:
                if ext not in formatss:
                    val+=1
                    valErr.append(index)
        
            image_data = f.read(name)
            image = Image.open(BytesIO(image_data))
            #height width
            exif_data = image.getexif()
            width, height = image.size
            if hauteurmin:
                if int(hauteurmin)>height:
                    exa +=1
                    exactErr.append(index)
            if hauteurmax:
                if height>int(hauteurmax):
                    exa +=1
                    exactErr.append(index)
            if largeurmin:
                if int(largeurmin)>width:
                    exa +=1
                    exactErr.append(index)
            if largeurmax:
                if width>int(largeurmax):
                    exa +=1
                    exactErr.append(index)
           
                #size
            out = BytesIO()
            image.save(out, format=image.format)
            taille = round(out.tell()/1024,2)
            if taille == 0:
                comp +=1
                complErr.append(index)

            if taillemin != '':
                if float(taillemin)>taille:
                    exa +=1
                    exactErr.append(index)
            if taillemax:
                if taille>float(taillemax):
                    exa +=1
                    exactErr.append(index)
           
            
                #date creation
            values = f.getinfo(name).date_time
            datec = str(datetime.datetime(*map(int, values)).date())


            if datecmin:
                if datetime.datetime.strptime(datecmin, '%Y-%m-%d').date() > datetime.datetime.strptime(datec, '%Y-%m-%d').date():
                    exa +=1
                    exactErr.append(index)
                
            if datecmax:
                if datetime.datetime.strptime(datecmax, '%Y-%m-%d').date() < datetime.datetime.strptime(datec, '%Y-%m-%d').date():
                    exa +=1
                    exactErr.append(index)
            
            
                #datemod
            datem = str(datetime.datetime.now().date())
            if datemin:
                if datetime.datetime.strptime(datemin, "%Y-%m-%d").date()>datem:
                    exa +=1
                    exactErr.append(index)
            if datemax:
                if datem>datetime.datetime.strptime(datemax, "%Y-%m-%d").date():
                    exa +=1
                    exactErr.append(index)
              
            if datec > datem:
                coh +=1
                coErr.append(index)
            index +=1
    exactErr = list(dict.fromkeys(exactErr))
    coh = round(100-(coh/nbelem)*100,2)
    val = round(100-(val/nbelem)*100,2)
    comp = round(100-(comp/nbelem)*100,2)
    exa = round(100-(exa/nbelem)*100,2)
    request.session['valErr'] = valErr
    request.session['exactErr'] = exactErr
    request.session['complErr'] = complErr
    request.session['coErr'] = coErr
    context = {
        'nbelem' : nbelem,
        'valErr' : len(valErr),
        'exactErr' : len(exactErr),
        'complErr' : len(complErr),
        'coErr' : len(coErr),
        'coh' : coh,
        'val' : val,
        'comp' : comp,
        'exa' : exa,
        'seuC' : seuC,
        'seuE' : seuE,
        'seuV' : seuV,
        'seuU' : seuU,
        'dimeE' : dimeE,
        'dimeC' : dimeC,
        'dimeV' : dimeV,
        'dimeU' : dimeU,

    }


    return render(request,'app/evalMul.html',context)

def mulamelioration(request):
    if request.method=='POST':
        request.session['ver'] = request.POST.get('ver')
        request.session['format'] = request.POST.get('format')
        request.session['nulles'] = request.POST.get('nulles')
        request.session['doub'] = request.POST.get('doub')
        return redirect('http://127.0.0.1:8000/downloadmul/')

    return render(request,'app/mulamelioration.html')


def downloadmul(request):
    return render(request,'app/downloadmul.html')



def downloadZIP(request):
    file_id = request.session['fileID']
    obj = Services.objects.get(pk=file_id)
    ver = request.session['ver']
    format = request.session['format']
    nulles = request.session['nulles']
    doub = request.session['doub']

    valErr = request.session['valErr']
    valErr = list(dict.fromkeys(valErr))
    exactErr = request.session['exactErr']
    exactErr = list(dict.fromkeys(exactErr))
    complErr = request.session['complErr']
    complErr = list(dict.fromkeys(complErr))
    coErr = request.session['coErr']
    coErr = list(dict.fromkeys(coErr))


    df = extract(obj.fichier)

    if(ver=='vs1'):
        df.drop(exactErr, inplace=True,errors='ignore')
    if(format=='f1'):
        df.drop(valErr, inplace=True,errors='ignore')
    if(nulles=='v1'):
        df.drop(complErr, inplace=True,errors='ignore')
    if(doub=='d1'):
        df.drop(coErr, inplace=True,errors='ignore')


    response =  HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename = data.csv'
    df.to_csv(path_or_buf=response,index=False)

    return response










def parametrage(request):
    col_names = request.session['col_names']
    return render(request,'app/parametrage.html',{'colmn_names':col_names})


#this is the function
def param2(request):
    file_id = request.session['fileID']
    form1=IntForm(request.POST)
    form2=FloatForm(request.POST)
    form3=StringForm(request.POST)
    colmn_names = request.session['col_names']
    champ=[]
    ids = []
    if request.method=='POST':
        poids = request.POST.getlist('poids')
        for col,p in zip(colmn_names,poids):
            chType = request.POST.get(col)
            champ.append(chType)
            obj = Services.objects.get(pk=file_id)
            md = MetaData.objects.create(nom_attribut=col,type_attribut=chType,poids=int(p) if p!="" else 1,Fichier_source=obj)
            ids.append(md.id)
    request.session['MDID'] = ids
    context={'list2': colmn_names,'champ' : champ,'form1' : form1,'form2' : form2, 'form3' : form3}
    return render(request,'app/param2.html',context)

def param4(request):
    ids = request.session['MDID']
    colmn_names = request.session['col_names']
    form1=IntForm(request.POST)
    form2=FloatForm(request.POST)
    form3=StringForm(request.POST)
    if request.method=='POST':
        regexList = request.POST.getlist('Expression_Reguliere')
        lenMinList = request.POST.getlist('longeur_min')
        lenMaxList = request.POST.getlist('longeur_max')
        IValMinList = request.POST.getlist('IVal_Min')
        IValMaxList = request.POST.getlist('IVal_Max')
        FValMinList = request.POST.getlist('FVal_Min')
        FValMaxList = request.POST.getlist('FVal_Max')
        i=0
        f=0
        s=0
        info=[]
        for id in ids:
            if form1.is_valid():
            #the integer form
                obj = MetaData.objects.get(pk=id)
                if (obj.type_attribut=='int'):
                    instance=Int.objects.create(IVal_Min=int(IValMinList[i]) if IValMinList[i]!="" else 0,IVal_Max=int(IValMaxList[i]) if IValMinList[i]!="" else 0,MetaData=obj)
                    info.append([obj.nom_attribut,obj.type_attribut,instance.IVal_Min,instance.IVal_Max])
                    i+=1
            if form2.is_valid():
            #the float form
                obj = MetaData.objects.get(pk=id)
                if (obj.type_attribut=='float'):
                    instance=Float.objects.create(FVal_Min=float(FValMinList[f]) if FValMinList[f]!="" else 0.0,FVal_Max=float(FValMaxList[f])  if FValMinList[f]!="" else 0.0,MetaData=obj)
                    info.append([obj.nom_attribut,obj.type_attribut,instance.FVal_Min,instance.FVal_Max])
                    f+=1
            if form3.is_valid():
            #the string form
                obj = MetaData.objects.get(pk=id)
                if (obj.type_attribut=='string'):
                    instance=String.objects.create(Expression_Reguliere=regexList[s] if regexList[s]!="" else ".+",longeur_min=int(lenMinList[s]) if lenMinList[s]!="" else 1,longeur_max=int(lenMaxList[s]) if lenMinList[s]!="" else 1,MetaData=obj)
                    info.append([obj.nom_attribut,obj.type_attribut,instance.Expression_Reguliere,instance.longeur_min,instance.longeur_max])
                    s+=1
#we send col names and ids here for evaluation
    request.session['info']= info
    context={'col_ids' : ids, 'col_names' : colmn_names}
    return render(request,'app/param4.html',context)

def choix_type(request):
    file_id = request.session['fileID']
    colmn_names = request.session['col_names']
    #nom type regle
    info= request.session['info']
    if request.method=='POST':
         #enregistrer les regles semaniques ici
        att1 = request.POST.getlist('col1')
        oper = request.POST.getlist('op')
        att2 = request.POST.getlist('col2')
        for le in range(len(oper)):
            obj1 = MetaData.objects.get(pk=att1[le])
            obj2 = MetaData.objects.get(pk=att2[le])
            instance=semantic_rules.objects.create(rule=oper[le],attribut1=obj1,attribut2=obj2)
    return render(request,'app/choix_type.html')

def param3(request):
    file_id = request.session['fileID']
    colmn_names = request.session['col_names']
    dimeC = 0
    dimeE = 0
    dimeV = 0
    dimeU = 0
    #nom type regle
    if request.method=='POST':
         #enregistrer les regles semaniques ici
        dim = request.POST.getlist('type')
        seuC = request.POST.get('poids1')
        seuE = request.POST.get('poids2')
        seuV = request.POST.get('poids3')
        seuU = request.POST.get('poids4')
        for t in dim:
            if t == 'comp':
                dimeC = 1
            if t == 'Exactitude':
                dimeE = 1
            if t == 'Vali':
                dimeV = 1
            if t == 'Unic':
                dimeU = 1


#regex duplicates format type range nullvalues semanticrules
    #get the file
    fich = Services.objects.get(pk=file_id)
    #get the metadata of the file
    mtlist = MetaData.objects.filter(Fichier_source=fich)
    #read the file

    if re.search('.csv',str(fich.fichier)):
        df = pd.read_csv(fich.fichier,error_bad_lines=False, warn_bad_lines=True)
        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    elif re.search('.xml',str(fich.fichier)):
        tree = et.parse(fich.fichier).iter()
        rows = [dictify_key_pairs(flatten_xml(row)) for row in tree]
        df = pd.DataFrame(rows)
        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    elif re.search('.json',str(fich.fichier)):
        this_dict = json.load(fich.fichier)
        df = pd.DataFrame([flatten_json(x) for x in this_dict[list(this_dict.keys())[0]]])
        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    #count rows
    nbrows=len(df.index)
    #count columns
    nbcol = len(df. columns)
    #for number of errors
    errors_list = []
    format_errors = []
    type_errors = []
    range_errors = []
    semantic_errors = []

    #for error index
    id_errors_list = []
    id_format_errors = []
    id_type_errors = []
    id_range_errors = []
    id_semantic_errors = []
    #for each column append 0
    for z in range(nbcol):
        errors_list.append(0)
    for z in range(nbcol):
        format_errors.append(0)
    for z in range(nbcol):
        type_errors.append(0)
    for z in range(nbcol):
        range_errors.append(0)
    for z in range(nbcol):
        semantic_errors.append(0)
    #elements
    errors_listt = []
    type_errorst = []
    range_errorst = []
    for z in range(nbcol):
        errors_listt.append(0)
    for z in range(nbcol):
        type_errorst.append(0)
    for z in range(nbcol):
        range_errorst.append(0)

    # for each column count the number of errors and append them to the index of each column 
    #rows
    for rows in range(len(df.index)):
        #somme des poids
        sp = 0
        poids = []
        #for cell
        for index,row in zip(range(nbcol), df.loc[rows]):
            sp = sp + mtlist[index].poids
            poids.append(mtlist[index].poids)
            if row:
                if mtlist[index].type_attribut=='string':
                    if(isinstance(row, str)):
                        
                        rules = String.objects.filter(MetaData=mtlist[index]).first()

                        if (not (re.match(rules.Expression_Reguliere,row))):
                            errors_listt[index]+=1
                            errors_list[index] = errors_list[index]+ 1
                            id_errors_list.append(rows)
                        if (len(row)<rules.longeur_min or len(row)>rules.longeur_max):
                            range_errorst[index] +=1
                            range_errors[index]= range_errors[index]+ 1
                            id_range_errors.append(rows)
                    else:
                        type_errorst[index] +=1
                        type_errors[index]= type_errors[index]+ 1
                        id_type_errors.append(rows) 

                if mtlist[index].type_attribut=='int':
                    if isinstance(row, np.integer):
                        rules = Int.objects.filter(MetaData=mtlist[index]).first()
                        if (int(row)<rules.IVal_Min or int(row)>rules.IVal_Max):
                            range_errorst[index] +=1
                            range_errors[index]= range_errors[index]+1
                            id_range_errors.append(rows)
                    else:
                        type_errorst[index] +=1
                        type_errors[index]=type_errors[index]+ 1
                        id_type_errors.append(rows)

                if mtlist[index].type_attribut=='float':
                    if isinstance(row, float):
                        rules = Float.objects.filter(MetaData=mtlist[index]).first()
                        if (float(row)<rules.FVal_Min or float(row)>rules.FVal_Max):
                            range_errorst[index] +=1
                            range_errors[index]= range_errors[index]+ 1
                            id_range_errors.append(rows)
                    else:
                        type_errorst[index] +=1
                        type_errors[index]= type_errors[index]+ 1
                        id_type_errors.append(rows)


    request.session['Terr'] = id_type_errors
    request.session['Rerr'] = id_range_errors
    request.session['Serr'] = id_errors_list

    #errors_list = []
    #range_errors = []
    #regex 

    exact =  round(100-sum(errors_list)/(nbrows*nbcol)*100,2)

    # format_errors = []
    # type_errors
    #format et types
    valid = 0
    for m in type_errorst:
        valid=valid+(m)
    valid = round(100-(valid)/(nbrows*nbcol)*100,2)


    #doublants
    uniq = 0
    dupes = df.duplicated().sum()
    uniq =  round(100-(dupes/nbrows)*100,2)


    #nulles
    comp = 0
    missin_values = df.isnull().sum()
    for m in missin_values:
        comp=comp+(m)
    comp = round(100-(comp/(nbrows*nbcol)*100),2)


    # semantic_errors = []
    coherence =0
#add percentages and seuille and dimension choices
    context = {
        'nbcol': nbcol,
        'nbrows': nbrows,
        'colnames' : list(colmn_names),
        'nullvals':missin_values.sum(),
        'missin_values' : list(missin_values),
        'nbdups' : dupes,
        'nberr' : errors_listt,
        'nberrr' : sum(errors_listt),
        'nterr' : sum(type_errorst),
        'terr' : type_errorst,
        'accuracy' : exact,
        'comp' : comp,
        'uniq' : uniq,
        'valid' : valid,
        'seuC' : seuC,
        'seuE' : seuE,
        'seuV' : seuV,
        'seuU' : seuU,
        'dimeE' : dimeE,
        'dimeC' : dimeC,
        'dimeV' : dimeV,
        'dimeU' : dimeU,
    }
    return render(request,'app/param3.html', context)


def catalog(request):
    file_id = request.session['fileID']
    info = request.session['info']
    comp=0
    
    datas = []
    fich = Services.objects.get(pk=file_id)
    mtlist = MetaData.objects.filter(Fichier_source=fich)
    for mt in mtlist:
        data = []
        data.append(mt.nom_attribut)
        data.append(mt.type_attribut)
        data.append(mt.poids)
        if mt.type_attribut=='int':
            rulz = Int.objects.get(MetaData=mt)
            data.append(rulz.IVal_Min)
            data.append(rulz.IVal_Max)
        if mt.type_attribut=='float':
            rulz = Float.objects.get(MetaData=mt)
            data.append(rulz.FVal_Min)
            data.append(rulz.FVal_Max)
        if mt.type_attribut=='string':
            rulz = String.objects.get(MetaData=mt)
            data.append(rulz.Expression_Reguliere)
            data.append(rulz.longeur_min)
            data.append(rulz.longeur_max)
        datas.append(list(data))
    return render(request,'app/catalog.html',{'info':info,'comp':comp,'datas': datas})



def catalog2(request):
    lst = []
    cc = []
    cols = []
    tt = 0
    file_id = request.session['fileID']
    fich = Services.objects.get(pk=file_id)
    if re.search('.csv',str(fich.fichier)):
        typed = 'structurées'
        tt = 1
    elif re.search('.json',str(fich.fichier)):
        typed = 'semi structurées'
        tt = 1
    elif re.search('.zip',str(fich.fichier)):
        typed = 'non structurées'

    if re.search('.csv',str(fich.fichier)):
        df = pd.read_csv(fich.fichier,error_bad_lines=False, warn_bad_lines=True)
        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    elif re.search('.xml',str(fich.fichier)):
        tree = et.parse(fich.fichier).iter()
        rows = [dictify_key_pairs(flatten_xml(row)) for row in tree]
        df = pd.DataFrame(rows)
        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    elif re.search('.json',str(fich.fichier)):
        this_dict = json.load(fich.fichier)
        df = pd.DataFrame([flatten_json(x) for x in this_dict[list(this_dict.keys())[0]]])
        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    if tt == 1:
        for rows in range(len(df.index)):
            for cell, col in zip(df.loc[rows],df.columns):
                cols.append(col)
                if isinstance(cell, str):
                    cc.append('string')
                if isinstance(cell, np.integer):
                    cc.append('integer')
                if isinstance(cell, float):
                    cc.append('float')
            break
    
    lst.append(fich.nom)
    lst.append(fich.domaine)
    lst.append(fich.nblignes)
    lst.append(fich.nbcolonnes)
    lst.append(fich.auteur)
    lst.append(fich.date_creation)
    context = {
        'lst': lst,
        'typed' : typed,
        'cc' : cc,
        'cols' : cols,
        'tt' : tt
    }
    return render(request,'app/catalog2.html',context)


def amelioration(request):
    if request.method=='POST':
        request.session['ver'] = request.POST.get('ver')
        request.session['pla'] = request.POST.get('pla')
        request.session['types'] = request.POST.get('types')
        request.session['nulles'] = request.POST.get('nulles')
        request.session['doub'] = request.POST.get('doub')
        request.session['rep'] = request.POST.get('rep')

        return redirect('http://127.0.0.1:8000/download/')
    return render(request,'app/amelioration.html')

def download(request):
    return render(request,'app/download.html')



def downloadCSV(request):
    file_id = request.session['fileID']
    fich = Services.objects.get(pk=file_id)
    ext = ''
    ver = request.session['ver']
    pla =  request.session['pla']
    types =  request.session['types']
    nulles = request.session['nulles']
    doub = request.session['doub']
    rep = request.session['rep'] #nulles = v3

    if re.search('.csv',str(fich.fichier)):
        ext = 'csv'
        df = pd.read_csv(fich.fichier,error_bad_lines=False, warn_bad_lines=True)
        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    elif re.search('.xml',str(fich.fichier)):
        ext = 'xml'
        tree = et.parse(fich.fichier).iter()
        rows = [dictify_key_pairs(flatten_xml(row)) for row in tree]
        df = pd.DataFrame(rows)
        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    elif re.search('.json',str(fich.fichier)):
        ext = 'json'
        this_dict = json.load(fich.fichier)
        df = pd.DataFrame([flatten_json(x) for x in this_dict[list(this_dict.keys())[0]]])
        df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    id_type_errors = request.session['Terr']
    id_type_errors = list(dict.fromkeys(id_type_errors))
    id_range_errors = request.session['Rerr']
    id_range_errors = list(dict.fromkeys(id_range_errors))
    id_errors_list = request.session['Serr']
    id_errors_list = list(dict.fromkeys(id_errors_list))

    if(ver=='vs1'):
        df.drop(id_errors_list, inplace=True,errors='ignore')

 
        
    if(pla=='pv1'):
        df.drop(id_range_errors, inplace=True,errors='ignore')





    if(types=='t1'):
        df.drop(id_type_errors, inplace=True,errors='ignore')

 

    if(nulles=='v1'):
        df.dropna( inplace=True)

    if(nulles=='v3'):
        df.fillna(value= rep, inplace=True)

    if(doub=='d1'):
        df.drop_duplicates( inplace=True)

    response =  HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename = data.csv'
    df.to_csv(path_or_buf=response,index=False)

    return response





