#!/usr/bin/python
# encoding=utf8

import PyPDF2
import sys

# Console colors
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
B = '\033[34m'  # blue

try:
    file = open(sys.argv[1], 'rb')
    fileReader = PyPDF2.PdfFileReader(file)
    num = fileReader.numPages

    out = fileReader.outlines
    title = fileReader.getDocumentInfo()
    print G, '\nScanning The pdf file \n ', W
    if '/CreationDate' in str(title.keys()):
        print '005', title['/CreationDate'].replace('D:', '')

    print '006 m#####s----#101#0#'
    print '007 cu#mn#---anuua'

    if '/ModDate' in str(title.keys()):
        print '008', title['/ModDate'][4:10], 's', title['/ModDate'][2:6], '####xx######s----#101#0#', 'ara', '#'
        print '040 ## $a DLC'

    if '/Producer' in str(title.keys()):
        print '508 ## $a Software used in production :', title['/Producer']

    if '/Creator' in str(title.keys()):
        print '508 ## $a software used in creation :', title['/Creator']

    if '/Author' in str(title.keys()):
        print '100	1# $a ', title.author.encode("utf-8")

    if '/Title' in str(title.keys()):
        if '/Author' in str(title.keys()):
            print '245 10 $a', str(title.title.encode("utf-8")).replace(':', ' :$b '), ' /$c ', str(title.author.encode("utf-8"))
            if ':' in str(title.title.encode("utf-8")):
                print '500 ## $a Caption Title'
        else:
            print '245 10 $a', title.title.encode("utf-8")

    if '/Subject' in str(title.keys()):
        print '650', '## $a ', title.subject.encode("utf-8")

    if '/Keywords' in str(title.keys()):
        print '650', '## $a ', title['/Keywords'].encode("utf-8")

    print '300 ## $a', num, 'Leaves. ;$c m.'

    num = int(num)
    x = 0
    while x < num:
        copy = '\xc2\xa9'
        # copy write
        page = fileReader.getPage(x)
        x = x + 1
        text = page.extractText()
        tex = text.encode("utf-8", 'ignore').lower()
        lista = tex.split()

        if 'master' in str(lista) and 'degree' in str(lista):
            degree = 'master degree'
            print '041 ## $a ara , $b ara , $b eng'
            print '546 ## $a The Text in arabic and English '
        x1 = 0
        listlen = int(len(lista))
        #print lista
        if 'university' in lista and 'faculty' in lista and 'department' in lista:
            while x1 < listlen:
                if 'university' in lista[x1] and 'faculty' in lista[x1+1]:
                    v = x1+1
                    while v<listlen:
                        if 'department' in lista[v]:
                            print '502 ## $a Thesis $b', degree, '--$c',  ' '.join(lista[x1-1:v+1]), ',$d', title['/CreationDate'].replace('D:', '')[0:4]
                            print '539 ## $a', title['/CreationDate'].replace('D:', '')[0:4]
                            print '533 ## $a National Network of University Letters . $b EG :$c Ain Shams University Archives ,$d', title['/CreationDate'].replace('D:', '')[0:4]
                        v = v+1

                if 'degree' in lista[x1] and 'in' in lista[x1+1]:
                    print '650 ## $a', lista[x1+2], lista[x1+3]
                    v1 = x1+3
                    while v1 < listlen:
                        if 'by' in lista[v1]:
                            v2 = v1
                            while v2 < listlen:
                                if 'supervis' in lista[v2]:
                                    print '100 1# $a', ' '.join(lista[v1+1:v2])
                                    print '500 ## $a ', ' '.join(lista[v2:])

                                v2 = v2 + 1
                        v1 = v1 + 1

                if 'http' in lista[x1]:
                    print '856 4# $u', lista[x1]

                x1 = x1 + 1

    outlen = len(out)
    contenttype = []
    realcontent = ''
    y = 0
    while y < outlen:
        if '[' in str(out[y]):
            out1 = out[y]
            y1 = 0
            while y1 < len(out1):
                if '[' in str(out1[y1]):
                    out2 = out1[y1]
                    y2 = 0
                    while y2 < len(out2):
                        realcontent += str(out2[y2].title.encode("utf-8")+ '--')
                        y2 = y2 + 1

                else:
                    realcontent += str(out1[y1].title.encode("utf-8")+ '--')

                y1 =y1 +1
        else:
            realcontent += str(out[y].title.encode("utf-8")+ '--')
            contenttype.append(str(out[y].title.encode("utf-8")).lower())
            if 'isbn' in str(out[y]).lower():
                print '020 ## $a', str(out[y].title.encode("utf-8")).lower().replace('isbn', '').replace('-', '')

            if 'contents' in str(out[y]).lower():
                print '500 ## $a includes contents'

            if 'acknowledgments' in str(out[y]).lower():
                print '500 ## $a includes acknowledgments'

            if 'introduction' in str(out[y]).lower():
                print '500 ## $a includes Introduction'

            if 'map' in str(out[y]).lower():
                print '500 ## $a includes map'

            if 'preface' in str(out[y]).lower():
                print '500 ## $a includes Preface'

            if 'appendix' in str(out[y]).lower():
                print '500 ## $a includes Appendix'

            if 'references' in str(out[y]).lower():
                print '500 ## $a includes References'

            if 'photo credits' in str(out[y]).lower():
                print '500 ## $a includes Photo Credits'

            if 'index' in str(out[y]).lower():
                print '500 ## $a includes Index'

            if 'name index' in str(out[y]).lower():
                print '510 1# $a name index'

            if 'subject index' in str(out[y]).lower():
                print '510 1# $a Subject index'

            if 'bibliography' in str(out[y]).lower():
                print '504 ## $a Bibliography'

        y = y + 1
    if 'contents' in contenttype:
        print '505 0# $a', str(contenttype[int(contenttype.index('contents')):]).replace("'contents',", '').replace("'", '').replace('[', '').replace(']', '').replace("\r", '').replace(',', '--').replace(' ', '-').replace('part', 'P.')
    elif 'contents' in str(contenttype):
        print '505 0# $a', str(contenttype[2:]).replace("'contents',", '').replace("'", '').replace('[', '').replace(']', '').replace("\r", '').replace(',', '--').replace(' ', '-').replace('part', 'P.')
    else:
        print '505 0# $a', str(contenttype).replace("'", '').replace('[', '').replace(']', '').replace("\r", '').replace(',', '--').replace(' ', '-').replace('part', 'P.')

    if '\xd9\x81\xd9\x87\xd8\xb1\xd8\xb3' in realcontent.lower():
        print '500 ## $a includes index'

    if '\xd9\x85\xd8\xb1\xd8\xa7\xd8\xac\xd8\xb9' in realcontent.lower():
        print '500 ## $a includes Reference'

    if '\xd9\x85\xd9\x84\xd8\xa7\xd8\xad\xd9\x82' in realcontent.lower():
        print '500 ## $a includes Supplements'

    if '\xd9\x85\xd9\x84\xd8\xae\xd8\xb5' in realcontent.lower():
        print '500 ## $a includes Abstract'

    print '505 0# $a ', realcontent
    print G, "\n finish!", W
except IndexError:
    print R + "please write the name of pdf file" + W
    print G, "Example : ", W, sys.argv[0], " file.pdf "
    exit()
except KeyboardInterrupt:
    print R, '\nYou press Ctrl+C', W
    exit()
except IOError:
    print R, 'Please Write The correct Path of Pdf file !', W
    exit()
