import os
import xml.etree.ElementTree as ET
from database import SessionLocal
from models import *
from datetime import datetime
from dadata import Dadata


dadata = Dadata(os.environ['DADATA_API_KEY'], os.environ['DADATA_SECRET_KEY'])

def parse_address(address: str) -> dict:
    result = dadata.clean("address", address)
    return {
        'index': result.get('postal_code'),
        'region': result.get('region_with_type'),
        'city': result.get('city_with_type') or result.get('settlement_with_type'),
        'street': result.get('street_with_type'),
        'house': result.get('house'),
        'flat': result.get('flat')
    }

def parse_date(s):
    try:
        return datetime.fromisoformat(s.replace('Z', ''))
    except:
        return None


session = SessionLocal()
tree = ET.parse("ExtrajudicialBankruptcy.xml")
root = tree.getroot()
for elem in root.findall("ExtrajudicialBankruptcyMessage"):
    msg = Message(
        id=elem.findtext("Id"),
        number=elem.findtext("Number"),
        type=elem.findtext("Type"),
        publish_date=parse_date(elem.findtext("PublishDate")),
        finish_reason=elem.findtext("FinishReason")
    )
    d_elem = elem.find("Debtor")
    if d_elem is not None:
        addr = parse_address(d_elem.findtext("Address"))
        debtor = Debtor(
            name=d_elem.findtext("Name"),
            birth_date=parse_date(d_elem.findtext("BirthDate")),
            birth_place=d_elem.findtext("BirthPlace"),
            inn=d_elem.findtext("Inn"),
            address_index=addr["index"],
            region=addr["region"],
            city=addr["city"],
            street=addr["street"],
            house=addr["house"],
            flat=addr["flat"]
        )
        session.add(debtor)
        session.flush()
        msg.debtor_id = debtor.id
    for b in elem.findall(".//Banks/Bank"):
        session.add(Bank(
            name=b.findtext("Name"),
            bik=b.findtext("Bik"),
            message=msg
        ))
    for mo in elem.findall(".//MonetaryObligation"):
        session.add(MonetaryObligation(
            creditor_name=mo.findtext("CreditorName"),
            content=mo.findtext("Content"),
            basis=mo.findtext("Basis"),
            total_sum=float(mo.findtext("TotalSum") or 0),
            debt_sum=float(mo.findtext("DebtSum") or 0),
            penalty_sum=float(mo.findtext("PenaltySum") or 0),
            message=msg
        ))
    for op in elem.findall(".//ObligatoryPayment"):
        session.add(ObligatoryPayment(
            name=op.findtext("Name"),
            sum=float(op.findtext("Sum") or 0),
            message=msg
        ))
    session.add(msg)
session.commit()
session.close()