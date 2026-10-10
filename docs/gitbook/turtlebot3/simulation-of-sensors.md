# Simulation of sensors

Make a script `simulation_sensors.py` and add the code below. This code will simulate the following parameters. These parameters will be published on ROS 2 topics under `/sim/...`:

* battery state
* battery percentage
* temperature
* humidty
* gas sensor

{% hint style="danger" %}
The topics start with `/sim/`. The real robot already publishes `/battery_state`:
a second publisher on the same topic would mix fake and real values (battery
icon, labo-check and *Measure while driving* would show nonsense).
{% endhint %}

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import random
import time

from sensor_msgs.msg import BatteryState, Temperature, RelativeHumidity, JointState
from std_msgs.msg import Float32


class RandomSensorNode(Node):
    def __init__(self):
        super().__init__("random_sensor_node")
        self.get_logger().info('Random sensors node started!')

        # Publishers
        self.pub_battery = self.create_publisher(BatteryState, "/sim/battery_state", 10)
        self.pub_temp = self.create_publisher(Temperature, "/sim/temperature", 10)
        self.pub_humidity = self.create_publisher(RelativeHumidity, "/sim/humidity", 10)
        self.pub_gas = self.create_publisher(Float32, "/sim/gas_value", 10)

        # Timer (10 Hz)
        self.timer = self.create_timer(0.1, self.publish_random_values)

    def publish_random_values(self):
        now = self.get_clock().now().to_msg()

        # --- Battery (sensor_msgs/BatteryState) ---
        batt = BatteryState()
        batt.header.stamp = now
        batt.voltage = random.uniform(10.5, 12.6)
        batt.percentage = random.uniform(0.0, 1.0)  # 0–1 (niet 0–100)
        self.pub_battery.publish(batt)

        # --- Temperature ---
        temp = Temperature()
        temp.header.stamp = now
        temp.temperature = random.uniform(18.0, 35.0)
        temp.variance = 0.1
        self.pub_temp.publish(temp)

        # --- Humidity (sensor_msgs/RelativeHumidity) ---
        hum = RelativeHumidity()
        hum.header.stamp = now
        hum.relative_humidity = random.uniform(0.20, 0.80)  # 0–1
        hum.variance = 0.02
        self.pub_humidity.publish(hum)

        # --- Gaswaarde ---
        gas = Float32()
        gas.data = random.uniform(0.0, 1024.0)
        self.pub_gas.publish(gas)

        self.get_logger().info(f'Bat Volt: {batt.voltage:.2f} | Bat perctage: {batt.percentage:.2f}  | Temp: {temp.temperature:.2f}  |  Hum: {hum.relative_humidity:.2f}  |  Gas: { gas.data:.2f} ')

def main(args=None):
    rclpy.init(args=args)
    node = RandomSensorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

```

Start the Python script with the following command:

```shellscript
python3 simulation_sensors.py
```

Use the ros2 command to echo the published topics, e.g. `ros2 topic echo /sim/battery_state`.
