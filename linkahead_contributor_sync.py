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
from caosadvancedtools.models.parser import parse_model_from_string

from fw_get_contributors import get_contributors


def _insert_model():

    yaml_string = """
Contributor:
  obligatory_properties:
    Full name:
      datatype: TEXT
    fw_uuid:
      datatype: TEXT
  recommended_properties:
    Email:
      datatype: TEXT
    ORCID:
      datatype: TEXT
    """
    model = parse_model_from_string(yaml_string)
    model.sync_data_model(noquestion=True)


def insert_contributors(list_of_contribs: list[dict], create_model: bool = False):

    if create_model:
        _insert_model()

    contrib_rt = db.RecordType(name="Contributor").retrieve()
    full_name_prop = db.Property(name="Full name").retrieve()
    uuid_prop = db.Property(name="fw_uuid").retrieve()
    email_prop = db.Property(name="Email").retrieve()
    orcid_prop = db.Property(name="ORCID").retrieve()

    inserts = db.Container()
    for contr in list_of_contribs:
        rec = db.Record(name=contr["name"]).add_parent(contrib_rt)
        rec.add_property(full_name_prop, value=contr["name"])
        rec.add_property(uuid_prop, value=contr["uuid"])
        if "email" in contr and contr["email"]:
            rec.add_property(email_prop, value=contr["email"])
        if "orcid" in contr and contr["orcid"]:
            rec.add_property(orcid_prop, value=contr["orcid"])
        inserts.append(rec)

    if inserts:
        inserts.insert()


if __name__ == "__main__":

    contribs = get_contributors(project_uuid='ae8496de-b75d-4226-a04a-cee6f0869878')

    insert_contributors(contribs, True)
