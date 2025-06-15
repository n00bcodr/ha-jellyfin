"""Config flow for Jellyfin integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_HOST, CONF_PORT, CONF_SSL
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .jellyfin_api import JellyfinAPI

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_API_KEY): str,
        vol.Optional(CONF_PORT, default=8096): int,
        vol.Optional(CONF_SSL, default=False): bool,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    session = async_get_clientsession(hass)

    api = JellyfinAPI(
        session,
        data[CONF_HOST],
        data[CONF_API_KEY],
        data.get(CONF_PORT, 8096),
        data.get(CONF_SSL, False),
        "2.1.0"  # Default version for validation
    )

    try:
        system_info = await api.get_system_info()
    except Exception as err:
        _LOGGER.error("Failed to connect to Jellyfin server: %s", err)
        raise CannotConnect from err

    # Return info that you want to store in the config entry.
    return {
        "title": f"Jellyfin ({system_info.get('ServerName', 'Unknown')})",
        "server_name": system_info.get("ServerName", "Unknown"),
        "server_id": system_info.get("Id"),
        "version": system_info.get("Version"),
    }


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Jellyfin."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Create a unique ID based on server ID
                server_id = info.get("server_id")
                if server_id:
                    await self.async_set_unique_id(server_id)
                    self._abort_if_unique_id_configured()

                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""