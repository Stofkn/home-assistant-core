"""Support for Homekit covers."""
from __future__ import annotations

import time

from RPi import GPIO

from homeassistant.components.cover import CoverEntity, CoverEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo

from .const import CONF_DEVICE_ID, CONF_DEVICE_NAME, DOMAIN

# from .uart import UART


# ODO add device
# https://developers.home-assistant.io/docs/device_registry_index/#what-is-a-device
async def async_setup_entry(hass, conf, async_add_entities):
    """Set up the Example Cover component."""
    async_add_entities([DummyCover(conf)])


class DummyCover(CoverEntity):
    """Representation of a dummy cover."""

    def __init__(self, conf: ConfigEntry) -> None:
        """Initialise a new Chicken cover."""
        self._is_opening = False
        self._is_closing = False
        self._is_open = False
        self._device_id = conf.data[CONF_DEVICE_ID]
        self._device_name = conf.data[CONF_DEVICE_NAME]
        # self._uart = UART()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(16, GPIO.OUT)

    @property
    def unique_id(self) -> str | None:
        """Return the unique id for this device."""
        return f"chicken_coop_{self._device_id}"

    @property
    def device_class(self):
        """Return the device class of the cover."""
        return "garage"

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=self.name,
        )

    @property
    def name(self):
        """Return the name of the cover."""
        return self._device_name if self._device_name else "Chicken coop"

    @property
    def is_opening(self):
        """Return true if the cover is opening."""
        return self._is_opening

    @property
    def is_closing(self):
        """Return true if the cover is closing."""
        return self._is_closing

    @property
    def is_closed(self):
        """Return true if the cover is closed."""
        return not self._is_open

    @property
    def supported_features(self):
        """Flag supported features."""
        return CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE

    async def async_open_cover(self, **kwargs):
        """Open the cover."""
        # => Perform call to Chicken coop via HC12.

        GPIO.output(16, GPIO.HIGH)  # Turn on the LED
        time.sleep(1)  # Wait for 1 second
        GPIO.output(16, GPIO.LOW)  # Turn off the LED
        time.sleep(1)  # Wait for 1 second

        # <= Wait until we have confirmation that the message was received well.
        # The confirmation contains the current state (open/closed).
        # Retry after 1 second, keep on trying (5 times) until we get OK back
        # Keep track of sequence number.

        # => Send OK back. (Receiver will stop sending previous message)
        # message = bytearray([0x01, 0x02])
        # self._uart.send_message()
        self._is_open = True

        self.async_write_ha_state()

    async def async_close_cover(self, **kwargs):
        """Close the cover."""
        GPIO.output(16, GPIO.HIGH)  # Turn on the LED
        time.sleep(1)  # Wait for 1 second
        GPIO.output(16, GPIO.LOW)  # Turn off the LED
        time.sleep(1)  # Wait for 1 second
        self._is_open = False
        self.async_write_ha_state()
