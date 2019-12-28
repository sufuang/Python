# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 15:12:50 2019

@author: syue003
"""



def parseXML(root,sm):
    print("A root:",root, "sm Bef:", sm)
    sm = sm + "/" + root.tag[root.tag.rfind('}')+1:]
    print("A sm _aft", sm)
    print("A type(root): ", type(root), "list(root):", list(root))
    for child in root:
      print("B Child", child)
      
      parseXML(child,sm)
    if len(list(root)) == 0:
        print("c_bef list(root) ", list(root), "len(list(root):",  len(list(root))
        
        my_list.append(sm)
        print("c_aft my_list: ", my_list) 
        

 Trace       
A root: <Element 'GetRetailStore' at 0x0000000008166638> sm Bef: 
A sm _aft /GetRetailStore
A type(root):  <class 'xml.etree.ElementTree.Element'> list(root): [<Element 'DocumentData' at 0x0000000008166688>, <Element 'RetailStoreData' at 0x0000000008105188>]
B Child <Element 'DocumentData' at 0x0000000008166688>

yue+: process 'DocumentData'
 child: 'Document',  'DocumentAction'
 yue_
B Child <Element 'Document' at 0x00000000081666D8>
A root: <Element 'DocumentData' at 0x0000000008166688> sm Bef: /GetRetailStore
A sm _aft /GetRetailStore/DocumentData
A type(root):  <class 'xml.etree.ElementTree.Element'> list(root): [<Element 'Document' at 0x00000000081666D8>, <Element 'DocumentAction' at 0x0000000008105098>]
B Child <Element 'Document' at 0x00000000081666D8>

yue+: process 'Document'
 child: 'Document',  'DocumentAction'
  xmlns:Abs="http://collab.safeway.com/it/architecture/info/default.aspx"
 yue_
A root: <Element 'Document' at 0x00000000081666D8> sm Bef: /GetRetailStore/DocumentData
A sm _aft /GetRetailStore/DocumentData/Document
A type(root):  <class 'xml.etree.ElementTree.Element'> list(root): [<Element '{http://collab.safeway.com/it/architecture/info/default.aspx}DocumentID' at 0x0000000008166728>, 
      <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}AlternateDocumentID' at 0x0000000008166778>, 
      <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}InboundOutboundInd' at 0x00000000081667C8>, 
      <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}DocumentNm' at 0x0000000008166818>, 
      <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}CreationDt' at 0x0000000008166868>, 
      <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}Description' at 0x00000000081668B8>, 
      <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}SourceApplicationCd' at 0x0000000008166908>, 
      <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}TargetApplicationCd' at 0x0000000008166958>, 
      <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}Note' at 0x00000000081669A8>, 
      <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}GatewayNm' at 0x00000000081669F8>, 
      <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}SenderId' at 0x0000000008166A48>, 
      <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}ReceiverId' at 0x0000000008166A98>, 
      <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}RoutingSystemNm' at 0x0000000008166AE8>, 
      <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}InternalFileTransferInd' at 0x0000000008166B38>, 
      <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}InterchangeDate' at 0x0000000008166B88>, 
      <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}InterchangeTime' at 0x0000000008166BD8>, 
      <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}ExternalTargetInd' at 0x0000000008166C28>, 
      <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}DataClassification' at 0x0000000008166C78>]
B Child <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}DocumentID' at 0x0000000008166728>
A root: <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}DocumentID' at 0x0000000008166728> sm Bef: /GetRetailStore/DocumentData/Document
A sm _aft /GetRetailStore/DocumentData/Document/DocumentID
A type(root):  <class 'xml.etree.ElementTree.Element'> list(root): []
c_bef list(root)  [] len(list(root): 0
c_aft my_list:  ['/GetRetailStore/DocumentData/Document/DocumentID']
B Child <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}AlternateDocumentID' at 0x0000000008166778>
A root: <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}AlternateDocumentID' at 0x0000000008166778> sm Bef: /GetRetailStore/DocumentData/Document
A sm _aft /GetRetailStore/DocumentData/Document/AlternateDocumentID
A type(root):  <class 'xml.etree.ElementTree.Element'> list(root): []
c_bef list(root)  [] len(list(root): 0
c_aft my_list:  ['/GetRetailStore/DocumentData/Document/DocumentID', '/GetRetailStore/DocumentData/Document/AlternateDocumentID']
B Child <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}InboundOutboundInd' at 0x00000000081667C8>
A root: <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}InboundOutboundInd' at 0x00000000081667C8> sm Bef: /GetRetailStore/DocumentData/Document
A sm _aft /GetRetailStore/DocumentData/Document/InboundOutboundInd
A type(root):  <class 'xml.etree.ElementTree.Element'> list(root): []
c_bef list(root)  [] len(list(root): 0
c_aft my_list:  ['/GetRetailStore/DocumentData/Document/DocumentID', '/GetRetailStore/DocumentData/Document/AlternateDocumentID', '/GetRetailStore/DocumentData/Document/InboundOutboundInd']
B Child <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}DocumentNm' at 0x0000000008166818>
A root: <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}DocumentNm' at 0x0000000008166818> sm Bef: /GetRetailStore/DocumentData/Document
A sm _aft /GetRetailStore/DocumentData/Document/DocumentNm
A type(root):  <class 'xml.etree.ElementTree.Element'> list(root): []
c_bef list(root)  [] len(list(root): 0
c_aft my_list:  ['/GetRetailStore/DocumentData/Document/DocumentID', '/GetRetailStore/DocumentData/Document/AlternateDocumentID', '/GetRetailStore/DocumentData/Document/InboundOutboundInd', '/GetRetailStore/DocumentData/Document/DocumentNm']
B Child <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}CreationDt' at 0x0000000008166868>
A root: <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}CreationDt' at 0x0000000008166868> sm Bef: /GetRetailStore/DocumentData/Document
A sm _aft /GetRetailStore/DocumentData/Document/CreationDt
A type(root):  <class 'xml.etree.ElementTree.Element'> list(root): []
c_bef list(root)  [] len(list(root): 0
c_aft my_list:  ['/GetRetailStore/DocumentData/Document/DocumentID', '/GetRetailStore/DocumentData/Document/AlternateDocumentID', '/GetRetailStore/DocumentData/Document/InboundOutboundInd', '/GetRetailStore/DocumentData/Document/DocumentNm', '/GetRetailStore/DocumentData/Document/CreationDt']
B Child <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}Description' at 0x00000000081668B8>
A root: <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}Description' at 0x00000000081668B8> sm Bef: /GetRetailStore/DocumentData/Document
A sm _aft /GetRetailStore/DocumentData/Document/Description
A type(root):  <class 'xml.etree.ElementTree.Element'> list(root): []
c_bef list(root)  [] len(list(root): 0
c_aft my_list:  ['/GetRetailStore/DocumentData/Document/DocumentID', '/GetRetailStore/DocumentData/Document/AlternateDocumentID', '/GetRetailStore/DocumentData/Document/InboundOutboundInd', '/GetRetailStore/DocumentData/Document/DocumentNm', '/GetRetailStore/DocumentData/Document/CreationDt', '/GetRetailStore/DocumentData/Document/Description']
B Child <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}SourceApplicationCd' at 0x0000000008166908>
A root: <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}SourceApplicationCd' at 0x0000000008166908> sm Bef: /GetRetailStore/DocumentData/Document
A sm _aft /GetRetailStore/DocumentData/Document/SourceApplicationCd
A type(root):  <class 'xml.etree.ElementTree.Element'> list(root): []
c_bef list(root)  [] len(list(root): 0
c_aft my_list:  ['/GetRetailStore/DocumentData/Document/DocumentID', '/GetRetailStore/DocumentData/Document/AlternateDocumentID', '/GetRetailStore/DocumentData/Document/InboundOutboundInd', '/GetRetailStore/DocumentData/Document/DocumentNm', '/GetRetailStore/DocumentData/Document/CreationDt', '/GetRetailStore/DocumentData/Document/Description', '/GetRetailStore/DocumentData/Document/SourceApplicationCd']
B Child <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}TargetApplicationCd' at 0x0000000008166958>
A root: <Element '{http://collab.safeway.com/it/architecture/info/default.aspx}TargetApplicationCd' at 0x0000000008166958> sm Bef: /GetRetailStore/DocumentData/Document

mylist:
    
['/GetRetailStore/DocumentData/Document/DocumentID', '/GetRetailStore/DocumentData/Document/AlternateDocumentID', '/GetRetailStore/DocumentData/Document/InboundOutboundInd',
 '/GetRetailStore/DocumentData/Document/DocumentNm', '/GetRetailStore/DocumentData/Document/CreationDt', '/GetRetailStore/DocumentData/Document/Description', 
 '/GetRetailStore/DocumentData/Document/SourceApplicationCd', '/GetRetailStore/DocumentData/Document/TargetApplicationCd', '/GetRetailStore/DocumentData/Document/Note', 
 '/GetRetailStore/DocumentData/Document/GatewayNm', '/GetRetailStore/DocumentData/Document/SenderId', '/GetRetailStore/DocumentData/Document/ReceiverId', 
 '/GetRetailStore/DocumentData/Document/RoutingSystemNm', '/GetRetailStore/DocumentData/Document/InternalFileTransferInd', '/GetRetailStore/DocumentData/Document/InterchangeDate', 
 '/GetRetailStore/DocumentData/Document/InterchangeTime', '/GetRetailStore/DocumentData/Document/ExternalTargetInd', 
 '/GetRetailStore/DocumentData/Document/DataClassification/DataClassificationLevel/Code', 
 '/GetRetailStore/DocumentData/Document/DataClassification/DataClassificationLevel/Description', 
 '/GetRetailStore/DocumentData/Document/DataClassification/DataClassificationLevel/ShortDescription', 
 '/GetRetailStore/DocumentData/Document/DataClassification/BusinessSensitivityLevel/Code', 
 '/GetRetailStore/DocumentData/Document/DataClassification/BusinessSensitivityLevel/Description', 
 '/GetRetailStore/DocumentData/Document/DataClassification/BusinessSensitivityLevel/ShortDescription', '/GetRetailStore/DocumentData/Document/DataClassification/PHIdataInd', 
 '/GetRetailStore/DocumentData/Document/DataClassification/PCIdataInd', '/GetRetailStore/DocumentData/Document/DataClassification/PIIdataInd', '/GetRetailStore/DocumentData/DocumentAction/ActionTypeCd', '/GetRetailStore/DocumentData/DocumentAction/RecordTypeCd', '/GetRetailStore/RetailStoreData/Corporation/CorporationId', '/GetRetailStore/RetailStoreData/Corporation/CorporationNm', '/GetRetailStore/RetailStoreData/Corporation/InCorporationCountryCd', '/GetRetailStore/RetailStoreData/Corporation/InCorporationDt', '/GetRetailStore/RetailStoreData/Corporation/CountryCd', '/GetRetailStore/RetailStoreData/Corporation/CorporationAddress/AddressUsageTypeCd', '/GetRetailStore/RetailStoreData/Corporation/CorporationAddress/AddressLine1txt', '/GetRetailStore/RetailStoreData/Corporation/CorporationAddress/AddressLine2txt', '/GetRetailStore/RetailStoreData/Corporation/CorporationAddress/CityNm', '/GetRetailStore/RetailStoreData/Corporation/CorporationAddress/CountyNm', '/GetRetailStore/RetailStoreData/Corporation/CorporationAddress/PostalZoneCd', '/GetRetailStore/RetailStoreData/Corporation/CorporationAddress/StateCd', '/GetRetailStore/RetailStoreData/Corporation/CorporationAddress/CountryCd', '/GetRetailStore/RetailStoreData/Corporation/CorporationAddress/LatitudeDegree', '/GetRetailStore/RetailStoreData/Corporation/CorporationAddress/LongitudeDegree', '/GetRetailStore/RetailStoreData/Corporation/CorporationAddress/TimeZoneCd', '/GetRetailStore/RetailStoreData/Corporation/CorporationAddress/PhoneNbr', '/GetRetailStore/RetailStoreData/Corporation/CorporationAddress/FaxNbr', '/GetRetailStore/RetailStoreData/Division/DivisionId', '/GetRetailStore/RetailStoreData/Division/DivisionNm', '/GetRetailStore/RetailStoreData/Division/SalesTypeCd', '/GetRetailStore/RetailStoreData/Division/SalesChannelCd', '/GetRetailStore/RetailStoreData/Division/AdminDivisionInd', '/GetRetailStore/RetailStoreData/Division/BusinessTypeCd', '/GetRetailStore/RetailStoreData/Division/DivisionAddress/AddressUsageTypeCd', '/GetRetailStore/RetailStoreData/Division/DivisionAddress/AddressLine1txt', '/GetRetailStore/RetailStoreData/Division/DivisionAddress/AddressLine2txt', '/GetRetailStore/RetailStoreData/Division/DivisionAddress/CityNm', '/GetRetailStore/RetailStoreData/Division/DivisionAddress/CountyNm', '/GetRetailStore/RetailStoreData/Division/DivisionAddress/PostalZoneCd', '/GetRetailStore/RetailStoreData/Division/DivisionAddress/StateCd', '/GetRetailStore/RetailStoreData/Division/DivisionAddress/CountryCd', '/GetRetailStore/RetailStoreData/Division/DivisionAddress/LatitudeDegree', '/GetRetailStore/RetailStoreData/Division/DivisionAddress/LongitudeDegree', '/GetRetailStore/RetailStoreData/Division/DivisionAddress/TimeZoneCd', '/GetRetailStore/RetailStoreData/Division/DivisionAddress/PhoneNbr', '/GetRetailStore/RetailStoreData/Division/DivisionAddress/FaxNbr', '/GetRetailStore/RetailStoreData/Division/AccountingUnitNm', '/GetRetailStore/RetailStoreData/Division/LevelDsc', '/GetRetailStore/RetailStoreData/ReportingDivision/DivisionId', '/GetRetailStore/RetailStoreData/ReportingDivision/DivisionNm', '/GetRetailStore/RetailStoreData/ReportingDivision/SalesTypeCd', '/GetRetailStore/RetailStoreData/ReportingDivision/SalesChannelCd', '/GetRetailStore/RetailStoreData/ReportingDivision/AdminDivisionInd', '/GetRetailStore/RetailStoreData/ReportingDivision/BusinessTypeCd', '/GetRetailStore/RetailStoreData/ReportingDivision/DivisionAddress/AddressUsageTypeCd', '/GetRetailStore/RetailStoreData/ReportingDivision/DivisionAddress/AddressLine1txt', '/GetRetailStore/RetailStoreData/ReportingDivision/DivisionAddress/AddressLine2txt', '/GetRetailStore/RetailStoreData/ReportingDivision/DivisionAddress/CityNm', '/GetRetailStore/RetailStoreData/ReportingDivision/DivisionAddress/CountyNm', '/GetRetailStore/RetailStoreData/ReportingDivision/DivisionAddress/PostalZoneCd', '/GetRetailStore/RetailStoreData/ReportingDivision/DivisionAddress    
        