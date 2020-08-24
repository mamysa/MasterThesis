import os
import sys

SRCFILES = [
    "src/__main__.py",
    "src/util.py",
    "src/parser.py",
    "src/model/pattern.py",
    "src/model/term.py",
    "src/model/tlform.py",
    "src/model/rpython.py",
    "src/preprocess/tlform.py",
    "src/preprocess/pattern/checkinhole.py",
    "src/preprocess/pattern/extractsym.py",
    "src/preprocess/pattern/checkntcycle.py",
    "src/preprocess/pattern/insertconstraintcheck.py",
    "src/preprocess/pattern/rewriteid.py",
    "src/preprocess/pattern/rewritent.py",
    "src/preprocess/pattern/solventclosure.py",
    "src/preprocess/pattern/solveholereachability.py",
    "src/preprocess/pattern/solveholereachability.py",
    "src/preprocess/term/checkellipsisdepth.py",
    "src/preprocess/term/rewritemfapply.py",
    "src/codegen/common.py",
    "src/codegen/tlform.py",
    "src/codegen/pattern.py",
    "src/codegen/term.py",
]    

lang_from_extension = {'py': 'python', 'rkt': 'racket'}


def genchapterfor(chaptername, indir, files, outdir, outname, rename_first_on_path=None):

    chaptercontents = []
    chaptercontents.append("\chapter{%s}" % chaptername)
    chaptercontents.append("\n")

    for filename in files:
        f = open(indir + filename, 'r')
        contents = f.read()
        f.close()

        filename = filename.replace('_', '')
        filename = filename.split('/')
        if rename_first_on_path is not None:
            filename[0] = rename_first_on_path
        try:
            lang = lang_from_extension[filename[-1].split('.')[1]]
        except KeyError:
            print("Extension %s not found")
            sys.exit(1)
        filename = '/'.join(filename)
        label = filename.replace('/', '-')
        caption = "Contents of \\texttt{%s}" % filename

        chaptercontents.append("\\begin{code}")
        chaptercontents.append("\\scriptsize")
        chaptercontents.append("\\begin{minted}[tabsize=2,obeytabs,fontsize=\\tiny]{%s}" % lang)
        chaptercontents.append(contents)
        chaptercontents.append("\end{minted}")
        chaptercontents.append("\label{%s}" % label)
        chaptercontents.append("\captionof{listing}{%s}" % caption)
        chaptercontents.append("\end{code}")
        chaptercontents.append("\n")

        f = open(outdir + outname, 'w')  
        f.write('\n'.join(chaptercontents))
        f.close()



try: 
    pyredexloc = os.environ['PyPltRedexBaseDir']
    outdir = os.environ['ThesisAppendixDir']

    genchapterfor("PyPltRedex Source Code", pyredexloc, SRCFILES, outdir, 'pypltredex-source.tex', rename_first_on_path='pypltredex')


except KeyError:
    print('error: environment variable PyPltRedexBaseDir not set')
