
class A:


    @classmethod
    def method_1(cls, some_field: dict) -> None:
        some_field['key_1'] = 'new_value_1'
        some_field['key_2'] = 'value_2'

    @classmethod
    def method_2(cls):

        my_dict = {
            'field_1': {},
            'field_2': {}
        }
        print(my_dict)
        cls.method_1(my_dict['field_1'])
        print(my_dict)

if __name__ == "__main__":
    A.method_2()



res = {
                    "driveStatus": False,
                    "dynamicLotDetails": {
                        "errorCode": "",
                        "buyerNumber": 1,
                        "source": "web",
                        "buyTodayBid": 0.0,
                        "currentBid": 0,
                        "totalAmountDue": 0.0,
                        "sealedBid": False,
                        "firstBid": True,
                        "hasBid": False,
                        "sellerReserveMet": False,
                        "lotSold": False,
                        "bidStatus": "NEVER_BID",
                        "saleStatus": "PURE_SALE",
                        "counterBidStatus": "DEFAULT",
                        "startingBidFlag": False,
                        "buyerHighBidder": False,
                        "anonymous": False,
                        "nonSyncedBuyer": False
                    },
                    "vehicleTypeCode": "VEHTYPE_V",
                    "memberVehicleType": "AUTOMOBILE",
                    "odometerUOM": "A",
                    "showClaimForm": False,
                    "lotPlugAcv": 0.0,
                    "readyForReplayFlag": False,
                    "carFaxReportAvailable": "",
                    "lotNumberStr": "74928564",
                    "lotYardSameAsKioskYard": False,
                    "pwlot": False,
                    "ln": 74928564,
                    "mkn": "SUBARU",
                    "lmg": "CROSSTREK",
                    "lm": "CROSSTREK",
                    "mmod": "CROSSTREK",
                    "lcy": 2024,
                    "fv": "4S4GUHM60R3******",
                    "la": 30125.5,
                    "rc": 27566.48,
                    "obc": "A",
                    "orr": 11797.0,
                    "lfd": [
                        "No License Required"
                    ],
                    "ord": "ACTUAL",
                    "egn": "2.5L  4",
                    "cy": "4",
                    "ld": "2024 SUBARU CROSSTREK LIMITED",
                    "yn": "PA - PITTSBURGH SOUTH",
                    "cuc": "USD",
                    "tz": "EST",
                    "ad": 1732114800000,
                    "lad": 1728025200000,
                    "at": "10:00:00",
                    "hb": 0.0,
                    "ss": 5,
                    "bndc": "",
                    "bnp": 0.0,
                    "sbf": False,
                    "ts": "PA",
                    "stt": "SC",
                    "td": "CERTIFICATE OF SALVAGE",
                    "tgc": "TITLEGROUP_S",
                    "tgd": "SALVAGE TITLE",
                    "dd": "REAR END",
                    "tims": "https://cs.copart.com/v1/AUTH_svc.pdoc00001/lpp/1024/e4b722e7da814641aed141a6358b0ca6_thb.jpg",
                    "lic": [
                        "CERT-D",
                        "IV",
                        "NLC"
                    ],
                    "gr": "",
                    "dtc": "RR",
                    "al": "",
                    "adt": "F",
                    "ynumb": 85,
                    "phynumb": 85,
                    "bf": False,
                    "ymin": 70,
                    "offFlg": False,
                    "locCountry": "USA",
                    "locState": "PA",
                    "htsmn": "Y",
                    "tmtp": "AUTOMATIC",
                    "myb": 0.0,
                    "lmc": "SUBA",
                    "lcc": "CERT-D",
                    "sdd": "SIDE",
                    "lcd": "RUNS AND DRIVES",
                    "clr": "BLACK",
                    "ft": "GAS",
                    "hk": "YES",
                    "drv": "All wheel drive",
                    "ess": "Pure Sale",
                    "lsts": "O",
                    "scn": "GEICO",
                    "scl": "",
                    "showSeller": True,
                    "sstpflg": False,
                    "hcr": True,
                    "syn": "PA - PITTSBURGH SOUTH",
                    "ifs": False,
                    "pbf": False,
                    "crg": 0.0,
                    "brand": "COPART",
                    "blucar": False,
                    "hegn": "Y",
                    "lstg": 50,
                    "ldu": "salvage-2024-subaru-crosstrek-limited-pa-pittsburgh-south",
                    "pcf": False,
                    "btcf": False,
                    "tpfs": False,
                    "trf": True,
                    "csc": "NOT_APPLICABLE",
                    "mlf": False,
                    "fcd": False,
                    "slgc": "0",
                    "cfx": False,
                    "hcfx": True,
                    "isPWlot": False,
                    "lspa": 0.0
                }