#!/usr/bin/python
# encoding=utf8

import PyPDF2
import sys

# Console colors
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
B = '\033[34m'  # blue


def all(tnum, id1, id2, subf1, texf1, subf2, texf2, subf3, texf3, subf4, texf4):
    if subf3 == '' and texf3 == '' and subf4 == '' and texf4 == '':
        fxml.write(
            '          <datafield tag="' + tnum + '" ind1="' + id1 + '" ind2="' + id2 + '">\n            <subfield code="' + subf1 + '">' + texf1 + '</subfield>\n            <subfield code="' + subf2 + '">' + texf2 + '</subfield>\n          </datafield>\n')
    elif subf4 == '' and texf4 == '':
        fxml.write(
            '          <datafield tag="' + tnum + '" ind1="' + id1 + '" ind2="' + id2 + '">\n            <subfield code="' + subf1 + '">' + texf1 + '</subfield>\n            <subfield code="' + subf2 + '">' + texf2 + '</subfield>\n            <subfield code="' + subf3 + '">' + texf3 + ' </subfield>\n          </datafield>\n')
    else:
        fxml.write(
            '          <datafield tag="' + tnum + '" ind1="' + id1 + '" ind2="' + id2 + '">\n            <subfield code="' + subf1 + '">' + texf1 + '</subfield>\n            <subfield code="' + subf2 + '">' + texf2 + '</subfield>\n            <subfield code="' + subf3 + '">' + texf3 + ' </subfield>\n            <subfield code="' + subf4 + '">' + texf4 + '</subfield>\n          </datafield>\n')


