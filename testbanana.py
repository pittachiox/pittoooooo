from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from random import randint
from kivy.config import Config

# บังคับให้ใช้ System Keyboard
Config.set('kivy', 'keyboard_mode', 'system')

Window.size = (800, 600)  # ตั้งค่าขนาดหน้าต่าง

class banana(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            # ใช้ภาพกล้วยแทนลูกบอล
            self.banana = Rectangle(source='images/banana-removebg-preview.png', size=(80, 80), pos=(randint(0, Window.width - 80), Window.height - 80))
        self.velocity_y = -400  # ความเร็วของลูกบอลในแนวตั้ง

    def move(self, dt):
        # การเคลื่อนไหวลูกบอล
        bx, by = self.banana.pos
        by += self.velocity_y * dt
        self.banana.pos = (bx, by)

    def reset(self):
        # ตั้งค่าลูกบอลใหม่
        self.banana.pos = (randint(0, Window.width - 50), Window.height - 50)

class Watermelon(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            # ใช้ภาพแตงโมแทนลูกบอล
            self.watermelon = Rectangle(source='images/watermelon-removebg-preview.png', size=(100, 100), pos=(randint(0, Window.width - 100), Window.height - 100))
        self.velocity_y = -600  # ความเร็วของแตงโมในแนวตั้ง

    def move(self, dt):
        # การเคลื่อนไหวแตงโม
        wx, wy = self.watermelon.pos
        wy += self.velocity_y * dt
        self.watermelon.pos = (wx, wy)

    def reset(self):
        # ตั้งค่าแตงโมใหม่
        self.watermelon.pos = (randint(0, Window.width - 100), Window.height - 100)

class stick(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            # ใช้ภาพกิ่งไม้แทน paddle
            self.paddle = Rectangle(source='images/stick-removebg-preview.png', size=(200, 150), pos=(Window.width / 2 - 100, 50))
        self.velocity_x = 1200

    def move(self, dt, pressed_keys):
        # การเคลื่อนไหว paddle
        cur_x, cur_y = self.paddle.pos
        step = 300 * dt  # ความเร็วของ paddle
        if 'a' in pressed_keys and cur_x > 0:
            cur_x -= step
        if 'd' in pressed_keys and cur_x < Window.width - self.paddle.size[0]:
            cur_x += step
        self.paddle.pos = (cur_x, cur_y)



class bananaCatchGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0

        # สร้าง stick, banana และ Watermelon
        self.paddle = stick()
        self.banana = banana()
        self.watermelon = Watermelon()  # เปลี่ยนชื่อเป็นตัวพิมพ์ใหญ่
        self.add_widget(self.paddle)
        self.add_widget(self.banana)
        self.add_widget(self.watermelon)

        # รับคีย์บอร์ด
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self.pressed_keys = set()

        # ตั้งเวลาให้เกมทำงาน
        Clock.schedule_interval(self.update_game, 1 / 60)

    def _on_keyboard_closed(self):
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_key_down)
            self._keyboard.unbind(on_key_up=self._on_key_up)
            self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.pressed_keys.add(text)

    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        self.pressed_keys.discard(text)

    def update_game(self, dt):
        # อัปเดตการเคลื่อนไหวของ paddle, banana และ watermelon
        self.paddle.move(dt, self.pressed_keys)
        self.banana.move(dt)
        self.watermelon.move(dt)

        # ตรวจจับการชน
        if self.check_collision(self.banana.banana):
            self.score += 1
            print(f"Score: {self.score}")
            self.banana.reset()

        if self.check_collision(self.watermelon.watermelon):
            self.score += 15
            print(f"Score: {self.score}")
            self.watermelon.reset()

        # ตรวจสอบว่าผลไม้ตกถึงพื้น
        if self.banana.banana.pos[1] < 0:
            print("Game Over!")
            self.banana.reset()

        if self.watermelon.watermelon.pos[1] < 0:
            print("Game Over!")
            self.watermelon.reset()

    def check_collision(self, fruit):
        # ตรวจสอบการชนระหว่าง paddle และผลไม้
        px, py = self.paddle.paddle.pos
        fx, fy = fruit.pos
        fw, fh = fruit.size
        pw, ph = self.paddle.paddle.size

        if (fx + fw > px) and (fx < px + pw) and (fy < py + ph):
            return True
        return False

class BananaCatchApp(App):
    def build(self):
        return bananaCatchGame()


if __name__ == '__main__':
    BananaCatchApp().run()


