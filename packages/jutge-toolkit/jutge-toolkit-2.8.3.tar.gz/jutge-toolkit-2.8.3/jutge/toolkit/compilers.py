#!/usr/bin/env python3
# coding=utf-8

import glob
import logging
import os
import signal
import subprocess
import sys
import time
import timeit

from colorama import Fore, Style
from jutge import util

# Maximum time to compile
max_compilation_time = 30

# List of available compilers (will be filled)
compilers = []


# Exceptions:


class CompilationTooLong(Exception):
    pass


class ExecutionError(Exception):
    pass


class CompilationError(Exception):
    pass


class Compiler:
    """Compiler base class (abstract)."""

    def __init__(self, handler, name):
        self.handler = handler
        self.name = name

    def name(self):
        """Returns the compiler name."""
        raise Exception('Abstract method')

    def id(self):
        """Returns the compiler id (automatically computed from its class name)."""
        return self.__class__.__name__.replace('Compiler_', '').replace('XX', '++')

    def type(self):
        """Returns the compiler type (compiler, interpreter, ...)."""
        raise Exception('Abstract method')

    def warning(self):
        """Returns some warning associated to the compiler."""
        return ""

    def executable(self):
        """Returns the file name of the resulting "executable"."""
        raise Exception('Abstract method')

    def prepare_execution(self, ori):
        """Copies the necessary files from ori to . to prepare the execution."""
        raise Exception('Abstract method')

    def language(self):
        """Returns the language name."""
        raise Exception('Abstract method')

    def version(self):
        """Returns the version of this compiler."""
        raise Exception('Abstract method')

    def flags1(self):
        """Returns flags for the first compilation."""
        raise Exception('Abstract method')

    def flags2(self):
        """Returns flags for the second compilation (if needed)."""
        raise Exception('Abstract method')

    def extension(self):
        """Returns extension of the source files (without dot)."""
        raise Exception('Abstract method')

    def compile(self):
        """Doc missing."""
        raise Exception('Abstract method')

    def execute(self, tst, correct, iterations=1):
        """Doc missing."""
        raise Exception('Abstract method')

    def execute_compiler(self, cmd):
        """Executes the command cmd, but controlling the execution time."""
        pid = os.fork()
        if pid == 0:
            # Child
            logging.info(cmd)
            print(Style.DIM + cmd + Style.RESET_ALL)

            error = False
            result = ''
            try:
                result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as exec:
                print(exec.output.decode('utf-8'))
                error = True

            if error or len(result) != 0:
                if len(result) != 0: print('\n' + result.decode('utf-8').strip() + '\n')
                print(
                    Style.BRIGHT + Fore.RED + 'Compilation error! ' + Style.NORMAL + 'Please check ' + self.name + '.' + self.extension() + ' and try again.' + Style.RESET_ALL)
                os._exit(1)

            if util.file_exists('program.exe'):
                os.system('strip program.exe')
            os._exit(0)
        else:
            # Parent
            c = 0
            while c <= max_compilation_time:
                ret = os.waitpid(pid, os.WNOHANG)
                if ret[0] != 0:
                    # Ok!
                    if ret[1] != 0: sys.exit(0)
                    return

                time.sleep(0.1)
                c += 0.1
            os.kill(pid, signal.SIGKILL)
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            raise CompilationTooLong

    def get_version(self, cmd, lin):
        """Private method to get a particular line from a command output."""
        return subprocess.getoutput(cmd).split('\n')[lin].strip()

    def info(self):
        return {
            'compiler_id': self.id(),
            'name': self.name,
            'language': self.language(),
            'version': self.version(),
            'flags1': self.flags1(),
            'flags2': self.flags2(),
            'extension': self.extension(),
            'type': self.type(),
            'warning': self.warning(),
        }


