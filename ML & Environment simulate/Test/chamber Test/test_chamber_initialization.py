import unittest
import numpy as np
from chamber import Chamber  # 假设 Chamber 类在 chamber.py 文件中

class TestChamber(unittest.TestCase):
    def setUp(self):
        # 初始化传感器数据
        self.temp = [20, 21, 19]  # 温度传感器数据
        self.moisture = [50, 52, 49]  # 湿度传感器数据
        self.oxygen = [18, 17, 19]  # 氧气传感器数据
        self.co2 = [0.04, 0.05, 0.03]  # 二氧化碳传感器数据
        self.methane = [0.01, 0.02, 0.15]  # 甲烷传感器数据
        
        # 创建 Chamber 实例
        self.chamber = Chamber(
            temperature=self.temp,
            moisture=self.moisture,
            oxygen=self.oxygen,
            co2=self.co2,
            methane=self.methane
        )

    def test_initialization(self):
        # 测试传感器数据是否正确初始化
        np.testing.assert_array_equal(self.chamber.temperature, np.array(self.temp))
        np.testing.assert_array_equal(self.chamber.moisture, np.array(self.moisture))
        np.testing.assert_array_equal(self.chamber.oxygen, np.array(self.oxygen))
        np.testing.assert_array_equal(self.chamber.co2, np.array(self.co2))
        np.testing.assert_array_equal(self.chamber.methane, np.array(self.methane))
        
        # 测试设备状态是否正确初始化
        self.assertFalse(self.chamber.paddle_status)  # Paddle 默认为关闭
        self.assertEqual(self.chamber.paddle_direction, 1)  # Paddle 方向默认为顺时针
        self.assertFalse(self.chamber.lid_status)  # Lid 默认为关闭
        self.assertFalse(self.chamber.air_pump_status)  # Air pump 默认为关闭
        self.assertTrue(self.chamber.isEmpty)  # Chamber 默认为空

if __name__ == '__main__':
    unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestChamber))
