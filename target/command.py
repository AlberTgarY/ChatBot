class Command(object):

    def __init__(self):
        self.commands = {
            "jump": self.jump,
            "help": self.help,
            "hello": self.hello
        }

    def handle_command(self, user, command):
        response = "<@" + user + ">: "

        if command in self.commands:
            response += self.commands[command]()
        else:
            response += "Sorry I don't understand the command: " + command + ". " + self.help()

        return response


    def hello(self):
        return "Hello! Hello! Hello!"

    def jump(self):
        return "Yes I jumped."

    def help(self):
        response = "Currently I support the following commands:\r\n"
        count = 0
        for command in self.commands:
            count = count + 1
            response += str(count) + ":" + command + "\r\n"

        return response