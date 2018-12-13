def writeReport():
    import createStaticMap
    import urllib
    import urllib.parse
    import json
    import os
    from latexWriter import texWriter

    # parse arguments
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-j", "--json-file", dest="jsonFile", nargs='?', const="report.json", type=str,
                        help="Create report from specified json file. Defaults to report.json if no option provided.")
    args = parser.parse_args()

    #setup dict for main object
    mo_dict = {}
    mo_dict['street'] = 'Langstrasse 1234'
    mo_dict['br_mo'] = '2000'
    mo_dict['ext_mo'] = '400'
    mo_dict['net_mo'] = '1600'
    mo_dict['m2_pa'] = '322'
    mo_dict['plz_city'] = '8004, Zürich'
    mo_dict['d_school'] = '100m, 1min'
    mo_dict['d_shop'] = '100m, 1min'
    mo_dict['d_fun'] = '100m, 1min'
    mo_dict['d_public'] = '100m, 1min'
    mo_dict['rooms'] = '4.0'
    mo_dict['size'] = '120m2'
    mo_dict['bath'] = '1 Bad/WC'
    mo_dict['kitchen'] = 'Offen'
    mo_dict['balkon'] = 'Vorhanden'
    mo_dict['lift'] = 'Vorhanden'
    mo_dict['floor'] = '4. OG'
    mo_dict['year'] = '1971'
    mo_dict['makro'] = createStaticMap.createStaticHOMap(zoom='14',exportPath='ho_images', exportedImgName='ho-makro.jpg')
    mo_dict['mikro'] = createStaticMap.createStaticHOMap(zoom='18',exportPath='ho_images', exportedImgName='ho-mikro.jpg')
    mo_dict['img'] = ['img/ho_images/img-0.png','img/ho_images/img-1.png','img/ho_images/img-2.png','img/ho_images/img-3.png','img/ho_images/img-4.png','img/ho_images/img-5.png',]


    generatedReportFilePath = ''.join((mo_dict['street'].replace(' ',''),'-GA'))
    generatedReportFileName = ''.join((mo_dict['street'].replace(' ',''),'.tex'))

    if not os.path.exists(generatedReportFilePath):
        os.makedirs(generatedReportFilePath)

    generatedReportImgDirectory = ''.join((generatedReportFilePath, '/', 'img'))
    if not os.path.exists(generatedReportImgDirectory):
        os.makedirs(generatedReportImgDirectory)


    #TODO finalise createVODictFromJson
    if args.jsonFile:
        jsonFileName = args.jsonFile
        if not os.path.isfile(jsonFileName):
            print('Specified XML file doesn\'t exist.')
        else:
            with open(jsonFileName) as fp:
                inputDict = json.load(fp)
                mo_dict = inputDict['mo']
                vo_dicts = inputDict['vo']
    else:
        # set up dict for comparable objects
        testInput = 'parsed-pyout.csv'
        vo_dicts = createVODictFromCSV(generatedReportImgDirectory,testInput)

    f = open(''.join((generatedReportFilePath, '/', generatedReportFileName)), 'w')
    writer = texWriter()
    writer.setupTexFilePackages(f)
    writer.writeTitlePage(f, mo_str='Langstrasse 123', mo_plz='8004', mo_rooms='4.0', mo_city='Zürich')
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
    with open('report.json', 'w') as fp:
        json.dump(joined_dict, fp, indent=4)

def createVODictFromCSV(generatedReportImgDirectory, filename='output.csv'):

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

    numberOfMaxAvailableImageLinks = sum('s_full_link' in key for key in objectsDict.keys())
    consolidatedObjectsDict = {}
    for i in range(len(objectsDict['double1group_id'])):
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
        equiptmentLUT = {'-1':'Unbekannt', '0':'Nicht vorhanden', '1':'Vorhanden', '2':'Vorhanden', '3':'Vorhanden', '4':'Vorhanden'}
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
        search_string = ','.join ((consolidatedObjectsDict[new_vo]['street'].split('(')[0], consolidatedObjectsDict[new_vo]['plz'], consolidatedObjectsDict[new_vo]['city']))
        search_string = urllib.parse.quote_plus(search_string) #parse so urls pose no problems in browsers
        consolidatedObjectsDict[new_vo]['makro'] = createStaticMap.createStaticVOMakroMap(address2=search_string, exportPath=generatedReportImgDirectory, voName=new_vo)
        consolidatedObjectsDict[new_vo]['mikro'] = createStaticMap.createStaticVOMikroMap(address=search_string, exportPath=generatedReportImgDirectory, voName=new_vo)


        # Download images and saving the export path in list
        consolidatedObjectsDict[new_vo]['img'] = []
        for j in range(numberOfMaxAvailableImageLinks):
            voImgLocalLink = ''.join(('img-',str(j),'.png'))
            fullExportPath = ''.join((generatedReportImgDirectory, '/', 'vo_images', '/', new_vo, '/', voImgLocalLink))
            if j==0:
                imgURL = objectsDict['s_full_link'][i]
                if objectsDict['s_full_link'][i] != 'NONE':
                    consolidatedObjectsDict[new_vo]['img'].append(saveVOImageLocally(new_vo, fullExportPath, imgURL))
            else:
                imgURL = objectsDict['_'.join(('s_full_link',str(j)))][i]
                if imgURL != 'NONE':
                    consolidatedObjectsDict[new_vo]['img'].append(saveVOImageLocally(new_vo, fullExportPath, imgURL))

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
            print('Could not access file through link. Exception:\n')
            print(e)
            print('\n')
        else:
            print('Image file for {} was downloaded as {}.\n'.format(VOName, fullExportPath))
            relativeImageLink = fullExportPath[fullExportPath.find('img/'):]
            return relativeImageLink
    else:
        print('File already exists for {} under {}.\n'.format(VOName, fullExportPath))
        relativeImageLink = fullExportPath[fullExportPath.find('img/'):]
        return relativeImageLink

if __name__=="__main__":
    writeReport()
    #createDictForObjects()