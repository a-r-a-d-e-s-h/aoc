#!/usr/bin/env python3.10

# 44:30
# 1:03:54

import re

def get_input():
    text = open("input.txt").read().rstrip("\n")
    return text


class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = {}
        self.files = {}

    def add_file(self, file):
        self.files[file.name] = file

    def size(self):
        size = 0
        for filename in self.files.keys():
            file = self.files[filename]
            size += file.size
        for directory in self.children.values():
            size += directory.size()
        return size


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


class System:
    def __init__(self, text):
        self.lines = text.splitlines()
        self.current_dir = None
        self.system_layout = Directory("/")

    def set_cwd_top(self):
        self.current_dir = self.system_layout

    def up(self):
        if self.current_dir.parent is not None:
            self.current_dir = self.current_dir.parent

    def parse_text(self):
        self.parse_position = 0
        while self.parse_position < len(self.lines):
            line = self.lines[self.parse_position]
            self.parse_position += 1
            self.parse_dollar_line(line)
    
    def parse_dollar_line(self, line):
        line = line[2:]
        if line[:2] == 'cd':
            line = line[3:]
            if line == '/':
                self.set_cwd_top()
            elif line == '..':
                self.up()
            else:
                if line not in self.current_dir.children:
                    self.mkdir(line)
                self.current_dir = self.current_dir.children[line]
        elif line[:2] == 'ls':
            while self.parse_position < len(self.lines):
                next_line = self.lines[self.parse_position]
                if next_line[0] == "$":
                    break
                self.parse_position += 1

                if next_line[:3] == "dir":
                    next_line = next_line[4:]
                    if next_line not in self.current_dir.children:
                        self.mkdir(next_line)
                else:
                    size, name = next_line.split(" ", 1)
                    self.current_dir.add_file(File(name, int(size)))


    def mkdir(self, name):
        self.current_dir.children[name] = Directory(name, self.current_dir)

    def walk_directories(self, directory=None):
        if directory is None:
            directory = self.system_layout
        yield directory
        for subdir in directory.children.values():
            yield from self.walk_directories(subdir)


def main():
    text = get_input()
    system = System(text)
    system.parse_text()

    # part 1
    total = 0
    for directory in system.walk_directories():
        size = directory.size()
        if size <= 100000:
            total += size
    print(total)

    # part 2
    used_space = system.system_layout.size()
    remaining = 70000000 - used_space
    need_to_free = 30000000 - remaining

    smallest_exceeding_min = used_space
    for directory in system.walk_directories():
        size = directory.size()
        if size >= need_to_free:
            smallest_exceeding_min = min(size, smallest_exceeding_min)
    print(smallest_exceeding_min)

if __name__ == "__main__":
    main()
