import requests

url = "http://10.203.135.75:8092/SIO"

headers = {
    'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction': ''
}

# XML corregido con el Header completo
soap_body = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Header>
      <ns5:HeaderRequest xmlns:ns5="http://telefonica.com/globalIntegration/header">
         <ns5:system>
            <ns5:systemId>SIO</ns5:systemId>
            <ns5:name>ValidatePersonPCO</ns5:name>
            <ns5:operation>ValidatePersonPCO</ns5:operation>
         </ns5:system>
         <ns5:service>
            <ns5:name>ValidatePersonPCO</ns5:name>
            <ns5:version>v1</ns5:version>
         </ns5:service>
         <ns5:transaction>
            <ns5:id>1012025040919750154</ns5:id>
            <ns5:timestamp>2025-02-10T10:03:32</ns5:timestamp>
         </ns5:transaction>
      </ns5:HeaderRequest>
   </soapenv:Header>
   <soapenv:Body>
      <ns2:Request xmlns:ns2="http://sio.experian.com/">
         <B2CInputWS>
            <Applicant>
               <ID>
                  <CustIDType>CC</CustIDType>
                  <CustIDNumber>52976918</CustIDNumber>
                  <CustIDExpeditionDate>2001-12-05</CustIDExpeditionDate>
               </ID>
               <TransactionID>1012025040919750154</TransactionID>
               <CustFirstLastname>TIGA</CustFirstLastname>
               <CustFlag>1</CustFlag>
               <CustValDate>2019-04-09</CustValDate>
               <CustMonthlyFee>102990</CustMonthlyFee>
               <CustInitialAmnt>100000000000</CustInitialAmnt>
            </Applicant>
            <Transaction>
               <TypeEval>1</TypeEval>
               <TypeTrans>029</TypeTrans>
            </Transaction>
            <CurrentSubscriptions>
               <SubscriptionAge>
                  <CustNameProdSubscriptionDate>BROADBAND SERVICE</CustNameProdSubscriptionDate>
                  <CustDateProdSubscriptionDate>2025-04-09</CustDateProdSubscriptionDate>
                  <CustModProdSubscriptionDate>POSPAGO</CustModProdSubscriptionDate>
               </SubscriptionAge>
               <CustLimitAvailableCreditAmount>608839</CustLimitAvailableCreditAmount>
            </CurrentSubscriptions>
            <NewSubscriptions>
               <PrimaryOffers>
                  <PrimaryProducts>
                     <CustIDProductPrymOffer>24382</CustIDProductPrymOffer>
                     <CustNameProductPrymOffer>BROADBAND SERVICE</CustNameProductPrymOffer>
                     <ExistingProduct>1</ExistingProduct>
                  </PrimaryProducts>
                  <Autopay>NO</Autopay>
               </PrimaryOffers>
               <CustPrimaryOfferingValue>87491</CustPrimaryOfferingValue>
               <SalesChannel>0205</SalesChannel>
               <BusinessChannel>601</BusinessChannel>
               <TypeOffer>0002</TypeOffer>
               <CustQtyLinesRqtd>1</CustQtyLinesRqtd>
               <CustSumNewSupplementaryOffering>15499</CustSumNewSupplementaryOffering>
               <Address>
                  <CustSocialLevel>9</CustSocialLevel>
                  <CustReg>01</CustReg>
                  <CustDept>11</CustDept>
                  <CustCity>001</CustCity>
                  <CustNeighborhood>110010001146</CustNeighborhood>
                  <CustAddress>CRA 21 9 10</CustAddress>
                  <CustAddressShield>10</CustAddressShield>
               </Address>
               <TypeProduct>2</TypeProduct>
            </NewSubscriptions>
            <Seller>
               <SellerReg>01</SellerReg>
               <SellerDept>63</SellerDept>
               <SellerCity>11001000</SellerCity>
               <SellerCode>659309</SellerCode>
               <SellerOffice>99-002-1008-0028</SellerOffice>
            </Seller>
         </B2CInputWS>
      </ns2:Request>
   </soapenv:Body>
</soapenv:Envelope>
"""

try:
    response = requests.post(url, data=soap_body, headers=headers, timeout=30)

    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{response.text}")

except requests.exceptions.RequestException as e:
    print(f"Error en la petición: {e}")