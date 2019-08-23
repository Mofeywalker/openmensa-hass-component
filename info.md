# OpenMensa
A platform sensor which tells you which meals are served in your canteen.

## Example configuration.yaml
```yaml
sensor:
    - platform: openmensa
      code: 828
```
The configuration key ```code``` is required. This code represents the id of your Mensa.
You can determine that key via the OpenMensa Website. If the Homepage of your Mensa is
e.g. [https://openmensa.org/c/828](https://openmensa.org/c/828), then your code is ```828```.

The sensor contains the data in its attributes. As each mensa has their own labeling for the meals they offer, this sensor aggregates the categories and groups the meals per category.
This allows to parse the data of every mensa in the same manner and also have to name of the
category available.

```python
[{
	'name': 'Komplett Menü',
	'meals': [{
		'name': 'Paniertes Putenschnitzel'
	}]
}, {
	'name': 'Vegetarisches Menü',
	'meals': [{
		'name': 'Gemüsefrikadelle'
	}]
}, {
	'name': 'Wahlessen',
	'meals': [{
		'name': 'Gemüsereis'
	}, {
		'name': 'Flammkuchen mit Ziegenkäse, Honig und Rosmarin'
	}]
}]
```

Use the Template engine to look at your mensa's meal categories with:
```
{{states.sensor.openmensa_sensor.attributes}}
```

To get the name of the first meal category, use the following template
```
{{states.sensor.openmensa_sensor.attributes.categories[0].name}}
```

To get e.g. the "Komplett Menü", use the following template:
```
{{states.sensor.openmensa_sensor.attributes.categories[0].meals[0].name}}
```

The state of the sensor is set to ```no_meals``` if openmensa does not provide any information for the current day.