class Compiler_GCC(Compiler):
    compilers.append('GCC')

    def name(self):
        return 'GNU C Compiler'

    def type(self):
        return 'compiler'

    def executable(self):
        return self.name + '.c.exe'

    def language(self):
        return 'C'

    def version(self):
        return self.get_version('gcc --version', 0)

    def flags1(self):
        # return '-D_JUDGE_ -DNDEBUG -O2'
        return '-D_JUDGE_ -O2 -DNDEBUG -Wall -Wextra -Wno-sign-compare'

    def flags2(self):
        return ''

    def extension(self):
        return 'c'

    def execute(self, tst, correct, iterations=1):
        if correct:
            ext = 'cor'
            print("./%s < %s.inp > %s.%s" % (self.executable(), tst, tst, ext), end='')
        else:
            ext = 'c.out'

        """func.system("./%s < %s.inp > %s.%s" %
                    (self.executable(), tst, tst, ext))"""
        func = 'import os; os.system("./%s < %s.inp > %s.%s")' % (self.executable(), tst, tst, ext)
        time = timeit.timeit(func, number=iterations) / iterations
        return time

    def compile(self):
        if 'source_modifier' in self.handler and (
                self.handler['source_modifier'] == 'no_main' or self.handler['source_modifier'] == 'structs'):
            return self.compile_no_main()
        else:
            return self.compile_normal()

    def compile_normal(self):
        # Compile original program
        util.del_file(self.executable())
        try:
            self.execute_compiler('gcc ' + self.flags1() + ' ' + self.name +
                                  '.c -o ' + self.executable() + ' -lm')
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            util.del_file(self.executable())
            return False
        return util.file_exists(self.executable())

    def compile_no_main(self):
        # Modify the program
        util.copy_file(self.name + '.c', 'modified.c')
        ori = util.read_file('modified.c')
        main = util.read_file('main.c')
        util.write_file('modified.c',
                        """
#define main main__3

%s

#undef main
#define main main__2

%s

#undef main

int main() {
    return main__2();
}

""" % (ori, main))

        # Compile modified program
        util.del_file(self.executable())
        try:
            self.execute_compiler('gcc ' + self.flags2() + ' modified.c -o ' +
                                  self.executable() + ' -lm')
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            util.del_file(self.executable())
            util.del_file('modified.c')
            return False

        # We are almost there
        util.del_file('modified.c')
        if util.file_exists(self.executable()):
            return True
        else:
            print(Style.BRIGHT + Fore.RED + 'Unreported error.' + Style.RESET_ALL)
            util.del_file(self.executable())
            return False


class Compiler_GXX(Compiler):
    compilers.append('GXX')

    def name(self):
        return 'GNU C++ Compiler'

    def type(self):
        return 'compiler'

    def executable(self):
        return self.name + '.cc.exe'

    def language(self):
        return 'C++'

    def version(self):
        return self.get_version('g++ --version', 0)

    def flags1(self):
        # return '-D_JUDGE_ -DNDEBUG -O2'
        return '-std=c++11 -D_JUDGE_ -O2 -DNDEBUG -Wall -Wextra -Wno-sign-compare -Wshadow'

    def flags2(self):
        # return '-D_JUDGE_ -DNDEBUG -O2'
        return '-std=c++11 -D_JUDGE_ -O2 -DNDEBUG -Wall -Wextra -Wno-sign-compare -Wshadow'

    def extension(self):
        return 'cc'

    def execute(self, tst, correct, iterations=1):
        if correct:
            ext = 'cor'
            print("./%s < %s.inp > %s.%s" % (self.executable(), tst, tst, ext), end='')
        else:
            ext = 'cc.out'

        """func.system("./%s < %s.inp > %s.%s" %
                    (self.executable(), tst, tst, ext))"""
        func = 'import os; os.system("./%s < %s.inp > %s.%s")' % (self.executable(), tst, tst, ext)
        time = timeit.timeit(func, number=iterations) / iterations
        return time

    def compile(self):
        if 'source_modifier' in self.handler and (
                self.handler['source_modifier'] == 'no_main' or self.handler['source_modifier'] == 'structs'):
            return self.compile_no_main()
        else:
            return self.compile_normal()

    def compile_normal(self):
        # Compile original program
        util.del_file(self.executable())
        try:
            self.execute_compiler('g++ ' + self.flags1() + ' ' + self.name +
                                  '.cc -o ' + self.executable())
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            util.del_file(self.executable())
            return False
        return util.file_exists(self.executable())

    def compile_no_main(self):
        # Modify the program
        util.copy_file(self.name + '.cc', 'modified.cc')
        ori = util.read_file('modified.cc')
        main = util.read_file('main.cc')
        util.write_file('modified.cc',
                        """
#define main main__3

%s

#undef main
#define main main__2

%s

#undef main

int main() {
    return main__2();
}

""" % (ori, main))

        # Compile modified program
        util.del_file(self.executable())
        try:
            self.execute_compiler(
                'g++ ' + self.flags2() + ' modified.cc -o ' + self.executable())
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            util.del_file(self.executable())
            util.del_file('modified.cc')
            return False

        # We are almost there
        util.del_file('modified.cc')
        if util.file_exists(self.executable()):
            return True
        else:
            print(Style.BRIGHT + Fore.RED + 'Unreported error.' + Style.RESET_ALL)
            util.del_file(self.executable())
            return False


