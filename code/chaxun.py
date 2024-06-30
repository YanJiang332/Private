from sqlalchemy.orm import sessionmaker
from sqlite3_orm_create_table_device_info import Router, Interface, L2vc, engine
Session = sessionmaker(bind=engine)
session = Session()

router_name = "KE-MOS0024-HW-ATN910C-B-CSG01-NAIROBI_KAPA"
# router = session.query(Router).filter_by(routername=router_name).first()
router = session.query(Router).filter(Router.routername == router_name).first()
# router = session.query(Router).get(router_name)
# print({router.ip})

try:
    if router:
        # Print device interface information
        print(f"Router: {router.routername}")
        for interface in router.interface:
            if interface.ip_address and "unnumbered" not in interface.ip_address:
                print(f"Interface: {interface.interface_name}, IP: {interface.ip_address}")
        
        # Query device's L2vc information
        l2vc_info_list = session.query(L2vc).filter(L2vc.router_id == router.id).all()

        if l2vc_info_list:
            print(f"L2vc Info for Router: {router.routername}")
            for l2vc_info in l2vc_info_list:
                if 'up' in l2vc_info.link_state:
                    print(f"Interface: {l2vc_info.interface}, Link Status: {l2vc_info.link_state}")
        else:
            print(f"No L2vc Info found for Router: {router.routername}")
    else:
        print(f"Router with name {router_name} not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    session.close()










