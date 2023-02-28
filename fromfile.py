import os
from pathlib import Path
from constants import EXTENSIONS
from methods import compareColoredImg, textFunc

def fromFile(folder):
    # TODO: change path to dynamic path
    filePath = os.path.abspath(os.path.join(Path().resolve(), str(folder)))
    print("FILEPATH", filePath)
    if not os.path.exists(filePath):
        return None

    files = os.listdir(filePath)
    for _ in range(0, len(files)):
        versionParent = 1
        versionChild = 1
        stepNumber = 1
        newFunc(versionParent,versionChild,stepNumber,files, filePath)



def newFunc(versionParent,versionChild,stepNumber,files, filePath):
    currentFile = f'_v{versionParent}.{versionChild}_s{stepNumber}_'
    print(currentFile)

    for file in files:
        fileVars = os.path.splitext(file)
        fileExt = fileVars[-1]
        fileName = os.path.basename(fileVars[0])
        print(fileVars, currentFile in fileName)
        # found file
        if currentFile in fileName:
            if fileName[0] == '1':
                # found type file
                for fileType, v in EXTENSIONS.items():
                    print(fileType)
                    if fileExt in v:
                        print(v)
                        vals = fileName.split('_')
                        duration = int(vals[3][1:])/ 10
                        coordination = tuple(int(r) for r in vals[4][1:].split(' ')) if vals[4][1:] != '' else None
                        print(coordination)

                        if fileType == 'img':
                            status = compareColoredImg(os.path.join(filePath, file), duration, coordination)

                        elif fileType == 'txt':
                            status = textFunc(os.path.join(filePath, file), duration, coordination)

                if status:
                    versionParent = versionChild
                    stepNumber += 1
                    newFunc(versionParent,versionChild,stepNumber,files, filePath)
                else:
                    versionChild += 1
                    newFunc(versionParent,versionChild,stepNumber,files, filePath)

            