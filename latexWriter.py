"""
Creates a CSV-to-LaTeX printer object.
"""

class texWriter:

    def __init__(self):
        pass

    def setupTexFilePackages(self, f):

        f.write(r'\documentclass{article}' + '\n')
        f.write(r'\usepackage[utf8]{inputenc}' + '\n')
        f.write(r'\usepackage{graphicx}' + '\n')
        f.write(r'\usepackage[table]{xcolor}' + '\n')
        f.write(r'\usepackage[a4paper,landscape,left=2cm, right=2cm, top=2cm, bottom=2.5cm, includehead, includefoot]{geometry}' + '\n')
        f.write(r'\usepackage{fancyhdr}' + '\n')
        f.write(r'\usepackage[T1]{fontenc}' + '\n')
        f.write(r'\usepackage[ngerman]{babel}' + '\n')
        f.write(r'\usepackage{caption}' + '\n')
        f.write(r'\usepackage{pgfplots}' + '\n')
        f.write(r'\usepackage{tabularx}' + '\n\n')

        f.write(r'\setcounter{tocdepth}{2}' + '\n\n')

        f.write(r'\newcommand\YUGE{\fontsize{100}{120}\selectfont}' + '\n\n')

        f.write(r'\newcommand{\fakesection}[1]{%' + '\n')
        f.write(r'\par\refstepcounter{section}% Increase section counter' + '\n')
        f.write(r'\sectionmark{#1}% Add section mark (header)' + '\n')
        f.write(r'\addcontentsline{toc}{section}{\protect\numberline{\thesection}#1}% Add section to ToC' + '\n')
        f.write(r'% Add more content here, if needed.' + '\n')
        f.write(r'}' + '\n\n')

        f.write(r'\newcommand{\fakesubsection}[1]{%' + '\n')
        f.write(r'\par\refstepcounter{subsection}% Increase subsection counter' + '\n')
        f.write(r'\subsectionmark{#1}% Add subsection mark (header)' + '\n')
        f.write(r'\addcontentsline{toc}{subsection}{\protect\numberline{\thesubsection}#1}% Add subsection to ToC' + '\n')
        f.write(r'% Add more content here, if needed.' + '\n')
        f.write(r'}' + '\n\n')

        f.write(r'\fancypagestyle{plain}{' + '\n')
        f.write(r'\fancyhf{}' + '\n')
        f.write(r'\lhead{\includegraphics[width=3cm]{img/hwz-logo.png}}' + '\n')
        f.write(r'\rhead{\includegraphics[width=3cm]{img/swissrei-logo.png}}' + '\n')
        f.write(r'\rfoot{Seite \thepage}' + '\n')
        f.write(r'\cfoot{Prof. Dr. Peter Ilg, Leiter Swiss Real Estate Institute}' + '\n')
        f.write(r'\lfoot{\today}' + '\n')
        f.write(r'}' + '\n\n')

        f.write(r'\pagestyle{plain}' + '\n')

    def writeTitlePage(self, f, mo_str='abcd', mo_plz='1234', mo_rooms='4.0', mo_city='abcity'):
        f.write(r'\begin{document}' + '\n')
        f.write(r'\vspace*{5cm}\noindent{\YUGE \underline{Gutachten zur Orts- oder Quartierüblichkeit}} \\' + '\n\n')
            
        f.write(r'\vspace{1cm} \noindent ' + mo_str + r'\\' + '\n')
        f.write(mo_rooms + ' Zimmer' + r'\\' + '\n')
        f.write(mo_plz + ' ' + mo_city + r'\\' + '\n')

    def writeTOC(self, f):
        f.write(r'\clearpage' + '\n')
        f.write(r'\renewcommand{\baselinestretch}{1.1}\normalsize' + '\n')
        f.write(r'\tableofcontents' + '\n')
        f.write(r'\renewcommand{\baselinestretch}{1.0}\normalsize' + '\n')

    def writeHOTablePage(self, f, mo_dict):
        f.write(r'\clearpage' + '\n')
        f.write(r'\section{Details zum Hauptobjekt}' + '\n')
        f.write(r'\subsection{Übersicht der relevanten Vergleichskriterien}' + '\n')
        f.write(r'\begin{flushleft}' + '\n')
        f.write(r'\renewcommand{\arraystretch}{1.1}' + '\n')
        f.write(r'\setlength{\tabcolsep}{10pt}' + '\n')
        f.write(r'\begin{tabular}{ |p{\dimexpr 0.18\linewidth-2\tabcolsep}|p{\dimexpr 0.15\linewidth-2\tabcolsep}| } ' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\textbf{Adresse} & \cellcolor{lightgray}\textbf{' + mo_dict['street'] + r'}\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\rowcolor{gray} Monatspreis (CHF) &\\ ' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Nettomietzins & \cellcolor{lightgray}' + mo_dict['net_mo'] + r'.-\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Nebenkosten & \cellcolor{lightgray}' + mo_dict['ext_mo'] + r'.-\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\textbf{Bruttomietzins} & \cellcolor{lightgray}\textbf{' + mo_dict['br_mo'] + r'.-}\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Mietzins/m2 p.a. & \cellcolor{lightgray}' + mo_dict['m2_pa'] + r'.-\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\rowcolor{gray} Lage \& Distanzen &\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Historisch/Administrativ & \cellcolor{lightgray}' + mo_dict['plz_city'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Schule & \cellcolor{lightgray}' + mo_dict['d_school'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Einkaufsmöglichkeiten & \cellcolor{lightgray}' + mo_dict['d_shop'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Naherholung & \cellcolor{lightgray}' + mo_dict['d_fun'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'ÖV & \cellcolor{lightgray}' + mo_dict['d_public'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\rowcolor{gray} Grösse &\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Zimmerzahl p.a. & \cellcolor{lightgray}' + mo_dict['rooms'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Fläche ($m^2$) & \cellcolor{lightgray}' + mo_dict['size'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\rowcolor{gray} Ausstattung &\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Anzahl Nasszellen & \cellcolor{lightgray}' + mo_dict['bath'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Küche & \cellcolor{lightgray}' + mo_dict['kitchen'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Balkon & \cellcolor{lightgray}' + mo_dict['balkon'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Lift & \cellcolor{lightgray}' + mo_dict['lift'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Stockwerk & \cellcolor{lightgray}' + mo_dict['floor'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\rowcolor{gray} Baujahr &\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Baujahr & \cellcolor{lightgray}' + mo_dict['year'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\end{tabular}' + '\n')
        f.write(r'\end{flushleft}' + '\n')

    def writeHOMacroPage(self, f, path):
        f.write(r'\clearpage' + '\n')
        f.write(r'\subsection{Analyse der Makrolage}' + '\n')
        f.write(r'\begin{figure}[!htbp]' + '\n')
        f.write(r'\begin{minipage}[c]{0.67\textwidth}' + '\n')
        f.write(r'\includegraphics[width=\textwidth]{'+ path +'}' + '\n')
        f.write(r'\end{minipage}\hfill' + '\n')
        f.write(r'\begin{minipage}[c]{0.3\textwidth}' + '\n')
        f.write(r'\begin{itemize}' + '\n')
        f.write(r'\item ÖV und Bahnhof in Gehdistanz' + '\n')
        f.write(r'\item Schulen sind schnell erreichbar' + '\n')
        f.write(r'\item Einkaufszentren nur wenige Minuten entfernt und ist nicht weit von Nachtclubs' + '\n')
        f.write(r'\item Nahe gelegen an populären Einkaufszentren' + '\n')
        f.write(r'\end{itemize}' + '\n')
        f.write(r'\end{minipage}' + '\n')
        f.write(r'\end{figure}' + '\n')

    def writeHOMikroPage(self, f, path):
        f.write(r'\clearpage' + '\n')
        f.write(r'\subsection{Analyse der Mikrolage}' + '\n')
        f.write(r'\begin{figure}[!htbp]' + '\n')
        f.write(r'\begin{minipage}[c]{0.67\textwidth}' + '\n')
        f.write(r'\includegraphics[width=\textwidth]{'+ path +'}' + '\n')
        f.write(r'\end{minipage}\hfill' + '\n')
        f.write(r'\begin{minipage}[c]{0.3\textwidth}' + '\n')
        f.write(r'\begin{itemize}' + '\n')
        f.write(r'\item ÖV und Bahnhof in Gehdistanz' + '\n')
        f.write(r'\item Schulen sind schnell erreichbar' + '\n')
        f.write(r'\item Einkaufszentren nur wenige Minuten entfernt und ist nicht weit von Nachtclubs' + '\n')
        f.write(r'\item Nahe gelegen an populären Einkaufszentren' + '\n')
        f.write(r'\end{itemize}' + '\n')
        f.write(r'\end{minipage}' + '\n')
        f.write(r'\end{figure}' + '\n')

    def writeHOAdditionalImagesPage(self, f):
        f.write(r'\clearpage' + '\n')
        f.write(r'\subsection{Details zur Ausstattung und weitere Ansichten}' + '\n')

    def writeCompareGraph(self, f, mo_dict, vo_dicts):
        average = 0
        maximum  = 0
        sum = 0
        for vo_dict in vo_dicts.values():
            sum = sum + float(vo_dict['br_mo'])
            if float(vo_dict['br_mo']) > maximum:
                maximum = float(vo_dict['br_mo'])

        average = int(sum/len(vo_dicts))
        missbrauch = int(1.2*average)
        avg_diff = int(sum/len(vo_dicts) - float(mo_dict['br_mo']))
        avg_diff_perc = round(100*(sum/len(vo_dicts) - float(mo_dict['br_mo']))/(sum/len(vo_dicts)),1)
        miss_diff = int(1.2*sum/len(vo_dicts)-float(mo_dict['br_mo']))
        miss_diff_perc = round(100*(1.2*sum/len(vo_dicts)-float(mo_dict['br_mo']))/(1.2*average),1) 
        
        f.write(r'\clearpage' + '\n')
        f.write(r'\section{Übersicht über die Mietzinse des Referenzobjektes und der Vergleichsobjekte}' + '\n')
        f.write(r'Der Bruttomietzins des Objekts an der' + str(mo_dict['street']) + r' liegt mit  CHF ' + str(mo_dict['br_mo']) + '.- etwa CHF ' + str(avg_diff) + '.- (' + str(avg_diff_perc)  + r'\%) unter dem Durchschnitt der Vergleichsobjkete\protect\footnote{Kriterien gemäss Art. 11 - Verordnung über die Miete und Pacht von Wohn- und Geschäftsräumen. (VMWG) vom 9.Mai 1990 (Stand 1. Juli 2014)}.\\ Er ist mit einem Unterschied von CHF ' + str(miss_diff) + '.- (' + str(miss_diff_perc) + r'\%), von der Missbrauchsgrenze\protect\footnote{Hausmann, Urs; Vertragsfreiheit im Schweizer Mietrech von 1804 bis 2014 unter besonderer Berücksichtigung der Mietzinses, Zürich, St. Gallen 2016}  entfernt.\\' + '\n')
        f.write(r'\pgfplotstableread[row sep=\\,col sep=&]{' + '\n')
        f.write(r'street  & br_mo \\' + '\n')
        f.write(mo_dict['street'] + '&' + mo_dict['br_mo'] + r'\\' + '\n')
        for vo_dict in vo_dicts.values():
            f.write(vo_dict['street'] + '&' + vo_dict['br_mo'] + r'\\' + '\n')
        f.write(r'}\mydatabla' + '\n')
        f.write(r'\begin{tikzpicture}'+ '\n')
        f.write(r'\begin{axis}['+ '\n')
        f.write(r'ybar,' + '\n')
        f.write(r'title={\textbf{Bruttomietzins pro Monat in CHF}},' + '\n')
        f.write(r'ymajorgrids=true,' + '\n')
        f.write(r'width=0.9\textwidth,' + '\n')
        f.write(r'height=.345\textwidth,' + '\n')
        f.write(r'legend style={at={(0.5,1)},' + '\n')
        f.write(r'anchor=north,legend columns=-1},' + '\n') 
        f.write(r'symbolic x coords={' + mo_dict['street'])
        for vo_dict in vo_dicts.values():
            f.write(',' + vo_dict['street'])
        f.write(r'},' + '\n')
        f.write(r'x tick label style={rotate=45, anchor=east, align=left},' + '\n')
        f.write(r'xtick=data,' + '\n')
        f.write(r'nodes near coords align={vertical},' + '\n')

        
        f.write(r'ymin=0,ymax=' + str(max(missbrauch, maximum)+300) + ',' + '\n')
        f.write(r']' + '\n')
        f.write(r'\addplot[nodes near coords, fill=blue!40] table[x=street,y=br_mo]{\mydatabla};' + '\n')
        f.write(r'\addplot[smooth, ultra thick, red]' + '\n')
        f.write(r'coordinates {(' + mo_dict['street'] + ',' + str(missbrauch) + ')')
        for vo_dict in vo_dicts.values():
            f.write('('+ vo_dict['street'] + ',' + str(missbrauch) + ')')
        f.write(r'};' + '\n')    

        f.write(r'\addplot[smooth, ultra thick]' + '\n')

        f.write(r'coordinates {(' + mo_dict['street'] + ',' + str(average) + ')')
        for vo_dict in vo_dicts.values():
            f.write('('+ vo_dict['street'] + ',' + str(average) + ')')
        f.write(r'};' + '\n')
        f.write(r'\end{axis}' + '\n') 
        f.write(r'\end{tikzpicture}' + '\n') 

    def writeCompareTable(self, f, mo_dict, vo_dicts, currentBinIndex, maxBinIndex):
        f.write(r'\clearpage' + '\n')
        if currentBinIndex == '1':
            f.write(r'\section{Übersicht der Vergleichskriterien aller Mietobjekte}' + '\n')
        f.write(r'\subsection*{Vergleich der Mietobjekte (Teil ' + str(currentBinIndex) + '/' + str(maxBinIndex) + ')}' + '\n')
        f.write(r'\begin{table}[!htbp]' + '\n')
        f.write(r'\begin{flushleft}' + '\n')
        f.write(r'\renewcommand{\arraystretch}{1.1}' + '\n')
        f.write(r'\setlength{\tabcolsep}{10pt}' + '\n')
        printStringList = [None] * 48
        printStringList[0] =r'\begin{tabular}{ | p{\dimexpr 0.172\linewidth-2\tabcolsep} | p{\dimexpr 0.138\linewidth-2\tabcolsep} |'
        printStringList[1] =r'\hline' + '\n'
        printStringList[2] =r'\textbf{Adresse} & \cellcolor{lightgray}\textbf{' + mo_dict['street'] + '}'
        printStringList[3] =r'\hline' + '\n'
        printStringList[4] =r'\rowcolor{gray} Monatspreis (CHF) & '
        printStringList[5] =r'\hline' + '\n'
        printStringList[6] =r'Nettomietzins & \cellcolor{lightgray} ' + mo_dict['net_mo'] + '.-'
        printStringList[7] =r'\hline' + '\n'
        printStringList[8] =r'Nebenkosten & \cellcolor{lightgray} ' + mo_dict['ext_mo'] + '.-'
        printStringList[9] =r'\hline' + '\n'
        printStringList[10] =r'\textbf{Bruttomietzins} & \cellcolor{lightgray}\textbf{' + mo_dict['br_mo'] + '.-}'
        printStringList[11] =r'\hline' + '\n'
        printStringList[12] =r'Mietzins/m2 p.a. & \cellcolor{lightgray} ' + mo_dict['m2_pa'] + '.-'
        printStringList[13] =r'\hline' + '\n'
        printStringList[14] =r'\rowcolor{gray} Lage \& Distanzen & '
        printStringList[15] =r'\hline' + '\n'
        printStringList[16] =r'Historisch/Administrativ & \cellcolor{lightgray} ' + mo_dict['plz_city']
        printStringList[17] =r'\hline' + '\n'
        printStringList[18] =r'Schule & \cellcolor{lightgray} ' + mo_dict['d_school']
        printStringList[19] =r'\hline' + '\n'
        printStringList[20] =r'Einkaufsmöglichkeiten & \cellcolor{lightgray} ' + mo_dict['d_shop']
        printStringList[21] =r'\hline' + '\n'
        printStringList[22] =r'Naherholung & \cellcolor{lightgray} ' + mo_dict['d_fun']
        printStringList[23] =r'\hline' + '\n'
        printStringList[24] =r'ÖV & \cellcolor{lightgray} ' + mo_dict['d_public']
        printStringList[25] =r'\hline' + '\n'
        printStringList[26] =r'\rowcolor{gray} Grösse & '
        printStringList[27] =r'\hline' + '\n'
        printStringList[28] =r'Zimmerzahl p.a. & \cellcolor{lightgray} ' + mo_dict['rooms']
        printStringList[29] =r'\hline' + '\n'
        printStringList[30] =r'Fläche ($m^2$) & \cellcolor{lightgray} ' + mo_dict['size']
        printStringList[31] =r'\hline' + '\n'
        printStringList[32] =r'\rowcolor{gray} Ausstattung & '
        printStringList[33] =r'\hline' + '\n'
        printStringList[34] =r'Anzahl Nasszellen & \cellcolor{lightgray} ' + mo_dict['bath']
        printStringList[35] =r'\hline' + '\n'
        printStringList[36] =r'Küche & \cellcolor{lightgray} ' + mo_dict['kitchen']
        printStringList[37] =r'\hline' + '\n'
        printStringList[38] =r'Balkon & \cellcolor{lightgray} ' + mo_dict['balkon']
        printStringList[39] =r'\hline' + '\n'
        printStringList[40] =r'Lift & \cellcolor{lightgray} ' + mo_dict['lift']
        printStringList[41] =r'\hline' + '\n'
        printStringList[42] =r'Stockwerk & \cellcolor{lightgray} ' + mo_dict['floor']
        printStringList[43] =r'\hline' + '\n'
        printStringList[44] =r'\rowcolor{gray} Baujahr & '
        printStringList[45] =r'\hline' + '\n'
        printStringList[46] =r'Baujahr & \cellcolor{lightgray} ' + mo_dict['year']
        printStringList[47] =r'\hline' + '\n'

        for vo_dict in vo_dicts.values():
            printStringList[0] = ''.join((printStringList[0], r'p{\dimexpr 0.138\linewidth-2\tabcolsep} |'))
            printStringList[2] = ''.join((printStringList[2],r' & \textbf{',vo_dict['street'], '}'))
            printStringList[4] = ''.join((printStringList[4],' & '))
            printStringList[6] = ''.join((printStringList[6],' & ',vo_dict['net_mo'],'.-'))
            printStringList[8] = ''.join((printStringList[8],' & ',vo_dict['ext_mo'],'.-'))
            printStringList[10] = ''.join((printStringList[10],r' & \textbf{', vo_dict['br_mo'], '.-}'))
            printStringList[12] = ''.join((printStringList[12],' & ', vo_dict['m2_pa'],'.-'))
            printStringList[14] = ''.join((printStringList[14],' & '))
            printStringList[16] = ''.join((printStringList[16],' & ', vo_dict['plz'],', ',vo_dict['city']))
            printStringList[18] = ''.join((printStringList[18],' & ', vo_dict['d_school']))
            printStringList[20] = ''.join((printStringList[20],' & ', vo_dict['d_shop']))
            printStringList[22] = ''.join((printStringList[22],' & ', vo_dict['d_fun']))
            printStringList[24] = ''.join((printStringList[24],' & ', vo_dict['d_public']))
            printStringList[26] = ''.join((printStringList[26],' & '))
            printStringList[28] = ''.join((printStringList[28],' & ', vo_dict['rooms']))
            printStringList[30] = ''.join((printStringList[30],' & ', vo_dict['size']))
            printStringList[32] = ''.join((printStringList[32],' & '))
            printStringList[34] = ''.join((printStringList[34],' & ', vo_dict['bath']))
            printStringList[36] = ''.join((printStringList[36],' & ', vo_dict['kitchen']))
            printStringList[38] = ''.join((printStringList[38],' & ', vo_dict['balkon']))
            printStringList[40] = ''.join((printStringList[40],' & ', vo_dict['lift']))
            printStringList[42] = ''.join((printStringList[42],' & ', vo_dict['floor']))
            printStringList[44] = ''.join((printStringList[44],' & '))
            printStringList[46] = ''.join((printStringList[46],' & ', vo_dict['year']))

        printStringList[0] = ''.join((printStringList[0],r' } ' + '\n'))
        printStringList[2] = ''.join((printStringList[2],r'\\' + '\n'))
        printStringList[4] = ''.join((printStringList[4],r'\\' + '\n'))
        printStringList[6] = ''.join((printStringList[6],r'\\' + '\n'))
        printStringList[8] = ''.join((printStringList[8],r'\\' + '\n'))
        printStringList[10] = ''.join((printStringList[10],r'\\' + '\n'))
        printStringList[12] = ''.join((printStringList[12],r'\\' + '\n'))
        printStringList[14] = ''.join((printStringList[14],r'\\' + '\n'))
        printStringList[16] = ''.join((printStringList[16],r'\\' + '\n'))
        printStringList[18] = ''.join((printStringList[18],r'\\' + '\n'))
        printStringList[20] = ''.join((printStringList[20],r'\\' + '\n'))
        printStringList[22] = ''.join((printStringList[22],r'\\' + '\n'))
        printStringList[24] = ''.join((printStringList[24],r'\\' + '\n'))
        printStringList[26] = ''.join((printStringList[26],r'\\' + '\n'))
        printStringList[28] = ''.join((printStringList[28],r'\\' + '\n'))
        printStringList[30] = ''.join((printStringList[30],r'\\' + '\n'))
        printStringList[32] = ''.join((printStringList[32],r'\\' + '\n'))
        printStringList[34] = ''.join((printStringList[34],r'\\' + '\n'))
        printStringList[36] = ''.join((printStringList[36],r'\\' + '\n'))
        printStringList[38] = ''.join((printStringList[38],r'\\' + '\n'))
        printStringList[40] = ''.join((printStringList[40],r'\\' + '\n'))
        printStringList[42] = ''.join((printStringList[42],r'\\' + '\n'))
        printStringList[44] = ''.join((printStringList[44],r'\\' + '\n'))
        printStringList[46] = ''.join((printStringList[46],r'\\' + '\n'))

        for list in printStringList:
            f.write(list)

        f.write(r'\end{tabular}' + '\n')
        f.write(r'\end{flushleft}' + '\n')
        f.write(r'\end{table}' + '\n')

    def writeVOMacroPage(self, f, mo_dict, vo_dict):
        f.write(r'\clearpage' + '\n')
        f.write(r'\subsection{' + vo_dict['street'] + '}' + '\n')
        f.write(r'\subsubsection*{Übersicht der Vergleichskriterien und Analyse der Makrolage}' + '\n')
        f.write(r'\begin{figure}[!htbp]' + '\n')
        f.write(r'\begin{minipage}[c]{0.55\textwidth}' + '\n')
        f.write(r'\includegraphics[width=\textwidth]{' + vo_dict['makro'] + '}' + '\n')
        f.write(r'\end{minipage}\hfill' + '\n')
        f.write(r'\begin{minipage}[c]{0.44\textwidth}' + '\n')
        f.write(r'\begin{flushleft}' + '\n')
        f.write(r'\renewcommand{\arraystretch}{1.1}' + '\n')
        f.write(r'\setlength{\tabcolsep}{10pt}' + '\n')
        f.write(r'\begin{tabular}{ |l|l|l| } ' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\textbf{Adresse} & \cellcolor{lightgray}\textbf{' + mo_dict['street'] + r'}&\textbf{' + vo_dict['street'] + r'}\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\rowcolor{gray} Monatspreis (CHF) & &\\ ' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Nettomietzins & \cellcolor{lightgray}' + mo_dict['net_mo'] + '.-&' + vo_dict['net_mo'] + r'.-\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Nebenkosten & \cellcolor{lightgray}' + mo_dict['ext_mo'] + '.-&' + vo_dict['ext_mo'] + r'.-\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Bruttomietzins & \cellcolor{lightgray}\textbf{' + mo_dict['br_mo'] + r'.-}&\textbf{' + vo_dict['br_mo'] + r'.-}\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Mietzins/m2 p.a. & \cellcolor{lightgray}' + mo_dict['m2_pa'] + '.-&' + vo_dict['m2_pa'] + r'.-\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\rowcolor{gray} Lage \& Distanzen & &\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Historisch/Administrativ & \cellcolor{lightgray}' + mo_dict['plz_city'] + '&' + vo_dict['plz'] + ', ' + vo_dict['city'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Schule & \cellcolor{lightgray}' + mo_dict['d_school'] + '&' + vo_dict['d_school'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Einkaufsmöglichkeiten & \cellcolor{lightgray}' + mo_dict['d_shop'] + '&' + vo_dict['d_shop'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Naherholung & \cellcolor{lightgray}' + mo_dict['d_fun'] + '&' + vo_dict['d_fun'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'ÖV & \cellcolor{lightgray}' + mo_dict['d_public'] + '&' + vo_dict['d_public'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\rowcolor{gray} Grösse & &\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Zimmerzahl p.a. & \cellcolor{lightgray}' + mo_dict['rooms'] + '&' + vo_dict['rooms'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Fläche ($m^2$) & \cellcolor{lightgray}' + mo_dict['size'] + '&' + vo_dict['size'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\rowcolor{gray} Ausstattung & & \\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Anzahl Nasszellen & \cellcolor{lightgray}' + mo_dict['bath'] + '&' + vo_dict['bath'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Küche & \cellcolor{lightgray}' + mo_dict['kitchen'] + '&' + vo_dict['kitchen'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Balkon & \cellcolor{lightgray}' + mo_dict['balkon'] + '&' + vo_dict['balkon'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Lift & \cellcolor{lightgray}' + mo_dict['lift'] + '&' + vo_dict['lift'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Stockwerk & \cellcolor{lightgray}' + mo_dict['floor'] + '&' + vo_dict['floor'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\rowcolor{gray} Baujahr & &\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'Baujahr & \cellcolor{lightgray}' + mo_dict['year'] + '&' + vo_dict['year'] + r'\\' + '\n')
        f.write(r'\hline' + '\n')
        f.write(r'\end{tabular}' + '\n')
        f.write(r'\end{flushleft}' + '\n')
        f.write(r'\end{minipage}' + '\n')
        f.write(r'\end{figure}' + '\n')

    def writeVOMicroPage(self, f, vo_dict):
        f.write(r'\clearpage' + '\n')
        f.write(r'\subsection*{' + vo_dict['street'] + '}' + '\n')
        f.write(r'\subsubsection*{Analyse der Mikrolage}' + '\n')
        f.write(r'\begin{figure}[!htbp]' + '\n')
        f.write(r'\centering' + '\n')
        f.write(r'\includegraphics[width=0.9\textwidth]{' + vo_dict['mikro'] + '}' + '\n')
        f.write(r'\end{figure}' + '\n')
           
    def writeVOAdditionalImagesPage(self, f, vo_dict):
        #TODO make size of images dynamic
        f.write(r'\clearpage' + '\n')
        f.write(r'\subsubsection*{Weitere Ansichten}' + '\n')

        imgList = vo_dict['img']
        if imgList and all(img is not None for img in imgList):
            f.write(r'\begin{figure}[!htbp]' + '\n')
            f.write(r'\centering' + '\n')
            for i, img in enumerate(imgList):
                f.write(r'\includegraphics[width=0.22\textwidth, height=0.25\textheight, keepaspectratio]{' + img + '}' + '\n')
            f.write(r'\end{figure}' + '\n')

    def endDocument(self, f):
        f.write(r'\end{document}')