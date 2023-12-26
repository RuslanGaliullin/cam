#!/usr/bin/env python3
# The MIT License (MIT)
#
# Copyright (c) 2021-2023 Yegor Bugayenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os
import javalang
import subprocess
import time

def collect_body(start, text):
    result = "{"
    balance = 1
    start += 1
    while balance != 0:
        if text[start] == "}":
            balance -= 1
        if text[start] == "{":
            balance += 1
        result += text[start]
        start += 1
        if balance == 0:
            break
    return result

def find_methods_in_file(methods, text):
    result_files = []
    for index in range(len(methods)):
        pair = methods[index].split(":+:+:")
        if len(pair) != 3:
            continue
        class_name, method_name, return_type = pair[0], pair[1], pair[2]
        if len(method_name) == 0:
            continue
        if method_name[0] == "<":
            method_name = method_name.replace("<init>", class_name)
            return_type = ""
        method_index = text.find(f" {method_name}")
        start = text[method_index:].find("{")
        if start != -1:
            result_class_name = f"{class_name}_{method_name[:method_name.find('(')]}_{index}"
            result_class_body = f"public {return_type} {method_name} {collect_body(start, text[method_index:])}"
            result_files.append((result_class_name, f"class {result_class_name} {{{result_class_body}}}"))
    return result_files

def create_files(methods, dir):
    for file, text in methods:
        with open(os.path.join(dir, file + ".java"), 'w', encoding='utf-8') as others:
            others.write(text)

if __name__ == '__main__':
    JAVA: str = sys.argv[1]
    LST: str = sys.argv[2]
    try:
        with open(JAVA, encoding='utf-8') as f:
            text = f.read()
            raw = javalang.parse.parse(text)
            tree = raw.filter(javalang.tree.ClassDeclaration)
            if not (tree := list((value for value in tree))):
                os.remove(JAVA)
                with open(LST, 'a+', encoding='utf-8') as others:
                    others.write(JAVA + "\n")
            else:
                # Compile the Java file
                compile_command = "javac /cam/filters/java/org/example/Main.java"
                subprocess.run(compile_command, shell=True, check=True)

                # Execute the Java program
                execute_command = f"java -cp /cam/filters/java org.example.Main {JAVA}"
                result = subprocess.run(execute_command, shell=True, capture_output=True)
                methods = find_methods_in_file(result.stdout.decode().split("\n"), text)
                create_files(methods, os.path.dirname(JAVA))
                with open(os.path.join(f"{os.path.dirname(LST)}/github/", JAVA), 'w', encoding='utf-8') as others:
                    others.write(text)
                os.remove(JAVA)
    except Exception as e:
        with open("/cam/filters/error.out", 'w+', encoding='utf-8') as others:
            others.write(f"Error {e.__str__()} occured in delete non classes files with file {JAVA} \n")
