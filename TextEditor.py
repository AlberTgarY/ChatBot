import sys
from PyQt5.QtWidgets import QWidget, QTextEdit, QApplication


class Readtxt(QWidget):
    def __init__(self):
        super().__init__()
        self.temp_list = [{'im.close': 3}, {'groups.set.Topic': 2}, {'channels.set.Topic': 4}, {'users.profile.get': 4}, {'files.delete': 4}, {'conversations.set.Topic': 2}, {'channels.create': 4}, {'im.replies': 2}, {'users.conversations': 3}, {'pins.add': 4}, {'stars.add': 2}, {'pins.remove': 3}, {'stars.remove': 2}, {'search.messages': 4}, {'search.all': 3}, {'users.profile.set': 2}, {'users.set.Photo': 2}, {'usergroups.list': 2}, {'conversations.invite': 3}, {'users.lookup.By.Email': 4}, {'channels.kick': 3}, {'reactions.list': 2}, {'conversations.replies': 4}, {'oauth.v2.access': 2}, {'views.publish': 3}, {'views.update': 4}, {'views.push': 2}, {'conversations.members': 3}, {'admin.apps.approve': 1}, {'admin.apps.requests.list': 1}, {'admin.apps.restrict': 1}, {'admin.conversations.set.Teams': 1}, {'admin.emoji.add': 1}, {'admin.emoji.list': 1}, {'admin.emoji.remove': 1}, {'admin.emoji.rename': 1}, {'admin.users.session.reset': 1}, {'admin.invite.Requests.approve': 1}, {'admin.invite.Requests.list': 1}, {'admin.invite.Requests.deny': 1}, {'admin.teams.admins.list': 1}, {'admin.teams.create': 1}, {'admin.teams.list': 1}, {'admin.teams.settings.info': 1}, {'admin.teams.settings.set.Default.Channels': 1}, {'admin.teams.settings.set.Description': 1}, {'admin.teams.settings.set.Discoverability': 1}, {'admin.teams.settings.set.Icon': 1}, {'admin.teams.settings.set.Name': 1}, {'admin.usergroups.add.Channels': 1}, {'admin.usergroups.list.Channels': 1}, {'admin.usergroups.remove.Channels': 1}, {'admin.users.assign': 1}, {'admin.users.invite': 1}, {'admin.users.list': 1}, {'admin.users.remove': 1}, {'admin.users.set.Expiration': 1}, {'admin.users.set.Owner': 1}, {'admin.users.set.Regular': 1}, {'auth.revoke': 1}, {'bots.info': 1}, {'calls.add': 1}, {'calls.end': 1}, {'calls.info': 1}, {'calls.participants.add': 1}, {'calls.update': 1}, {'channels.archive': 1}, {'channels.leave': 2}, {'channels.mark': 1}, {'channels.rename': 1}, {'channels.replies': 2}, {'channels.set.Purpose': 4}, {'channels.unarchive': 1}, {'chat.schedule.Message': 3}, {'chat.get.Permalink': 2}, {'chat.unfurl': 1}, {'conversations.archive': 1}, {'conversations.close': 1}, {'conversations.create': 2}, {'conversations.join': 1}, {'conversations.kick': 1}, {'conversations.leave': 1}, {'conversations.rename': 1}, {'conversations.set.Purpose': 1}, {'conversations.unarchive': 1}, {'dnd.end.Snooze': 1}, {'dnd.info': 1}, {'dnd.set.Snooze': 1}, {'dnd.team.Info': 1}, {'files.comments.delete': 1}, {'files.remote.info': 1}, {'files.remote.list': 1}, {'files.remote.add': 2}, {'files.remote.update': 1}, {'files.remote.remove': 1}, {'files.remote.share': 1}, {'files.revoke.Public.URL': 1}, {'files.shared.Public.URL': 1}, {'groups.archive': 1}, {'groups.create': 4}, {'groups.history': 3}, {'groups.kick': 1}, {'groups.leave': 1}, {'groups.mark': 1}, {'groups.open': 1}, {'groups.rename': 1}, {'groups.replies': 1}, {'groups.set.Purpose': 1}, {'groups.unarchive': 1}, {'im.mark': 1}, {'migration.exchange': 1}, {'mpim.close': 1}, {'mpim.history': 1}, {'mpim.list': 1}, {'mpim.mark': 1}, {'mpim.open': 3}, {'mpim.replies': 1}, {'pins.list': 3}, {'reminders.add': 3}, {'reminders.complete': 1}, {'reminders.delete': 1}, {'reminders.info': 1}, {'reminders.list': 1}, {'search.files': 1}, {'stars.list': 1}, {'team.access.Logs': 1}, {'team.billable.Info': 1}, {'team.integration.Logs': 1}, {'team.profile.get': 1}, {'usergroups.create': 1}, {'usergroups.disable': 1}, {'usergroups.enable': 1}, {'usergroups.update': 1}, {'usergroups.users.list': 1}, {'usergroups.users.update': 1}, {'users.delete.Photo': 1}, {'users.identity': 1}, {'users.set.Presence': 1}]
        self.settings()
        self.write()
    def settings(self):

        self.info = QTextEdit(self)
        self.info.setGeometry(50, 80, 450, 500)

        self.setGeometry(300, 300, 600, 600)
        self.setWindowTitle('Text')
        self.show()

    def write(self):
        for dict in self.temp_list:
            for key in dict.keys():
                line = str(key)+": "+str(dict[key])
                self.info.append(line+"\n")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Readtxt()
    sys.exit(app.exec_())
