__author__ = 'Steven'


from loader import Conf

import csv, os


class Conf2Csv(object):
    def __init__(self, conf_name):
        self._cols = []
        self._conf = Conf(conf_name)
        self._datas = self._conf.getAll()
        self._rows = []

        self._cols.append("type")
        self._cols.append("path")
        self._cols.append("promotion")
        self._cols.append("triche")
        self._prepare_columns()


    def _write(self, file_name, rows, directory="."):
        with open(os.path.join(directory, file_name), 'w') as f:
            writer = csv.writer(f,delimiter=';', quoting=csv.QUOTE_NONE, lineterminator='\n')
            writer.writerows(rows)

    def _prepare_columns(self):
        for k, v in self._datas.items():
            for col in v:
                if col not in self._cols:
                    self._cols.append(col)

    def _generate_header(self, first="slug"):
        row = []
        row.append(first)
        for key in self._cols:
            row.append(key)
        return row

    def _generate_rows(self):
        for k, v in self._datas.items():
            row = []
            row.append(k)
            for key in self._cols:
                row.append((", ".join(v[key]) if isinstance(v[key], list) else v[key] ) if key in v else "")
            self._rows.append(row)

    def export(self, csv_name):
        self._generate_rows()
        self._rows.insert(0, self._generate_header())
        self._write(csv_name, self._rows)


class Csv2Conf(object):
    def __init__(self, csv_name):
        self._rows = self._reader(csv_name)
        self._cols = self._rows[0]
        self._rows = self._rows[1:]
        self._dict = {}

    def _transform(self):
        for row in self._rows:
            obj = {}
            i = 1
            for k in self._cols[1:]:
                if len(row[i]) > 0:
                    obj[k] = row[i]
                i += 1
            self._dict[row[0]] = obj

    def export(self, conf_name):
        self._transform()
        conf = Conf(conf_name)
        for k, v in self._dict.items():
            conf.removeSection(k)
            conf.setSection(k, v)
        conf.save()

    def _reader(self, filename, directory="."):
        rows = []
        with open(os.path.join(directory, filename), 'r') as f:
                #next(f)
                reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
                for row in reader:
                    rows.append(row)
        return rows

if __name__ == "__main__":
    c = Conf2Csv("./slugs.conf")
    c.export("export.csv")
    s = Csv2Conf("./export.csv")
    s.export("result.conf")