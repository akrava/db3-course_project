import signal
import sys
import npyscreen
from cui.forms.main import MainForm
from cui.forms.data_generation import DataGenerationForm
from cui.forms.clusters import ClusterForm
from cui.forms.backup_restore import BackupRestoreForm


class App(npyscreen.StandardApp):
    STARTING_FORM = "MAIN"

    def __init__(self):
        super().__init__()
        signal.signal(signal.SIGINT, self.__handle_interrupt_event)
        self.__program_name = " | course project"
        self.current_username = None

    def onStart(self):
        self.addForm("MAIN", MainForm, name="Main menu" + self.__program_name)
        self.addForm("GEN", DataGenerationForm, name="Data generation" + self.__program_name)
        self.addForm("CLST", ClusterForm, name="Cluster cassandra setup" + self.__program_name)
        self.addForm("BPR", BackupRestoreForm, name="Backup & restore" + self.__program_name)

    def __handle_interrupt_event(self, _sig, _frame):
        self.onCleanExit()
        sys.exit(0)
