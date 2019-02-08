def writeReport():
    import createStaticMap
    import urllib
    import urllib.parse
    import json
    import os
    from shutil import copyfile
    from latexWriter import texWriter

    # parse arguments to check for report json file
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-j", "--json-file", dest="jsonFile", nargs='?', const="report.json", type=str,
                        help="Create report from specified json file. Defaults to report.json if no option provided.")
    args = parser.parse_args()

    # importing the mo_dict from input json file
    with open('input.json', encoding='utf-8') as fp:
                inputDict = json.load(fp)
                mo_dict = inputDict['mo']

    # create folder and file name for report
    generatedReportFilePath = ''.join((mo_dict['street'].replace(' ',''),'-GA'))
    generatedReportFileName = ''.join((mo_dict['street'].replace(' ',''),'.tex'))

    if not os.path.exists(generatedReportFilePath):
        os.makedirs(generatedReportFilePath)

    generatedReportImgDirectory = ''.join((generatedReportFilePath, '/', 'img'))
    if not os.path.exists(generatedReportImgDirectory):
        os.makedirs(generatedReportImgDirectory)

    # move logos to img folder
    copyfile('img/hwz-logo.png', ''.join((generatedReportImgDirectory, '/', 'hwz-logo.png')))
    copyfile('img/swissrei-logo.png', ''.join((generatedReportImgDirectory, '/', 'swissrei-logo.png')))

    # write sql query
    moSQLFile = writeSQLQuery(generatedReportFilePath, mo_dict)

    # parse street name of mo to create makro/mikro maps
    search_string = ','.join ((mo_dict['street'], mo_dict['plz'], mo_dict['city']))
    search_string = urllib.parse.quote_plus(search_string) #parse so urls pose no problems in browsers
    mo_dict['makro'] = createStaticMap.createStaticHOMap(address=search_string, zoom='14',exportPath=generatedReportImgDirectory, exportedImgName='ho-makro.jpg')
    mo_dict['mikro'] = createStaticMap.createStaticHOMap(address=search_string, zoom='18',exportPath=generatedReportImgDirectory, exportedImgName='ho-mikro.jpg')

    # create mo and vo dict
    if args.jsonFile:
        jsonFileName = args.jsonFile
        if not os.path.isfile(jsonFileName):
            print('Specified file doesn\'t exist.')
        else:
            with open(jsonFileName, encoding='utf-8') as fp:
                inputDict = json.load(fp)
                mo_dict = inputDict['mo']
                vo_dicts = inputDict['vo']
    else:
        # set up dict for comparable objects
        testInput = 'parsed-pyout.csv'
        vo_dicts = createVODictFromCSV(mo_dict,generatedReportImgDirectory,testInput)

    f = open(''.join((generatedReportFilePath, '/', generatedReportFileName)), 'w', encoding='utf-8')
    writer = texWriter()
    writer.setupTexFilePackages(f)
    writer.writeTitlePage(f, mo_dict)
    writer.writeTOC(f)
    writer.writeHOTablePage(f, mo_dict)
    writer.writeHOMakroPage(f, mo_dict)
    writer.writeHOMikroPage(f, mo_dict)
    writer.writeHOAdditionalImagesPage(f, mo_dict)
    writer.writeCompareGraph(f, mo_dict, vo_dicts)
    
    # Create sub-dicts of vo's with bin size of 5
    # Creates page for every new 5 objects
    vo_dict_5bin = {}
    bin_counter = 1
    vo_dict_5bin[str(bin_counter)] = {}
    for i, obj in enumerate(vo_dicts):
        vo_dict_5bin[str(bin_counter)][obj] = vo_dicts[obj]
        if (i+1)%5==0 and (i+1)!=len(vo_dicts):
            bin_counter += 1
            vo_dict_5bin[str(bin_counter)] = {}
    for bin_key, bin_dict in vo_dict_5bin.items():
        writer.writeCompareTable(f, mo_dict, bin_dict, bin_key, len(vo_dict_5bin)) 

    # Write Makro, Mikro und Additional Images Page für jedes VO
    for vo_key, vo_dict in vo_dicts.items():
        search_string = ','.join ((vo_dict['street'].split('(')[0], vo_dict['plz'], vo_dict['city']))
        search_string = (urllib.parse.quote_plus(search_string))
        writer.writeVOMacroPage(f, mo_dict, vo_dict)
        writer.writeVOMicroPage(f, vo_dict)
        writer.writeVOAdditionalImagesPage(f, vo_dict)         

    # End the Document
    writer.endDocument(f)

    # Join ho and vo dicts for xml output
    # Can later on be used to easily recreate existing reports
    joined_dict = {}
    joined_dict['mo'], joined_dict['vo'] = mo_dict, vo_dicts
    with open('report.json', 'w', encoding='utf-8') as fp:
        json.dump(joined_dict, fp, indent=4)

