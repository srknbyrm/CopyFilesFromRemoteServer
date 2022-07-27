import datetime
import sys
import schedule
import time
import os
import pexpect as pexpect

servers_and_passwords = {"server_ip": "password"}


def copy_files():
    try:
        for server_ip, password in servers_and_passwords.items():
            ssh_password = (password + "\n").encode()
            date_time = str(datetime.datetime.now())
            date_time = date_time.replace(" ", "-")
            print(date_time)
            os.system(f"/usr/bin/mkdir /home/serkan/{server_ip}-{date_time}")
            scp_command = f'/usr/bin/scp root@{server_ip}:/var/log/nginx/access.log.2.gz ' \
                          f'/home/serkan/{server_ip}-{date_time}'
            child = pexpect.spawn(scp_command)
            # make output visible for debugging / progress watching
            child.logfile = sys.stdout.buffer

            i = child.expect([pexpect.TIMEOUT, "password:"])
            if i == 0:
                print("Got unexpected output: {} {}".format(child.before, child.after))
            else:
                child.sendline(ssh_password)
            child.read()
            time.sleep(1)
    except Exception as ex:
        print(ex)


schedule.every(1).hour.do(copy_files)

while True:
    schedule.run_pending()
    time.sleep(1)
