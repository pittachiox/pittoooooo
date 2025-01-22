from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from random import randint
from kivy.config import Config
from kivy.uix.button import Button
from kivy.properties import ObjectProperty

# บังคับให้ใช้ System Keyboard
Config.set('kivy', 'keyboard_mode', 'system')

Window.size = (800, 600)  # ตั้งค่าขนาดหน้าต่าง


class StartScreen(Screen):
    """หน้าจอเริ่มต้น"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = Widget()  # ใช้ Widget เป็นพื้นฐาน
        self.add_widget(self.layout)

        # เพิ่ม Label ชื่อเกม
        self.label = Label(
            text="Banana Catch Game",
            font_size=50,
            size_hint=(None, None),
            pos=(Window.width / 2 - 200, Window.height / 2 + 100),
            color=(1, 1, 1, 1)
        )
        self.layout.add_widget(self.label)

        # เพิ่มปุ่ม Start Game
        self.start_button = Button(
            text="Start Game",
            size_hint=(None, None),
            size=(200, 50),
            pos=(Window.width / 2 - 100, Window.height / 2 - 50),
            font_size=20
        )
        self.start_button.bind(on_press=self.start_game)
        self.layout.add_widget(self.start_button)

    def start_game(self, instance):
        """เปลี่ยนไปหน้าจอเกมเมื่อกดปุ่ม"""
        self.manager.current = "game_screen"

class GameScreen(Screen):
    """หน้าจอเกมหลัก"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = bananaCatchGame()
        self.add_widget(self.game)

class StartButton(Widget):
    on_start = ObjectProperty(None)  # กำหนด Property สำหรับ Callback

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # สร้าง Label สำหรับปุ่มเริ่มเกม
        self.label = Label(
            text="START GAME",
            font_size=50,
            size_hint=(None, None),
            pos=(Window.width / 2 - 150, Window.height / 2),
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.label)

    def on_touch_down(self, touch):
        """Callback เมื่อกดปุ่ม"""
        if self.label.collide_point(*touch.pos):  # ตรวจสอบว่ากดปุ่มหรือไม่
            if self.on_start:  # ถ้ามี Callback ที่ผูกไว้
                self.on_start()  # เรียกฟังก์ชัน Callback
            return True  # ส่งสัญญาณว่ากดปุ่มสำเร็จ
        return super().on_touch_down(touch)


