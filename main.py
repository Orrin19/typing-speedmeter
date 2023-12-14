import tkinter as tk
import timeit
import random


class TypingSpeedmeter:
    TEXTS = [
        "Скорость — ключ к успеху!",
        "Быстро печатай, не ошибайся.",
        "Тренируй руки, ум и глаза.",
        "Клавиши — твои лучшие друзья.",
        "Печатай точно, не спеша.",
        "Скорость растет с практикой.",
        "Печатай без задержек!",
        "Клавиатура — твой инструмент.",
        "Уверенность — важнее скорости.",
        "Точность — залог успеха."
    ]

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Тест скорости печати")
        self.root.geometry("1000x550")
        root.resizable(width=False, height=False)

        self.create_label("Нажмите кнопку «Старт»")
        self.create_text()
        self.create_input()
        self.create_button()
        self.create_reset()
        
    def start_typing(self) -> None:
        self.update_label("Введите этот текст:")
        self.generate_text_to_type()
        self.update_text()
        self.create_input()
        self.change_input_state()
        self.change_button_to_pause()
        self.show_reset()
        self.start_time()

    def generate_text_to_type(self) -> None:
        self.text_to_type = random.choice(self.TEXTS)

    def pause_typing(self) -> None:
        self.pause_time()
        self.change_button_to_continue()

    def continue_typing(self) -> None:
        self.unpause_time()
        self.change_button_to_pause()

    def end_typing(self) -> None:
        self.end_time()
        self.update_label(
            f"Вы потратили {self._elapse:.2f} секунд на печать.\nСкорость " + \
            f"печати: {(len(self.text_to_type) / self._elapse):.2f} " + \
            "символов в секунду"
        )
        self.change_button_to_start()

    def reset_typing(self) -> None:
        self.update_label("Нажмите кнопку «Старт»")
        self.reset_text()
        self.create_input()
        self.change_button_to_start()
        self.hide_reset()

    def change_button_to_start(self) -> None:
        self.button.config(text="Старт", command=self.start_typing)

    def change_button_to_pause(self) -> None:
        self.button.config(text="Пауза", command=self.pause_typing)

    def change_button_to_continue(self) -> None:
        self.button.config(text="Продолжить", command=self.continue_typing)

    def start_time(self) -> None:
        self._start = timeit.default_timer()
        self._pause = 0
        self._pause_all = 0

    def pause_time(self) -> None:
        self.change_input_state()
        self._pause = timeit.default_timer()

    def unpause_time(self) -> None:
        self.change_input_state()
        self._pause_all += (timeit.default_timer() - self._pause)

    def end_time(self) -> None:
        self.change_input_state()
        self._elapse = timeit.default_timer() - (self._start + self._pause_all)
        self._start = 0
        self._pause = 0
        self._pause_all = 0

    def create_label(self, text: str) -> None:
        self.label = tk.Label(
            root,
            text = text,
            font = ("Arial", 24)
        )
        self.label.pack()

    def update_label(self, text: str) -> None:
        self.label.config(text = text)

    def create_text(self) -> None:
        self.text = tk.Label(
            root,
            text = ' ',
            font = ("Arial", 18)
        )
        self.text.pack(after=self.label)

    def update_text(self) -> None:
        self.text.config(text = self.text_to_type)
        self.text.pack_forget()
        self.text.pack(after=self.label)

    def reset_text(self) -> None:
        self.text.config(text = ' ')

    def create_input(self) -> None:
        try:
            self.input.destroy()
        except AttributeError:
            pass
        self.input = tk.Text(
            root,
            font = ("Arial", 18),
            state = tk.DISABLED,
            height = 10,
            width = 90
        )
        self.input.pack(after=self.text)

    def change_input_state(self) -> None:
        if self.input.cget("state") == "disabled":
            self.input.config(state = tk.NORMAL)
            self.input.focus_set()
            self.input.bind("<KeyRelease>", self.start_comparing)
        else:
            self.input.config(state = tk.DISABLED)
            self.input.unbind("<KeyRelease>")

    def create_button(self) -> None:
        self.button = tk.Button(
            root,
            text = "Старт",
            font = ("Arial", 18),
            command = self.start_typing,
            padx = 15,
            pady = 15
        )
        self.button.pack(pady = 10)

    def create_reset(self) -> None:
        self.reset = tk.Button(
            root,
            text = "Сбросить",
            font = ("Arial", 18),
            command = self.reset_typing,
            padx = 15,
            pady = 15
        )
        self.reset.pack(pady = 10)
        self.hide_reset()

    def hide_reset(self) -> None:
        self.reset.pack_forget()

    def show_reset(self) -> None:
        self.reset.pack(pady = 10)

    def start_comparing(self, _: tk.Event) -> None:
        self.update_text()
        current_text = self.input.get("1.0", tk.END)
        self.compare_texts(self.text_to_type, current_text)

    def compare_texts(self, first: str, second: str):
        for i in range(min(len(first), len(second))):
            if (
                first[i] == second[i] or
                first[i] in "-–—" and second[i] in "-–—" or
                first[i] in "\"«»„“" and second[i] in "\"«»„“" or
                first[i] in "её" and second[i] in "её"
            ):
                continue
            if (len(second) - 1 != i):
                self.update_label("Исправьте ошибку!")
            else:
                self.update_label("Введите этот текст:")
            return
        if len(first) == len(second) - 1:
            self.end_typing()
        

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedmeter(root)
    root.mainloop()
