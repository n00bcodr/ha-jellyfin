"""Buttons for the Media Browser (Emby/Jellyfin) integration."""

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DATA_HUB, DOMAIN, ENTITY_TITLE_MAP, EntityType, SERVICE_PURGE_DEVICES
from .entity import MediaBrowserEntity
from .hub import MediaBrowserHub


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MediaBrowser buttons."""
    hub: MediaBrowserHub = hass.data[DOMAIN][entry.entry_id][DATA_HUB]
    async_add_entities(
        [
            MediaBrowserRescanButton(hub),
            MediaBrowserRestartButton(hub),
            MediaBrowserShutdownButton(hub),
            MediaBrowserClearSessionsButton(hub),
        ]
    )


class MediaBrowserRestartButton(MediaBrowserEntity, ButtonEntity):
    """Representation of a restart button entity."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_device_class = ButtonDeviceClass.RESTART

    def __init__(self, hub: MediaBrowserHub) -> None:
        super().__init__(hub)
        self._attr_name = (
            f"{self.hub.server_name} {ENTITY_TITLE_MAP[EntityType.RESTART]}"
        )
        self._attr_unique_id = f"{self.hub.server_id}-{EntityType.RESTART}"
        self._attr_icon = "mdi:restart"

    async def async_press(self) -> None:
        await self.hub.async_restart()


class MediaBrowserShutdownButton(MediaBrowserEntity, ButtonEntity):
    """Representation of a shutdown button entity."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, hub: MediaBrowserHub) -> None:
        super().__init__(hub)
        self._attr_name = (
            f"{self.hub.server_name} {ENTITY_TITLE_MAP[EntityType.SHUTDOWN]}"
        )
        self._attr_unique_id = f"{self.hub.server_id}-{EntityType.SHUTDOWN}"
        self._attr_icon = "mdi:power"

    async def async_press(self) -> None:
        await self.hub.async_shutdown()


class MediaBrowserRescanButton(MediaBrowserEntity, ButtonEntity):
    """Representation of a rescan button entity."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, hub: MediaBrowserHub) -> None:
        super().__init__(hub)
        self._attr_name = (
            f"{self.hub.server_name} {ENTITY_TITLE_MAP[EntityType.RESCAN]}"
        )
        self._attr_unique_id = f"{self.hub.server_id}-{EntityType.RESCAN}"
        self._attr_icon = "mdi:database-refresh"

    async def async_press(self) -> None:
        await self.hub.async_rescan()


class MediaBrowserClearSessionsButton(MediaBrowserEntity, ButtonEntity):
    """Representation of a button to clear orphaned session devices."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_icon = "mdi:trash-can"

    def __init__(self, hub: MediaBrowserHub) -> None:
        super().__init__(hub)
        self._attr_name = f"{self.hub.server_name} Clear Sessions"
        self._attr_unique_id = f"{self.hub.server_id}-clear-sessions"

    async def async_press(self) -> None:
        await self.hass.services.async_call(DOMAIN, SERVICE_PURGE_DEVICES, {}, True)