class banana(Widget):
    def __init__(self, size=(80, 80), **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.banana = Rectangle(source='images/banana-removebg-preview.png', size=size, pos=(randint(0, Window.width - size[0]), Window.height - size[1]))
        self.size = size  # เก็บขนาดไว้ในวัตถุ
        

    def move(self, dt):
        bx, by = self.banana.pos
        by += self.velocity_y * dt
        self.banana.pos = (bx, by)

    def reset(self):
        self.banana.pos = (randint(0, Window.width - self.size[0]), Window.height - self.size[1])


class Watermelon(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.watermelon = Rectangle(source='images/watermelon-removebg-preview.png', size=(120, 120), pos=(randint(0, Window.width - 100), Window.height - 100))
        self.velocity_y = -600

    def move(self, dt):
        wx, wy = self.watermelon.pos
        wy += self.velocity_y * dt
        self.watermelon.pos = (wx, wy)

    def reset(self):
        self.watermelon.pos = (randint(0, Window.width - 100), Window.height - 100)


class Goldencoin(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.goldencoin = Rectangle(source='images/goldencoin-removebg-preview.png', size=(60, 60), pos=(randint(0, Window.width - 100), Window.height - 100))
        self.velocity_y = -800

    def move(self, dt):
        wx, wy = self.goldencoin.pos
        wy += self.velocity_y * dt
        self.goldencoin.pos = (wx, wy)

    def reset(self):
        self.goldencoin.pos = (randint(0, Window.width - 100), Window.height - 100)


class Greycoin(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.greycoin = Rectangle(source='images/greycoin-removebg-preview.png', size=(90, 90), pos=(randint(0, Window.width - 100), Window.height - 100))
        self.velocity_y = -700

    def move(self, dt):
        wx, wy = self.greycoin.pos
        wy += self.velocity_y * dt
        self.greycoin.pos = (wx, wy)

    def reset(self):
        self.greycoin.pos = (randint(0, Window.width - 100), Window.height - 100)

class Boom(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.boom = Rectangle(source='images/boom-removebg-preview.png', size=(150, 150), pos=(randint(0, Window.width - 100), Window.height - 100))
        self.velocity_y = -800

    def move(self, dt):
        wx, wy = self.boom.pos
        wy += self.velocity_y * dt
        self.boom.pos = (wx, wy)

    def reset(self):
        self.boom.pos = (randint(0, Window.width - 100), Window.height - 100)

class stick(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.paddle = Rectangle(source='images/stick-removebg-preview.png', size=(150, 150), pos=(Window.width / 2 - 100, 50))
        self.velocity_x = 1200

    def move(self, dt, pressed_keys):
        cur_x, cur_y = self.paddle.pos
        step = self.velocity_x * dt
        if 'a' in pressed_keys and cur_x > 0:
            cur_x -= step
        if 'd' in pressed_keys and cur_x < Window.width - self.paddle.size[0]:
            cur_x += step
        self.paddle.pos = (cur_x, cur_y)

    def increase_speed(self, increment):
        self.velocity_x += increment


class BoomManager(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.booms = []  # เก็บรายการระเบิด
        self.active = False  # สถานะเริ่มต้น

    def add_boom(self, position=None):
        """สร้างระเบิดใหม่และเพิ่มในรายการ"""
        boom = Boom()
        if position:
            boom.boom.pos = position
        self.booms.append(boom)
        self.add_widget(boom)

    def activate(self):
        """เปิดใช้งานระเบิดทั้งหมด"""
        self.active = True

    def deactivate(self):
        """ปิดการใช้งานระเบิดทั้งหมด"""
        self.active = False

    def move(self, dt):
        """ขยับระเบิดทั้งหมด"""
        if not self.active:
            return
        for boom in self.booms:
            boom.move(dt)
            if boom.boom.pos[1] < 0:  # รีเซ็ตถ้าหลุดจากหน้าจอ
                boom.reset()


class GameOverWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # สร้าง Label สำหรับข้อความ "Game Over"
        self.label = Label(
            text="GAME OVER",
            font_size=200,
            pos=(Window.width / 2 - 100, Window.height / 2),
            size_hint=(None, None),
            color=(1, 0, 0, 1)
        )
        self.add_widget(self.label)
        self.opacity = 0  # ซ่อน Widget ไว้ในตอนเริ่ม

    def show(self):
        self.opacity = 1  # แสดงข้อความ


class GameState(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_game_over = False  # สถานะเริ่มต้นของเกม

    def set_game_over(self):
        self.is_game_over = True

    def reset_game(self):
        self.is_game_over = False


class GameOverScreen(Screen):
    def __init__(self, final_score, **kwargs):
        super().__init__(**kwargs)
        self.final_score = final_score
        self.layout = Widget()
        self.add_widget(self.layout)

        # เพิ่มภาพพื้นหลัง
        with self.canvas.before:
            self.background = Rectangle(source="images/gameover.png", size=Window.size, pos=(0, 0))

        # แสดงคะแนนสุดท้าย
        self.score_label = Label(
            text=f"Final Score: {self.final_score}",
            font_size=50,
            pos=(Window.width / 2 - 30, Window.height / 4 - 50),
            size_hint=(None, None),
            color=(1, 1, 1, 1)
        )
        self.layout.add_widget(self.score_label)

        # ปุ่มเริ่มเกมใหม่
        self.retry_button = Button(
            size=(400, 150),
            pos=(Window.width / 2 - 170, Window.height / 4 - 200),
            background_normal="images/retrybutton-removebg-preview.png",  # ปุ่มขณะไม่ได้กด
        )
        self.retry_button.bind(on_press=self.restart_game)
        self.layout.add_widget(self.retry_button)

    def restart_game(self, instance):
        """เริ่มเกมใหม่"""
        self.manager.current = "game_screen"  # เปลี่ยนกลับไปที่หน้าจอเกม
        # รีเซ็ตคะแนนในหน้าจอเกม
        game_screen = self.manager.get_screen("game_screen")
        game_screen.game.score = 0
        game_screen.game.update_score()
        game_screen.game.game_state.reset_game()


class bananaCatchGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.game_started = True

        # เพิ่มปุ่มเริ่มเกม
        self.start_button = StartButton()
        self.add_widget(self.start_button)

        # ผูก Callback ให้ปุ่ม
        self.start_button.on_start = self.start_game  # กำหนดฟังก์ชัน Callback
    
        # สร้าง GameState Widget
        self.game_state = GameState()
        self.add_widget(self.game_state)

        self.boom_manager = BoomManager()
        self.add_widget(self.boom_manager)

        # สร้าง stick, banana, และ watermelon
        self.paddle = stick()
        self.banana1 = banana()
        self.banana2 = banana()
        self.watermelon = Watermelon()
        self.boom = Boom()
        self.goldencoin = Goldencoin()
        self.greycoin = Greycoin()


        self.banana1 = banana(size=(80, 80))  # กล้วยเล็ก
        self.banana2 = banana(size=(120, 120))  # กล้วยใหญ่

        
        self.banana1.velocity_y = -500
        self.banana2.velocity_y = -700

        self.add_widget(self.paddle)
        self.add_widget(self.banana1)
        self.add_widget(self.banana2)
        self.add_widget(self.watermelon)
        self.add_widget(self.boom)
        self.add_widget(self.goldencoin)
        self.add_widget(self.greycoin)

        # เพิ่ม Label สำหรับแสดงคะแนน
        self.score_label = Label(text=f"Score: {self.score}", font_size=50, pos=(70, Window.height - 80), size_hint=(None, None))
        self.add_widget(self.score_label)

        # เพิ่ม Widget "Game Over"
        self.game_over_widget = GameOverWidget()
        self.add_widget(self.game_over_widget)

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

    def start_game(self):
        """ฟังก์ชัน Callback เมื่อเริ่มเกม"""
        self.remove_widget(self.start_button)  # ลบปุ่มออก
        self.game_started = True  # ตั้งสถานะว่าเกมเริ่มแล้ว
        print("Game Started!")  # Debug Message

    def update_game(self, dt):
        # หยุดเกมถ้า is_game_over เป็น True
        if self.game_state.is_game_over:
            return

        self.paddle.move(dt, self.pressed_keys)
        self.banana1.move(dt)
        self.banana2.move(dt)
        self.watermelon.move(dt)
        self.boom.move(dt)
        self.goldencoin.move(dt)
        self.greycoin.move(dt)
        self.boom_manager.move(dt)


        # ตรวจจับการชน
        if self.check_collision(self.banana1.banana):
            self.score += 5
            self.update_score()
            self.banana1.reset()

        if self.check_collision(self.banana2.banana):
            self.score += 10
            self.update_score()
            self.banana2.reset()

        if self.check_collision(self.watermelon.watermelon):
            self.score += 15
            self.update_score()
            self.watermelon.reset()

        if self.check_collision(self.goldencoin.goldencoin):
            self.score += 25
            self.update_score()
            self.goldencoin.reset()

        if self.check_collision(self.greycoin.greycoin):
            self.score += 20
            self.update_score()
            self.greycoin.reset()

        if self.check_collision(self.boom.boom):
            self.end_game()

        if self.score >= 400 and not self.boom_manager.active:
            self.boom_manager.activate()
            self.boom_manager.add_boom()  # สร้างระเบิดลูกใหม่
            self.boom_manager.add_boom()  # เพิ่มอีกลูก (ตามต้องการ)

        for boom in self.boom_manager.booms:
            if self.check_collision(boom.boom):
                self.end_game()


        # ตรวจสอบว่าผลไม้ตกถึงพื้น
        if self.banana1.banana.pos[1] < 0:
            self.banana1.reset()

        if self.banana2.banana.pos[1] < 0:
            self.banana2.reset()

        if self.watermelon.watermelon.pos[1] < 0:
            self.watermelon.reset()

        if self.boom.boom.pos[1] < 0:
            self.boom.reset()

        if self.goldencoin.goldencoin.pos[1] < 0:
            self.goldencoin.reset()

        if self.greycoin.greycoin.pos[1] < 0:
            self.greycoin.reset()

    def check_collision(self, fruit):
        px, py = self.paddle.paddle.pos
        fx, fy = fruit.pos
        fw, fh = fruit.size
        pw, ph = self.paddle.paddle.size

        if (fx + fw > px) and (fx < px + pw) and (fy < py + ph):
            return True
        return False

        if not self.game_started:
            return  # หยุดการทำงานถ้ายังไม่ได้เริ่มเกม

        # ใส่โค้ดอัปเดตเกม เช่น การเคลื่อนไหวของวัตถุหรือการตรวจจับการชน
        pass

    def update_score(self):
        self.score_label.text = f"Score: {self.score}"

    def end_game(self):
        # เรียกให้ GameState หยุดเกม
        self.game_state.set_game_over()

        # เปลี่ยนหน้าจอไปยัง GameOverScreen พร้อมส่งคะแนน
        game_over_screen = self.parent.manager.get_screen("game_over_screen")
        game_over_screen.final_score = self.score
        game_over_screen.score_label.text = f"Final Score: {self.score}"
        self.parent.manager.current = "game_over_screen"



class BananaCatchApp(App):
    def build(self):
        # สร้าง ScreenManager
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start_screen"))  # เพิ่มหน้าจอเริ่มต้น
        sm.add_widget(GameScreen(name="game_screen"))    # เพิ่มหน้าจอเกม
        sm.add_widget(GameOverScreen(name="game_over_screen", final_score=0))  # เพิ่มหน้าจอเกมจบ
        return sm



if __name__ == '__main__':
    
    BananaCatchApp().run()