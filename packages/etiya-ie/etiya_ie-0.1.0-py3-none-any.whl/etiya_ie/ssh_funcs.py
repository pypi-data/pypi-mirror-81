import subprocess


class ssh_funcs:
    def __init__(self, user, host):
        self.user = user
        self.host = host

    def create_file_to_server(self, filename):
        subprocess.Popen("ssh {user}@{host} {cmd}".format(user=self.user, host=self.host, cmd='touch ' + filename),
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
