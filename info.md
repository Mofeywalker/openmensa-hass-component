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

The sensor contains the data in its attributes. As each mensa has their own labeling for the meals they offer,
this sensor aggregates the meals per category. E.g. if your mensa has "Komplett Menü", "Vegetarisches Menü" and
"Wahlessen", the attributes are build the following way:

```json
{
	'komplett_menu': [{
		'name': 'Frikadelle (Rind)'
	}],
	'vegetarisches_menu': [{
		'name': 'Bunter Salatteller'
	}],
	'wahlessen': [{
		'name': 'Tortellini vegetarisch'
	}, {
		'name': 'Tagesessen: Nudelgratin'
	}, {
		'name': 'Big Bacon Burger'
	}]
}
```

Use the Template engine to look at your mensa's meal categories with:
```
{{states.sensor.openmensa_sensor.attributes}}
```

To get e.g. the "Komplett Menü", use the following template:
```
{{states.sensor.openmensa_sensor.attributes.komplett_menu[0].name}}
```
