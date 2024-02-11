"""Sensor platform for Smar #1/#3 intergration."""
from __future__ import annotations
import dataclasses

from datetime import timedelta

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
)

from pysmarthashtag.models import ValueWithUnit

from .const import CONF_VEHICLE, DOMAIN
from .coordinator import SmartHashtagDataUpdateCoordinator
from .entity import SmartHashtagEntity

ENTITY_BATTERY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="remaining_range",
        name="Remaining Range",
        icon="mdi:road-variant",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement="km",
    ),
    SensorEntityDescription(
        key="remaining_range_at_full_charge",
        name="Remaining Range at full battery",
        icon="mdi:road-variant",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement="km",
    ),
    SensorEntityDescription(
        key="remaining_battery_percent",
        name="Remaining battery charge",
        icon="mdi:percent",
        device_class=SensorDeviceClass.BATTERY,
    ),
    # FIXME: Sort out type issue with None and Strings
    #    SensorEntityDescription(
    #        key="charging_status",
    #        name="Charging status",
    #        icon="mdi:power-plug-battery",
    #    ),
    SensorEntityDescription(
        key="charger_connection_status",
        name="Charger connection status",
        icon="mdi:battery-unknown",
    ),
    SensorEntityDescription(
        key="is_charger_connected",
        name="is charger connected",
        icon="mdi:power-plug-battery",
    ),
    SensorEntityDescription(
        key="charging_voltage",
        name="Charging voltage",
        icon="mdi:car-battery",
        device_class=SensorDeviceClass.VOLTAGE,
    ),
    SensorEntityDescription(
        key="charging_current",
        name="Charging current",
        icon="mdi:car-battery",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement="A",
    ),
    SensorEntityDescription(
        key="charging_power",
        name="Charging power",
        icon="mdi:car-battery",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement="W",
    ),
    SensorEntityDescription(
        key="charging_time_remaining",
        name="Charging time remaining",
        icon="mdi:clock-outline",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement="min",
    ),
    SensorEntityDescription(
        key="charging_target_soc",
        name="Target state of charge",
        icon="mdi:percent",
        device_class=SensorDeviceClass.BATTERY,
    ),
)

# FIXME: Find out how the position is handled in HA
ENTITY_POSITION_DESCRIPTIONS = (
    SensorEntityDescription(
        key="position",
        name="Postion",
        icon="mdi:map-marker",
    ),
    SensorEntityDescription(
        key="position_can_be_trusted",
        name="Position can be trusted",
        icon="mdi:map-marker-alert",
    ),
)


ENTITY_TIRE_DESCRIPTIONS = (
    SensorEntityDescription(
        key="temperature_0",
        name="Tire temperature driver front",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement="°C",
    ),
    SensorEntityDescription(
        key="temperature_1",
        name="Tire temperature driver rear",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement="°C",
    ),
    SensorEntityDescription(
        key="temperature_2",
        name="Tire temperature passender front",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement="°C",
    ),
    SensorEntityDescription(
        key="temperature_3",
        name="Tire temperature passenger rear",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement="°C",
    ),
    SensorEntityDescription(
        key="tire_pressure_0",
        name="Tire pressure front driver",
        icon="mdi:gauge",
        device_class=SensorDeviceClass.PRESSURE,
        native_unit_of_measurement="hPa",
    ),
    SensorEntityDescription(
        key="tire_pressure_1",
        name="Tire pressure rear driver",
        icon="mdi:gauge",
        device_class=SensorDeviceClass.PRESSURE,
        native_unit_of_measurement="hPa",
    ),
    SensorEntityDescription(
        key="tire_pressure_2",
        name="Tire pressure front passenger",
        icon="mdi:gauge",
        device_class=SensorDeviceClass.PRESSURE,
        native_unit_of_measurement="hPa",
    ),
    SensorEntityDescription(
        key="tire_pressure_3",
        name="Tire pressure rear passenger",
        icon="mdi:gauge",
        device_class=SensorDeviceClass.PRESSURE,
        native_unit_of_measurement="hPa",
    ),
)

