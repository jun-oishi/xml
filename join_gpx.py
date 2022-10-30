# coding:utf-8

import sys
import os
import shutil
import re
import copy


class Gpx:
    """
    gpxファイルを操作するクラス
    """

    def __init__(self, source_filename: str) -> None:
        # TODO: check if file exists
        # TODO: separate dirname
        self.source_filename: str = source_filename
        self.__buf_filename: str = source_filename + ".buf"
        self.__fun_buf_filename: str = source_filename + ".buf.tmp"
        shutil.copy(self.source_filename, self.__buf_filename)
        self.__saved: bool = True
        return

    def __del__(self) -> None:
        if (not self.__saved):
            dist_name: str = input('Enter file name to save editted `' + self.source_filename + '` (or nothing to discard): ')
            if (dist_name != ''):
                os.rename(self.__buf_filename, dist_name)
        os.remove(self.__buf_filename)
        return

    def __init_fun_buf(self) -> None:
        with open(self.__fun_buf_filename, 'w') as f:
            f.write('')
        return

    def __writelines(self, lines: list[str]) -> None:
        dist_filename = self.__fun_buf_filename
        if not isinstance(lines, list):
            lines = [lines]
        lines = [line if line.endswith('\n') else (line + '\n') for line in lines]

        with open(dist_filename, 'a') as f:
            f.writelines(lines)
        return

    def __refresh_buf(self) -> None:
        os.rename(self.__buf_filename, self.__fun_buf_filename)
        return

    def save(self, dist_filename: str) -> None:
        os.rename(self.__buf_filename, dist_filename)
        self.__saved = True
        return

    def save_with_suffix(self, suffix: str):
        source_filename_without_ext = os.path.splitext(self.source_filename)[0]
        dist_filename: str = source_filename_without_ext + suffix + '.gpx'
        self.save(dist_filename)
        return

    def trim_extention(self):
        initializer: str = '<extensions>'
        terminater: str = '</extensions>'
        buffer: list[str] = []

        self.__init_fun_buf()

        with open(self.__buf_filename, 'r') as f:
            in_extensions: bool = False
            while True:
                line: str = f.readline()
                if in_extensions:
                    if terminater in line:
                        in_extensions = False
                        continue
                    else:
                        continue
                else:
                    if initializer in line:
                        self.__writelines(buffer)
                        buffer.clear()
                        in_extensions = True
                        continue
                    else:
                        buffer.append(line)
                if not line:
                    self.__writelines(buffer)
                    break

        self.__refresh_buf()
        return

    def fix_ele(self):
        source_filename: str = self.__buf_filename
        dist_filename: str = self.__buf_filename + ".tmp"

        with open(dist_filename, 'w') as f:
            f.write('')

        with open(source_filename, 'r') as f:
            while True:
                line: str = f.readline()
                if ('<ele>' in line) and ('</ele>' in line):
                    m = re.match(r'.*<ele>(.*)</ele>.*', line)
                    if m is None:
                        raise Exception('Failed to parse ele')
                    ele: float = float(m.group(1))
                    if ele < 0:
                        ele = 0.0
                    line = line.replace(m.group(1), str(ele))
                self.__writelines([line])
                if not line:
                    break

        self.__refresh_buf()
        return

    @classmethod
    def join(cls, filenames: list[str], dist_filename: str) -> None:
        initial = filenames[0]
        final = filenames[-1]

        with open(initial, 'r') as fr:
            lines = fr.readlines()
            with open(dist_filename, 'w') as fw:
                fw.writelines(lines[:-4])

        for filename in filenames[1:-1]:
            with open(filename, 'r') as fr:
                lines = fr.readlines()
                with open(dist_filename, 'a') as fa:
                    fa.writelines(lines[9:-4])

        with open(final, 'r') as fr:
            lines = fr.readlines()
            with open(dist_filename, 'a') as fa:
                fa.writelines(lines[9:])

        return

# end class Gpx


if __name__ == '__main__':
    args = sys.argv
    filename = args[1]
    gpx = Gpx(filename)
    gpx.fix_ele()
    gpx.save_with_suffix('_fixed')
    # dist_filename = dirname + '/' + dirname + '_joined.gpx'
    # source_filenames = [dirname + '/' + filename for filename in os.listdir(dirname) if filename.endswith('.gpx')]
    # source_filenames.sort()
