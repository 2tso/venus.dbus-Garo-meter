import logging
import device
import probe
from register import *

log = logging.getLogger()

nr_phases = [ 3, 3, 2, 1, 3 ]

phase_configs = [
    '3P.n',
    '3P.1',
    '2P',
    '1P',
    '3P',
]

#switch_positions = [
#    'kVARh',
#    '2',
#    '1',
#    'Locked',
#]

class GNM3D_Meter(device.EnergyMeter):
    # vendor_id = 'cg'
    # vendor_name = 'Carlo Gavazzi'
    productid = 0xFFFF
    productname = 'Garo GNM3D Energy Meter'
    

    
    def __init__(self, spec, modbus, model):      
        super().__init__(spec, modbus, model)
        self.min_timeout = 0.5
        self.nr_phases = 3
        
    
    def phase_regs(self, n):
        s = 2 * (n - 1)
        return [
            Reg_s32l(0x0000 + s, '/Ac/L%d/Voltage' % n,        10, '%.1f V'),
            Reg_s32l(0x000c + s, '/Ac/L%d/Current' % n,      1000, '%.1f A'),
            Reg_s32l(0x0012 + s, '/Ac/L%d/Power' % n,          10, '%.1f W'),
            Reg_s32l(0x0040 + s, '/Ac/L%d/Energy/Forward' % n, 10, '%.1f kWh'),
        ]

    def device_init(self):
        log.info('Initializing Garo energy meter using connection "%s"', self.connection())
        
        self.info_regs = [
            Reg_u16( 0x0302, '/HardwareVersion'),
            Reg_u16( 0x0303, '/FirmwareVersion'),
            # Reg_u16( 0x1002, '/PhaseConfig', text=phase_configs, write=(0, 4)),
            Reg_text(0x5000, 7, '/Serial'),
        ]
        
        #self.read_info()
        phases = 3 #nr_phases[int(self.info['/PhaseConfig'])]
        regs = [
            Reg_s32l(0x0028, '/Ac/Power',          10, '%.1f W'),
            Reg_u16( 0x0033, '/Ac/Frequency',      10, '%.1f Hz'),
            Reg_s32l(0x0034, '/Ac/Energy/Forward', 10, '%.1f kWh'),
            Reg_s32l(0x004e, '/Ac/Energy/Reverse', 10, '%.1f kWh'),            
        ]

        for n in range(1, phases + 1):
            regs += self.phase_regs(n)

        self.data_regs = regs
        # self.nr_phases = phases
    
    def get_ident(self):
        log.info('get_ident_returns cg_%s' % self.info['/Serial'])
        return 'cg_%s' % self.info['/Serial']


    #def dbus_write_register(self, reg, path, val):
    #    super().dbus_write_register(reg, path, val)
    #    self.sched_reinit()

models = {
    341: {
        'model':    'GNM3D-RS485',
        'handler':  GNM3D_Meter,
    },
    342: {
        'model':    'GNM3T-RS485',
        'handler':  GNM3D_Meter,
    },    
}

probe.add_handler(probe.ModelRegister(Reg_u16(0x000b), models,
                                      methods=['rtu'],
                                      rates=[9600],
                                      units=[2]))