ENTITY_MAINTENANCE_DESCRIPTIONS = (
    SensorEntityDescription(
        key="main_battery_state_of_charge",
        name="Main battery state of charge",
        icon="mdi:car-battery",
    ),
    SensorEntityDescription(
        key="main_battery_charge_level",
        name="Main battery charge level",
        icon="mdi:car-battery",
        device_class=SensorDeviceClass.BATTERY,
    ),
    SensorEntityDescription(
        key="main_battery_energy_level",
        name="Main battery energy level",
        icon="mdi:car-battery",
    ),
    SensorEntityDescription(
        key="main_battery_state_of_health",
        name="Main battery state of health",
        icon="mdi:car-battery",
    ),
    SensorEntityDescription(
        key="main_batter_power_level",
        name="Main battery power level",
        icon="mdi:car-battery",
    ),
    SensorEntityDescription(
        key="main_battery_voltage",
        name="Main battery voltage",
        icon="mdi:car-battery",
        device_class=SensorDeviceClass.VOLTAGE,
        native_unit_of_measurement="V",
    ),
    SensorEntityDescription(
        key="odometer",
        name="Odometer",
        icon="mdi:counter",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement="km",
    ),
    SensorEntityDescription(
        key="days_to_service",
        name="Service due in",
        icon="mdi:calendar-check",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement="d",
    ),
    SensorEntityDescription(
        key="engine_hours_to_service",
        name="Service due in",
        icon="mdi:calendar-check",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement="h",
    ),
    SensorEntityDescription(
        key="distance_to_service",
        name="Service due in",
        icon="mdi:calendar-check",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement="km",
    ),
    SensorEntityDescription(
        key="break_fluid_level_status",
        name="Break fluid level status",
        icon="mdi:car-brake-fluid-level",
    ),
    SensorEntityDescription(
        key="washer_fluid_level_status",
        name="Washer fluid level status",
        icon="mdi:wiper-wash",
    ),
    SensorEntityDescription(
        key="service_warning_status",
        name="Service warning status",
        icon="mdi:account-wrench",
    ),
)

