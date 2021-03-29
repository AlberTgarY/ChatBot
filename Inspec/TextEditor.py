import sys
from PyQt5.QtWidgets import QWidget, QTextEdit, QApplication

# A useless TextEditor :D
class Readtxt(QWidget):
    def __init__(self,temp_list):
        super().__init__()
        self.temp_list = temp_list
        self.settings()
        self.write()
    def settings(self):

        self.info = QTextEdit(self)
        self.info.setGeometry(50, 80, 450, 500)

        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('Text')
        self.show()

    def write(self):
            for key in self.temp_list.keys():
                if str(self.temp_list[key]) == '7':
                    line = str(key)
                    self.info.append(line)
                else:
                    line = str(key)+": "+str(self.temp_list[key])
                    self.info.append(line+"\n")


def restruct(List):
    temp = {}
    for scope in List:
        temp.update(scope)

    return temp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    List = [{'conversations.replies': 1}, {'channels.archive': 7}, {'channels.leave': 7}, {'channels.mark': 7}, {'channels.rename': 7}, {'channels.set.Purpose': 7}, {'channels.set.Topic': 7}, {'channels.unarchive': 7}, {'groups.archive': 7}, {'groups.kick': 7}, {'groups.mark': 7}, {'groups.open': 7}, {'groups.rename': 7}, {'groups.set.Purpose': 7}, {'mpim.close': 6}, {'mpim.history': 7}, {'mpim.list': 7}, {'mpim.mark': 6}, {'pins.add': 7}, {'pins.list': 6}, {'pins.remove': 6}, {'reactions.get': 7}, {'search.files': 7}, {'stars.list': 7}, {'team.access.Logs': 7}, {'users.set.Active': 7}, {'users.set.Presence': 6}, {'chat.unfurl': 1}, {'conversations.info': 4}, {'conversations.join': 1}, {'views.open': 3}, {'dialog.open': 2}, {'conversations.list': 6}, {'chat.get.Permalink': 1}, {'conversations.history': 4}, {'files.remote.add': 1}, {'files.remote.share': 1}, {'api.test': 4}, {'users.conversations': 2}, {'conversations.members': 1}, {'views.push': 1}, {'calls.update': 1}, {'users.profile.get': 5}, {'oauth.v2.access': 2}, {'users.identity': 2}, {'conversations.open': 2}, {'groups.replies': 1}, {'channels.replies': 2}, {'dnd.end.Snooze': 4}, {'dnd.info': 4}, {'dnd.set.Snooze': 4}, {'dnd.team.Info': 4}, {'reminders.add': 4}, {'reminders.complete': 3}, {'reminders.delete': 3}, {'reminders.info': 3}, {'reminders.list': 3}, {'stars.add': 4}, {'stars.remove': 4}, {'views.publish': 2}, {'usergroups.users.list': 2}, {'users.profile.set': 1}, {'team.billable.Info': 1}, {'team.integration.Logs': 2}, {'team.profile.get': 1}, {'views.update': 2}, {'files.comments.delete': 1}, {'files.revoke.Public.URL': 1}, {'files.shared.Public.URL': 1}, {'usergroups.create': 1}, {'usergroups.disable': 1}, {'usergroups.enable': 1}, {'usergroups.list': 1}, {'usergroups.update': 1}, {'usergroups.users.update': 1}]
    List = restruct(List)
    List = dict(sorted(List.items(), key = lambda l: (l[1], l[0]),reverse=True))
    ex = Readtxt(List)
    sys.exit(app.exec_())
