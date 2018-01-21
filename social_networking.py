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
    """ this seems pointless, but we might alter it later to add more info"""
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


def read_from_wall(user):
    """ Read from the wall of any given user
    """
    with open(get_wallname(user), 'r') as f:
        wall_contents = f.readlines()
    return wall_contents


class SocialNetworkUser(object):
    def __init__(self, username):
        self.name = username
        self.following = []

        with open(ALL_USERS_NAMES, 'r') as f:
            all_user_names = f.readlines()

        if username not in all_user_names:
            self.user_data = add_user(username)
        else:
            self.user_data = get_wallname(username)

    def post_to_wall(self, wall_text):
        with open(self.user_data, 'a+') as f:
            f.write('{}: {}\n'.format(datetime.datetime.utcnow(), wall_text))

    def add_follow(self, other_user_name):
        with open(ALL_USERS_NAMES, 'r') as f:
            all_user_names = f.readlines()
            if other_user_name not in all_user_names:
                return "Cannot follow non-existent user!"

        if other_user_name not in self.following:
            self.following.append(other_user_name)

        return read_from_wall(other_user_name)


class MyPrompt(cmd.Cmd):
    """ Prompt interacted with by the user to access  social network functions
    """
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '> '
        self.social_network_user = None

    def precmd(self, line):
        if '->' in line:
            to_wall = line.split('->')[-1].strip(' ')
            return 'wall_post ' + to_wall

        elif 'follows' in line:
            to_follow = line.split('follows')[-1]
            return 'follow' + to_follow

        elif 'wall' in line:
            return 'wall_read ' + line.split('wall')[0]

        else:
            return line

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

    def do_follow(self, user_to_follow):
        self.social_network_user.add_follow(user_to_follow)
        self.do_wall_read(user_to_follow)

    def do_wall_read(self, user):
        users_wall = read_from_wall(user)
        for line in users_wall:
            print(line)


if __name__ == "__main__":
    prompt = MyPrompt()
    prompt.cmdloop('Say hello, user!')
