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

