# Python LT8900 via SPI

This Python module enables a Python to talk to an LT8900 radio attached to an serial peripheral interface (SPI).

## API
### Synopsis

    lt8900_spi.Radio(spi_bus, spi_dev, config = None) -> instance
    lt8900_spi.Radio.put_register(reg, value) -> value
    lt8900_spi.Radio.put_register_bits(reg, bits_dict) -> value
    lt8900_spi.Radio.get_register(reg) -> value
    lt8900_spi.Radio.get_register_bits(reg, value = None) -> dictionary
    lt8900_spi.Radio.configure(config) -> None
    lt8900_spi.Radio.initialize() -> boolean
    lt8900_spi.Radio.set_channel(channel) -> dictionary
    lt8900_spi.Radio.set_syncword(syncword) -> None
    lt8900_spi.Radio.fill_fifo(message, include_length = True) -> list
    lt8900_spi.Radio.transmit(message, channel = None) -> boolean
    lt8900_spi.Radio.multi_transmit(message, channels, retries = 3, delay = 0.1) -> boolean
    lt8900_spi.Radio.start_listening(channel) -> boolean
    lt8900_spi.Radio.stop_listening() -> boolean
    lt8900_spi.Radio.receive(channel = None, wait = False, length = None, wait_time = 0.1) -> list

### instance.get\_register\_bits

Low-level primitive to get a named register with bitfields expanded to names.

### instance.put\_register\_bits

Low-level primitive to set a named register by bitfield value.

### instance.set\_syncword

High-level interface to syncword mechanism.  The syncword can be 1, 2, 3, or 4 16-bit words long and should be provided as an array.

Example:

    instance.set_syncword([1, 2, 3, 4])

### instance.transmit

Transmit a message.  If a channel is specified transmit on that channel -- otherwise the current channel is queried and then used.

### instance.multi\_transmit

Transmit a message across multiple channels multiple times.  This is a common pattern so this function is provided for convience.

## Example

    #! /usr/bin/env python3
    
    import time

    import gpiozero
    import lt8900_spi
    
    # Need to keep this attached to drive the line high -- if the object disappears then
    # the GPIO port gets reconfigured as an input port
    # Note broadcom pin numbers are used
    reset_gpio = gpiozero.LED(24)
    reset_gpio.on()
    def reset_module_via_gpio():    
    	reset_gpio.off()
    	time.sleep(0.1)
    	reset_gpio.on()
    	time.sleep(0.1)

    radio = lt8900_spi.Radio(0, 0, {
    	'reset_command': reset_module_via_gpio
    })
    
    if not radio.initialize():
    	raise ValueError('Initialize failed')

    radio.set_syncword([0x258B, 0x147A])

    radio.multi_transmit([0xB0, 0x51, 0xF0, 0x00, 0x00, 0x01, 212], [9, 40, 71], delay = 0.5)