class Compiler_P1XX(Compiler_GXX):
    compilers.append('P1XX')

    def flags1(self):
        return '-D_JUDGE_ -DNDEBUG -O2 -Wall -Wextra -Werror -Wno-sign-compare -Wshadow'

    def name(self):
        return 'GNU C++ Compiler with extra flags for beginners'


class Compiler_GXX11(Compiler_GXX):
    compilers.append('GXX11')

    def name(self):
        return 'GNU C++11 Compiler'

    def flags1(self):
        return '-D_JUDGE_ -DNDEBUG -O2 -std=c++11'

    def flags2(self):
        return '-D_JUDGE_ -DNDEBUG -O2 -std=c++11'


class Compiler_GXX17(Compiler_GXX):
    compilers.append('GXX17')

    def name(self):
        return 'GNU C++17 Compiler'

    def flags1(self):
        return '-D_JUDGE_ -DNDEBUG -O2 -std=c++17'

    def flags2(self):
        return '-D_JUDGE_ -DNDEBUG -O2 -std=c++17'


class Compiler_GHC(Compiler):
    compilers.append('GHC')

    def name(self):
        return 'Glasgow Haskell Compiler'

    def type(self):
        return 'compiler'

    def executable(self):
        return self.name + '.hs.exe'

    def language(self):
        return 'Haskell'

    def version(self):
        return self.get_version('ghc --version', 0)

    def flags1(self):
        return ' -O3 '

    def flags2(self):
        return ' -O3 '

    def extension(self):
        return 'hs'

    def execute(self, tst, correct, iterations=1):
        if correct:
            ext = 'cor'
            print("./%s < %s.inp > %s.%s" % (self.executable(), tst, tst, ext), end='')
        else:
            ext = 'hs.out'

        """func.system("./%s < %s.inp > %s.%s" %
                    (self.executable(), tst, tst, ext))"""
        func = 'import os; os.system("./%s < %s.inp > %s.%s")' % (self.executable(), tst, tst, ext)
        time = timeit.timeit(func, number=iterations) / iterations
        return time

    def compile(self):
        if 'source_modifier' in self.handler and self.handler['source_modifier'] == 'no_main':
            return self.compile_no_main()
        else:
            return self.compile_normal()

    def compile_normal(self):
        util.del_file(self.executable())
        try:
            self.execute_compiler('ghc ' + self.flags1() + ' ' + self.name +
                                  '.hs -o ' + self.executable() + ' 1> /dev/null')
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            util.del_file(self.executable())
            return False

        util.del_file(self.name + '.hi')
        util.del_file(self.name + '.o')
        util.file_exists(self.executable())
        return True

    def compile_no_main(self):
        util.copy_file(self.name + '.hs', 'modified.hs')
        ori = util.read_file('modified.hs')
        main = util.read_file('main.hs')
        util.write_file('modified.hs',
                        """
%s

%s
""" % (ori, main))

        util.del_file(self.executable())
        try:
            self.execute_compiler('ghc ' + self.flags1() + ' modified.hs -o ' +
                                  self.executable() + ' 1> /dev/null')
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            util.del_file(self.executable())
            return False

        util.del_file('modified.hs')
        util.del_file('modified.hi')
        util.del_file('modified.o')
        return util.file_exists(self.executable())


