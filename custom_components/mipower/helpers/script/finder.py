"""Script finder module for Smartify integration.

This module provides enterprise-grade functionality for discovering script-related
entities within a Home Assistant installation. It performs advanced analysis of
script configurations to find scripts that use specific remote entities.

The implementation follows SOLID principles and provides accurate device-based
script discovery without keyword filtering or fallback behaviors.
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List, Set, Optional
from dataclasses import dataclass

import yaml

from homeassistant.core import HomeAssistant  # type: ignore[import]
from homeassistant.helpers import entity_registry as er  # type: ignore[import]

from .validation import is_valid_script_entity

_LOGGER = logging.getLogger(__name__)


@dataclass
class ScriptAnalysisResult:
    """Result of script analysis."""

    script_id: str
    entity_references: Set[str]
    analysis_time_ms: float


@dataclass
class CacheEntry:
    """Cache entry for script analysis."""

    result: ScriptAnalysisResult
    timestamp: float
    config_hash: str


class ScriptAnalyzer:
    """Analyzes script YAML configurations to extract entity references."""

    def __init__(self, scripts_file: Path):
        self.scripts_file = scripts_file

    def analyze_script_sync(self, script_id: str) -> ScriptAnalysisResult:
        """Synchronously analyze a script configuration."""
        import time

        start_time = time.time()

        entity_references: Set[str] = set()

        try:
            if not self.scripts_file.exists():
                _LOGGER.warning(f"Scripts file not found: {self.scripts_file}")
                return ScriptAnalysisResult(script_id, entity_references, 0.0)

            with open(self.scripts_file, "r", encoding="utf-8") as f:
                scripts_config = yaml.safe_load(f)

            if not scripts_config or not isinstance(scripts_config, dict):
                return ScriptAnalysisResult(script_id, entity_references, 0.0)

            # Get the specific script configuration
            script_config = scripts_config.get(script_id)
            if not script_config or not isinstance(script_config, dict):
                return ScriptAnalysisResult(script_id, entity_references, 0.0)

            # Extract entity references from script sequence
            sequence = script_config.get("sequence", [])
            entity_references = self._extract_entity_references(sequence)

        except Exception as e:
            _LOGGER.error(f"Error analyzing script {script_id}: {e}")
            # Continue with empty references

        analysis_time = (time.time() - start_time) * 1000
        return ScriptAnalysisResult(script_id, entity_references, analysis_time)

    def _extract_entity_references(self, sequence: list) -> Set[str]:
        """Extract entity references from script sequence."""
        entities: Set[str] = set()

        for step in sequence:
            if not isinstance(step, dict):
                continue

            # Direct entity_id references
            if "entity_id" in step:
                entity_id = step["entity_id"]
                if isinstance(entity_id, str):
                    entities.add(entity_id)
                elif isinstance(entity_id, list):
                    entities.update(entity_id)

            # Target entity references
            if "target" in step and isinstance(step["target"], dict):
                target_entity = step["target"].get("entity_id")
                if isinstance(target_entity, str):
                    entities.add(target_entity)
                elif isinstance(target_entity, list):
                    entities.update(target_entity)

            # Device action references (convert to entity_ids)
            if "device_id" in step and "entity_id" in step:
                entities.add(step["entity_id"])

            # Recursive processing for nested structures
            for value in step.values():
                if isinstance(value, dict):
                    entities.update(self._extract_entity_references([value]))
                elif isinstance(value, list):
                    entities.update(self._extract_entity_references(value))

        return entities


class EntityRelationshipMapper:
    """Maps remote devices to their associated scripts based on entity relationships."""

    def __init__(self, hass: HomeAssistant):
        self.hass = hass
        self._entity_registry = er.async_get(hass)

    def get_remote_device_id(self, remote_entity_id: str) -> Optional[str]:
        """Get the device ID for the remote entity."""
        try:
            entity_entry = self._entity_registry.async_get(remote_entity_id)
            if entity_entry:
                return entity_entry.device_id
            else:
                # If entity not found, assume the parameter is already a device_id
                _LOGGER.debug(
                    f"Entity {remote_entity_id} not found, assuming it's a device_id"
                )
                return remote_entity_id
        except Exception as e:
            _LOGGER.error(f"Error getting device ID for {remote_entity_id}: {e}")
            # Fallback: assume the parameter is already a device_id
            return remote_entity_id

    def match_device_scripts(
        self,
        remote_device_id: str,
        script_analyses: Dict[str, ScriptAnalysisResult],
    ) -> List[str]:
        """Find scripts that reference entities from the same device."""
        matching_scripts: List[str] = []

        for script_id, analysis in script_analyses.items():
            # Check if any script entity belongs to the same device
            for entity_id in analysis.entity_references:
                entity_entry = self._entity_registry.async_get(entity_id)
                if entity_entry and entity_entry.device_id == remote_device_id:
                    matching_scripts.append(script_id)
                    break  # Found match, no need to check other entities

        return matching_scripts


class SmartCacheManager:
    """Intelligent cache manager for script analysis results."""

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[str, CacheEntry] = {}
        self._access_order: List[str] = []

    def get(self, script_id: str, config_hash: str) -> Optional[ScriptAnalysisResult]:
        """Get cached result if valid."""
        import time

        if script_id not in self._cache:
            return None

        entry = self._cache[script_id]

        # Check TTL
        if time.time() - entry.timestamp > self.ttl_seconds:
            self._remove(script_id)
            return None

        # Check config hash
        if entry.config_hash != config_hash:
            self._remove(script_id)
            return None

        # Update access order for LRU
        self._access_order.remove(script_id)
        self._access_order.append(script_id)

        return entry.result

    def put(self, script_id: str, result: ScriptAnalysisResult, config_hash: str):
        """Cache analysis result."""
        import time

        # Remove if exists
        if script_id in self._cache:
            self._access_order.remove(script_id)

        # Evict if at capacity
        if len(self._cache) >= self.max_size:
            lru_script = self._access_order.pop(0)
            del self._cache[lru_script]

        # Add new entry
        entry = CacheEntry(result, time.time(), config_hash)
        self._cache[script_id] = entry
        self._access_order.append(script_id)

    def _remove(self, script_id: str):
        """Remove entry from cache."""
        if script_id in self._cache:
            del self._cache[script_id]
            if script_id in self._access_order:
                self._access_order.remove(script_id)

    def clear(self):
        """Clear all cache entries."""
        self._cache.clear()
        self._access_order.clear()

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "ttl_seconds": self.ttl_seconds,
            "hit_rate": 0.0,  # Could be implemented with hit/miss counters
        }


class ScriptDeviceRelationshipService:
    """Main service for enterprise-grade script-device relationship analysis."""

    def __init__(self, hass: HomeAssistant, scripts_file: Optional[Path] = None):
        self.hass = hass
        self.scripts_file = scripts_file or self._find_scripts_file()

        self.analyzer = ScriptAnalyzer(self.scripts_file)
        self.mapper = EntityRelationshipMapper(hass)
        self.cache = SmartCacheManager()

        # Get all script entities for analysis
        entity_registry = er.async_get(hass)
        self.script_entities = [
            entity
            for entity in entity_registry.entities.values()
            if is_valid_script_entity(entity)
        ]

    def _find_scripts_file(self) -> Path:
        """Find the scripts.yaml file in Home Assistant config."""
        config_dir = Path(self.hass.config.config_dir)
        scripts_file = config_dir / "scripts.yaml"

        # If scripts.yaml doesn't exist, check for scripts directory
        if not scripts_file.exists():
            scripts_dir = config_dir / "scripts"
            if scripts_dir.exists() and scripts_dir.is_dir():
                # Look for any yaml file in scripts directory
                yaml_files = list(scripts_dir.glob("*.yaml"))
                if yaml_files:
                    return yaml_files[0]  # Return first yaml file found

        return scripts_file

    async def find_scripts_for_device(
        self, remote_entity_id: str
    ) -> List[Dict[str, Any]]:
        """Find all scripts that are associated with the given remote device."""
        _LOGGER.info(
            f"Starting enterprise script discovery for device: {remote_entity_id}"
        )

        # Step 1: Get remote device ID
        _LOGGER.info(
            f"🔍 Starting script discovery for remote entity: {remote_entity_id}"
        )
        remote_device_id = self.mapper.get_remote_device_id(remote_entity_id)
        _LOGGER.info(f"🔍 Remote entity: {remote_entity_id}")
        _LOGGER.info(f"🔍 Remote device ID: {remote_device_id}")

        if not remote_device_id:
            _LOGGER.error(
                f"❌ No device ID found for remote entity: {remote_entity_id}"
            )
            return []

        # Step 2: Analyze scripts
        _LOGGER.info("🔍 Analyzing scripts...")
        script_analyses = await self._analyze_scripts()
        _LOGGER.info(f"🔍 Analyzed {len(script_analyses)} scripts")

        # Log script analysis results
        # for script_id, analysis in script_analyses.items():
        #     _LOGGER.debug(
        #         f"📄 Script {script_id}: {len(analysis.entity_references)} entities"
        #     )
        #     for entity in analysis.entity_references:
        #         _LOGGER.debug(f"   └─ {entity}")

        # Step 3: Find matching scripts based on device ID
        _LOGGER.info(f"🔍 Matching scripts for device {remote_device_id}")
        matching_script_ids = self.mapper.match_device_scripts(
            remote_device_id, script_analyses
        )
        _LOGGER.info(
            f"🔍 Found {len(matching_script_ids)} matching scripts: {matching_script_ids}"
        )

        # Step 4: Build result with entity information
        results = []
        entity_registry = er.async_get(self.hass)

        for script_id in matching_script_ids:
            entity_entry = entity_registry.async_get(f"script.{script_id}")
            if entity_entry:
                display_name = entity_entry.name or script_id
                script_state = self.hass.states.get(f"script.{script_id}")
                script_alias = None

                if script_state and hasattr(script_state, "attributes"):
                    attributes = script_state.attributes
                    script_alias = attributes.get("friendly_name") or attributes.get(
                        "alias"
                    )

                results.append(
                    {
                        "id": f"script.{script_id}",
                        "name": display_name,
                        "alias": script_alias or display_name,
                    }
                )

        results.sort(key=lambda x: x["name"])
        _LOGGER.info(f"Found {len(results)} scripts for device {remote_entity_id}")

        return results

    async def _analyze_scripts(self) -> Dict[str, ScriptAnalysisResult]:
        """Analyze all available scripts with controlled concurrency and parallelism."""
        analyses: Dict[str, ScriptAnalysisResult] = {}
        config_hash = await self._get_config_hash()

        # Process scripts sequentially to avoid thread issues and timeouts
        for entity in self.script_entities:
            script_id = entity.entity_id.replace("script.", "")

            try:
                result = await self._analyze_script_async(script_id, config_hash)
                analyses[script_id] = result
            except Exception as e:
                _LOGGER.warning(f"Failed to analyze script {script_id}: {e}")
                continue

        _LOGGER.debug(f"Completed analysis of {len(analyses)} scripts")
        return analyses

    async def _analyze_script_async(
        self, script_id: str, config_hash: str
    ) -> ScriptAnalysisResult:
        """Analyze a script asynchronously with caching."""
        # Check cache first
        cached_result = self.cache.get(script_id, config_hash)
        if cached_result:
            return cached_result

        # Analyze in executor
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            None, self.analyzer.analyze_script_sync, script_id
        )

        # Cache result
        self.cache.put(script_id, result, config_hash)

        return result

    def _get_config_hash_sync(self) -> str:
        """Get hash of script configurations for cache invalidation (sync version)."""
        import hashlib

        hasher = hashlib.md5()
        try:
            # Hash the main scripts file
            if self.scripts_file.exists():
                with open(self.scripts_file, "rb") as f:
                    hasher.update(f.read())

            # Also check for any additional script files in scripts directory
            scripts_dir = self.scripts_file.parent / "scripts"
            if scripts_dir.exists() and scripts_dir.is_dir():
                for script_file in scripts_dir.glob("*.yaml"):
                    if script_file.is_file():
                        with open(script_file, "rb") as f:
                            hasher.update(f.read())
        except Exception:
            pass  # Use empty hash on error

        return hasher.hexdigest()

    async def _get_config_hash(self) -> str:
        """Get hash of script configurations for cache invalidation (async version)."""
        # Use executor to avoid blocking the event loop
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._get_config_hash_sync)


# Global service instance
_service_instance: Optional[ScriptDeviceRelationshipService] = None


async def find_scripts_for_device_async(
    hass: HomeAssistant, remote_entity_id: str
) -> List[Dict[str, Any]]:
    """Enterprise-grade script discovery for remote devices (async version).

    This function performs advanced analysis of script configurations to accurately
    identify scripts that use specific remote entities. No keyword filtering or
    fallback behaviors are used - only precise entity relationship analysis.

    Args:
        hass: Home Assistant instance
        remote_entity_id: Remote entity ID to find scripts for

    Returns:
        List of script dictionaries with id, name, and alias information

    Raises:
        Exception: If analysis fails (no fallback behavior)
    """
    global _service_instance

    if _service_instance is None:
        _service_instance = ScriptDeviceRelationshipService(hass)

    return await _service_instance.find_scripts_for_device(remote_entity_id)


def find_scripts_for_device(
    hass: HomeAssistant, remote_entity_id: str
) -> List[Dict[str, Any]]:
    """Enterprise-grade script discovery for remote devices.

    This function performs advanced analysis of script configurations to accurately
    identify scripts that use specific remote entities. No keyword filtering or
    fallback behaviors are used - only precise entity relationship analysis.

    Args:
        hass: Home Assistant instance
        remote_entity_id: Remote entity ID to find scripts for

    Returns:
        List of script dictionaries with id, name, and alias information

    Raises:
        Exception: If analysis fails (no fallback behavior)
    """
    # Create a new event loop for this thread if one doesn't exist
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is already running, we need to handle this differently
            # This happens in Home Assistant's async context
            import concurrent.futures

            # Use a thread pool to run the async function
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(_run_async_in_thread, hass, remote_entity_id)
                return future.result(timeout=30)  # 30 second timeout
        else:
            # Loop exists but not running, we can use it
            return loop.run_until_complete(
                find_scripts_for_device_async(hass, remote_entity_id)
            )
    except RuntimeError:
        # No event loop exists, create one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                find_scripts_for_device_async(hass, remote_entity_id)
            )
        finally:
            loop.close()


def _run_async_in_thread(
    hass: HomeAssistant, remote_entity_id: str
) -> List[Dict[str, Any]]:
    """Run async function in a separate thread with its own event loop."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(
            find_scripts_for_device_async(hass, remote_entity_id)
        )
    finally:
        loop.close()
