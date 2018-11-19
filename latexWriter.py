"""
Creates a CSV-to-LaTeX printer object.
"""

class texWriter:

    def setupTexFilePackages(self, f):

        f.write(r'\documentclass{article}' + '\n')
        f.write(r'\usepackage[utf8]{inputenc}' + '\n')
        f.write(r'\usepackage{graphicx}' + '\n')
        f.write(r'\usepackage[table]{xcolor}' + '\n')
        f.write(r'\usepackage[a4paper,landscape,left=2cm, right=2cm, top=2cm, bottom=2.5cm, includehead, includefoot]{geometry}' + '\n')
        f.write(r'\usepackage{fancyhdr}' + '\n')
        f.write(r'\usepackage[german]{babel}' + '\n')
        f.write(r'\usepackage{caption}' + '\n\n')

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
        f.write(r'\lhead{\includegraphics[width=3cm]{img/hwz-logo.jpg}}' + '\n')
        f.write(r'\rhead{\includegraphics[width=3cm]{img/swissrei-logo.jpg}}' + '\n')
        f.write(r'\rfoot{Seite \thepage}' + '\n')
        f.write(r'\cfoot{Prof. Dr. Peter Ilg, Leiter Swiss Real Estate Institute}' + '\n')
        f.write(r'\lfoot{09.11.2018}' + '\n')
        f.write(r'}' + '\n\n')

        f.write(r'\pagestyle{plain}' + '\n')

    def writeTitlePage(self, f, mo_str='abcd', mo_plz='1234', mo_rooms='4.0', mo_city='abcity'):
        f.write(r'\begin{document}' + '\n')
        f.write(r'\vspace*{5cm}\noindent{\YUGE \underline{Gutachten zur Orts- oder Quartierüblichkeit}} \\' + '\n\n')
            
        f.write(r'\vspace{1cm} \noindent ' + mo_str + r'\\' + '\n')
        f.write(mo_rooms + ' Zimmer' + r'\\' + '\n')
        f.write(mo_plz + ' ' + mo_city + r'\\' + '\n')

        f.write(r'\end{document}')

    def writeMOTablePage(self, f, mo_dict):
        pass
    def writeHOTablePage(f, mo_dict):
        pass
    def writeHOMacroPage(f, 'path_to_macro_HO.jpg'):
        pass
    def writeHOMikroPage(f, 'path_to_mikro_HO.jpg'):
        pass
    def writeCompareGraph(f, mo_dict, vo_dict):
        pass
    def writeCompareTable(f, mo_dict, vo_dict):
        pass # if more than 5 VO exist
    def writeVOMacroPage(f, mo_dict, vo_dict):
        pass
