import os
import db
import pickle


def get_db_cur():
    return db.getCur()


def receive(socket, buff):
    first_rec = socket.recv(buff)
    if len(first_rec) == 0:
        return ''
    split_first = first_rec.split(b' ', 1)
    rec_len = int(split_first[0])
    rec_msg = split_first[1]
    while len(rec_msg) < rec_len:
        rec_msg += socket.recv(buff)
    return pickle.loads(rec_msg)


def attach_send(send_data):
    dump_data = pickle.dumps(send_data)
    return bytes(f'{len(dump_data)} ', 'utf-8') + dump_data


def clr_scr():
    clear_cmd = ''
    if os.name == 'nt':
        clear_cmd = 'cls'
    else:
        if os.name == 'posix':
            clear_cmd = 'clear'
    # return subprocess.run(clear_cmd, shell=True) == 0
    os.system(clear_cmd)


def format_line(line):
    formated_line = ''
    gap_size = 5
    if str(type(line)) == "<class 'tuple'>":
        for i in range(len(line) - 1):
            formated_line += str(line[i]) + ' ' * gap_size
        formated_line += str(line[len(line) - 1])
    else:
        formated_line = line
    return formated_line


def print_res(res):
    if str(type(res)) == "<class 'list'>":
        for r in res:
            print(format_line(r))
    else:
        print(format_line(res))


def is_valid_cmd(cmd, para):
    command_map = {
        '!su': (2, 3),
        '!si': (2,),
        '!ls': (0,),
        '!scr': (1,),
        '!help': (0,)
    }
    if len(para) in command_map.get(cmd, ()):
        return True
    return False


def process_send(con, req, is_signin, is_admin, cur):
    res = ''
    cmd = req.split()[0]
    para = tuple(req.split()[1:])
    if not is_valid_cmd(cmd, para):
        res = 'Invalid command'
    else:
        if not is_signin:
            if cmd == '!su':
                res = db.signup(cur, para)
            elif cmd == '!si':
                res, is_admin, is_signin = db.signin(cur, para)
            else:
                res = 'Sign in first'
        else:
            if cmd == '!su' or cmd == '!si':
                res = 'You\'ve already signed in'
            elif cmd != '!help':
                if cmd == '!ls':
                    res = db.get_all_match(cur)
                else:
                    match_id = para[0]
                    res = db.get_all_event(cur, match_id)
        if cmd == '!help':
            res = ['!su [username] [password] [key] : sign up (with key if you are admin)', '!si [username] [password] : sign in',
                   '!ls : show the list of all matches', '!scr [id] : show the score of the given id', '!help : show this help']
    con.sendall(attach_send(res))
    return is_signin, is_admin
