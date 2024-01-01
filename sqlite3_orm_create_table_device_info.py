

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime

tzutc_8 = datetime.timezone(datetime.timedelta(hours=8))  # 设置时区为东八区

# -------------------------sqlite3-------------------------
engine = create_engine('sqlite:///sqlalchemy_sqlite3_device_info.db?check_same_thread=False',
                       # echo=True
                       )


Base = declarative_base()


class Router(Base):
    __tablename__ = 'router'

    id = Column(Integer, primary_key=True)
    routername = Column(String(64), nullable=False, index=True)
    ip = Column(String(64), nullable=False, index=True)
    routernamenew = Column(String(64), nullable=True, index=True)
    interface = relationship('Interface', back_populates="router", passive_deletes=True)
    # uselist=False表示onetoone
    l2vc = relationship('L2vc', back_populates="router", uselist=False, passive_deletes=True)
    arp = relationship('Arp', back_populates="router", uselist=False, passive_deletes=True)
    lldp = relationship('Lldp', back_populates="router", uselist=False, passive_deletes=True)
    bgp = relationship('Bgp', back_populates="router", uselist=False, passive_deletes=True)    
    # cpu_usage = relationship('CPUUsage', back_populates="router", passive_deletes=True)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.routername})"


class Interface(Base):
    __tablename__ = 'interface'

    id = Column(Integer, primary_key=True)
    router_id = Column(Integer, ForeignKey("router.id", ondelete='CASCADE'), nullable=False)
    interface_name = Column(String(64), nullable=False)
    Physical_State = Column(String(64), nullable=False)
    Protocol_State = Column(String(64), nullable=False)
    Description = Column(String(64), nullable=False)
    ip_address = Column(String(64), nullable=False)
    Current_BW = Column(String(64), nullable=False)
    Port_max_bw = Column(String(64), nullable=False)
    Transceiver_Mode = Column(String(64), nullable=False)
    WaveLength = Column(String(64), nullable=False)
    Transmission_Distance = Column(String(64), nullable=False)
    Rx_Power = Column(String(64), nullable=False)
    Tx_Power = Column(String(64), nullable=False)
    Last_physical_down_time = Column(String(64), nullable=False)
    Input_bandwidth = Column(String(64), nullable=False)
    Output_bandwidth = Column(String(64), nullable=False)
    router = relationship('Router', back_populates="interface", passive_deletes=True)

    def __repr__(self):
        return f"{self.__class__.__name__}(Router: {self.router.routername} "\
               f"| Interface_name: {self.interface_name})"
               # f"| IP: {self.ip} / {self.mask})"


class L2vc(Base):
    __tablename__ = 'l2vc'

    id = Column(Integer, primary_key=True)
    router_id = Column(Integer, ForeignKey("router.id", ondelete='CASCADE'), nullable=False)
    interface  = Column(String(64), nullable=False)
    AC_status  = Column(String(64), nullable=False)
    VC_State  = Column(String(64), nullable=False)
    VC_ID  = Column(String(64), nullable=False)
    VC_Type  = Column(String(64), nullable=False)
    session_state  = Column(String(64), nullable=False)
    Destination  = Column(String(64), nullable=False)
    link_state  = Column(String(64), nullable=False)
    router = relationship('Router', back_populates="l2vc", passive_deletes=True)


    def __repr__(self):
        return f"{self.__class__.__name__}(Router: {self.router.routername} " \
               f"| Interface: {self.Interface})"


class Arp(Base):
    __tablename__ = 'arp'

    id = Column(Integer, primary_key=True)
    router_id = Column(Integer, ForeignKey("router.id", ondelete='CASCADE'), nullable=False)
    IP_ADDRESS  = Column(String(64), nullable=False)
    MAC_ADDRESS  = Column(String(64), nullable=False)
    EXPIRE  = Column(String(64), nullable=False)
    TYPE  = Column(String(64), nullable=False)
    INTERFACE  = Column(String(64), nullable=False)
    VPN_INSTANCE  = Column(String(64), nullable=False)
    router = relationship('Router', back_populates="arp", passive_deletes=True)


    def __repr__(self):
        return f"{self.__class__.__name__}(Router: {self.router.routername} " \
               f"| Interface: {self.INTERFACE})"


class Lldp(Base):
    __tablename__ = 'lldp'

    id = Column(Integer, primary_key=True)
    router_id = Column(Integer, ForeignKey("router.id", ondelete='CASCADE'), nullable=False)
    Local_Port = Column(String(64), nullable=False)
    Peer_Port = Column(String(64), nullable=False)
    Peer_Device = Column(String(64), nullable=False)
    router = relationship('Router', back_populates="lldp", passive_deletes=True)


    def __repr__(self):
        return f"{self.__class__.__name__}(Router: {self.router.routername} " \
               f"| Local_Port: {self.local_port} " \
               f"| Peer_Port: {self.peer_port} " \
               f"| Peer_Device: {self.peer_device})"


class Bgp(Base):
    __tablename__ = 'bgp'

    id = Column(Integer, primary_key=True)
    router_id = Column(Integer, ForeignKey("router.id", ondelete='CASCADE'), nullable=False)
    Peer = Column(Integer, nullable=False)
    Version = Column(String(64), nullable=False)
    AS_number = Column(String(64), nullable=False)
    Peer_status = Column(String(64), nullable=False)    
    router = relationship('Router', back_populates="bgp", passive_deletes=True)


    def __repr__(self):
        return f"{self.__class__.__name__}(Router: {self.router.routername} " \
               f"| Bgp_Peer: {self.Peer} " \
               f"| Peer_status: {self.Peer_status} " 


# class OSPFNetwork(Base):
#     __tablename__ = 'ospf_network'

#     id = Column(Integer, primary_key=True)
#     area_id = Column(Integer, ForeignKey("area.id", ondelete='CASCADE'), nullable=False)
#     network = Column(String(64), nullable=False)
#     wildmask = Column(String(64), nullable=False)
#     area = relationship('Area', back_populates="ospf_network", passive_deletes=True)

#     def __repr__(self):
#         return f"{self.__class__.__name__}(Router: {self.area.ospf_process.router.routername} " \
#                f"| Process: {self.area.ospf_process.processid} " \
#                f"| Area: {self.area.area_id} " \
#                f"| Network: {self.network}/{self.wildmask})"


# class CPUUsage(Base):
#     __tablename__ = 'cpu_usage'

#     id = Column(Integer, primary_key=True)
#     router_id = Column(Integer, ForeignKey("router.id", ondelete='CASCADE'), nullable=False)
#     cpu_useage_percent = Column(Integer, nullable=False)
#     cpu_useage_datetime = Column(DateTime(timezone='Asia/Chongqing'), default=datetime.datetime.now)
#     router = relationship('Router', back_populates="cpu_usage", passive_deletes=True)

#     def __repr__(self):
#         return f"{self.__class__.__name__}(Router: {self.router.routername} " \
#                f"| Datetime: {self.cpu_useage_datetime} " \
#                f"| Percent: {self.cpu_useage_percent})"


if __name__ == '__main__':
    # checkfirst=True，表示创建表前先检查该表是否存在，如同名表已存在则不再创建。其实默认就是True
    Base.metadata.create_all(engine, checkfirst=True)