ENTITY_GENERAL_DESCRIPTIONS = (
    SensorEntityDescription(
        key="last_update",
        name="Last update",
        icon="mdi:update",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
)

ENTITY_RUNNING_DESCRIPTIONS = (
    SensorEntityDescription(
        key="ahbc_status",
        name="Adaptive high beam control",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="goodbye",
        name="Goodbye Light",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="home_safe",
        name="Home Safe Light",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="corner_light",
        name="Corner Light",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="front_fog_light",
        name="Front Fog Light",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="stop_light",
        name="Stop Light",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="trip_meter1",
        name="Trip meter 1",
        icon="mdi:counter",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement="km",
    ),
    SensorEntityDescription(
        key="trip_meter2",
        name="Trip meter 2",
        icon="mdi:counter",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement="km",
    ),
    SensorEntityDescription(
        key="approach",
        name="Approach Light",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="high_beam",
        name="High Beam Light",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="engine_coolant_level_status",
        name="Engine coolant level status",
        icon="mdi:car-coolant-level",
    ),
    SensorEntityDescription(
        key="low_beam",
        name="Low Beam Light",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="position_light_rear",
        name="Position Light Rear",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="light_show",
        name="Light Show",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="welcome",
        name="Welcome Light",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="drl",
        name="Daytime running light",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="ahl",
        name="Adaptive headlight",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="trun_indicator_left",
        name="Turn indicator left",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="trun_indicator_right",
        name="Turn indicator right",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="adaptive_front_light",
        name="Adaptive front light",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="dbl",
        name="Double Light",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="average_speed",
        name="Average speed",
        icon="mdi:speedometer",
        device_class=SensorDeviceClass.SPEED,
        native_unit_of_measurement="km/h",
    ),
    SensorEntityDescription(
        key="position_light_front",
        name="Position Light Front",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="reverse_light",
        name="Reverse Light",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="highway_light",
        name="Highway Light",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="rear_fog_light",
        name="Rear Fog Light",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="flash_light",
        name="Flash Light",
        icon="mdi:car-parking-lights",
    ),
    SensorEntityDescription(
        key="all_weather_light",
        name="All Weather Light",
        icon="mdi:car-parking-lights",
    ),
)


def remove_vin_from_key(key: str) -> str:
    """Remove the vin from the key."""
    return "_".join(key.split("_")[1:])


def vin_from_key(key: str) -> str:
    """Get the vin from the key."""
    return key.split("_")[0]


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    vehicle = hass.data[DOMAIN][CONF_VEHICLE]

    async_add_devices(
        SmartHashtagBatteryRangeSensor(
            coordinator=coordinator,
            entity_description=dataclasses.replace(
                entity_description, key=f"{vehicle}_{entity_description.key}"
            ),
        )
        for entity_description in ENTITY_BATTERY_DESCRIPTIONS
    )

    async_add_devices(
        SmartHashtagTireSensor(
            coordinator=coordinator,
            entity_description=dataclasses.replace(
                entity_description, key=f"{vehicle}_{entity_description.key}"
            ),
        )
        for entity_description in ENTITY_TIRE_DESCRIPTIONS
    )

    async_add_devices(
        SmartHashtagUpdateSensor(
            coordinator=coordinator,
            entity_description=dataclasses.replace(
                entity_description, key=f"{vehicle}_{entity_description.key}"
            ),
        )
        for entity_description in ENTITY_GENERAL_DESCRIPTIONS
    )

    async_add_devices(
        SmartHashtagMaintenanceSensor(
            coordinator=coordinator,
            entity_description=dataclasses.replace(
                entity_description, key=f"{vehicle}_{entity_description.key}"
            ),
        )
        for entity_description in ENTITY_MAINTENANCE_DESCRIPTIONS
    )

    async_add_devices(
        SmartHashtagRunningSensor(
            coordinator=coordinator,
            entity_description=dataclasses.replace(
                entity_description, key=f"{vehicle}_{entity_description.key}"
            ),
        )
        for entity_description in ENTITY_RUNNING_DESCRIPTIONS
    )


class SmartHashtagBatteryRangeSensor(SmartHashtagEntity, SensorEntity):
    """Battery Sensor class."""

    def __init__(
        self,
        coordinator: SmartHashtagDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{self._attr_unique_id}_{entity_description.key}"
        self.entity_description = entity_description

    @property
    def native_value(self) -> int:
        """Return the native value of the sensor."""
        data = getattr(
            self.coordinator.account.vehicles.get(
                vin_from_key(self.entity_description.key)
            ).battery,
            remove_vin_from_key(self.entity_description.key),
        )

        if "charging_current" in self.entity_description.key:
            if data.value != 0:
                self.coordinator.update_interval = timedelta(seconds=30)
            else:
                self.coordinator.update_interval = timedelta(minutes=5)

        if "charging_power" in self.entity_description.key:
            if data.value == -0.0:
                return 0.0

        if isinstance(data, ValueWithUnit):
            return data.value

        return data

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of the sensor."""
        data = getattr(
            self.coordinator.account.vehicles.get(
                vin_from_key(self.entity_description.key)
            ).battery,
            remove_vin_from_key(self.entity_description.key),
        )
        if isinstance(data, ValueWithUnit):
            return data.unit

        return data


class SmartHashtagTireSensor(SmartHashtagEntity, SensorEntity):
    """Tire Status class."""

    def __init__(
        self,
        coordinator: SmartHashtagDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{self._attr_unique_id}_{entity_description.key}"
        self.entity_description = entity_description

    @property
    def native_value(self) -> float:
        """Return the native value of the sensor."""
        key = "_".join(self.entity_description.key.split("_")[1:-1])
        tire_idx = int(self.entity_description.key.split("_")[-1])
        return getattr(
            self.coordinator.account.vehicles.get(
                vin_from_key(self.entity_description.key)
            ).tires,
            key,
        )[tire_idx].value

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of the sensor."""
        key = "_".join(self.entity_description.key.split("_")[1:-1])
        tire_idx = int(self.entity_description.key.split("_")[-1])
        data = getattr(
            self.coordinator.account.vehicles.get(
                vin_from_key(self.entity_description.key)
            ).tires,
            key,
        )[tire_idx]

        # FIXME: if pysmarthashtag is updated to return the unit as °C remove this
        if data.unit == "C":
            return "°C"

        return data.unit


class SmartHashtagUpdateSensor(SmartHashtagEntity, SensorEntity):
    """Tire Status class."""

    def __init__(
        self,
        coordinator: SmartHashtagDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{self._attr_unique_id}_{entity_description.key}"
        self.entity_description = entity_description

    @property
    def native_value(self) -> float:
        """Return the native value of the sensor."""
        key = remove_vin_from_key(self.entity_description.key)
        vin = vin_from_key(self.entity_description.key)
        if key.startswith("service"):
            key = self.entity_description.key.split("_")[-1]
            data = self.coordinator.account.vehicles.get(vin).service[key]
        else:
            data = getattr(
                self.coordinator.account.vehicles.get(vin),
                remove_vin_from_key(self.entity_description.key),
            )
        if isinstance(data, ValueWithUnit):
            return data.value
        return data

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of the sensor."""
        key = remove_vin_from_key(self.entity_description.key)
        vin = vin_from_key(self.entity_description.key)
        if key.startswith("service"):
            key = key.split("_")[-1]
            data = self.coordinator.account.vehicles.get(vin).service[key]
        else:
            data = getattr(
                self.coordinator.account.vehicles.get(vin),
                key,
            )
        if isinstance(data, ValueWithUnit):
            return data.unit
        return self.entity_description.native_unit_of_measurement


class SmartHashtagMaintenanceSensor(SmartHashtagEntity, SensorEntity):
    """Tire Status class."""

    def __init__(
        self,
        coordinator: SmartHashtagDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{self._attr_unique_id}_{entity_description.key}"
        self.entity_description = entity_description

    @property
    def native_value(self) -> float | int | str | None:
        """Return the native value of the sensor."""
        key = remove_vin_from_key(self.entity_description.key)
        vin = vin_from_key(self.entity_description.key)
        data = getattr(
            self.coordinator.account.vehicles.get(vin).maintenance,
            key,
        )
        if isinstance(data, ValueWithUnit):
            return data.value
        return data

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of the sensor."""
        key = remove_vin_from_key(self.entity_description.key)
        vin = vin_from_key(self.entity_description.key)
        data = getattr(
            self.coordinator.account.vehicles.get(vin).maintenance,
            key,
        )
        if isinstance(data, ValueWithUnit):
            return data.unit
        return self.entity_description.native_unit_of_measurement


class SmartHashtagRunningSensor(SmartHashtagEntity, SensorEntity):
    """Tire Status class."""

    def __init__(
        self,
        coordinator: SmartHashtagDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{self._attr_unique_id}_{entity_description.key}"
        self.entity_description = entity_description

    @property
    def native_value(self) -> float | int | str | None:
        """Return the native value of the sensor."""
        key = remove_vin_from_key(self.entity_description.key)
        vin = vin_from_key(self.entity_description.key)
        data = getattr(
            self.coordinator.account.vehicles.get(vin).running,
            key,
        )
        if isinstance(data, ValueWithUnit):
            return data.value
        return data

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of the sensor."""
        key = remove_vin_from_key(self.entity_description.key)
        vin = vin_from_key(self.entity_description.key)
        data = getattr(
            self.coordinator.account.vehicles.get(vin).running,
            key,
        )
        if isinstance(data, ValueWithUnit):
            return data.unit
        return self.entity_description.native_unit_of_measurement
