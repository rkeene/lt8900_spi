#! /usr/bin/env python3

# Example wiring (LT-8900 on board to Raspberry Pi):
#
#                        LT-8900
# _--------------------------------------------------------_
# | VCC   | RST   | MISO  | MOSI  | SCK   | CS    | GND    |
# |-------+-------+----- -+-------+-------+-------+--------|
# | 3.3v  | Reset | SPI   | SPI   | SPI   | SPI   | Ground |
# |       |       |       |       | Clock | CE0   |        |
# -___+___|___+___|___+___|___+___|___+___|___+___|___+____-
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

class radio:
	_register_map = [
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
		{                    # 33
			'name': "vco_pa_delays",
			'vco_on_delay': [8, 15],
			'pa_off_delay': [6, 7],
			'pa_tx_delay': [0, 5]
		},
		{                    # 34
			'name': "tx_packet_delays",
			'packet_control_direct': [15, 15],
			'tx_cw_delay': [8, 14],
			'reserved_1': [6, 7],
			'tx_sw_on_delay': [0, 5]
		},
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
		self._spi = spi

		self.configure(config)

		if len(self._register_map) != 53:
			raise ValueError('Inconsistent register map!')

		return None

	def __del__(self):
		self._spi.close()

	def _debug(self, message):
		#print("LT8900 DEBUG: " + message)
		return None

	def _reset_device(self):
		if self._config is not None:
			if self._config['reset_command'] is not None:
				return self._config['reset_command']()
		return None

	def _register_name(self, reg_number):
		return self._register_map[reg_number]['name']

	def _register_number(self, reg_string):
		reg_string_orig = reg_string

		if isinstance(reg_string, int):
			return reg_string
		if reg_string.isnumeric():
			return int(reg_string)
		for reg_number, reg_info in enumerate(self._register_map):
			if reg_info['name'] == reg_string:
				return reg_number
		raise NameError("Invalid register value {}".format(reg_string_orig))

	def _check_radio(self):
		value1 = self.get_register(0);
		value2 = self.get_register(1);

		if value1 == 0x6fe0 and value2 == 0x5681:
			return True
		return False

	def _set_defaults(self):
		self.put_register_bits('radio_state', {'tx_enabled': 0, 'rx_enabled': 0, 'channel': 76})
		self.put_register_bits('power', {'current': 4, 'gain': 0})
		self.put_register_bits('rssi_power', {'mode': 0})
		self.put_register_bits('crystal', {'trim_adjust': 0})
		self.put_register_bits('packet_config', {
			'preamble_len': 2,
			'syncword_len': 1,
			'trailer_len': 0,
			'packet_type': 0,
			'fec_type': 0,
			'br_clock_sel': 0
		})
		self.put_register_bits('chip_power', {
			'power_down': 0,
			'sleep_mode': 0,
			'br_clock_on_sleep': 0,
			'rexmit_times': 3,
			'miso_tri_opt': 0,
			'scramble_value': 0
		})
		self.put_register_bits('thresholds', {
			'fifo_empty_threshold': 8,
			'fifo_full_threshold': 16,
			'syncword_error_bits': 2
		})
		self.put_register_bits('format_config', {
			'crc_enabled': 1,
			'scramble_enabled': 0,
			'packet_length_encoded': 1,
			'auto_term_tx': 1,
			'auto_ack': 0,
			'pkt_fifo_polarity': 0,
			'crc_initial_data': 0
		})
		self.put_register_bits('scan_rssi', {'channel': 63, 'ack_time': 176})
		self.put_register_bits('gain_block', {'enabled': 1})
		self.put_register_bits('vco_calibrate', {'enabled': 1})
		self.put_register_bits('scan_rssi_state', {'enabled': 0, 'channel_offset': 0, 'wait_time': 15})

		return True

	def _put_register_high_low(self, reg, high, low, delay = 7):
		reg = self._register_number(reg)
		result = self._spi.xfer([reg, high, low], self._spi.max_speed_hz, delay)

		if reg & 0x80 == 0x80:
			self._debug(" regRead[%02X] = %s" % ((reg & 0x7f), result))
		else:
			self._debug("regWrite[%02X:0x%02X%02X] = %s" % (reg, high, low, result))

		#if reg & 0x80 != 0x80:
		#	time.sleep(delay / 1000.0)

		return result

	def put_register(self, reg, value):
		high = (value >> 8) & 0xff
		low  = value & 0xff
		return self._put_register_high_low(reg, high, low)

	def put_register_bits(self, reg, bits_dict):
		# Convert register to an integer
		reg = self._register_number(reg)

		# Lookup register in the register map
		register_info = self._register_map[reg]

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
		reg = self._register_number(reg)

		# Reading of a register is indicated by setting high bit
		read_reg = reg | 0b10000000

		# Put the request with space for the reply
		value = self._put_register_high_low(read_reg, 0, 0)

		# The reply is stored in the lower two bytes
		result = value[1] << 8 | value[2]

		# Return result
		return result

	def get_register_bits(self, reg, value = None):
		# Convert register to an integer
		reg = self._register_number(reg)

		# Get the register's value (unless one was supplied)
		if value is None:
			value = self.get_register(reg)

		# Lookup register in the register map
		register_info = self._register_map[reg]

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
		self._config = config

		if config is None:
			return None

		self._spi.max_speed_hz = self._config.get('frequency', 4000000)
		self._spi.bits_per_word = self._config.get('bits_per_word', 8)
		self._spi.cshigh = self._config.get('csigh', False)
		self._spi.no_cs  = self._config.get('no_cs', False)
		self._spi.lsbfirst = self._config.get('lsbfirst', False)
		self._spi.threewire = self._config.get('threewire', False)
		self._spi.mode = self._config.get('mode', 1)

		return None

	def initialize(self):
		self._reset_device()

		self._set_defaults()

		if not self._check_radio():
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

		return None

	def fill_fifo(self, message, include_length = True):
		new_message = [self._register_number('fifo')]
		if include_length:
			new_message = new_message + [len(message)]
		new_message = new_message + message
		log_message = [] + new_message

		# Transfer the message
		result = self._spi.xfer(new_message, self._spi.max_speed_hz, 10)
		self._debug("Writing: {} = {}".format(log_message, result))

		return new_message

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
		self.fill_fifo(message, True)

		# Tell the radio to transmit the FIFO buffer to the specified channel
		self.put_register_bits('radio_state', {
			'tx_enabled': 1,
			'rx_enabled': 0,
			'channel': channel
		})

		# Wait for buffer to empty
		# XXX: Untested
		while True:
			radio_status = self.get_register_bits('status')
			self._debug("radio_status={}".format(radio_status))

			if radio_status['packet_flag'] == 1:
				break
			time.sleep(0.1)

		return True

	def multi_transmit(self, message, channels, retries = 3, delay = 0.1):
		for channel in channels:
			for i in range(retries):
				if not self.transmit(message, channel):
					return False
				time.sleep(delay / retries)
		return True

	def start_listening(self, channel):
		# Initialize the receiver
		self.stop_listening()

		# Go into listening mode
		self.put_register_bits('radio_state', {
			'tx_enabled': 0,
			'rx_enabled': 1,
			'channel': channel
		})

		return True

	def stop_listening(self):
		# Initialize the receiver
		self.put_register_bits('radio_state', {
			'tx_enabled': 0,
			'rx_enabled': 0,
			'channel': 0
		})

		self.put_register_bits('fifo_state', {
			'clear_read': 1,
			'clear_write': 1
		})

		return True

	def receive(self, channel = None, wait = False, length = None, wait_time = 0.1):
		if wait:
			if channel is None:
				state = self.get_register_bits('radio_state')
				channel = state['channel']

			self.start_listening(channel)

		message = []

		while True:
			radio_status = self.get_register_bits('status')
			if radio_status['packet_flag'] == 0:
				if wait:
					time.sleep(wait_time)
					continue
				else:
					return None

			if radio_status['crc_error'] == 1:
				# Handle invalid packet ?
				self.start_listening(channel)
				continue

			# Data is available, read it from the FIFO register
			# The first result will include the length
			# XXX *IF* length encoding is enabled ?
			fifo_data = self.get_register('fifo')
			message_length = fifo_data >> 8

			# Keep track of the total message length to truncate it
			final_message_length = message_length

			message += [fifo_data & 0xff]
			message_length -= 1

			# Read subsequent bytes from the FIFO register until
			# there are no more bytes to read
			while message_length > 0:
				fifo_data = self.get_register('fifo')
				message += [fifo_data >> 8, fifo_data & 0xff]
				message_length -= 2

			# Truncate the message to its final size, since we have
			# to read in 16-bit words, we may have an extra byte
			message = message[0:final_message_length]
			break

		return message
