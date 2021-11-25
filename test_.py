from modules import battery
import unittest




class TestClass(unittest.TestCase):
    def test_battery_level(self):
        battery_levels = []
        for i in range(0, 101):
            battery_levels.append(str(i) + "%")
            
        battery_s = battery.battery_status() #instanciate the class in battery module
        status = battery_s.get_status() #take the actual status of the battery
        self.assertIn(status, battery_levels)


if __name__ == "__main__":
    unittest.main()