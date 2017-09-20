__author__ = 'Dimitry Lvovsky'
# Copyright 2014 ReviewRank S.A ( ReviewPro )
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from connect_py import Connect

def main():
    connect = Connect.Connect("<your api_key>", "<your shared sec>")

    j = '<product id="102531" source="LimeSurvey CSQ Hotel: "><review><author>SAMPLE AUTHOR NAME</author><text></text><language>es</language><review_id>123456</review_id><date_of_stay date_format="dd/MM/yyyy">10/12/2013</date_of_stay><email>sampleaddress@example.es</email><reservation_source>ABC</reservation_source><overall value="100" out_of="100"/><service value="100" out_of="100"/><cleanliness value="100" out_of="100"/><location value="100" out_of="100"/><value value="100" out_of="100"/><gastronomy value="100" out_of="100"/><room value="100" out_of="100"/><reception value="100" out_of="100"/></review></product>'

    resp = connect.pushCSQXML(j, 102531)

    print resp.status_code


if __name__ == "__main__":
    main()