class Compiler_RunHaskell(Compiler):
    compilers.append('RunHaskell')

    def name(self):
        return 'Glasgow Haskell Compiler (with tweaks for testing in the judge)'

    def type(self):
        return 'compiler'

    def executable(self):
        return self.name + '.hs'

    def language(self):
        return 'Haskell'

    def version(self):
        return self.get_version('ghc --version', 0)

    def flags1(self):
        return '-O3'

    def flags2(self):
        return '-O3'

    def extension(self):
        return 'hs'

    def execute(self, tst, correct, iterations=1):
        if correct:
            ext = 'cor'
            print("runhaskell work.hs > %s.%s" % (tst, ext))
        else:
            ext = 'hs.out'

        self.compile_work(tst)

        """func.system("runhaskell work.hs > %s.%s" % (tst, ext))"""
        func = 'import os; os.system("runhaskell work.hs > %s.%s")' % (tst, ext)
        time = timeit.timeit(func, number=iterations) / iterations

        util.del_file('work.hs')

        return time

    def compile(self):
        util.del_file("work")
        util.del_file("work.hi")
        util.del_file("work.o")
        util.copy_file(self.name + '.hs', "work.hs")
        f = open("work.hs", "a")
        print("""main = do print "OK" """, file=f)
        f.close()

        try:
            self.execute_compiler('ghc -O3 work.hs 1> /dev/null')
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            return False

        util.del_file("work")
        util.del_file("work.hi")
        util.del_file("work.hs")
        util.del_file("work.o")
        return True

    def compile_work(self, tst):
        f = open("extra.hs", "w")
        print('"testing"', file=f)
        f.close()
        return self.compile_with("extra.hs", tst)

    def compile_with(self, extra, tst):
        try:
            util.copy_file(self.name + ".hs", "work.hs")
            if util.file_exists("judge.hs"):
                os.system("cat judge.hs >> work.hs")
            f = open("work.hs", "a")
            print("main = do", file=f)
            for line in open(tst + ".inp").readlines():
                line = line.rstrip()
                if line.startswith("let "):
                    print("    %s" % line, file=f)
                else:
                    print("    print (%s)" % line, file=f)
            f.close()
            self.execute_compiler(
                'ghc ' + self.flags1() + ' work.hs -o work.exe 1> /dev/null')
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            return False

        if util.file_exists('work.exe'):
            util.del_file("work.hi")
            util.del_file('work.exe')
            return True
        else:
            return False


class Compiler_RunPython(Compiler):
    compilers.append('RunPython')

    def name(self):
        return 'Python3 Interpreter (with tweaks for testing in the judge)'

    def type(self):
        return 'interpreter'

    def executable(self):
        return self.name + '.py'

    def language(self):
        return 'Python'

    def version(self):
        return self.get_version('python3 --version', 0)

    def flags1(self):
        return ''

    def flags2(self):
        return ''

    def extension(self):
        return 'py'

    def gen_wrapper(self):
        util.write_file('py3c.py',
                        """
#!/usr/bin/python3

import py_compile, sys

py_compile.compile(sys.argv[1])
""")

    def del_wrapper(self):
        util.del_file('py3c.py')

    def execute(self, tst, correct, iterations=1):
        if correct:
            ext = 'cor'
            print("python3 %s.py > %s.%s" % (self.name, tst, ext))
        else:
            ext = 'py.out'

        if self.compile_with(tst + ".inp"):
            os.system("cat solution.py %s.inp > work.py" % tst)
            func = 'import os; os.system("python3 work.py > %s.%s")' % (tst, ext)
            time = timeit.timeit(func, number=iterations) / iterations
            util.del_dir('__pycache__')
            util.del_file('work.py')
            return time
        else:
            return -1

    def compile(self):
        try:
            self.gen_wrapper()
            code = util.read_file(self.name + '.py')
            util.write_file(self.name + '.py', code)
            self.execute_compiler(
                'python3 py3c.py ' + self.name + '.py 1> /dev/null')
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            return False
        self.del_wrapper()
        return True

    def compile_with(self, extra):
        try:
            util.copy_file(self.name + ".py", "work.py")
            os.system("echo '' >> work.py")
            os.system("echo '' >> work.py")
            if util.file_exists("judge.py"):
                os.system("cat judge.py >> work.py")
            os.system("cat %s >> work.py" % extra)
            self.gen_wrapper()
            self.execute_compiler(
                'python3 py3c.py work.py 1> /dev/null')
            return True
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            return False

        self.del_wrapper()
        return False