def createVODictFromCSV(mo_dict, generatedReportImgDirectory, filename='output.csv'):

    import csv
    with open(filename, 'rt', encoding='utf-8') as objectCsvFile:
        reader = csv.reader(objectCsvFile, delimiter=',')
        headers = next(reader)
        objectsDict = {}
        for header in headers:
            objectsDict[header] = []
        for row in reader:
            for header, value in zip(headers, row):
                objectsDict[header].append(value)

    numberOfMaxAvailableImageLinks = sum('s_full_link' in key for key in objectsDict.keys())
    consolidatedObjectsDict = {}
    for i in range(len(objectsDict['double1group_id'])):
        print("\n({}/{}) Setting up the dict and images for {}...".format(i+1, len(objectsDict['double1group_id']), objectsDict['s_street'][i]))

        new_vo = ''.join(('vo_', str(i+1)))
        consolidatedObjectsDict[new_vo] = {}
        consolidatedObjectsDict[new_vo]['street'] = objectsDict['s_street'][i]
        consolidatedObjectsDict[new_vo]['br_mo'] = objectsDict['s_grossrent'][i]
        consolidatedObjectsDict[new_vo]['net_mo'] = objectsDict['s_netrent'][i]
        consolidatedObjectsDict[new_vo]['ext_mo'] = str(int(objectsDict['s_grossrent'][i]) - int(objectsDict['s_netrent'][i]))
        consolidatedObjectsDict[new_vo]['m2_pa'] = str(int(12.0 * float(objectsDict['s_grossrent'][i]) / float(objectsDict['s_surface_usuable'][i])))
        consolidatedObjectsDict[new_vo]['plz'] = objectsDict['s_zip'][i]
        consolidatedObjectsDict[new_vo]['city'] = objectsDict['s_city'][i]
        consolidatedObjectsDict[new_vo]['lat'] = objectsDict['s_lat'][i]
        consolidatedObjectsDict[new_vo]['lon'] = objectsDict['s_lon'][i]

        import createStaticMap
        # Distances
        location = [float(objectsDict['s_lat'][i]), float(objectsDict['s_lon'][i])]
            # Distance to schools
        nearestSchool = createStaticMap.findClosestPlace(location=location, type='school')
        consolidatedObjectsDict[new_vo]['d_school'] = ''.join((str(nearestSchool['dist10m']),'m, ', str(nearestSchool['distWalkingTime']), 'min'))
            # Distance to shops
        nearestShop = createStaticMap.findClosestPlace(location=location, type='grocery_or_supermarket')
        consolidatedObjectsDict[new_vo]['d_shop'] = ''.join((str(nearestShop['dist10m']),'m, ', str(nearestShop['distWalkingTime']), 'min'))
            #tbd - distnace to naherholung
        nearestPark = createStaticMap.findClosestPlace(location=location, type='park')
        consolidatedObjectsDict[new_vo]['d_fun'] = ''.join((str(nearestPark['dist10m']),'m, ', str(nearestPark['distWalkingTime']), 'min'))
            # Distance to public transport
        nearestBusStop = createStaticMap.findClosestPlace(location=location, type='bus_station')
        consolidatedObjectsDict[new_vo]['d_public'] = ''.join((str(nearestBusStop['dist10m']),'m, ', str(nearestBusStop['distWalkingTime']), 'min'))
        # Criteria for size
        consolidatedObjectsDict[new_vo]['rooms'] = objectsDict['s_nbrooms'][i]
        consolidatedObjectsDict[new_vo]['size'] = objectsDict['s_surface_usuable'][i]
        # Criteria for Equipment
        # Available: te_a_balkon_oc,te_a_garten_oc,te_a_lift_oc,te_a_minergie_oc,te_a_ofen_oc,te_a_rollst_oc,te_a_sicht_oc,te_a_wasch_oc
        equiptmentLUT = {'-1':'Unbekannt', '0':'Nicht vorhanden', '1':'Vorhanden', '2':'Vorhanden', '3':'Vorhanden', '4':'Vorhanden', '5':'Vorhanden'}
        consolidatedObjectsDict[new_vo]['bath'] = 'tbd'
        consolidatedObjectsDict[new_vo]['kitchen'] = 'tbd'
        consolidatedObjectsDict[new_vo]['balkon'] = equiptmentLUT[objectsDict['te_a_balkon_oc'][i]]
        consolidatedObjectsDict[new_vo]['lift'] = equiptmentLUT[objectsDict['te_a_lift_oc'][i]]
        consolidatedObjectsDict[new_vo]['floor'] = objectsDict['te307o_floor_id'][i]
        # Year built
        consolidatedObjectsDict[new_vo]['year'] = objectsDict['s_construction_year'][i]
        # Description
        consolidatedObjectsDict[new_vo]['description'] = ' | '.join((objectsDict['s_title'][i],objectsDict['s_description'][i]))

        # Makro images
        # TODO implement download functions to return relative img links!!!!!!!
        import urllib
        mo_search_string = ','.join((mo_dict['street'], mo_dict['plz'], mo_dict['city']))
        mo_search_string = urllib.parse.quote_plus(mo_search_string) #parse so urls pose no problems in browsers
        search_string = ','.join ((consolidatedObjectsDict[new_vo]['street'].split('(')[0], consolidatedObjectsDict[new_vo]['plz'], consolidatedObjectsDict[new_vo]['city']))
        search_string = urllib.parse.quote_plus(search_string) #parse so urls pose no problems in browsers
        consolidatedObjectsDict[new_vo]['makro'] = createStaticMap.createStaticVOMakroMap(address1=mo_search_string, address2=search_string, exportPath=generatedReportImgDirectory, voName=new_vo)
        consolidatedObjectsDict[new_vo]['mikro'] = createStaticMap.createStaticVOMikroMap(address=search_string, exportPath=generatedReportImgDirectory, voName=new_vo)


        # Download images and saving the export path in list
        consolidatedObjectsDict[new_vo]['img'] = []
        for j in range(numberOfMaxAvailableImageLinks):
            voImgName = ''.join(('img-',str(j),'.png'))
            fullExportPath = ''.join((generatedReportImgDirectory, '/', 'vo_images', '/', new_vo, '/', voImgName))
            if j==0:
                imgURL = objectsDict['s_full_link'][i]
                if imgURL != 'NONE':
                    locallySavedImageRelativePath = saveVOImageLocally(new_vo, fullExportPath, imgURL)
                    if locallySavedImageRelativePath:
                        resizeImage(fullExportPath)
                        consolidatedObjectsDict[new_vo]['img'].append(locallySavedImageRelativePath)
            else:
                imgURL = objectsDict['_'.join(('s_full_link',str(j)))][i]
                if imgURL != 'NONE':
                    locallySavedImageRelativePath = saveVOImageLocally(new_vo, fullExportPath, imgURL)
                    if locallySavedImageRelativePath:
                        resizeImage(fullExportPath)
                        consolidatedObjectsDict[new_vo]['img'].append(locallySavedImageRelativePath)

    #Rename doppelte Strassennamen
    streetNames = list()
    objectKeys = list()
    for vo_key, vo_dict in consolidatedObjectsDict.items():
        streetNames.append(vo_dict['street'])
        objectKeys.append(vo_key)
    
    for street in streetNames:
        c = streetNames.count(street)
        if c > 1:
            idx = 1
            for i in range(len(streetNames)):
                if streetNames[i] == street:
                    streetNames[i] = ''.join((streetNames[i], ' (', str(idx), ')'))
                    idx += 1

    for vo_key, changedStreetName in zip(objectKeys, streetNames):
        consolidatedObjectsDict[vo_key]['street'] = changedStreetName

    return consolidatedObjectsDict

