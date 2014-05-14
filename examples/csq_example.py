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
from connect import Connect
import json


def main():
    connect = Connect.Connect("<your api_key>", "<your shared sec>")
    j = json.dumps({
        "id": 102531,
        "source": "LimeSurvey CSQ Hotel: ",
        "reviews": [
            {
                "title": "Survey para Hotel ReviewPro",
                "text": "",
                "author": "SAMPLE AUTHOR NAME",
                "email": "sampleaddress@example.es",
                "dateFormat": "dd/MM/yyyy",
                "dateOfStay": "10/12/2013",
                "language": "es",
                "externalId": "12bf5c58-25b4-1c2d-d5b8-52a6a11f7901",
                "ratingValues": [
                    {
                        "ratingType": "OVERALL",
                        "value": 9,
                        "outOf": 10
                    }
                ]
            }
        ]
    })
    resp = connect.pushCSQ(j, 102531)

    print resp.status_code


if __name__ == "__main__":
    main()