class Compiler_JDK(Compiler):
    compilers.append('JDK')

    def name(self):
        return 'OpenJDK Runtime Environment'

    def type(self):
        return 'compiler (vm)'

    def executable(self):
        return 'Main.class'

    def language(self):
        return 'Java'

    def version(self):
        return self.get_version('java -version', 0).replace('"', "'")

    def flags1(self):
        return ''

    def flags2(self):
        return ''

    def extension(self):
        return 'java'

    def gen_wrapper(self):
        util.write_file("wrapper.java",
                        """
class WrapperMain {

    public static void main (String[] args) {
        try {
            Main.main(args);
            System.exit(0);
        } catch (Throwable e) {
            // We hide the exception.
            // System.out.println(e);
            System.exit(1);
        }
    }

}
""")

    def del_wrapper(self):
        util.del_file('wrapper.java')

    def execute(self, tst, correct, iterations=1):
        if correct:
            ext = 'cor'
            print("java Main < %s.inp > %s.%s" % (tst, tst, ext), end='')
        else:
            ext = 'java.out'

        """func.system("java Main < %s.inp > %s.%s" % (tst, tst, ext))"""
        func = 'import os; os.system("java Main < %s.inp > %s.%s")' % (tst, tst, ext)
        time = timeit.timeit(func, number=iterations) / iterations
        return time

    def compile(self):
        if 'source_modifier' in self.handler and self.handler['source_modifier'] == 'no_main':
            return self.compile_no_main()
        else:
            return self.compile_normal()

    def compile_normal(self):
        for f in glob.glob('*.class'):
            util.del_file(f)
        try:
            util.copy_file(self.name + '.java', 'Main.java')
            self.gen_wrapper()
            self.execute_compiler(
                'javac ' + self.flags1() + ' wrapper.java')
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            return False

        self.del_wrapper()
        return util.file_exists(self.executable())

    def compile_no_main(self):
        # esta fet a sac!!! cal fer-ho be

        for f in glob.glob('*.class'):
            util.del_file(f)
        try:
            # create Solution.class
            self.execute_compiler(
                'javac ' + self.flags1() + ' ' + self.name + '.java')
            # create Main.class
            self.execute_compiler(
                'javac ' + self.flags1() + ' main.java')
            # create JudgeMain.class
            self.gen_wrapper()
            self.execute_compiler(
                'javac ' + self.flags1() + ' wrapper.java')
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            return False
        self.del_wrapper()
        return util.file_exists('Main.class')


class Compiler_Python3(Compiler):
    compilers.append('Python3')

    def name(self):
        return 'Python3'

    def type(self):
        return 'interpreter'

    def executable(self):
        return self.name + '.py'

    def language(self):
        return 'Python'

    def version(self):
        return self.get_version('python3 -V', 0)

    def flags1(self):
        return ''

    def flags2(self):
        return ''

    def extension(self):
        return 'py'

    def gen_wrapper(self):
        util.write_file('py3c.py',
                        """
#!/usr/bin/python3

import py_compile, sys

py_compile.compile(sys.argv[1])
""")

    def del_wrapper(self):
        util.del_file('py3c.py')

    def execute(self, tst, correct, iterations=1):
        if 'source_modifier' in self.handler and (
                self.handler['source_modifier'] == 'no_main' or self.handler['source_modifier'] == 'structs'):
            util.copy_file(self.name + '.py', 'modified.py')
            ori = util.read_file(self.name + '.py')
            main = util.read_file('main.py')
            util.write_file('modified.py', '%s\n%s\n' % (ori, main))

            exec = 'modified.py'
        else:
            exec = self.executable()

        if correct:
            ext = 'cor'
            print("python3 %s < %s.inp > %s.%s" % (exec, tst, tst, ext), end='')
        else:
            ext = 'py.out'

        """func.system("python3 %s < %s.inp > %s.%s" % (exec, tst, tst, ext))"""
        func = 'import os; os.system("python3 %s < %s.inp > %s.%s")' % (exec, tst, tst, ext)
        time = timeit.timeit(func, number=iterations) / iterations

        util.del_file('modified.py')
        util.del_dir('__pycache__')

        return time

    def compile(self):
        if 'source_modifier' in self.handler and (
                self.handler['source_modifier'] == 'no_main' or self.handler['source_modifier'] == 'structs'):
            return self.compile_no_main()
        else:
            return self.compile_normal()

    def compile_normal(self):
        try:
            self.gen_wrapper()
            code = util.read_file(self.name + '.py')
            util.write_file(self.name + '.py', code)
            util.write_file('py3c.py',
                            """#!/usr/bin/python3

import py_compile, sys

py_compile.compile(sys.argv[1])""")
            self.execute_compiler(
                'python3 py3c.py ' + self.name + '.py 1> /dev/null')
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            return False
        self.del_wrapper()
        return True

    def compile_no_main(self):
        if not self.compile_normal():
            return False

        # Modify the program
        util.copy_file(self.name + '.py', 'modified.py')
        ori = util.read_file(self.name + '.py')
        main = util.read_file('main.py')
        util.write_file('modified.py', '%s\n%s\n' % (ori, main))

        # Compile modified program
        try:
            self.gen_wrapper()
            self.execute_compiler(
                'python3 py3c.py modified.py 1> /dev/null')
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            return False
        self.del_wrapper()
        return True


