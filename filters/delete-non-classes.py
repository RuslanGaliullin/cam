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
from timeit import default_timer as timer
import sys
import os
import javalang
import subprocess
import time
from multiprocessing import Pool, cpu_count
import asyncio
import aiofiles

def collect_body(start, text):
    result = "{"
    balance = 1
    flag_double = False
    start += 1
    while start < len(text) and balance != 0:
        if text[start] == "\"" and text[start - 1] != "\\":
            flag_double = not flag_double
        elif not flag_double and text[start] == "}":
            if start + 1 < len(text) and text[start - 1] != '\'' and text[start + 1] != '\'':
                balance -= 1
        elif not flag_double and text[start] == "{":
            if start + 1 < len(text) and text[start - 1] != '\'' and text[start + 1] != '\'':
                balance += 1
        result += text[start]
        if balance == 0:
            break
        start += 1
    return result

def split_list(input_list, chunk_size):
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

async def find_methods_in_file(methods, text, dir_name):
    result_files = []
    create_file_coroutines = []
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
        method_index = text.find(f" {method_name} ")
        if method_index == -1:
            continue
        start = text[method_index:].find("{")
        if start == -1:
            continue
        result_class_name = f"{class_name}_{method_name[:method_name.find('(')]}_{index}"
        result_class_body = f"public {return_type} {method_name} {collect_body(start, text[method_index:])}"

        create_file_coroutine = create_file(result_class_name, f"class {result_class_name} {{{result_class_body}}}", dir_name)
        create_file_coroutines.append(create_file_coroutine)

    # Await all create_file coroutines concurrently
    await asyncio.gather(*create_file_coroutines)

    return result_files

async def create_file(file, text, dir):
    async with aiofiles.open(os.path.join(dir, file + ".java"), 'w', encoding='utf-8') as others:
        await others.write(text)

def run_async(methods, text, dir_name):
    asyncio.run(find_methods_in_file(methods, text, dir_name))

if __name__ == '__main__':
    JAVA: str = sys.argv[1]
    LST: str = sys.argv[2]
    try:
        # start = timer()
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
                compile_command = "javac /cam/filters/java/org/example/Main.java" #/home/rmg
                subprocess.run(compile_command, shell=True, check=True)

                # Execute the Java program
                execute_command = f"java -cp /cam/filters/java org.example.Main {JAVA}"
                result = subprocess.run(execute_command, shell=True, capture_output=True)
                result = result.stdout.decode().split("\n")
                dir_name = os.path.dirname(JAVA)
                run_async(result, text, dir_name)
                # with Pool() as pool:
                    # Use starmap to pass multiple arguments to the function
                    # res = pool.starmap(run_async, [(methods, text, dir_name) for methods in split_list(result, cpu_count())])
                    # print(res)
                # with open(os.path.join(f"{os.path.dirname(LST)}/github/", JAVA), 'w', encoding='utf-8') as others:
                #     others.write(text)
                os.remove(JAVA)
        # end = timer()
        # print(end-start)
    except Exception as e:
        with open("/cam/filters/error.out", 'w+', encoding='utf-8') as others:
            others.write(f"Error {e.__str__()} occured in delete non classes files with file {JAVA} \n")