try:
    fxml = open('marcrecord.xml', 'w')
    fxml.write('''<zs:searchRetrieveResponse xmlns:zs="http://www.mans.edu.eg">
  <zs:version>1.1</zs:version>
  <zs:numberOfRecords>1</zs:numberOfRecords>
  <zs:records>
    <zs:record>
      <zs:recordSchema>info:srw/schema/1/marcxmlv1.1</zs:recordSchema>
      <zs:recordPacking>xml</zs:recordPacking>
      <zs:recordData>
        <record xmlns="http://www.mans.edu.eg">
          <leader>00000ntm##2200000#a#0000</leader>
          <controlfield tag="001">12345678</controlfield>
          <controlfield tag="003">FFF</controlfield>\n''')
    file = open(sys.argv[1], 'rb')
    fileReader = PyPDF2.PdfFileReader(file)
    num = fileReader.numPages

    out = fileReader.outlines
    title = fileReader.getDocumentInfo()
    print '\nScanning The pdf file \n '
    if '/CreationDate' in str(title.keys()):
        fxml.write('          <controlfield tag="005">' + title['/CreationDate'].replace('D:', '')[0:14] + '</controlfield>\n')
        print '005', title['/CreationDate'].replace('D:', '')[0:14]

    print '006 m#####s----#101#0#'
    print '007 cu#mn#---anuua'

    if '/ModDate' in str(title.keys()):
        fxml.write('          <controlfield tag="008">' + title['/ModDate'][4:10] + 's' + title['/ModDate'][2:6] + '####xx#ka##frmb###000#0#' + 'eng' + '#' + 'c' + '</controlfield>\n')
        print '008', title['/ModDate'][4:10] + 's' + title['/ModDate'][2:6] + '####xx#ka##frmb###000#0#' + 'eng' + '#' + 'c'
        print '040 ## $a EG-EULC , $c EG-EULC , $a NAME'

    if '/Producer' in str(title.keys()):
        print '508 ## $a Software used in production :', title['/Producer'].encode("utf-8")

    if '/Creator' in str(title.keys()):
        print '508 ## $a software used in creation :', title['/Creator'].encode("utf-8")

    if '/Subject' in str(title.keys()):
        print '650', '## $a ', title.subject.encode("utf-8")

    if '/Keywords' in str(title.keys()):
        print '650', '## $a ', title['/Keywords'].encode("utf-8")

    print '300 ## $a', num, 'p. ;$c cm.'

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
            print '041 ## $a ara , $b ara , $b eng ,$a NAME'
            print '546 ## $a The Text in arabic and English '
        else:
            degree = 'NONE'
        x1 = 0
        listlen = int(len(lista))
        # print lista
        # if 'university' in lista and 'faculty' in lista and 'department' in lista or 'university' in lista and 'faculty' in lista:
        while x1 < listlen:
            if 'university' in lista[x1] and 'faculty' in lista[x1 + 1] and 'department' in lista:
                v = x1 + 1
                while v < listlen:
                    if 'department' in lista[v]:
                        print '502 ## $a Thesis $b', degree, '--$c', ' '.join(lista[x1 - 1:v + 1]), ',$d', title['/CreationDate'].replace('D:', '')[0:4]
                        all('502', '#', '#', 'a', 'Thesis ' + degree + ' - ' + ' '.join(lista[x1 - 1:v + 1]), 'a', '  ', '', '', '', '' )
                        print '539 ## $a', title['/CreationDate'].replace('D:', '')[0:4]
                        print '533 ## $a National Network of University Letters . $b EG :$c Ain Shams University Archives ,$d', \
                        title['/CreationDate'].replace('D:', '')[0:4]
                        v4 = v
                        while v4 < listlen:
                            if 'by' in lista[v4]:
                                print '100 1# $a', ' '.join(lista[v4:v4 + 4]).replace('by', '')
                                print '245 10 $a', ' '.join(lista[v + 1:v4])
                                fxml.write(
                                    '          <datafield tag="000" ind1="0" ind2="0">\n            <subfield code="a">' + ' '.join(
                                        lista[v + 1:v4]) + ' /</subfield>\n' + '          </datafield>\n')
                                fxml.write(
                                    '          <datafield tag="040" ind1="#" ind2="#">\n            <subfield code="a">EG-EULC</subfield>\n            <subfield code="c">EG-EULC</subfield>\n            <subfield code="a">' + ' '.join(
                                        lista[v + 1:v4]) + ' /</subfield>\n          </datafield>\n')
                                all('041', '0', '#', 'a', 'eng', 'b', 'eng', 'b', 'ara', 'a', ' '.join(lista[v + 1:v4]))
                                all('082', '0', '4', '2', '21', 'a', ' ', 'a', ' '.join(lista[v + 1:v4]), '', '')
                                all('100', '1', '#', 'a', ' '.join(lista[v4:v4 + 4]).replace('by', ''), 'a',
                                    ' '.join(lista[v + 1:v4]), '', '', '', '')
                                all('245', '1', '0', 'a', ' '.join(lista[v + 1:v4]), 'c',
                                    ' '.join(lista[v4:v4 + 4]).replace('by', ''), '', '', '', '')
                                all('246', '1', '5', 'a', '  ', 'a', ' '.join(lista[v + 1:v4]), '', '', '', '')
                                all('260', '#', '#', 'c', title['/ModDate'][2:6], 'a', ' '.join(lista[v + 1:v4]), '', '', '', '')
                                all('300', '#', '#', 'a', str(num)+' p. :', 'b', 'ill. ;', 'c', '30 cm.', 'e', '+ 1 c.d.')

                            v4 = v4 + 1

                    v = v + 1

            elif 'university' in lista[x1] and 'faculty' in lista[x1 + 1]:
                print '502 ## $a Thesis $b', degree, '--$c', ' '.join(lista[x1 - 1:x1 + 5]), ',$d', title['/CreationDate'].replace('D:', '')[0:4]
                all('502', '#', '#', 'a', 'Thesis ' + degree + ' - ' + ' '.join(lista[x1 - 1:x1 + 5]), 'a', '  ', '', '', '', '')
                print '539 ## $a', title['/CreationDate'].replace('D:', '')[0:4]
                print '533 ## $a National Network of University Letters . $b EG :$c Ain Shams University Archives ,$d', \
                title['/CreationDate'].replace('D:', '')[0:4]
                if 'of' in lista[x1 + 2]:
                    v3 = x1 + 4
                    while v3 < listlen:
                        if 'by' in lista[v3]:
                            feald = lista[x1 + 4:v3]
                            if 'supervis' in str(feald):
                                print '100 1# $a', ' '.join(feald[int(feald.index('by')):len(feald) - 1]).replace('by ','')
                                print '245 10 $a', ' '.join(feald[:len(feald) - 1]).replace('by', '/$c')
                                fxml.write('          <datafield tag="000" ind1="0" ind2="0">\n            <subfield code="a">' + ' '.join(feald[:int(feald.index('by'))]).replace('by ','') + ' /</subfield>\n' + '          </datafield>\n')
                                fxml.write('          <datafield tag="040" ind1="#" ind2="#">\n            <subfield code="a">EG-EULC</subfield>\n            <subfield code="c">EG-EULC</subfield>\n            <subfield code="a">' + ' '.join(feald[:int(feald.index('by'))]).replace('by ','') + ' /</subfield>\n          </datafield>\n')
                                all('041', '0', '#', 'a', 'eng', 'b', 'eng', 'b', 'ara', 'a',' '.join(feald[:int(feald.index('by'))]).replace('by ', ''))
                                all('082', '0', '4', '2', '21', 'a', ' ', 'a', ' '.join(feald[:int(feald.index('by'))]).replace('by ',''), '', '')
                                all('100', '1', '#', 'a', ' '.join(feald[int(feald.index('by')):len(feald) - 1]).replace('by ',''), 'a', ' '.join(feald[:int(feald.index('by'))]).replace('by ',''), '', '', '', '')
                                all('245', '1', '0', 'a', ' '.join(feald[:int(feald.index('by'))]).replace('by ',''), 'c', ' '.join(feald[int(feald.index('by')):len(feald) - 1]).replace('by ',''), '', '', '', '')
                                all('246', '1', '5', 'a', '  ', 'a', ' '.join(feald[:int(feald.index('by'))]).replace('by ',''), '', '', '', '')
                                all('260', '#', '#', 'c', title['/ModDate'][2:6], 'a', ' '.join(feald[:int(feald.index('by'))]).replace('by ',''), '', '', '', '')
                                all('300', '#', '#', 'a', str(num)+' p. :', 'b', 'ill. ;', 'c', '30 cm.', 'e', '+ 1 c.d.')

                        v3 = v3 + 1

            if 'degree' in lista[x1] and 'in' in lista[x1 + 1]:
                print '650 ## $a', lista[x1 + 2], lista[x1 + 3]
                all('650', '#', '#', 'a', lista[x1 + 2]+ lista[x1 + 3], 'a', ' ', '', '', '', '')
                v1 = x1 + 3
                while v1 < listlen:
                    if 'by' in lista[v1]:
                        v2 = v1
                        while v2 < listlen:
                            if 'supervis' in lista[v2]:
                                print '100 1# $a', ' '.join(lista[v1 + 1:v2]), ', $a NAME'
                                print '245 10 $a', ' '.join(lista[:v1])
                                fxml.write('          <datafield tag="000" ind1="0" ind2="0">\n            <subfield code="a">' + ' '.join(lista[:v1]) + ' /</subfield>\n' + '          </datafield>\n')
                                fxml.write('          <datafield tag="040" ind1="#" ind2="#">\n            <subfield code="a">EG-EULC</subfield>\n            <subfield code="c">EG-EULC</subfield>\n            <subfield code="a">' + ' '.join(lista[:v1]) + ' /</subfield>\n          </datafield>\n')
                                print '500 ## $a ', ' '.join(lista[v2:])
                                all('041', '0', '#', 'a', 'eng', 'b', 'eng', 'b', 'ara', 'a', ' '.join(lista[:v1]))
                                all('082', '0', '4', '2', '21', 'a', ' ', 'a', ' '.join(lista[:v1]), '', '')
                                all('100', '1', '#', 'a', ' '.join(lista[v1 + 1:v2]), 'a', ' '.join(lista[:v1]), '', '', '', '')
                                all('245', '1', '0', 'a', ' '.join(lista[:v1]), 'c', ' '.join(lista[v1 + 1:v2])+' ;'+' '.join(lista[v2:]), '', '', '', '')
                                all('246', '1', '5', 'a', ' ', 'a', ' '.join(lista[:v1]), '', '', '', '')
                                all('260', '#', '#', 'c', title['/ModDate'][2:6], 'a', ' '.join(lista[:v1]), '', '', '', '')
                                all('300', '#', '#', 'a', str(num)+' p. :', 'b', 'ill. ;', 'c', '30 cm.', 'e', '+ 1 c.d.')

                            v2 = v2 + 1
                    v1 = v1 + 1
            elif 'degree' in lista[x1] and 'of' in lista[x1 + 1] and 'in' in lista[x1 + 3]:
                print '650 ## $a', lista[x1 + 4], lista[x1 + 5]
                all('650', '#', '#', 'a', lista[x1 + 4]+ lista[x1 + 5], 'a', ' ', '', '', '', '')
            elif 'degree' in lista[x1] and 'of' in lista[x1 + 1] and 'of' in lista[x1 + 3]:
                print '650 ## $a', lista[x1 + 4], lista[x1 + 5]
                all('650', '#', '#', 'a', lista[x1 + 4]+ lista[x1 + 5], 'a', ' ', '', '', '', '')

            # if 'http' in lista[x1]:
            #    print '856 4# $u', lista[x1]

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
                        realcontent += str(out2[y2].title.encode("utf-8") + '--')
                        y2 = y2 + 1

                else:
                    realcontent += str(out1[y1].title.encode("utf-8") + '--')

                y1 = y1 + 1
        else:
            realcontent += str(out[y].title.encode("utf-8") + '--')
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
        print '505 0# $a', str(contenttype[int(contenttype.index('contents')):]).replace("'contents',", '').replace("'",
                                                                                                                    '').replace(
            '[', '').replace(']', '').replace("\r", '').replace(',', '--').replace(' ', '-').replace('part', 'P.')
    elif 'contents' in str(contenttype):
        print '505 0# $a', str(contenttype[2:]).replace("'contents',", '').replace("'", '').replace('[', '').replace(
            ']', '').replace("\r", '').replace(',', '--').replace(' ', '-').replace('part', 'P.')
    # else:
    #    print '505 0# $a', str(contenttype).replace("'", '').replace('[', '').replace(']', '').replace("\r", '').replace(',', '--').replace(' ', '-').replace('part', 'P.')

    if '\xd9\x81\xd9\x87\xd8\xb1\xd8\xb3' in realcontent.lower():
        print '500 ## $a includes index'

    if '\xd9\x85\xd8\xb1\xd8\xa7\xd8\xac\xd8\xb9' in realcontent.lower():
        print '500 ## $a includes Reference'

    if '\xd9\x85\xd9\x84\xd8\xa7\xd8\xad\xd9\x82' in realcontent.lower():
        print '500 ## $a includes Supplements'

    if '\xd9\x85\xd9\x84\xd8\xae\xd8\xb5' in realcontent.lower():
        print '500 ## $a includes Abstract'

    print '505 0# $a ', realcontent

    fxml.write('''        </record>
      </zs:recordData>
    </zs:record>
  </zs:records>
</zs:searchRetrieveResponse>
''')

    print "\n finish!"
except IndexError:
    print "please write the name of pdf file"
    print "Example : ", sys.argv[0], " file.pdf "
    exit()
except KeyboardInterrupt:
    print '\nYou press Ctrl+C'
    exit()
except IOError:
    print 'Please Write The correct Path of Pdf file !'
    exit()
except PyPDF2.utils.PdfReadError:
    print 'Cannot open the pdf'
    exit()