class Compiler_R(Compiler):
    compilers.append('R')

    def name(self):
        return 'R'

    def type(self):
        return 'interpreter'

    def executable(self):
        return self.name + '.R'

    def language(self):
        return 'R'

    def version(self):
        return self.get_version('R --version', 0)

    def flags1(self):
        return ''

    def flags2(self):
        return ''

    def extension(self):
        return 'R'

    def execute(self, tst, correct, iterations=1):
        if correct:
            ext = 'cor'
            print("Rscript solution.R < %s.inp > %s.%s" % (tst, tst, ext), end='')
        else:
            ext = 'R.out'

        """func.system("Rscript solution.R < %s.inp > %s.%s" % (tst, tst, ext))"""
        func = 'import os; os.system("Rscript solution.R < %s.inp > %s.%s")' % (tst, tst, ext)
        time = timeit.timeit(func, number=iterations) / iterations
        return time

    def compile(self):
        if self.handler['source_modifier'] == 'no_main':
            return self.compile_no_main()
        else:
            return self.compile_normal()

    def compile_normal(self):
        try:
            s = util.read_file(self.name + ".R")
            util.write_file("wrapper.R",
                            """
wrapper_R <- function() {

%s

}
""" % s)
            util.write_file("compiler.R",
                            """
library("codetools")

source("wrapper.R")

checkUsage(wrapper_R)
            """)
            self.execute_compiler(
                'Rscript compiler.R 1> /dev/null')
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            return False
        util.del_file("compiler.R")
        util.del_file("wrapper.R")
        return True

    def compile_no_main(self):
        # Modify the program
        util.copy_file(self.name + '.R', 'modified.R')
        ori = util.read_file('modified.R')
        main = util.read_file('main.R')
        util.write_file('modified.R', '%s\n%s\n' % (ori, main))
        try:
            s = util.read_file("modified.R")
            util.write_file("wrapper.R",
                            """
wrapper_R <- function() {

%s

}
""" % s)
            util.write_file("compiler.R",
                            """
library("codetools")

source("wrapper.R")

checkUsage(wrapper_R)
        """ % s)
            self.execute_compiler(
                'Rscript compiler.R 1> /dev/null')
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            return False
        util.del_file("compiler.R")
        util.del_file("wrapper.R")
        util.del_file("modified.R")
        return True


class Compiler_PRO2(Compiler):
    compilers.append('PRO2')

    def name(self):
        return 'PRO2 - GNU C++ Compiler'

    def type(self):
        return 'compiler'

    def executable(self):
        return self.name + '.pro2.exe'

    def language(self):
        return 'C++'

    def version(self):
        return self.get_version('g++ --version', 0)

    def flags1(self):
        return '-D_JUDGE_ -D_GLIBCXX_DEBUG -O2 -Wall -Wextra -Werror -Wno-sign-compare -std=c++11'

    def flags2(self):
        return '-D_JUDGE_ -D_GLIBCXX_DEBUG -O2 -std=c++11'

    def extension(self):
        return 'cc'

    def execute(self, tst, correct, iterations=1):
        if correct:
            ext = 'cor'
            print("./%s < %s.inp > %s.%s" % (self.executable(), tst, tst, ext), end='')
        else:
            ext = 'pro2.out'

        """func.system("./%s < %s.inp > %s.%s" %
                    (self.executable(), tst, tst, ext))"""
        func = 'import os; os.system("./%s < %s.inp > %s.%s")' % (self.executable(), tst, tst, ext)
        time = timeit.timeit(func, number=iterations) / iterations
        return time

    def compile(self):
        util.del_file(self.executable())
        util.del_dir(self.name + '.dir')
        os.mkdir(self.name + ".dir")

        try:
            if util.file_exists("solution.cc"):
                util.system('cp solution.cc ' + self.name + '.dir/' + 'program.cc')
            elif util.file_exists("solution.hh"):
                util.system('cp solution.hh ' + self.name + '.dir/program.hh')
            else:
                print("There is no solution.cc nor solution.hh")

            util.system('cp public/* ' + self.name + '.dir')
            util.system('cp private/* ' + self.name + '.dir')

            os.chdir(self.name + '.dir')
            self.execute_compiler('g++ ' + self.flags1() + ' *.cc -o ../' +
                                  self.executable())
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            os.chdir('..')
            util.del_file(self.executable())
            return False
        os.chdir('..')
        if util.file_exists(self.executable()):
            util.system("(cd public && tar cf ../public.tar *)")
            util.system("(cd private && tar cf ../private.tar *)")
            return True
        else:
            return False


