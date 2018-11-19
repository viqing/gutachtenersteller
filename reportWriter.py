def writeReport():
    import createStaticMap
    from latexWriter import texWriter

    #setup dict for main object
    mo_dict = {}
    mo_dict['street'] = 'Langstrasse 1234'
    mo_dict['br_mo'] = '2000'
    mo_dict['net_mo'] = '1600'
    mo_dict['plz'] = '8004'
    mo_dict['city'] = 'Zürich'
    mo_dict['d_school'] = 'Langstrasse 1234'
    mo_dict['d_shop'] = 'Langstrasse 1234'
    mo_dict['d_fun'] = 'Langstrasse 1234'
    mo_dict['d_public'] = 'Langstrasse 1234'
    mo_dict['d_rooms'] = '4.0'
    mo_dict['d_size'] = 'Langstrasse 1234'
    mo_dict['d_year'] = 'Langstrasse 1234'

    vo_dict = {}

    f = open('py2texTest2.tex', 'w')
    writer = texWriter()
    writer.setupTexFilePackages(f)
    writer.writeTitlePage(f, mo_str='Langstrasse 123', mo_plz='8004', mo_rooms='4.0', mo_city='Zürich')
    writer.writeHOTablePage(f, mo_dict)
    writer.writeHOMacroPage(f, 'path_to_macro_HO.jpg')
    writer.writeHOMikroPage(f, 'path_to_mikro_HO.jpg')
    writer.writeCompareGraph(f, mo_dict, vo_dict)
    writer.writeCompareTable(f, mo_dict, vo_dict)
    writer.writeCompareTable(f, mo_dict, vo_dict) # if more than 5 VO exist
    writer.writeVOMacroPage(f, mo_dict, vo_dict)


if __name__=="__main__":
    writeReport()