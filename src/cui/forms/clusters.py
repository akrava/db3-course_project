import npyscreen
import curses
import subprocess


class ClusterForm(npyscreen.FormBaseNew):
    def create(self):
        y, x = self.useable_space()
        self.box = self.add(npyscreen.BoxTitle, name="Choose action", width=50, height=10,
                            relx=(x - 50) // 2, rely=(y - 10) // 2,
                            values=["Create cluster", "Start cluster", "Stop cluster"])
        self.box.when_value_edited = self.sample
        new_handlers = {
            curses.KEY_BACKSPACE: self.go_back,
        }
        self.add_handlers(new_handlers)

    def sample(self):
        index = self.box.value
        if index == 0:
            subprocess.call(['gnome-terminal', "--", 'bash', '-c', f'./scripts/start-cassandra.sh 1; '
                                                                   f'./scripts/start-cassandra.sh 2; '
                                                                   f'./scripts/start-cassandra.sh 3; '
                                                                   f'./scripts/start-cassandra.sh 4; bash'])
        elif index == 1:
            subprocess.call(['gnome-terminal', "--", 'bash', '-c', f'./scripts/run-cassandra.sh 1; '
                                                                   f'./scripts/run-cassandra.sh 2; '
                                                                   f'./scripts/run-cassandra.sh 3; '
                                                                   f'./scripts/run-cassandra.sh 4; bash'])
        elif index == 2:
            subprocess.call(['gnome-terminal', "--", 'bash', '-c', f'./scripts/stop-cassandra.sh 1; '
                                                                   f'./scripts/stop-cassandra.sh 2; '
                                                                   f'./scripts/stop-cassandra.sh 3; '
                                                                   f'./scripts/stop-cassandra.sh 4; bash'])

    def go_back(self, _e):
        self.parentApp.getForm('MAIN').box.value = None
        self.parentApp.switchForm("MAIN")
