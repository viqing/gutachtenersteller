def writeReport():
    import createStaticMap
    from latexWriter import texWriter

    #setup dict for main object
    mo_dict = {}
    mo_dict['street'] = 'Langstrasse 1234'
    mo_dict['br_mo'] = '2000'
    mo_dict['ext_mo'] = '400'
    mo_dict['net_mo'] = '1600'
    mo_dict['m2_pa'] = '322'
    mo_dict['plz_city'] = '8004, Zürich'
    mo_dict['d_school'] = 'Langstrasse 1234'
    mo_dict['d_shop'] = 'Langstrasse 1234'
    mo_dict['d_fun'] = 'Langstrasse 1234'
    mo_dict['d_public'] = 'Langstrasse 1234'
    mo_dict['rooms'] = '4.0'
    mo_dict['size'] = '120m2'
    mo_dict['bath'] = '1 Bad/WC'
    mo_dict['kitchen'] = 'Offen'
    mo_dict['balkon'] = 'Vorhanden'
    mo_dict['lift'] = 'Vorhanden'
    mo_dict['floor'] = '4. OG'
    mo_dict['year'] = '1971'

    vo_dicts = createDictForObjects()

    f = open('py2texTest2.tex', 'w')
    writer = texWriter()
    #import necessary packages into the tex file
    writer.setupTexFilePackages(f)
    writer.writeTitlePage(f, mo_str='Langstrasse 123', mo_plz='8004', mo_rooms='4.0', mo_city='Zürich')
    writer.writeHOTablePage(f, mo_dict)
    writer.writeHOMacroPage(f, createStaticMap.createStaticHOMap(zoom='14', exportedImgName='ho-makro.jpg'))
    writer.writeHOMikroPage(f, createStaticMap.createStaticHOMap(zoom='18', exportedImgName='ho-mikro.jpg'))

    #@TODO diese Seiten müssen noch gefinisht werden
    writer.writeCompareGraph(f, mo_dict, vo_dicts)
    
    #
    vo_dict_5bin = {}
    bin_counter = 1
    vo_dict_5bin[str(bin_counter)] = {}
    for i, obj in enumerate(vo_dicts):
        vo_dict_5bin[str(bin_counter)][obj] = vo_dicts[obj]
        if (i+1)%5==0 and (i+1)!=len(vo_dicts):
            bin_counter += 1
            vo_dict_5bin[str(bin_counter)] = {}

    #LOOP THROUGH VO_DICT_BIN TODO
    for bin_key, bin_dict in vo_dict_5bin.items():
        writer.writeCompareTable(f, mo_dict, bin_dict, bin_key, len(vo_dict_5bin)) 

    for vo_key, vo_dict in vo_dicts.items():
        search_string = ','.join ((vo_dict['street'], vo_dict['plz'], vo_dict['city']))
        search_string = search_string.replace('ä','ae')
        search_string = search_string.replace('ü','ue')
        search_string = search_string.replace('ö','oe')
        search_string = search_string.replace('è','e')
        search_string = search_string.replace('é','e')
        search_string = search_string.replace('Ă¨','e')
        search_string = search_string.replace(' ','+')
        writer.writeVOMacroPage(f, mo_dict, vo_dict, createStaticMap.createStaticVOMakroMap(address2=search_string, exportPath=vo_key))
        #writer.writeVOMicroPage()

    writer.endDocument(f)

def createDictForObjects(filename='output.csv'):

    import csv
    with open(filename, 'rt') as objectCsvFile:
        reader = csv.reader(objectCsvFile, delimiter=',')
        headers = next(reader)
        objectsDict = {}
        for header in headers:
            objectsDict[header] = []
        for row in reader:
            for header, value in zip(headers, row):
                objectsDict[header].append(value)

    #LON AND LAT ALREADY EXIST FOR THESE OBJECTS
    dictKeys = ('street', 'br_mo', 'ext_mo', 'net_mo', 'm2_pa', 'plz', 'city', 'd_school', 'd_shop', 'd_fun', 'd_public', 'rooms', 'size', 'bath', 'kitchen', 'balkon', 'lift', 'floor', 'year', 'description')
    numberOfMaxAvailableImageLinks = sum('s_full_link' in key for key in objectsDict.keys())
    consolidatedObjectsDict = {}
    for i in range(len(objectsDict['double1group_id'])):
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))] = dict.fromkeys(dictKeys)
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['street'] = objectsDict['s_street'][i]
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['br_mo'] = objectsDict['s_grossrent'][i]
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['net_mo'] = objectsDict['s_netrent'][i]
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['ext_mo'] = str(float(objectsDict['s_grossrent'][i]) - float(objectsDict['s_netrent'][i]))
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['m2_pa'] = str(int(12.0 * float(objectsDict['s_grossrent'][i]) / float(objectsDict['s_surface_usuable'][i])))
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['plz'] = objectsDict['s_zip'][i]
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['city'] = objectsDict['s_city'][i]
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['d_school'] = 'tbd'
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['d_shop'] = 'tbd'
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['d_fun'] = 'tbd'
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['d_public'] = 'tbd'
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['rooms'] = objectsDict['s_nbrooms'][i]
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['size'] = objectsDict['s_surface_usuable'][i]
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['bath'] = 'tbd'
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['kitchen'] = 'tbd'
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['balkon'] = 'tbd'
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['lift'] = 'tbd'
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['floor'] = 'tbd'
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['year'] = objectsDict['s_construction_year'][i]
        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['description'] = ' | '.join((objectsDict['s_title'][i],objectsDict['s_description'][i]))

        consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['img'] = []
        for j in range(numberOfMaxAvailableImageLinks):
            if j==0:
                if objectsDict['s_full_link'][i] != 'NONE':
                    consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['img'].append(saveVOImageLocally(''.join(('vo_', str(i+1))), ''.join(('img-',str(j),'.png')), objectsDict['s_full_link'][i]))
            else:
                if objectsDict['_'.join(('s_full_link',str(j)))][i] != 'NONE':
                    consolidatedObjectsDict[''.join(('vo_', str(i+1)))]['img'].append(saveVOImageLocally(''.join(('vo_', str(i+1))), ''.join(('img-',str(j),'.png')), objectsDict['_'.join(('s_full_link',str(j)))][i]))

    return consolidatedObjectsDict

def saveVOImageLocally(VOName, imgName, imgURL):
    #takes in the meta-sys server link and stores the image locally
    #returns None if image cant be retrieved
    import os
    import urllib.request
    print(imgURL)
    print(os.path.join('img','vo_images', VOName, imgName))
    #create dir if path doesn't exist
    os.makedirs(os.path.dirname(os.path.join('img', 'vo_images',VOName,imgName)), exist_ok=True)
    try:
        urllib.request.urlretrieve(imgURL, os.path.join('img', 'vo_images',VOName,imgName))
    except Exception as e:
        print('Didnt work.')
        print(e)
        print('\n')
    else:
        return os.path.join('img', 'vo_images', VOName, imgName)



if __name__=="__main__":
    writeReport()
    #createDictForObjects()