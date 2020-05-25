import npyscreen
import curses
import subprocess


class DataGenerationForm(npyscreen.FormBaseNew):
    def create(self):
        y, x = self.useable_space()
        self.box = self.add(npyscreen.BoxTitle, name="Choose type", width=50, height=10,
                            relx=(x - 50) // 2, rely=(y - 10) // 2,
                            values=["Load static GTFS", "Load dynamic GTFS"])
        self.box.when_value_edited = self.sample
        new_handlers = {
            curses.KEY_BACKSPACE: self.go_back,
        }
        self.add_handlers(new_handlers)

    def sample(self):
        index = self.box.value
        if index == 0:
            subprocess.call(['gnome-terminal', "--", 'bash', '-c', f'pipenv run python src/main.py --static; bash'])
        elif index == 1:
            timeout = 3
            subprocess.call(['gnome-terminal', "--", 'bash', '-c', f'pipenv run python src/main.py --dynamic {str(timeout)}; bash'])

    def go_back(self, _e):
        self.parentApp.getForm('MAIN').box.value = None
        self.parentApp.switchForm("MAIN")
