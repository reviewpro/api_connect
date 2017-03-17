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
import sys
from connect_py import Connect
import json


def main():

    if len(sys.argv) < 3:
        print "Too few arguments: " + str(len(sys.argv) - 1)
        print "Usage: $ python python_backoffice_example.py api_key shared_secret"
        return

    connect = Connect.Connect(sys.argv[1], sys.argv[2])

    data = json.dumps({})

    resp = connect.postBackofficeProduct(data)
    print "Backoffice post product returns " + str(resp.status_code) + " (expected 400)"

    resp = connect.putBackofficeProduct("a1b2c3d4e5", data)
    print "Backoffice put product returns " + str(resp.status_code) + " (expected 400)"

    resp = connect.getBackofficeProduct("a1b2c3d4e5", 54321)
    print "Backoffice get product returns " + str(resp.status_code) + " (expected 403)"

    resp = connect.listBackofficeProduct(54321)
    print "Backoffice list products returns " + str(resp.status_code) + " (expected 403)"

    resp = connect.deleteBackofficeProduct("a1b2c3d4e5", 54321)
    print "Backoffice delete product returns " + str(resp.status_code) + " (expected 403)"

    resp = connect.postBackofficeUser(data)
    print "Backoffice post user returns " + str(resp.status_code) + " (expected 400)"

    resp = connect.putBackofficeUser("fakeUsername12345", data)
    print "Backoffice put user returns " + str(resp.status_code) + " (expected 400)"

    resp = connect.getBackofficeUser("fakeUsername12345", 54321)
    print "Backoffice get user returns " + str(resp.status_code) + " (expected 403)"

    resp = connect.listBackofficeUser()
    print "Backoffice list users returns " + str(resp.status_code) + " (expected 200)"

    resp = connect.deleteBackofficeUser("fakeUsername12345")
    print "Backoffice delete user returns " + str(resp.status_code) + " (expected 404)"


if __name__ == "__main__":
    main()
