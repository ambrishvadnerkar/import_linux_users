#!/usr/bin/python
from shutil import copyfile

def compare_lists(lst1, lst2):
    com_lst = []
    if len(lst1) > 0 and len(lst2) > 0:
        for ls in lst1:
            if ls in lst2:
                com_lst.append(ls)
    return com_lst

def get_data(filetype, filepath, data_type):
    data = []
#    if (filetype!='password' or filetype!='groups') or filepath=='' or data_type=='':
#        return data
    fpass = open(filepath,'r')

    if filetype == 'password':
        sel = {
            "user": 0,
            "uid": 2,
            "gid": 3,
            "homedir": 5
        }
    else:
        sel = {
            "groupname": 0,
            "gid": 2,
            "users": 3,
        }

    if data_type in sel.keys():
        for ln in fpass:
         lst = ln.rsplit(":")
         data.append(lst[sel.get(data_type)])

    fpass.close()
    return data

def fetch_group_data(data_type):
    fpass = open('/etc/group','r')
    data = {
        "groupname": [],
        "gid": [],
    }
    sel = {
        "groupname": 0,
        "gid": 2,
        "users": 3,
    }
    groupid = fetch_pass_data("gid")

    for ln in fpass:
        lst = ln.rsplit(":")
        data["groupname"].append(lst[sel.get("groupname")])
        data["gid"].append(lst[sel.get("gid")])

    fpass.close()
    return data

def fetch_pass_data(data_type):
    fpass = open('/etc/passwd','r')
    data = {
        "user": [],
        "uid": [],
        "gid": [],
        "homedir": []
    }
    sel = {
        "user": 0,
        "uid": 2,
        "gid": 3,
        "homedir": 5
    }

    if data_type in sel.keys():
        shll = tuple(("/bin/bash","/bin/false"))
        for ln in fpass:
         lst = ln.rsplit(":")
         data["user"].append(lst[sel.get("user")])
         data["uid"].append(lst[sel.get("uid")])
         data["gid"].append(lst[sel.get("gid")])
         data["homedir"].append(lst[sel.get("homedir")])

    fpass.close()
    return data
def verify_users():
    usrlist =  get_data("password", "/root/tmp/pass.out.txt", "user")
    uidlist = get_data("password", "/root/tmp/pass.out.txt", "uid")
    users = fetch_pass_data("user")
    unmlist = users["user"]
    uilist = users["uid"]

    cname = compare_lists(usrlist, unmlist)
    cuid = compare_lists(uidlist, uilist)

    if len(cname) > 0:
        print(cname)
        return False
    if len(cuid) > 0:
        print(cuid)
        return False
    return True

def verify_groups():
    gnm = get_data("groups", "/root/tmp/group.out.txt", "groupname")
    grpid = get_data("groups", "/root/tmp/group.out.txt", "gid")
    grpname = fetch_group_data("groupname")

    #gname = list(set(gnm).intersection(set(grpname["groupname"])))
    #gid = list(set(grpid).intersection(set(grpname["gid"])))
    gname = compare_lists(gnm,grpname["groupname"])
    gid = compare_lists(grpid,grpname["gid"])
#    print(gnm)
#    print(grpname)
    if len(gname) > 0:
        print(gname)
        return False
    if len(gid) > 0:
        print(gid)
        return False

    return True
def import_users():
    fpass = open('/root/tmp/pass.out.txt', 'r')
    fgrp = open('/root/tmp/group.out.txt', 'r')
    fshw = open('/root/tmp/shadow.out.txt', 'r')

    copyfile('/etc/passwd', '/etc/passwd.bkp')
    print("Password backed up to /etc/passwd.bkp")
    copyfile('/etc/group', '/etc/group.bkp')
    print("Group backed up to /etc/group.bkp")
    copyfile('/etc/shadow', '/etc/shadow.bkp')
    print("Shadow backed up to /etc/shadow.bkp")

    wrpass = open('/etc/passwd', 'a+')
    wrgrp = open('/etc/group', 'a+')
    wrshw = open('/etc/shadow', 'a+')

    for lnp in fpass:
        wrpass.writelines(lnp)
    for lng in fgrp:
        wrgrp.writelines(lng)
    for lns in fshw:
        wrshw.writelines(lns)

    fpass.close()
    fgrp.close()
    fshw.close()
    wrpass.close()
    wrgrp.close()
    wrshw.close()

def main():

    if verify_users() and verify_groups():
        import_users()
    else:
        print("Some users or groups have conflicted")

if __name__ == '__main__':main()