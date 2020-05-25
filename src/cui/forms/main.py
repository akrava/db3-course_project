import npyscreen
import subprocess


class MainForm(npyscreen.FormBaseNew):
    def create(self):
        y, x = self.useable_space()
        self.box = self.add(npyscreen.BoxTitle, name="Choose action", width=50, height=10,
                            relx=(x - 50) // 2, rely=(y - 10) // 2,
                            values=["Data generation", "Custer setup", "Backup and restore", "Analyze data", "Results"])
        self.box.when_value_edited = self.handle_enter

    def handle_enter(self):
        index = self.box.value
        if index == 0:
            self.parentApp.switchForm("GEN")
        elif index == 1:
            self.parentApp.switchForm("CLST")
        elif index == 2:
            self.parentApp.switchForm("BPR")
        elif index == 3:
            subprocess.call(['gnome-terminal', "--", 'bash', '-c', f'pipenv run python src/main.py --analyze; bash'])
        elif index == 4:
            subprocess.call(['gnome-terminal', "--", 'bash', '-c', f'pipenv run jupyter notebook; bash'])
