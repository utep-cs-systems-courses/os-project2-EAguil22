#! /usr/bin/env python3

import os, sys, re

def ch_dir(path):
    try:
        os.chdir(path)
    except:
        os.write(2, "cd: no such file or directory: {}".format(path))
        
def redir1(pid, cmd):

    if pid < 0:
        os.write(2, ("fork failed, returning %d\n" % pid).encode())

    elif pid == 0:
        path = cmd[-1]
        os.close(1)

        try:
            os.open(path, os.O_CREAT | os.O_WRONLY)
            os.set_inheritable(1, True)
        except FileNotFoundError:
            os.write(2, ("%s: No such file or directory" % path).encode())

        cmd = cmd[:cmd.index(">")]

        for dir in re.split(":", os.environ['PATH']):
            prog = "%s/%s" % (dir, cmd[0])

            try:
                os.execve(prog, cmd, os.environ)
            except FileNotFoundError:
                pass

        os.write(2, ("Child: could not exec %s\n" % cmd[0]).encode())
        sys.exit(1)

    else:
        childPidCode = os.wait()


def redir2(pid, cmd):

    if pid < 0:
        os.write(2, ("fork failed, returning %d\n" % pid).encode())
        sys.exit(1)

    elif pid == 0:
        path = cmd[-1]
        os.close(0)
    
        try:
            os.open(path, os.O_CREAT | os.O_RDONLY)
            os.set_inheritable(0, True)
        except FileNotFoundError:
            os.write(2, ("%s: No such file or directory" % path).encode())
            
        cmd = cmd[:cmd.index("<")]

        for dir in re.split(":", os.environ['PATH']):
            prog = "%s/%s" % (dir, cmd[0])

            try:
                os.execve(prog, cmd, os.environ)
            except FileNotFoundError:
                pass

        os.write(2, ("Child: could not exec %s\n" % cmd[0]).encode())
        sys.exit(1)

    else:
        childPidCode = os.wait()

        
                

    
# def myPipe():
    

def progExec(pid, args):
    if pid < 0:
        os.write(2, ("fork failed, returning %d\n" % pid).encode())
        sys.exit()

    elif pid == 0:
        for dir in re.split(":", os.environ['PATH']):
            prog = "%s/%s" % (dir, args[0])

            try:
                os.execve(prog, args, os.environ)
            except FileNotFoundError:
                pass

        os.write(2, "Child: could not exec %s\n" % args[0].encode())
        sys.exit(1)

    else:
        childPidCode = os.wait()





while True:
    path = os.getcwd() +  "/myShell$ "
    os.write(1, path.encode())

    cmd = os.read(0, 1000).decode().split()


    if cmd[0] == "exit":
        os.write(1, "exting myShell...\n".encode())
        sys.exit()
        
    elif cmd[0] == "cd":
        ch_dir(cmd[1])

    
    #TESTING

    else:
        
        if "|" in cmd:
            pr, pw = os.pipe()

            for fd in (pr, pw):
                os.set_inheritable(fd, True)

            rc = os.fork()
            myPipe(rc, cmd, pr, pw)

        elif ">" in cmd:
            rc = os.fork()
            redir1(rc, cmd)

        elif "<" in cmd:
            rc = os.fork()
            redir2(rc, cmd)
            
        rc = os.fork()
        progExec(rc, cmd)
    
