#! /usr/bin/env python3

# Example wiring (LT-8900 on board to Raspberry Pi):
#
#                        LT-8900
# _--------------------------------------------------------_
# | VCC   | RST   | MISO  | MOSI  | SCK   | CS    | GND    |
# |-------+-------+----- -+-------+-------+-------+--------|
# | 3.3v  | Reset | SPI   | SPI   | SPI   | SPI   | Ground |
# |       |       |       |       | Clock | CE0   |        |
# -___+_______+_______+_______+_______+_______+_______+____-
#     |       |       |       |       |       |       |
#     |       |       |       |       |       |       |
#     |       |       |       |       |       |       |
# _---+-------+-------+-------+-------+-------+-------+----_
# | 3.3v  | GPIO5 | MISO  | MOSI  | SCLK  | CE0   | 0v     |
# |-------+-------+-------+-------+-------+-------+--------|
# | P1-17 | P1-18 | P1-21 | P1-19 | P1-23 | P1-24 | P1-25  |
# -________________________________________________________-
#                     Raspberry Pi

import spidev
import time
import copy

class radio:
	__register_map = [
		{'name': "Unknown"}, # 0
		{'name': "Unknown"}, # 1
		{'name': "Unknown"}, # 2
		{                    # 3
			'name': 'phase_lock',
			'reserved_1': [13, 15],
			'rf_synth_lock': [12, 12],
			'reserved_2': [0, 11] 
		},
		{'name': "Unknown"}, # 4
		{'name': "Unknown"}, # 5
		{                    # 6
			'name': "raw_rssi",
			'raw_rssi': [10, 15],
			'reserved_1': [0, 9]
		},
		{                    # 7
			'name': "radio_state",
			'reserved_1': [9, 15],
			'tx_enabled': [8, 8],
			'rx_enabled': [7, 7],
			'channel': [0, 6]
		},
		{'name': "Unknown"}, # 8
		{                    # 9
			'name': "power",
			'current': [12, 15],
			'reserved_1': [11, 11],
			'gain': [7, 10],
			'reserved_2': [0, 6]
		},
		{                    # 10
			'name': "gain_block",
			'reserved_1': [1, 15],
			'enabled': [0, 0]
		},
		{                    # 11
			'name': "rssi_power",
			'reserved_1': [9, 15],
			'mode': [8, 8],
			'reserved_2': [0, 7]
		},
		{'name': "Unknown"}, # 12
		{'name': "Unknown"}, # 13
		{'name': "Unknown"}, # 14
		{'name': "Unknown"}, # 15
		{'name': "Unknown"}, # 16
		{'name': "Unknown"}, # 17
		{'name': "Unknown"}, # 18
		{'name': "Unknown"}, # 19
		{'name': "Unknown"}, # 20
		{'name': "Unknown"}, # 21
		{'name': "Unknown"}, # 22
		{                    # 23
			'name': "vco_calibrate",
			'reserved_1': [3, 15],
			'enabled': [2, 2],
			'reserved_2': [0, 1]
		},
		{'name': "Unknown"}, # 24
		{'name': "Unknown"}, # 25
		{'name': "Unknown"}, # 26
		{                    # 27
			'name': "crystal",
			'reserved_1': [6, 15],
			'trim_adjust': [0, 5]
		},
		{'name': "Unknown"}, # 28
		{                    # 29
			'name': "minor_version",
			'reserved_1': [8, 15],
			'rf': [4, 7],
			'reserved_2': [3, 3],
			'digital': [0, 2]
		},
		{                    # 30
			'name': "manufacture_1",
			'manuf_code_low': [0, 15]
		},
		{                    # 31
			'name': "manufacture_2",
			'rf_code': [12, 15],
			'manuf_code_high': [0, 11]
		},
		{                    # 32
			'name': "packet_config",
			'preamble_len': [13, 15],
			'syncword_len': [11, 12],
			'trailer_len': [8, 10],
			'packet_type': [6, 7],
			'fec_type': [4, 5],
			'br_clock_sel': [1, 3],
			'reserved_1': [0, 0]
		},
		{'name': "Unknown"}, # 33
		{'name': "Unknown"}, # 34
		{                    # 35
			'name': "chip_power",
			'power_down': [15, 15],
			'sleep_mode': [14, 14],
			'reserved_1': [13, 13],
			'br_clock_on_sleep': [12, 12],
			'rexmit_times': [8, 11],
			'miso_tri_opt': [7, 7],
			'scramble_value': [0, 6]
		},
		{                    # 36
			'name': "syncword_0",
			'value': [0, 15]
		},
		{                    # 37
			'name': "syncword_1",
			'value': [0, 15]
		},
		{                    # 38
			'name': "syncword_2",
			'value': [0, 15]
		},
		{                    # 39
			'name': "syncword_3",
			'value': [0, 15]
		},
		{                    # 40
			'name': "thresholds",
			'fifo_empty_threshold': [11, 15],
			'fifo_full_threshold': [6, 10],
			'syncword_error_bits': [0, 5]
		},
		{                    # 41
			'name': "format_config",
			'crc_enabled': [15, 15],
			'scramble_enabled': [14, 14],
			'packet_length_encoded': [13, 13],
			'auto_term_tx': [12, 12],
			'auto_ack': [11, 11],
			'pkt_fifo_polarity': [10, 10],
			'reserved_1': [8, 9],
			'crc_initial_data': [0, 7]
		},
		{                    # 42
			'name': "scan_rssi",
			'channel': [10, 15],
			'reserved_1': [8, 9],
			'ack_time': [0, 7]
		},
		{                    # 43
			'name': "scan_rssi_state",
			'enabled': [15, 15],
			'channel_offset': [8, 14],
			'wait_time': [0, 7]
		},
		{'name': "Unknown"}, # 44
		{'name': "Unknown"}, # 45
		{'name': "Unknown"}, # 46
		{'name': "Unknown"}, # 47
		{                    # 48
			'name': "status",
			'crc_error': [15, 15],
			'fec_error': [14, 14],
			'framer_status': [8, 13],
			'syncword_rx': [7, 7],
			'packet_flag': [6, 6],
			'fifo_flag': [5, 5],
			'reserved_1': [0, 4]
		},
		{'name': "Unknown"}, # 49
		{                    # 50
			'name': "fifo",
			'value': [0, 15]
		},
		{'name': "Unknown"}, # 51
		{                    # 52
			'name': "fifo_state",
			'clear_write': [15, 15],
			'reserved_1': [14, 14],
			'write_ptr': [8, 13],
			'clear_read': [7, 7],
			'reserved_2': [6, 6],
			'read_ptr': [0, 5]
		}
	]

	def __init__(self, spi_bus, spi_dev, config = None):
		spi = spidev.SpiDev()
		spi.open(spi_bus, spi_dev)
		self.__spi = spi

		self.__set_spi_mode(1)

		self.configure(config)

		if len(self.__register_map) != 53:
			raise ValueError('Inconsistent register map!')

		return None

	def __debug(self, message):
		print(message)
		return None

	def __reset_device(self):
		if self.__config is not None:
			if self.__config['reset_command'] is not None:
				return self.__config['reset_command']()
		return None

	def __register_name(self, reg_number):
		return self.__register_map[reg_number]['name']

	def __register_number(self, reg_string):
		reg_string_orig = reg_string

		if isinstance(reg_string, int):
			return reg_string
		if reg_string.isnumeric():
			return int(reg_string)
		for reg_number, reg_info in enumerate(self.__register_map):
			if reg_info['name'] == reg_string:
				return reg_number
		raise NameError("Invalid register value {}".format(reg_string_orig))

	def __set_spi_mode(self, mode):
		if mode != self.__spi.mode:
			self.__spi.mode = mode
		return True

	def __get_spi_mode(self):
		return self.__spi.mode

	def __check_radio(self):
		old_mode = self.__get_spi_mode()

		value1 = self.get_register(0);
		value2 = self.get_register(1);

		if value1 == 0x6fe0 and value2 == 0x5681:
			return True
		return False

	def __set_defaults(self):
		self.put_register
		return True

	def __put_register_high_low(self, reg, high, low, delay = 7):
		reg = self.__register_number(reg)
		result = self.__spi.xfer([reg, high, low], self.__spi.max_speed_hz, delay)

		if reg & 0x80 == 0x80:
			self.__debug(" regRead[%02X] = %s" % ((reg & 0x7f), result))
		else:
			self.__debug("regWrite[%02X:0x%02X%02X] = %s" % (reg, high, low, result))

		if reg & 0x80 != 0x80:
			time.sleep(delay / 1000.0)

		return result

	def put_register(self, reg, value):
		high = (value >> 8) & 0xff
		low  = value & 0xff
		return self.__put_register_high_low(reg, high, low)

	def put_register_bits(self, reg, bits_dict):
		# Convert register to an integer
		reg = self.__register_number(reg)

		# Lookup register in the register map
		register_info = self.__register_map[reg]

		# Create a dictionary to hold the parsed results
		value = 0
		for key in bits_dict:
			if key == "name":
				continue
			bit_range = register_info[key]
			mask = ((1 << (bit_range[1] - bit_range[0] + 1)) - 1) << bit_range[0]
			key_value = (bits_dict[key] << bit_range[0]) & mask
			value = value | key_value

		result = self.put_register(reg, value)

		return result

	def get_register(self, reg):
		# Convert register to an integer
		reg = self.__register_number(reg)

		# Reading of a register is indicated by setting high bit
		read_reg = reg | 0b10000000

		# Put the request with space for the reply
		value = self.__put_register_high_low(read_reg, 0, 0)

		# The reply is stored in the lower two bytes
		result = value[1] << 8 | value[2]

		# Return result
		return result

	def get_register_bits(self, reg, value = None):
		# Convert register to an integer
		reg = self.__register_number(reg)

		# Get the register's value (unless one was supplied)
		if value is None:
			value = self.get_register(reg)

		# Lookup register in the register map
		register_info = self.__register_map[reg]

		# Create a dictionary to hold the parsed results
		result = {'name': register_info['name']}
		for key in register_info:
			if key == "name":
				continue
			bit_range = register_info[key]
			mask = ((1 << (bit_range[1] - bit_range[0] + 1)) - 1) << bit_range[0]
			key_value = (value & mask) >> bit_range[0]
			result[key] = key_value

		# Return the filled in structure
		return result

	def configure(self, config):
		self.__config = config

		self.__spi.max_speed_hz = self.__config.get('frequency', 4000000)

		return None

	def initialize(self):
		self.__reset_device()

		self.__set_defaults()

		if not self.__check_radio():
			return False
		return True

	def set_channel(self, channel):
		state = self.get_register_bits('radio_state')
		state['channel'] = channel

		self.put_register_bits('radio_state', state)

		return state

	def set_syncword(self, syncword):
		packet_config = self.get_register_bits('packet_config')
		packet_config['syncword_len'] = len(syncword) - 1
		print("packet_config = {}".format(packet_config))

		self.put_register_bits('packet_config', packet_config)

		if len(syncword) == 1:
			self.put_register("syncword_0", syncword[0])
		elif len(syncword) == 2:
			self.put_register("syncword_0", syncword[1])
			self.put_register("syncword_3", syncword[0])
		elif len(syncword) == 3:
			self.put_register("syncword_0", syncword[2])
			self.put_register("syncword_2", syncword[1])
			self.put_register("syncword_3", syncword[0])
		elif len(syncword) == 4:
			self.put_register("syncword_0", syncword[3])
			self.put_register("syncword_1", syncword[2])
			self.put_register("syncword_2", syncword[1])
			self.put_register("syncword_3", syncword[0])
		elif len(syncword) > 4:
			raise ValueError("SyncWord length must be less than 5")

	def transmit(self, message, channel = None):
		if channel is None:
			state = self.get_register_bits('radio_state')
			channel = state['channel']

		# Initialize the transmitter
		self.put_register_bits('radio_state', {
			'tx_enabled': 0,
			'rx_enabled': 0,
			'channel': 0
		})

		self.put_register_bits('fifo_state', {
			'clear_read': 1,
			'clear_write': 1
		})

		# Format message to send to fifo
		## XXX: TODO: Length encoding is optional, should check register
		message = [self.__register_number('fifo'), len(message)] + message

		# Transfer the message
		result = self.__spi.xfer(copy.copy(message), self.__spi.max_speed_hz, 10)
		self.__debug("Writing: {} = {}".format(message, result))

		# Tell the radio to transmit the FIFO buffer to the specified channel
		self.put_register_bits('radio_state', {
			'tx_enabled': 1,
			'rx_enabled': 0,
			'channel': channel
		})

		# Wait for buffer to empty
		while True:
			radio_state = self.get_register_bits('radio_state')
			print(radio_state)

			if radio_state['tx_enabled'] == 0:
				break
			time.sleep(0.1)

		return False

	def multi_transmit(self, message, channels, retries = 3):
		for i in range(retries):
			for channel in channels:
				self.transmit(message, channel)
				time.sleep(0.01)
