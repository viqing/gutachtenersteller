"""
Creates a CSV-to-LaTeX printer object.
"""
f = open('pytotextest.tex', 'w')

f.write('\\documentclass{article}\n')
f.write('\\usepackage[utf8]{inputenc}\n')
f.write('\\usepackage{graphicx}\n')
f.write('\\usepackage[table]{xcolor}\n')
f.write('\\usepackage[a4paper,landscape,left=2cm, right=2cm, top=2cm, bottom=2.5cm, includehead, includefoot]{geometry}\n')
f.write('\\usepackage{fancyhdr}\n')
f.write('\\usepackage[german]{babel}\n')
f.write('\\usepackage{caption}\n\n')

f.write('\\newcommand\YUGE{\fontsize{100}{120}\selectfont}\n\n')

f.write('\\newcommand{\\fakesection}[1]{%\n')
f.write('\t\\par\\refstepcounter{section}% Increase section counter\n')
f.write('\t\\sectionmark{#1}% Add section mark (header)\n')
f.write('\t\\addcontentsline{toc}{section}{\\protect\\numberline{\\thesection}#1}% Add section to ToC\n')
f.write('\t% Add more content here, if needed.\n')
f.write('}\n')

f.write('\\begin{document}\n')
f.write('\\end{document}\n')