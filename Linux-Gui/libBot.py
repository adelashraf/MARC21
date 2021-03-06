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
    if '/CreationDate' in str(title.keys()):
        print '005', title['/CreationDate'].replace('D:', '')

    print '006 m#####s----#101#0#'
    print '007 cu#mn#---anuua'

    if '/ModDate' in str(title.keys()):
        print '008', title['/ModDate'][4:10], 's', title['/ModDate'][2:6], '####xx######s----#101#0#', '---', '#'
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

    print '300 ## $a', num, 'Pages. ;$c m.'

    num = int(num)
    x = 0
    while x < num:
        copy = '\xc2\xa9'
        # copy write
        page = fileReader.getPage(x)
        x = x + 1
        text = page.extractText()
        tex = text.encode("utf-8")
        if "LIBRARY OF CONGRESS CATALOGING-IN-PUBLICATION DATA".lower() in tex.lower():
            LOCCIPD = tex[int(tex.index('LIBRARY OF CONGRESS CATALOGING-IN-PUBLICATION DATA')):].replace('\xc5\xa0',
                                                                                                         '--').replace(
                '\n\n', '\n')
            LOCCIPd = LOCCIPD.replace('LIBRARY OF CONGRESS CATALOGING-IN-PUBLICATION DATA', '').splitlines()
            x2 = 0
            while x2 < len(LOCCIPd):
                if 'eISBN' in LOCCIPd[x2]:
                    print '020 ## $a', LOCCIPd[x2].replace('eISBN', '').replace('-', '')
                    print '650', '#0 $a', LOCCIPd[x2 + 1].replace('1.', '').replace('2.', '').replace('.',
                                                                                                             '').replace(
                        '--', '-')

                if ',' in LOCCIPd[x2] and '.' in LOCCIPd[x2]:
                    print '100 1# $a', LOCCIPd[x2]

                if ':' in LOCCIPd[x2] and '/' in LOCCIPd[x2] and '.' in LOCCIPd[x2]:
                    print '245 10 $a', LOCCIPd[x2].replace(':', ':$b').replace('/', '/$c')
                    print '250 ## $a', LOCCIPd[x2 + 1][int(LOCCIPd[x2 + 1].index('--')):].replace('--', '')
                    print '500 ## $a Caption Title'

                if 'p.' in LOCCIPd[x2] and 'm.' in LOCCIPd[x2]:
                    print '300 ## $a', num, LOCCIPd[x2].replace('m.', ';$c m.')

                if 'dc22' in LOCCIPd[x2] or 'dc23' in LOCCIPd[x2] or 'dc21' in LOCCIPd[x2]:
                    print '082 0# $a', LOCCIPd[x2].replace('--', '').replace('dc', ' $2 ')
                    print '084 ## $a', LOCCIPd[x2 - 1]

                if 'www' in LOCCIPd[x2]:
                    print '856 4# $u', LOCCIPd[x2]

                x2 = x2 + 1

        lista = tex.split()
        x1 = 0
        listlen = int(len(lista))
        while x1 < listlen:
            if 'Published' in lista[x1]:
                if x in range(0, 15) or x in range(num - 10, num):
                    Pub = lista[lista.index('Published'):lista.index('Published') + 20]
                    iN = ' '.join(Pub[int(Pub.index('in')):int(Pub.index('in')) + 4]).replace('in', '').replace(',', '')
                    by = ' '.join(Pub[int(Pub.index('by')):int(Pub.index('by')) + 3]).replace('by', '')
                    print '260 ## $a', iN, ':$b', by, ',$c', t260y

            if 'ISBN' in lista[x1]:
                if len(lista[x1]) == 4:
                    print '020 ## $a', lista[x1 + 1].replace('-', '')
                elif len(lista[x1]) == 5:
                    print '020 ## $a', lista[x1 + 1].replace('-', '')
                elif len(lista[x1]) == 7:
                    print '020 ## $a', lista[x1 + 1].replace('-', '')
                elif len(lista[x1]) == 8:
                    print '020 ## $a', lista[x1 + 1].replace('-', '')
                else:
                    if len(lista[x1]) == 3:
                        "!!"
                    elif len(lista[x1]) == 6:
                        "!!"
                    elif str(lista[x1])[6] == '3':
                        print '020 ## $a', str(lista[x1])[0:25].replace('ISBN-13:', '').replace('ISBN-10:', '').replace(
                            '-', '')
                        if str(lista[x1])[25] == 'I':
                            print '020 ## $a', str(lista[x1])[25:46].replace('ISBN-13:', '').replace('ISBN-10:',
                                                                                                     '').replace('-',
                                                                                                                 '')
                    elif str(lista[x1])[6] == '0':
                        print '020 ## $a', str(lista[x1])[0:20].replace('ISBN-13:', '').replace('ISBN-10:', '').replace(
                            '-', '')
                        if str(lista[x1])[20] == 'I':
                            print '020 ## $a', str(lista[x1])[20:46].replace('ISBN-13:', '').replace('ISBN-10:',
                                                                                                     '').replace('-',
                                                                                                                 '')

            if copy in lista[x1]:
                if x in range(0, 15):
                    year = lista[x1:x1 + 7]
                    x3 = 0
                    while x3 < len(year):
                        if '0' in year[x3] or '1' in year[x3] or '2' in year[x3] or '3' in year[x3] or '4' in year[
                            x3] or '5' in year[x3] or '6' in year[x3] or '7' in year[x3] or '8' in year[x3] or '9' in \
                                year[x3]:
                            t260y = str(year[x3])
                            if '/EBX_PUBLISHER' in str(title.keys()):
                                print '260 ## $a  :$b', title['/EBX_PUBLISHER'].replace('/', ''), ',$c ', t260y.replace(
                                    '\xc2\xa9', '')[0:4]

                            if '/Producer' in str(title.keys()):
                                print '264 #0 $a ', ':$b ', title.producer.encode("utf-8"), ',$c ', t260y.replace('\xc2\xa9', '')[0:4]
                            elif '/Producer' in str(title.keys()) and '/Creator' in str(title.keys()):
                                print '264 #0 $a ', ':$b ', title.producer.encode("utf-8"), ',$c ', t260y.replace('\xc2\xa9', '')[
                                                                                    0:4], '-$3 ', title.creator.encode("utf-8")
                            else:
                                print '264 #4 $c ', t260y.replace('\xc2\xa9', '')[0:4]

                        x3 = x3 + 1
                elif x in range(num - 10, num):
                    year = lista[x1:x1 + 7]
                    x3 = 0
                    while x3 < len(year):
                        if '0' in year[x3] or '1' in year[x3] or '2' in year[x3] or '3' in year[x3] or '4' in year[
                            x3] or '5' in year[x3] or '6' in year[x3] or '7' in year[x3] or '8' in year[x3] or '9' in \
                                year[x3]:
                            t260y = str(year[x3])
                            if '/Producer' in str(title.keys()):
                                print '264 #0 $a ', ':$b ', title.producer.encode("utf-8"), ',$c ', t260y.replace('\xc2\xa9', '')[0:4]
                            elif '/Producer' in str(title.keys()) and '/Creator' in str(title.keys()):
                                print '264 #0 $a ', ':$b ', title.producer.encode("utf-8"), ',$c ', t260y.replace('\xc2\xa9', '')[
                                                                                    0:4], '-$3 ', title.creator.encode("utf-8")
                            else:
                                print '264 #4 $c ', t260y.replace('\xc2\xa9', '')[0:4]

                        x3 = x3 + 1
            if "Copyright" in lista[x1]:
                if x in range(0, 15):
                    year = lista[x1:x1 + 7]
                    x3 = 0
                    while x3 < len(year):
                        if '0' in year[x3] or '1' in year[x3] or '2' in year[x3] or '3' in year[x3] or '4' in year[
                            x3] or '5' in year[x3] or '6' in year[x3] or '7' in year[x3] or '8' in year[x3] or '9' in \
                                year[x3]:
                            t260y = str(year[x3])

                        x3 = x3 + 1
                elif x in range(num - 10, num):
                    year = lista[x1:x1 + 7]
                    x3 = 0
                    while x3 < len(year):
                        if '0' in year[x3] or '1' in year[x3] or '2' in year[x3] or '3' in year[x3] or '4' in year[
                            x3] or '5' in year[x3] or '6' in year[x3] or '7' in year[x3] or '8' in year[x3] or '9' in \
                                year[x3]:
                            t260y = str(year[x3])

                        x3 = x3 + 1
            elif "COPYRIGHT" in lista[x1]:
                if x in range(0, 15):
                    year = lista[x1:x1 + 7]
                    x3 = 0
                    while x3 < len(year):
                        if '0' in year[x3] or '1' in year[x3] or '2' in year[x3] or '3' in year[x3] or '4' in year[
                            x3] or '5' in year[x3] or '6' in year[x3] or '7' in year[x3] or '8' in year[x3] or '9' in \
                                year[x3]:
                            t260y = str(year[x3])

                        x3 = x3 + 1
                elif x in range(num - 10, num):
                    year = lista[x1:x1 + 7]
                    x3 = 0
                    while x3 < len(year):
                        if '0' in year[x3] or '1' in year[x3] or '2' in year[x3] or '3' in year[x3] or '4' in year[
                            x3] or '5' in year[x3] or '6' in year[x3] or '7' in year[x3] or '8' in year[x3] or '9' in \
                                year[x3]:
                            t260y = str(year[x3])

                        x3 = x3 + 1

            if 'edition' in lista[x1].lower():
                if x in range(0, 15) or x in range(num - 10, num):
                    if 'first' in lista[x1].lower() or 'second' in lista[x1].lower() or 'third' in lista[
                        x1].lower() or 'fourth' in lista[x1].lower() or 'fifth' in lista[x1].lower() or 'sixth' in \
                            lista[x1].lower() or 'seventh' in lista[x1].lower() or 'eighth' in lista[
                        x1].lower() or 'ninth' in lista[x1].lower() or 'tenth' in lista[x1].lower() or 'eleventh' in \
                            lista[x1].lower():
                        ed = lista[x1].replace(',', ' ').lower()
                        print '250 ## $a', ed[int(ed.index('edition')) - 6:]

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
                        realcontent += str(B + '  --' + W + out2[y2].title.encode("utf-8") + '\n')
                        y2 = y2 + 1

                else:
                    realcontent += str(B + ' -' + W + out1[y1].title.encode("utf-8") + '\n')

                y1 =y1 +1
        else:
            realcontent += str(B + out[y].title.encode("utf-8") + W + '\n')
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

    #print '__'*15
    #print '\n', realcontent
    print '__'*25
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
