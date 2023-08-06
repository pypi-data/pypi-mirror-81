from ptypes import Point
import re
import config


def normalize(row, tabsize, tabcount):
    row = row.replace('\n', '')
    tabcount[0] += row.count('\t')
    row = row.replace('\t', ' ' * tabsize)
    return row


class Document:
    def __init__(self, filename=''):
        self.clear()
        self.filename = filename
        self.tabs_replaced = False
        self.text = ['']
        self.valid = False
        self.undos = []
        self.undoing = False
        self.modified = False

    def clear(self):
        self.filename = ''
        self.text = ['']
        self.valid = False
        self.undos = []
        self.undoing = False
        self.modified = False

    def load(self, filename):
        try:
            self.tabs_replaced = False
            f = open(filename, 'r')
            self.text = f.readlines()
            f.close()
            if len(self.text) == 0:
                self.text = ['']
            else:
                if self.text[-1].endswith('\n'):
                    self.text.append('')
            tabsize = config.getint('tabsize')
            tabcount = [0]
            self.text = [normalize(row, tabsize, tabcount) for row in self.text]
            if tabcount[0] > 0:
                self.tabs_replaced = True
            self.filename = filename
            self.invalidate()
        except IOError:
            pass
            # message_box('Failed to open {}'.format(filename))

    def saveas(self, path):
        self.filename = path
        return self.save()

    def save(self):
        if len(self.filename) == 0:
            return False
        f = open(self.filename, 'w')
        f.write('\n'.join(self.text))
        f.close()
        self.modified = False
        return True

    def rows_count(self):
        return len(self.text)

    def get_row(self, index):
        if index < 0 or index >= self.rows_count():
            return ''
        return self.text[index]

    def find_in_row(self, cursor, text, case, regex, word):
        if cursor.y < 0 or cursor.y >= self.rows_count():
            return -1
        row = self.get_row(cursor.y)
        if not case:
            row = row.lower()
            text = text.lower()
        if word:
            text = '(^|\W){}($|\W)'.format(text)
            regex = True
        if regex:
            pat = re.compile(text)
            m = pat.search(row, cursor.x + 1)
            if m:
                return 1 + m.start()
            return -1
        else:
            return row.find(text, cursor.x + 1)

    def join_next_row(self, row_index):
        if 0 <= row_index < (self.rows_count() - 1):
            row = self.get_row(row_index)
            next_row = self.get_row(row_index + 1)
            del self.text[row_index + 1]
            self.text[row_index] = row + next_row
            if not self.undoing:
                self.undos.append([self.new_line, Point(len(row), row_index)])
            self.modified = True
        return Point(0, 0)

    def insert_block(self, text, cursor):
        if cursor.y < 0 or cursor.y >= self.rows_count():
            return False
        row = self.get_row(cursor.y)
        if cursor.x <= len(row):
            if not self.undoing:
                self.undos.append([self.delete_block, cursor.y, cursor.x, cursor.x + len(text)])
            row = row[0:cursor.x] + text + row[cursor.x:]
            self.text[cursor.y] = row
        return Point(len(text), 0)

    def delete_block(self, row_index, x0, x1):
        if 0 <= row_index < self.rows_count():
            row = self.get_row(row_index)
            if x1 < x0:
                x1 = len(row)
            if not self.undoing:
                self.undos.append([self.insert_block, row[x0:x1], Point(x0, row_index)])
            self.text[row_index] = row[0:x0] + row[x1:]
            self.modified = True
        return Point(0, 0)

    def insert_row(self, row_index, text=''):
        if 0 <= row_index < self.rows_count():
            if not self.undoing:
                self.undos.append([self.delete_row, row_index])
            self.text.insert(row_index, text)
        return Point(0, 0)

    def delete_row(self, row_index):
        if 0 <= row_index < self.rows_count():
            if not self.undoing:
                self.undos.append([self.insert_row, row_index, self.get_row(row_index)])
            del self.text[row_index]
            self.modified = True
        return Point(0, 0)

    def word_right(self, cursor):
        if cursor.y < 0 or cursor.y >= self.rows_count():
            return cursor
        row = self.get_row(cursor.y)
        x = cursor.x
        space_found = False
        if x < len(row):
            while x < len(row):
                if not row[x].isalnum():
                    space_found = True
                if row[x].isalnum() and space_found:
                    break
                x = x + 1
        else:
            if cursor.y < (self.rows_count() - 1):
                return Point(0, cursor.y + 1)
        return Point(x, cursor.y)

    def word_left(self, cursor):
        if cursor.y < 0 or cursor.y >= self.rows_count():
            return cursor
        row = self.get_row(cursor.y)
        x = cursor.x
        if x == 0:
            if cursor.y > 0:
                return Point(len(self.get_row(cursor.y - 1)), cursor.y - 1)
        while x > 0:
            x -= 1
            if x > 0 and row[x].isalnum() and not row[x - 1].isalnum():
                break
        return Point(x, cursor.y)

    def set_cursor(self, cursor):
        if cursor.y < 0:
            return Point(0, 0)
        if cursor.y >= self.rows_count():
            return Point(0, self.rows_count() - 1)
        row = self.get_row(cursor.y)
        x = cursor.x
        if x < 0:
            x = 0
        if x > len(row):
            x = len(row)
        return Point(x, cursor.y)

    def delete_char(self, cursor):
        row = self.text[cursor.y]
        if cursor.x < len(row):
            if not self.undoing:
                self.undos.append([self.add_char, row[cursor.x], Point(cursor), True])
            row = row[0:cursor.x] + row[cursor.x + 1:]
            self.text[cursor.y] = row
            self.invalidate()
        else:
            self.join_next_row(cursor.y)
        self.modified = True
        return Point(0, 0)

    def add_char(self, c, cursor, insert):
        row = self.text[cursor.y]
        if not insert and cursor.x < len(row):
            self.delete_char(cursor)
        row = row[0:cursor.x] + c + row[cursor.x:]
        if not self.undoing:
            self.undos.append([self.delete_char, Point(cursor)])
        self.text[cursor.y] = row
        self.invalidate()
        self.modified = True
        return Point(1, 0)

    def add_text(self, text, cursor, insert):
        cx = cursor.x
        res = Point(0, 0)
        if cursor.x < 0 or cursor.y < 0 or cursor.y >= self.rows_count():
            return res
        for c in text:
            if ord(c) == 10:
                self.new_line(cursor)
                cursor = Point(0, cursor.y + 1)
                res = Point(-cx, res.y + 1)
            else:
                self.add_char(c, cursor, insert)
                cursor = cursor + Point(1, 0)
                res += (1, 0)
        self.modified = True
        return res

    def new_line(self, cursor):
        row = self.get_row(cursor.y)
        cur = [row[0:cursor.x], row[cursor.x:]]
        self.text = self.text[0:cursor.y] + cur + self.text[cursor.y + 1:]
        if not self.undoing:
            self.undos.append([self.join_next_row, cursor.y])
        self.modified = True
        return Point(-cursor.x, 1)

    def invalidate(self):
        self.valid = False

    def validate(self):
        self.valid = True

    def start_compound(self):
        if not self.undoing:
            self.undos.append('{')

    def stop_compound(self):
        if not self.undoing:
            self.undos.append('}')

    def undo(self):
        depth = 0
        self.undoing = True
        res = Point(0, 0)
        while len(self.undos) > 0:
            cmd = self.undos[-1]
            del self.undos[-1]
            if isinstance(cmd, str):
                if cmd == '{':
                    depth += 1
                if cmd == '}':
                    depth -= 1
            else:
                f = cmd[0]
                res += f(*cmd[1:])
            if depth == 0:
                break
        self.undoing = False
        return res
