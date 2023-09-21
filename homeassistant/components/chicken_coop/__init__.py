"""The Chicken coop integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

# List the platforms that we want to support.
PLATFORMS: list[Platform] = [Platform.COVER]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Chicken coop from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    # ODO 1. Create API instance
    # ODO 2. Validate the API connection (and authentication)
    # ODO 3. Store an API object for your platforms to access
    hass.data[DOMAIN][entry.entry_id] = entry
    # MyApi(...)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
