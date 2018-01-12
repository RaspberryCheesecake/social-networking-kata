# -*- coding: utf-8 -*-
"""
Kata from https://github.com/sandromancuso/social_networking_kata
"""
import cmd
import datetime
import os

USER_DATA_STORE = os.path.join(os.getcwd(), 'user_data')
ALL_USERS_NAMES = os.path.join(USER_DATA_STORE, 'usernames.txt')


def get_wallname(user):
    """ this seems pointless, but we might alter it later"""
    return user + '.txt'


def add_user(user):
    """ Add user to list of user names in file storage, plus make their wall
    """
    with open(ALL_USERS_NAMES, 'r+') as f:
        f.write(user)

    wall = get_wallname(user)
    with open(os.path.join(USER_DATA_STORE, wall), 'w+') as f:
        f.write("{}: {} joined the network".format(datetime.datetime.utcnow(),
                                                   user))

    return wall


class SocialNetworkUser(object):
    def __init__(self, username):
        self.name = username

        with open(ALL_USERS_NAMES, 'r') as f:
            all_user_names = f.readlines()

        if username not in all_user_names:
            self.user_data = add_user(username)
        else:
            self.user_data = get_wallname(username)

    def post_to_wall(self, wall_text):
        with open(self.user_data, 'a+') as f:
            f.write('{}: {}\n'.format(datetime.datetime.utcnow(), wall_text))


class MyPrompt(cmd.Cmd):
    """ Prompt interacted with by the user to access  social network functions
    """
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '> '
        self.social_network_user = None

    def do_quit(self, args):
        """ Quit. """
        print("Goodbye!")
        raise SystemExit

    def do_login(self, user):
        """Login as a user to the social network. Creates account if needed
        """
        if self.social_network_user is None:
            self.social_network_user = SocialNetworkUser(username=user)
            self.prompt = '{}> '.format(user)
            print("Welcome, {}".format(user))
        else:
            print("Already logged in")

    def do_logout(self, args):
        """ If you are logged in, log out"""
        if self.social_network_user is not None:
            print("Goodbye {}".format(self.social_network_user.name))
            self.social_network_user = None
            self.prompt = '> '
        else:
            print("Already logged out")

    def do_wall_post(self, wall_text):
        """ Post to wall"""
        self.social_network_user.post_to_wall(wall_text)


if __name__ == "__main__":
    prompt = MyPrompt()
    prompt.cmdloop('Say hello, user!')