class Compiler_MakePRO2(Compiler):
    compilers.append('MakePRO2')

    def name(self):
        return 'Make for PRO2'

    def type(self):
        return 'compiler'

    def executable(self):
        return self.name + '.makepro2.exe'

    def language(self):
        return 'Make'

    def version(self):
        return self.get_version('make -v', 0)

    def flags1(self):
        return ''

    def flags2(self):
        return ''

    def extension(self):
        return 'tar'

    def compile(self):
        util.del_file(self.executable())
        util.del_dir(self.name + ".dir")

        if not util.file_exists("solution"):
            raise Exception("There is no solution directory")
        if not util.file_exists("public"):
            raise Exception("There is no public directory")
        if not util.file_exists("private"):
            raise Exception("There is no private directory")

        try:
            util.mkdir(self.name + '.dir')
            util.system('cp solution/*  public/* private/* ' +
                        self.name + '.dir')
            os.chdir(self.name + '.dir')

            self.execute_compiler('make program.exe 1> make.log')
        except CompilationTooLong:
            print(Style.BRIGHT + Fore.RED + 'Compilation time exceeded!' + Style.RESET_ALL)
            os.chdir('..')
            return False

        os.chdir('..')

        if util.file_exists(self.name + '.dir/program.exe'):
            util.copy_file(self.name + '.dir/program.exe', './' + self.executable())

        util.del_dir(self.name + ".dir")

        if util.file_exists(self.executable()):
            util.system("(cd public && tar cf ../public.tar *)")
            util.system("(cd private && tar cf ../private.tar *)")
            util.system("(cd solution && tar cf ../solution.tar *)")
            return True
        else:
            return False

    def execute(self, tst, correct, iterations=1):
        if correct:
            ext = 'cor'
            print("./%s < %s.inp > %s.%s" % (self.executable(), tst, tst, ext), end='')
        else:
            ext = 'makepro2.out'

        """func.system("./%s < %s.inp > %s.%s" %
                    (self.executable(), tst, tst, ext))"""
        func = 'import os; os.system("./%s < %s.inp > %s.%s")' % (self.executable(), tst, tst, ext)
        time = timeit.timeit(func, number=iterations) / iterations
        return time


################################################################################


def available_compilers():
    available_list = []
    supported_list = info()
    for k, v in supported_list.items():
            if "not found" not in v["version"]:
                available_list.append(k)

    if available_list != {}: print("Available compilers:", end = ' ')
    for compiler in available_list:
        print(compiler, end = '')
        if compiler == available_list[-2]: print(' and ', end = '')
        elif compiler != available_list[-1]: print(', ', end = '')
        else: print()


def compiler(cpl, handler=None, name=None):
    """Returns a compiler for cpl."""

    cpl = cpl.replace('++', 'XX')
    return eval('Compiler_%s(handler, name)' % cpl)


def compiler_extensions(handler_compiler):
    """Returns the info on all the compilers."""

    r = {}
    for x in compilers:
        ext = compiler(x).extension()
        if x == handler_compiler:
            r[ext] = x
        elif 'Run' not in x and ext not in r:
            # Python3 has priority over RunPython and GHC has priority over RunHaskell
            r[ext] = x
    return r


def info():
    """Returns the info on all the compilers."""

    r = {}
    for x in compilers:
        r[x] = compiler(x).info()
    return r


def main():
    """Prints the info on all the compilers in YML format."""
    util.print_yml(info())


if __name__ == '__main__':
    main()
