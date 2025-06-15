"""The Jellyfin integration."""
from __future__ import annotations

import logging
from datetime import timedelta
import json
import os

import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, PLATFORMS
from .jellyfin_api import JellyfinAPI

_LOGGER = logging.getLogger(__name__)

# Reduced interval for better responsiveness
SCAN_INTERVAL = timedelta(seconds=1)


def get_integration_version() -> str:
    """Get the integration version from manifest.json."""
    try:
        # Get the directory of this file
        integration_dir = os.path.dirname(__file__)
        manifest_path = os.path.join(integration_dir, "manifest.json")

        with open(manifest_path, "r") as f:
            manifest = json.load(f)
            return manifest.get("version", "2.1.0")
    except Exception as err:
        _LOGGER.warning("Could not read version from manifest.json: %s", err)
        return "2.1.0"  # Fallback version


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Jellyfin from a config entry."""
    session = async_get_clientsession(hass)

    # Get version from manifest
    integration_version = get_integration_version()

    api = JellyfinAPI(
        session,
        entry.data["host"],
        entry.data["api_key"],
        entry.data.get("port", 8096),
        entry.data.get("use_ssl", False),
        integration_version
    )

    # Test the connection
    try:
        await api.get_system_info()
    except Exception as err:
        _LOGGER.error("Failed to connect to Jellyfin server: %s", err)
        raise ConfigEntryNotReady from err

    coordinator = JellyfinDataUpdateCoordinator(hass, api)

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class JellyfinDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, api: JellyfinAPI) -> None:
        """Initialize."""
        self.api = api
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        """Update data via library."""
        try:
            async with async_timeout.timeout(10):
                data = {}

                # Get system info
                data["system_info"] = await self.api.get_system_info()

                # Get active sessions (only those with active playback)
                all_sessions = await self.api.get_sessions()
                data["sessions"] = [
                    session for session in all_sessions
                    if session.get("NowPlayingItem")
                ]

                # Get library stats
                data["library_stats"] = await self.api.get_library_stats()

                # Get users for reference
                data["users"] = await self.api.get_users()

                # Get latest media items (last 30)
                data["latest_movies"] = await self.api.get_latest_media("Movie", 30)
                data["latest_episodes"] = await self.api.get_latest_media("Episode", 30)
                data["latest_music"] = await self.api.get_latest_media("Audio", 30)

                return data

        except Exception as exception:
            raise UpdateFailed(f"Error communicating with API: {exception}") from exception