import sys
from typing import List, Dict


class Dependencies:
    deps: Dict[str, List[str]] = {}
    installed: List[str] = []
    explicitly_installed: List[str] = [] # these are NOT removed implicitly

    def make_dependent(self, package: str, *args: str) -> None:
        """ make package dependent on *args """
        # if any *args depend on package, abort
        for arg in args:
            if package in self.deps.get(arg, []):
                print('{} depends on {}, ignoring command'.format(arg, package))
                return
        p_deps = self.deps.get(package)
        if p_deps:
            p_deps.extend(args)
        else:
            self.deps[package] = [x for x in args]

    def list_packages(self) -> None:
        print('\n'.join(self.installed))

    def install_package(self, to_install: str) -> None:
        """add to_install to installed packages, as well as all its dependencies"""
        if to_install in self.installed:
            print('{} is already installed'.format(to_install))
            return

        self.explicitly_installed.append(to_install)
        self._install_package_recur(to_install)

    def remove_package(self, to_remove: str) -> None:
        """remove to_remove if nothing needs it, then remove all dependencies in the same way"""
        for i in self.installed:
            if to_remove in self.deps.get(i, []):
                print('{} is still needed'.format(to_remove))
                return

        # if not installed return
        if to_remove not in self.installed:
            print('{} is not installed'.format(to_remove))
            return

        # first we remove the head explicitly
        print('Removing {}'.format(to_remove))
        self.installed.remove(to_remove)

        # then we remove the dependencies *implicitly*
        for d in self.deps.get(to_remove, []):
            self._remove_package_recur(d)

    def run_commands(self, command_list: List[List[str]]) -> None:
        # assume commands are formatted properly in input
        for com in command_list:
            print(' '.join(com))
            if com[0] == 'LIST':
                self.list_packages()
            elif com[0] == 'DEPEND':
                self.make_dependent(com[1], *com[2:])
            elif com[0] == 'INSTALL':
                self.install_package(com[1])
            elif com[0] == 'REMOVE':
                self.remove_package(com[1])
            else:
                return

    def _install_package_recur(self, package: str) -> None:
        p_dep = self.deps.get(package, [])

        # first we install all of package's dependencies
        for d in p_dep:
            self._install_package_recur(d)

        # then we install package
        if package not in self.installed:
            print('Installing {}'.format(package))
            self.installed.append(package)

    '''only called by remove_package, after removing the explicit package'''
    def _remove_package_recur(self, to_remove: str) -> None:
        p_deps = self.deps.get(to_remove, [])

        # first we remove the head (if we can)
        if to_remove in self.explicitly_installed:
            return

        can_remove = True  # one way flag
        for i in self.installed:
            if to_remove in self.deps.get(i, []):
                can_remove = False
                break

        if can_remove:
            print('Removing {}'.format(to_remove))
            self.installed.remove(to_remove)

            # then we go to the dependencies
            for p in p_deps:
                self._remove_package_recur(p)


if __name__ == '__main__':
    dep = Dependencies()
    commands: List[List[str]] = []
    # parse input
    s = ''
    while s != 'END':
        s = input().strip()
        commands.append(s.split())

    # run the program
    dep.run_commands(commands)
    sys.exit(0)
