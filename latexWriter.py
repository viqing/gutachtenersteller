"""
Creates a CSV-to-LaTeX printer object.
"""
f = open('pytotextest.tex', 'w')

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
f.write(r'}' + '\n')

f.write(r'\newcommand{\fakesubsection}[1]{%' + '\n')
f.write(r'\par\refstepcounter{subsection}% Increase subsection counter' + '\n')
f.write(r'\subsectionmark{#1}% Add subsection mark (header)' + '\n')
f.write(r'\addcontentsline{toc}{subsection}{\protect\numberline{\thesubsection}#1}% Add subsection to ToC' + '\n')
f.write(r'% Add more content here, if needed.' + '\n')
f.write(r'}' + '\n')

f.write(r'\fancypagestyle{plain}{' + '\n')
f.write(r'\fancyhf{}' + '\n')
f.write(r'\lhead{\includegraphics[width=3cm]{img/hwz-logo.jpg}}' + '\n')
f.write(r'\rhead{\includegraphics[width=3cm]{img/swissrei-logo.jpg}}' + '\n')
f.write(r'\rfoot{Seite \thepage}' + '\n')
f.write(r'\cfoot{Prof. Dr. Peter Ilg, Leiter Swiss Real Estate Institute}' + '\n')
f.write(r'\lfoot{09.11.2018}' + '\n')
f.write(r'}' + '\n')

f.write(r'\pagestyle{plain}' + '\n')


f.write(r'\begin{document}' + '\n')
f.write(r'\vspace*{5cm}\noindent{\YUGE \underline{Gutachten zur Orts- oder Quartierüblichkeit}} \\' + '\n\n')
	
f.write(r'\vspace{1cm} \noindent Teststrasse 123 \\' + '\n')
f.write(r'3.5 Zimmer \\' + '\n')
f.write(r'8001 Zürich \\' + '\n')

f.write(r'\end{document}')
	