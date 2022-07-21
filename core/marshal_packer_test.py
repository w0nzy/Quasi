import marshal
from core.utils.parser import parse_header
def MARSHALPacker(header,**params):
    return marshal.dumps({header:params})
def MARSHALUnpacker(data: bytes) -> type:
    class Data:
        """
        bu class'ın oluşturulma sebebi daha kolaylık sağlaması içindir
        çağırırkem Data.header
        ve Data.data gibi basit ve kısaltma içindir 
        """
    try:
        data = marshal.loads(data)
    except:
        data = {"invalid":"marshalled_data"}
    header = parse_header(data,index=0)
    setattr(Data,"header",header)
    setattr(Data,"data",data)
    return Data