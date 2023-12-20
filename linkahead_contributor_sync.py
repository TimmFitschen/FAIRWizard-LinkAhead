#
# This file is a part of the LinkAhead Project.
#
# Copyright (C) 2023 Indiscale GmbH <info@indiscale.com>
# Copyright (C) 2023 Florian Spreckelsen <f.spreckelsen@indiscale.com>
# Copyright (C) 2022 Timm Fitschen <t.fitschen@indiscale.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#

import linkahead as db


def _insert_model():
    # This would probably be replaced by reading in e.g., a YAML file with the
    # datamodel in a real production use case.
    contrib_rt = db.RecordType(name="Contributor")
    full_name_prop = db.Property(name="Full name", datatype=db.TEXT)
    # All contributors have to have a name
    contrib_rt.add_property(full_name_prop, importance=db.OBLIGATORY)
    db.Container().exetend([contrib_rt, full_name_prop]).insert()

    return contrib_rt, full_name_prop


def insert_contributors(list_of_names: list[str], create_model: bool = False):

    if create_model:
        contrib_rt, full_name_prop = _insert_model()
    else:
        contrib_rt = db.RecordType(name="Contributor").retrieve()
        full_name_prop = db.Propert(name="Full name").retrieve()

    inserts = db.Container()
    for name in list_of_names:
        rec = db.Record(name=name).add_parent(contrib_rt)
        rec.add_property(full_name_prop, value=name)
        inserts.append(rec)

    if inserts:
        inserts.insert()


if __name__ == "__main__":

    test_names = [
        "Sarah Scientist",
        "John Doe"
    ]

    insert_contributors(test_names, True)