def saveVOImageLocally(VOName, fullExportPath, imgURL):
    #takes in the meta-sys server link and stores the image locally
    import os
    import urllib.request
    if not os.path.isfile(fullExportPath):
        os.makedirs(os.path.dirname(fullExportPath), exist_ok=True) #create dir if file doesn't exist
        try:
            urllib.request.urlretrieve(imgURL, fullExportPath)
        except Exception as e:
            print('Could not access file through link:')
            print(e)
        else:
            print('Image file for {} was downloaded as {}.'.format(VOName, fullExportPath))
            relativeImageLink = fullExportPath[fullExportPath.find('img/'):]
            return relativeImageLink
    else:
        print('File already exists for {} under {}.'.format(VOName, fullExportPath))
        relativeImageLink = fullExportPath[fullExportPath.find('img/'):]
        return relativeImageLink

def resizeImage(imageLink):
    from PIL import Image
    im = Image.open(imageLink)

    aspectRatio = im.width / im.height
    im = im.resize((int(im.height * aspectRatio), 640))
    
    im.save(imageLink)

def writeSQLQuery(targetFolder, mo_dict):
    sqlFile = ''.join((targetFolder, '/', 'sql-', mo_dict['street'].replace(' ',''),'.sql'))
    with open(sqlFile, 'w', encoding='utf-8') as fp:
        fp.write(r"""SELECT srei_ads.*,ftta_199a1_adds_housing.te_a_balkon_oc, ftta_199a1_adds_housing.te_a_lift_oc, ftta_199a1_adds_housing.te307o_floor_id, 'https://s3-eu-west-1.amazonaws.com/' || fto_199a3_images.amazonpath AS 's_full_link' """ + '\n')
        fp.write(r"""FROM srei_ads LEFT OUTER JOIN ftta_199a1_adds_housing	ON srei_ads.id = ftta_199a1_adds_housing.id LEFT OUTER JOIN fto_199a3_images ON srei_ads.id = fto_199a3_images.ft_199a3_add_housing_id""" + '\n')
        fp.write(r"""WHERE""" + '\n')
        # Bruttomiete
        fp.write(r"""srei_ads.s_zip=1004 AND""" + '\n')
        # Zimmer
        if float(mo_dict['rooms']) <= 3.0:
            fp.write(r"""srei_ads.s_nbrooms=""" + mo_dict['rooms'] + """ AND""" + '\n')
        elif float(mo_dict['rooms']) <=4.5:
            fp.write(r"""(srei_ads.s_nbrooms BETWEEN """ + str(float(mo_dict['rooms'])-0.5) + """ AND """ + str(float(mo_dict['rooms'])+0.5) + """) AND """ + '\n')
        else:
            fp.write(r"""(srei_ads.s_nbrooms BETWEEN """ + str(float(mo_dict['rooms'])-1.0) + """ AND """ + str(float(mo_dict['rooms'])+1.0) + """) AND """ + '\n')
        fp.write(r"""srei_ads.s_grossrent>=""" + mo_dict['br_mo'] + """AND""")
        # Baujahr
        fp.write(r"""(srei_ads.s_construction_year BETWEEN """ + str(float(mo_dict['year'])-20) + """ AND """ + str(float(mo_dict['year'])+20) + """) AND """ + '\n')
        # Wohnraum
        fp.write(r"""(srei_ads.s_construction_year BETWEEN """ + str(float(mo_dict['size'])*0.8) + """ AND """ + str(float(mo_dict['size'])*1.2) + """) AND """ + '\n')
        # Nicht leer
        fp.write(r"""srei_ads.s_street IS NOT NULL AND""" + '\n')
        fp.write(r"""srei_ads.s_netrent IS NOT NULL""" + '\n')
    print('Created SQL query file under {}.'.format(sqlFile))
    return sqlFile

if __name__=="__main__":
    writeReport()