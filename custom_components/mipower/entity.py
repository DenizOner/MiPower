# custom_components/mipower/entity.py
"""MiPower switch entity implementation."""

from __future__ import annotations

import logging
import shutil
from typing import Any, List, Optional, Callable

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.event import async_track_state_change_event, async_call_later

from .const import DOMAIN, DEFAULT_OFF_DEBOUNCE

_LOGGER = logging.getLogger(__name__)

SCAN_TIMEOUT = 15
CONNECT_TIMEOUT = 20


class MiPowerSwitch(SwitchEntity):
    """MiPower switch entity with debounce and bluetooth connect."""

    def __init__(self, hass: HomeAssistant, entry_id: str, name: str, mac: Optional[str], device_id: Optional[str] = None, media_player_entity_id: Optional[str] = None, coordinator=None) -> None:
        self.hass = hass
        self._entry_id = entry_id
        self._name = name or "MiPower"
        self._mac = (mac or "").upper()
        self._device_id = device_id
        self._media_player_entity_id = media_player_entity_id
        self._available = True
        self._is_on_internal = False
        self._coordinator = coordinator

        self._attr_unique_id = f"mipower_{(self._mac or '').replace(':','')}"
        self._attr_icon = "mdi:power"

        # set device_info so device registry shows a device (this helps UI)
        self._device_info = {
            "identifiers": {(DOMAIN, self._mac)},
            "name": self._name,
            "manufacturer": "Xiaomi (MiPower)",
            "model": "MiPower (bluetooth wake)",
        }

        self._unsub_media: Optional[Callable] = None
        self._off_check_handle: Optional[Callable] = None
        self._off_debounce_seconds: int = DEFAULT_OFF_DEBOUNCE

        self._connect_failures = 0
        self._connect_failure_threshold = 3

    @property
    def device_info(self):
        return self._device_info

    @property
    def name(self) -> str:
        return self._name

    @property
    def available(self) -> bool:
        return self._available

    @property
    def is_on(self) -> bool:
        if self._media_player_entity_id or self._device_id:
            if self._off_check_handle:
                return True
            return self._device_is_on()
        return self._is_on_internal

    def _get_device_entity_ids(self) -> List[str]:
        if not self._device_id:
            return []
        registry = er.async_get(self.hass)
        entity_ids: List[str] = []
        for ent in registry.entities.values():
            if ent.device_id == self._device_id:
                entity_ids.append(ent.entity_id)
        return entity_ids

    def _get_tracked_entity_ids(self) -> List[str]:
        if self._media_player_entity_id:
            return [self._media_player_entity_id]
        return self._get_device_entity_ids()

    def _device_is_on(self) -> bool:
        for entity_id in self._get_tracked_entity_ids():
            st = self.hass.states.get(entity_id)
            if st is None:
                continue
            if st.state in ("on", "playing", "active"):
                return True
        return False

    async def async_added_to_hass(self) -> None:
        entry = self.hass.config_entries.async_get_entry(self._entry_id)
        if entry:
            opt = entry.options.get("off_debounce")
            if opt is not None:
                try:
                    self._off_debounce_seconds = int(opt)
                except Exception:
                    pass

            # if options contain connect_failure_threshold adjust
            cf = entry.options.get("connect_failure_threshold")
            if cf:
                try:
                    self._connect_failure_threshold = int(cf)
                except Exception:
                    pass

        tracked = self._get_tracked_entity_ids()
        if tracked:
            self._unsub_media = async_track_state_change_event(self.hass, tracked, self._async_media_state_changed)
        self.async_write_ha_state()

    async def async_will_remove_from_hass(self) -> None:
        if self._unsub_media:
            try:
                self._unsub_media()
            except Exception:
                pass
        self._unsub_media = None
        self._cancel_off_check()

    def _cancel_off_check(self) -> None:
        if self._off_check_handle:
            try:
                self._off_check_handle()
            except Exception:
                pass
        self._off_check_handle = None

    def _schedule_off_check(self) -> None:
        self._cancel_off_check()
        self._off_check_handle = async_call_later(self.hass, self._off_debounce_seconds, self._confirm_off)

    async def _confirm_off(self, _now) -> None:
        self._off_check_handle = None
        if not self._device_is_on():
            self.async_write_ha_state()

    @callback
    def _async_media_state_changed(self, event) -> None:
        entity_id = event.data.get("entity_id")
        if self._device_is_on():
            self._cancel_off_check()
            self.async_write_ha_state()
            return
        self._schedule_off_check()

    async def async_turn_on(self, **kwargs: Any) -> None:
        self._cancel_off_check()
        if (self._media_player_entity_id or self._device_id) and self._device_is_on():
            self.async_write_ha_state()
            return

        if not shutil.which("bluetoothctl"):
            _LOGGER.error("MiPower: bluetoothctl bulunamadi; connect yapılamaz.")
            return

        if not (self._media_player_entity_id or self._device_id):
            self._is_on_internal = True
            self.async_write_ha_state()

        try:
            success = await self.hass.async_add_executor_job(self._connect_device_blocking, self._mac)
            if success:
                self._connect_failures = 0
            else:
                self._connect_failures += 1
                if self._connect_failures >= self._connect_failure_threshold:
                    _LOGGER.warning("MiPower: connect başarısız %s (failure_count=%s)", self._mac, self._connect_failures)
                else:
                    _LOGGER.debug("MiPower: connect başarısız %s (attempt %s)", self._mac, self._connect_failures)
        except Exception:
            _LOGGER.exception("MiPower: connect sırasında hata")
        finally:
            if not (self._media_player_entity_id or self._device_id):
                self._is_on_internal = False
                self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        self._cancel_off_check()
        targets = []
        if self._media_player_entity_id:
            targets.append(self._media_player_entity_id)
        elif self._device_id:
            targets = [eid for eid in self._get_device_entity_ids() if eid.startswith("media_player.")]

        if targets:
            for target in targets:
                try:
                    await self.hass.services.async_call("media_player", "turn_off", {"entity_id": target}, blocking=True)
                except Exception:
                    _LOGGER.exception("MiPower: media_player.turn_off sırasında hata %s", target)
            self.async_write_ha_state()
            return

        self._is_on_internal = False
        self.async_write_ha_state()

    def _connect_device_blocking(self, mac: str) -> bool:
        """
        Robust connect / wake flow:
        - register NoInputNoOutput agent and default-agent
        - start scan for SCAN_TIMEOUT seconds
        - attempt pair (if possible) then connect
        - if connect fails, do a couple of retries with small delays
        Returns True on success, False otherwise.
        """
        try:
            import pexpect  # type: ignore
        except Exception as e:
            _LOGGER.exception("MiPower: pexpect import edilemedi: %s", e)
            return False

        # sanity: mac uppercase and normalized
        mac = (mac or "").upper()

        try:
            child = pexpect.spawn("bluetoothctl", encoding="utf-8", timeout=CONNECT_TIMEOUT)
        except Exception as e:
            _LOGGER.exception("MiPower: bluetoothctl başlatılamadı: %s", e)
            return False

        try:
            # Try to register agent (best-effort)
            try:
                child.sendline("agent NoInputNoOutput")
                child.expect([r"Agent registered", pexpect.TIMEOUT], timeout=3)
            except Exception:
                # non-fatal
                pass
            try:
                child.sendline("default-agent")
            except Exception:
                pass

            # Start scanning
            try:
                child.sendline("scan on")
            except Exception:
                pass

            # Wait SCAN_TIMEOUT seconds for device to appear (or just wait the timeout)
            found_mac = False
            try:
                # Wait either for mac to appear in output or for timeout
                idx = child.expect([mac, pexpect.TIMEOUT], timeout=SCAN_TIMEOUT)
                if idx == 0:
                    found_mac = True
            except Exception:
                found_mac = False

            # Try pairing (best-effort). Some devices accept pair which wakes them.
            try:
                child.sendline(f"pair {mac}")
                # look for common success indicators
                idx = child.expect([r"Pairing successful", r"Paired: yes", r"AlreadyExists", pexpect.TIMEOUT], timeout=PAIRING_TIMEOUT)
                if idx in (0, 1, 2):
                    # pairing-like success -> trust and continue
                    try:
                        child.sendline(f"trust {mac}")
                    except Exception:
                        pass
            except Exception:
                # pairing may fail or be unnecessary; continue to connect attempt
                pass

            # Try to connect (retry loop)
            attempts = 0
            max_attempts = max(1, self._connect_failure_threshold or 3)
            while attempts < max_attempts:
                attempts += 1
                try:
                    child.sendline(f"connect {mac}")
                except Exception:
                    # maybe bluetoothctl died; break
                    _LOGGER.debug("MiPower: connect sendline failed (attempt %s)", attempts)
                    break

                try:
                    idx = child.expect([r"Connection successful", r"Failed to connect", r"Connection timed out", pexpect.TIMEOUT], timeout=CONNECT_TIMEOUT)
                    if idx == 0:
                        # optionally disconnect to leave device in idle; but success is success
                        try:
                            child.sendline("disconnect")
                        except Exception:
                            pass
                        try:
                            child.sendline("scan off")
                        except Exception:
                            pass
                        child.close()
                        _LOGGER.debug("MiPower: connect successful (attempt %s) mac=%s", attempts, mac)
                        return True
                    else:
                        # failed attempt; try again after short wait
                        _LOGGER.debug("MiPower: connect attempt %s failed (idx=%s).", attempts, idx)
                except Exception as exc:
                    _LOGGER.debug("MiPower: connect expect raised on attempt %s: %s", attempts, exc)

                # short backoff before retrying
                try:
                    import time
                    time.sleep( max(1, int(getattr(self, "_retry_interval", 2))) )
                except Exception:
                    awaitable_sleep = getattr(self, "_retry_interval", 2)
                    try:
                        # in blocking context, fallback to time.sleep
                        import time as _time
                        _time.sleep(awaitable_sleep)
                    except Exception:
                        pass

            # If we reached here, connection attempts exhausted
            try:
                child.sendline("scan off")
            except Exception:
                pass
            try:
                child.close()
            except Exception:
                pass

            _LOGGER.debug("MiPower: all connect attempts failed for mac=%s", mac)
            return False

        except Exception as exc:
            _LOGGER.exception("MiPower: connect sürecinde beklenmeyen hata: %s", exc)
            try:
                child.sendline("scan off")
            except Exception:
                pass
            try:
                child.close()
            except Exception:
                pass
            return False
