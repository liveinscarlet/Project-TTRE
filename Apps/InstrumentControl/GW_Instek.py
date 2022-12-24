
class PUGW_Instek(PowerUnit):
    def __init__(self, visa_manager: pyvisa.ResourceManager, addr: str = 'TCPIP0::192.168.1.227::inst0::INSTR'):  # Добавить в локальную сеть и установить IP
        super().__init__(visa_manager, addr)
        self.myPU = visa_manager.open_resource(addr)
        print(self.myPU.query("*IDN?"))

    def default_setup_ch1(self):
        self.myPU.write(":OUT1")
        self.myPU.write(":SOURCE1:VOLTAGE 0")
        self.myPU.write(":SOURCE1:CURRENT 0.01")

    def default_setup_ch2(self):
        self.myPU.write(":OUT2")
        self.myPU.write(":SOURCE1:VOLTAGE 0")
        self.myPU.write(":SOURCE1:CURRENT 0.01")

    def v_change_1(self, V1):
        self.myPU.write(f":SOURCE1:VOLTAGE {V1}")
        time.sleep(1)

    def v_change_2(self, V2):
        self.myPU.write(f":SOURCE1:VOLTAGE {V2}")
        time.sleep(1)

    def reset(self):
        self.myPU.write("*RST")

    def end_of_work(self):
        self.myPU.write(":ALLOUTOFF")