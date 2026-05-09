# plc_handler.py
import threading
import logging
from PyQt6.QtCore import QObject, pyqtSignal
from pymodbus.client import ModbusTcpClient

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class PLCHandler(QObject):
    """Advanced PLC Handler with all Modbus features"""
    
    # Signals for UI
    data_updated = pyqtSignal(dict)
    connection_status = pyqtSignal(bool)
    connection_error = pyqtSignal(str)
    
    def __init__(self, ip="192.168.1.1", port=502, pulses_per_200mm=2000):
        super().__init__()
        self.ip = ip
        self.port = port
        self.pulses_per_200mm = pulses_per_200mm
        self.client = None
        self.lock = threading.Lock()  # Thread-safe PLC access
        self.running = False
        self.connected = False
        self.poll_thread = None
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 3
        
    # ========== CONNECTION MANAGEMENT ==========
    
    def connect(self):
        """Connect to PLC Modbus TCP client"""
        try:
            self.client = ModbusTcpClient(self.ip, port=self.port)
            if self.client.connect():
                self.connected = True
                self.reconnect_attempts = 0
                logger.info(f"Connected to PLC at {self.ip}:{self.port}")
                self.connection_status.emit(True)
                return True
            else:
                logger.error(f"Failed to connect to PLC at {self.ip}:{self.port}")
                self.connection_error.emit(f"Failed to connect to {self.ip}:{self.port}")
                self.connection_status.emit(False)
                return False
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            self.connection_error.emit(f"Connection error: {str(e)}")
            self.connection_status.emit(False)
            return False
    
    def disconnect(self):
        """Close the Modbus TCP client connection"""
        self.running = False
        if self.poll_thread and self.poll_thread.is_alive():
            self.poll_thread.join(timeout=2)
        
        if self.client:
            self.client.close()
        self.connected = False
        logger.info("Disconnected from PLC")
        self.connection_status.emit(False)
    
    @property
    def is_connected(self):
        """Check if PLC is connected"""
        return self.client.is_socket_open() if self.client else False
    
    # ========== OUTPUT PIN WRITE (Y addresses) ==========
    
    def write_coil(self, address, state):
        """
        Write a boolean state to a coil (Y outputs)
        
        :param address: Coil address to write
        :param state: True or False, coil state
        :return: True if success, False if error
        """
        with self.lock:
            try:
                result = self.client.write_coil(address, state)
                if result.isError():
                    logger.error(f"Failed to write coil at {address} with state {state}")
                    return False
                logger.info(f"Set coil at address {address} to {state}")
                return True
            except Exception as e:
                logger.error(f"Exception writing coil: {str(e)}")
                return False
    
    # ========== INPUT PIN READ (X addresses) ==========
    
    def read_discrete_input(self, address, count=1):
        """
        Read discrete inputs (X addresses)
        
        :param address: Starting discrete input address
        :param count: Number of inputs to read
        :return: Single boolean if count=1, else list of booleans; None on error
        """
        with self.lock:
            try:
                result = self.client.read_discrete_inputs(address, count=count)
                if result.isError():
                    logger.error(f"Failed to read discrete input at {address}")
                    return None
                values = result.bits
                if count == 1:
                    logger.debug(f"Discrete input at {address} value: {values[0]}")
                    return values[0]
                logger.debug(f"Discrete inputs at {address} values: {values}")
                return values
            except Exception as e:
                logger.error(f"Exception reading discrete input: {str(e)}")
                return None
    
    # ========== M ADDRESS READ/WRITE (Internal relays) ==========
    
    def read_coil(self, address, count=1):
        """
        Read coils (M addresses)
        
        :param address: Starting coil address
        :param count: Number of coils to read
        :return: Single boolean if count=1, else list of booleans; None on error
        """
        with self.lock:
            try:
                result = self.client.read_coils(address, count=count)
                if result.isError():
                    logger.error(f"Failed to read coil at {address}")
                    return None
                values = result.bits
                if count == 1:
                    logger.debug(f"Coil at {address} value: {values[0]}")
                    return values[0]
                logger.debug(f"Coils at {address} values: {values}")
                return values
            except Exception as e:
                logger.error(f"Exception reading coil: {str(e)}")
                return None
    
    def write_coil_m(self, address, state):
        """
        Write to M addresses (internal relays)
        Same as write_coil but for clarity
        
        :param address: M address to write
        :param state: True or False
        :return: True if success
        """
        return self.write_coil(address, state)
    
    # ========== D ADDRESS READ/WRITE (Holding Registers) ==========
    
    def write_register(self, address, value):
        """
        Write an integer value to a holding register (D addresses)
        
        :param address: Register address
        :param value: Integer to write (0-65535)
        :return: True if success, False if error
        """
        with self.lock:
            try:
                result = self.client.write_register(address, value)
                if result.isError():
                    logger.error(f"Failed to write register at {address} with value {value}")
                    return False
                logger.info(f"Wrote value {value} to register at {address}")
                return True
            except Exception as e:
                logger.error(f"Exception writing register: {str(e)}")
                return False
    
    def read_holding_registers(self, address, count=1):
        """
        Read one or more holding registers (D addresses)
        
        :param address: Starting register address
        :param count: Number of registers to read
        :return: Integer if count=1, else list of integers; None on error
        """
        with self.lock:
            try:
                result = self.client.read_holding_registers(address, count=count)
                if result.isError():
                    logger.error(f"Failed to read holding register at {address}")
                    return None
                registers = result.registers
                if count == 1:
                    return registers[0]
                logger.debug(f"Holding registers at {address} values: {registers}")
                return registers
            except Exception as e:
                logger.error(f"Exception reading holding register: {str(e)}")
                return None
    
    # ========== 32-BIT REGISTER SUPPORT ==========
    
    def write_register_32bit(self, address, value):
        """
        Write a 32-bit integer to two consecutive holding registers
        
        :param address: Starting register address (low word)
        :param value: 32-bit integer to write
        :return: True if success
        """
        low_word, high_word = self.int32_to_words(value)
        with self.lock:
            try:
                # Write low word first
                result1 = self.client.write_register(address, low_word)
                if result1.isError():
                    logger.error(f"Failed to write low word at {address}")
                    return False
                # Write high word
                result2 = self.client.write_register(address + 1, high_word)
                if result2.isError():
                    logger.error(f"Failed to write high word at {address + 1}")
                    return False
                logger.info(f"Wrote 32-bit value {value} to registers {address}-{address+1}")
                return True
            except Exception as e:
                logger.error(f"Exception writing 32-bit register: {str(e)}")
                return False
    
    def read_holding_registers_32bit(self, address):
        """
        Read a 32-bit integer from two consecutive holding registers
        
        :param address: Starting register address (low word)
        :return: 32-bit integer value, None on error
        """
        with self.lock:
            try:
                result = self.client.read_holding_registers(address, count=2)
                if result.isError():
                    logger.error(f"Failed to read 32-bit register at {address}")
                    return None
                registers = result.registers
                if len(registers) >= 2:
                    value = self.words_to_int32([registers[0], registers[1]])
                    logger.debug(f"Read 32-bit value {value} from registers {address}-{address+1}")
                    return value
                return None
            except Exception as e:
                logger.error(f"Exception reading 32-bit register: {str(e)}")
                return None
    
    # ========== UNIT CONVERSION UTILITIES ==========
    
    def mm_to_pulses(self, mm_value):
        """Convert millimeters to pulses for axis positioning"""
        pulses_per_mm = self.pulses_per_200mm / 200.0
        pulses = int(mm_value * pulses_per_mm)
        logger.debug(f"Converted {mm_value} mm to {pulses} pulses")
        return pulses
    
    def pulses_to_mm(self, pulse_value):
        """Convert pulses to millimeters for axis positioning"""
        pulses_per_mm = self.pulses_per_200mm / 200.0
        mm = pulse_value / pulses_per_mm
        mm_int = int(mm)  # truncate decimals
        logger.debug(f"Converted {pulse_value} pulses to {mm_int} mm")
        return mm_int
    
    @staticmethod
    def int32_to_words(value):
        """Convert signed 32-bit integer to two 16-bit words (low, high)"""
        # Handle negative numbers
        if value < 0:
            value = 0x100000000 + value
        low_word = value & 0xFFFF
        high_word = (value >> 16) & 0xFFFF
        return low_word, high_word
    
    @staticmethod
    def words_to_int32(words):
        """Convert [low, high] words back to signed 32-bit integer"""
        low, high = words
        value = (high << 16) | low
        if value & 0x80000000:  # negative (2^31)
            value -= 0x100000000
        return value
    
    # ========== DATA POLLING (For UI Updates) ==========
    
    def start_polling(self, interval_ms=200, config=None):
        """Start continuous polling of PLC data"""
        if not self.connected:
            logger.warning("Cannot start polling: PLC not connected")
            return False
        
        self.running = True
        self.poll_interval = interval_ms / 1000.0
        self.poll_config = config or self._get_default_config()
        
        self.poll_thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.poll_thread.start()
        logger.info(f"Started polling every {interval_ms}ms")
        return True
    
    def stop_polling(self):
        """Stop polling loop"""
        self.running = False
        logger.info("Stopped polling")
    
    def _get_default_config(self):
        """Get default polling configuration"""
        return {
            'sensors': {
                's1': {'type': 'discrete', 'address': 0},
                's2': {'type': 'discrete', 'address': 1},
                's3': {'type': 'discrete', 'address': 2},
                's4': {'type': 'discrete', 'address': 3},
            },
            'analog': {
                'cutter_pos': {'address': 0x4000, 'scale': 0.1},
                'speed': {'address': 0x4001, 'scale': 0.01},
                'temp': {'address': 0x4002, 'scale': 0.1},
                'pressure': {'address': 0x4003, 'scale': 0.01},
            },
            'counters': {
                'total_cuts': {'address': 0x3000, 'scale': 1},
                'material_length': {'address': 0x3001, 'scale': 0.1},
                'production_count': {'address': 0x3002, 'scale': 1},
            },
            'status': {'address': 0x4200}
        }
    
    def _poll_loop(self):
        """Main polling loop running in separate thread"""
        consecutive_errors = 0
        
        while self.running:
            if self.connected and self.client:
                try:
                    data = {
                        'sensors': {},
                        'analog': {},
                        'counters': {},
                        'status': 'UNKNOWN',
                        'timestamp': None
                    }
                    
                    import time
                    data['timestamp'] = time.time()
                    
                    # Read sensors (discrete inputs)
                    for name, cfg in self.poll_config.get('sensors', {}).items():
                        value = self.read_discrete_input(cfg['address'])
                        if value is not None:
                            data['sensors'][name] = value
                    
                    # Read analog values (holding registers)
                    for name, cfg in self.poll_config.get('analog', {}).items():
                        value = self.read_holding_registers(cfg['address'])
                        if value is not None:
                            data['analog'][name] = value * cfg.get('scale', 1)
                    
                    # Read counters
                    for name, cfg in self.poll_config.get('counters', {}).items():
                        value = self.read_holding_registers(cfg['address'])
                        if value is not None:
                            data['counters'][name] = value * cfg.get('scale', 1)
                    
                    # Read status
                    status_map = {0: "IDLE", 1: "RUNNING", 2: "STOPPED", 3: "ERROR", 4: "PAUSED"}
                    status_val = self.read_holding_registers(self.poll_config.get('status', {}).get('address', 0x4200))
                    if status_val is not None:
                        data['status'] = status_map.get(status_val, "UNKNOWN")
                    
                    self.data_updated.emit(data)
                    consecutive_errors = 0
                    
                except Exception as e:
                    consecutive_errors += 1
                    if consecutive_errors >= 3:
                        logger.error(f"Polling error: {str(e)}")
                        self.connected = False
                        self.connection_status.emit(False)
                        self._reconnect()
                        consecutive_errors = 0
            else:
                if not self.connected and self.running:
                    self._reconnect()
            
            import time
            time.sleep(self.poll_interval)
    
    def _reconnect(self):
        """Attempt to reconnect to PLC"""
        if self.reconnect_attempts < self.max_reconnect_attempts:
            self.reconnect_attempts += 1
            logger.info(f"Reconnect attempt {self.reconnect_attempts}/{self.max_reconnect_attempts}")
            import time
            time.sleep(2)
            self.connect()
        else:
            logger.warning("Max reconnection attempts reached, waiting 10 seconds...")
            import time
            time.sleep(10)
            self.reconnect_attempts = 0
            self.connect()
    
    # ========== COMMAND METHODS (For UI Controls) ==========
    
    def send_command(self, command):
        """Send control command to PLC"""
        command_map = {
            'START': 1,
            'STOP': 0,
            'RESET': 2,
            'PAUSE': 3,
            'RESUME': 4,
            'EMERGENCY_STOP': 5
        }
        
        if command.upper() in command_map:
            return self.write_register(0x4100, command_map[command.upper()])
        else:
            logger.error(f"Unknown command: {command}")
            return False
    
    def set_speed(self, speed_type, value):
        """Set speed value in PLC"""
        speed_addresses = {
            'feeding': 0x4101,
            'unloading': 0x4102,
            'upstroke': 0x4103
        }
        
        if speed_type in speed_addresses:
            return self.write_register(speed_addresses[speed_type], value)
        return False
    
    # ========== HELPER METHODS ==========
    
    def get_status(self):
        """Get current connection status"""
        return {
            'connected': self.connected,
            'ip': self.ip,
            'port': self.port,
            'polling': self.running,
            'is_socket_open': self.client.is_socket_open() if self.client else False
        }