
import logging
from datetime import timedelta, datetime

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_CODE, CONF_HOST, STATE_UNAVAILABLE
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

CONF_DEFAULT_MENSA = 828
MEAL_CATEGORY = "category"
MEAL_CATEGORY_KOMPLETT = "Komplett Menü"
MEAL_CATEGORY_VEGETARISCH = "Vegetarisches Menü"
MEAL_CATEGORY_WAHLESSEN = "Wahlessen"

ATTR_KOMPLETT_MENU = "komplett_menu"
ATTR_VEGETARISCHES_MENU = "vegetarisches_menu"
ATTR_WAHLESSEN = "wahlessen_"
MAX_WAHLESSEN_COUNT = 4

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)
CONST_NAME = "name"
STATE_ONLINE = "online"

ICON = "mdi:hamburger"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_CODE, default=CONF_DEFAULT_MENSA): cv.positive_int
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    from openmensa import OpenMensa as om
    _LOGGER.debug("in setup methode")
    mensa = config.get(CONF_CODE)
    add_entities([OpenmensaSensor(om, mensa)], True)

class OpenmensaSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, om, mensa):
        """Initialize the sensor."""
        self._om = om
        self._mensa = mensa
        self._state = STATE_UNAVAILABLE

        self._komplett_menu = None
        self._vegetarisches_menu = None
        self._wahlessen = None

    def get_meals_of_the_day(self):
        date_str = datetime.now().strftime("%Y-%m-%d")
        meals = self._om.get_meals_by_day(self._mensa, date_str)
        komplett_menu = None
        vegetarisches_menu = None
        wahlessen = []
        for meal in meals:
            if meal[MEAL_CATEGORY] == MEAL_CATEGORY_KOMPLETT:
                komplett_menu = meal[CONST_NAME]
            if meal[MEAL_CATEGORY] == MEAL_CATEGORY_VEGETARISCH:
                vegetarisches_menu = meal[CONST_NAME]
            if meal[MEAL_CATEGORY] == MEAL_CATEGORY_WAHLESSEN:
                wahlessen.append(meal[CONST_NAME])
        return (komplett_menu, vegetarisches_menu, wahlessen)

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Openmensa Sensor'

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return ICON

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def state_attributes(self):
        if self._state == STATE_UNAVAILABLE:
            return {}
        attr = {
            ATTR_KOMPLETT_MENU: self._komplett_menu,
            ATTR_VEGETARISCHES_MENU: self._vegetarisches_menu,
        }
        # There can be multiple Wahlessen and the number of meals is mostly random
        # check if a meal exists, otherwise set to None
        for idx in range(MAX_WAHLESSEN_COUNT):
            try:
                attr[ATTR_WAHLESSEN + str(idx)] = self._wahlessen[idx]
            except IndexError:
                attr[ATTR_WAHLESSEN + str(idx)] = None
        return attr

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Fetch new meals for the day
        """
        _LOGGER.debug("Updating meals of the day.")
        komplett, vegetarisch, wahlessen = self.get_meals_of_the_day()
        self._komplett_menu = komplett
        self._vegetarisches_menu = vegetarisch
        self._state = STATE_ONLINE
        self._wahlessen = wahlessen