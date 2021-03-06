__author__ = 'Dimitry Lvovsky, dimitry@reviewpro.com'
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
import requests
import hashlib
import time

class Connect():
    DEFAULT_URL = "http://connect.reviewpro.com"
    DEFAULT_HTTPS_URL = "https://connect.reviewpro.com"
    REVIEW_SUMMARIES_URL = "/v1/lodging/review/summaries"
    CSQ_URL = "/v1/lodging/csq"
    REVIEW_AVAILABLE_SRC_URL = "/v1/lodging/sources/available"
    PUBLISHED_REVIEWS_SRC_URL = "/v1/lodging/review/published"
    MANAGEMENT_RESPONSES_URL =  "/v1/lodging/review/responses"
    PIDS_FOR_ACCOUNT_URL = "/v1/account/lodgings"
    DAILY_INDEX_URL = "/v1/lodging/index/daily"
    LODGIN_DIST_URL = "/v1/lodging/review/rating/distribution"
    REVENUE_INDEXES_URL = "/v1/lodging/revenueindexes"
    BACKOFFICE_PRODUCT_URL = "/bo/v1/product"
    BACKOFFICE_USER_URL = "/bo/v1/user"

    def __init__(self, api_key, api_sec):
        self.__api_key = api_key
        self.__api_sec = api_sec

    def fetchDailyIndexForRating(self, pid, fd, td, rt, max_error=3):
        params = {"pid": pid, "fd": fd, "td": td, "rt": rt}
        self.__add_api_key(params)
        url = Connect.DEFAULT_URL + Connect.DAILY_INDEX_URL
        error_count = 0
        while error_count < max_error:
            resp = requests.get(url, params=params)
            if resp.status_code == requests.codes.ok:
                return resp.json()
            error_count += 1
            print "endpoint %s responded with error code %s, error %s out of %s sleeping for %s sec" % (url, resp.status_code, error_count, max_error, error_count ** 2)
            time.sleep(error_count ** 2)

    def fetchDailyDistribution(self, pid, fd, td, rt, max_error=3):
        params = {"pid": pid, "fd": fd, "td": td, "rt": rt, 'timeseries':True}
        self.__add_api_key(params)
        url = Connect.DEFAULT_URL + Connect.LODGIN_DIST_URL
        error_count = 0
        while error_count < max_error:
            resp = requests.get(url, params=params)
            if resp.status_code == requests.codes.ok:
                return resp.json()
            error_count += 1
            print "endpoint %s responded with error code %s, error %s out of %s sleeping for %s sec" % (url, resp.status_code, error_count, max_error, error_count ** 2)
            time.sleep(error_count ** 2)

    def fetchReviewSummaries(self, pid, fd, td, rw=10, st=0, max_error=3):
        params = {"pid": pid, "fd": fd, "td": td, "rw": rw, "st": st}
        self.__add_api_key(params)
        url = Connect.DEFAULT_URL + Connect.REVIEW_SUMMARIES_URL
        error_count = 0
        while error_count < max_error:
            resp = requests.get(url, params=params)
            if resp.status_code == requests.codes.ok:
                return resp.json()
            error_count += 1
            print "endpoint %s responded with error code %s, error %s out of %s sleeping for %s sec" % (url, resp.status_code, error_count, max_error, error_count ** 2)
            time.sleep(error_count ** 2)

    def fetchAvailableSrc(self, pid, fd, td, max_error=3):
        params = {"pid": pid, "fd": fd, "td": td}
        self.__add_api_key(params)
        url = Connect.DEFAULT_URL + Connect.REVIEW_AVAILABLE_SRC_URL
        error_count = 0
        while error_count < max_error:
            resp = requests.get(url, params=params)
            if resp.status_code == requests.codes.ok:
                return resp.json()
            error_count += 1
            print "endpoint %s responded with error code %s, error %s out of %s, sleeping for %s sec" % (url, resp.status_code, error_count, max_error, error_count ** 2)
            time.sleep(error_count ** 2)
    
    def fetchPublishedReviews(self, pid, max_error=3):
        params = {"pid": pid}
        self.__add_api_key(params)
        url = Connect.DEFAULT_URL + Connect.PUBLISHED_REVIEWS_SRC_URL
        error_count = 0
        while error_count < max_error:
            resp = requests.get(url, params=params)
            if resp.status_code == requests.codes.ok:
                return resp.json()
            error_count += 1
            print "endpoint %s responded with error code %s, error %s out of %s, sleeping for %s sec" % (url, resp.status_code, error_count, max_error, error_count ** 2)
            time.sleep(error_count ** 2)

    def fetchPidsForAccount(self, max_error=3):
        params = {'aid':'143'}
        self.__add_api_key(params)
        url = Connect.DEFAULT_URL + Connect.PIDS_FOR_ACCOUNT_URL
        error_count = 0
        while error_count < max_error:
            resp = requests.get(url, params=params)
            if resp.status_code == requests.codes.ok:
                return resp.json()
            error_count += 1
            print "endpoint %s responded with error code %s, error %s out of %s, sleeping for %s sec" % (url, resp.status_code, error_count, max_error, error_count ** 2)
            time.sleep(error_count ** 2)

    def fetchManagementResponses(self, pid, fd, td, max_error=3):
        params = {"pid": pid, "fd": fd, "td": td}
        self.__add_api_key(params)
        url = Connect.DEFAULT_URL + Connect.MANAGEMENT_RESPONSES_URL
        print url
        error_count = 0
        while error_count < max_error:
            resp = requests.get(url, params=params)
            if resp.status_code == requests.codes.ok:
                return resp.json()
            error_count += 1
            print "endpoint %s responded with error code %s, error %s out of %s, sleeping for %s sec" % (url, resp.status_code, error_count, max_error, error_count ** 2)
            time.sleep(error_count ** 2)

    def pushCSQ(self, data, pid, max_error=3):
        url = Connect.DEFAULT_URL + Connect.CSQ_URL
        print url
        params = {"pid": pid}
        self.__add_api_key(params)
        self.__add_signature(params)
        headers = {'content-type': 'application/json'}
        return requests.post(url, data=data, headers=headers, params=params)

    def pushCSQXML(self, data, pid, max_error=3):
        url = Connect.DEFAULT_URL + Connect.CSQ_URL
        print url
        params = {"pid": pid}
        self.__add_api_key(params)
        self.__add_signature(params)
        headers = {'content-type': 'application/xml'}
        return requests.post(url, data=data, headers=headers, params=params)

    def postRevenueIndexes(self, data):
        url = Connect.DEFAULT_HTTPS_URL + Connect.REVENUE_INDEXES_URL
        params = {}
        self.__add_api_key(params)
        self.__add_signature(params)
        headers = {'content-type': 'application/json'}
        return requests.post(url, data=data, headers=headers, params=params)

    def postBackofficeProduct(self, data):
        url = Connect.DEFAULT_HTTPS_URL + Connect.BACKOFFICE_PRODUCT_URL
        params = {}
        self.__add_api_key(params)
        self.__add_signature(params)
        headers = {'content-type': 'application/json'}
        return requests.post(url, data=data, headers=headers, params=params)

    def putBackofficeProduct(self, ppid, data):
        url = Connect.DEFAULT_HTTPS_URL + Connect.BACKOFFICE_PRODUCT_URL + "/" + ppid
        params = {}
        self.__add_api_key(params)
        self.__add_signature(params)
        headers = {'content-type': 'application/json'}
        return requests.put(url, data=data, headers=headers, params=params)

    def getBackofficeProduct(self, ppid, dpid):
        url = Connect.DEFAULT_HTTPS_URL + Connect.BACKOFFICE_PRODUCT_URL + "/" + ppid
        params = {"sourceType": dpid}
        self.__add_api_key(params)
        self.__add_signature(params)
        headers = {'content-type': 'application/json'}
        return requests.get(url, headers=headers, params=params)

    def listBackofficeProduct(self, dpid):
        url = Connect.DEFAULT_HTTPS_URL + Connect.BACKOFFICE_PRODUCT_URL + "s"
        params = {"sourceType": dpid}
        self.__add_api_key(params)
        self.__add_signature(params)
        headers = {'content-type': 'application/json'}
        return requests.get(url, headers=headers, params=params)

    def deleteBackofficeProduct(self, ppid, dpid):
        url = Connect.DEFAULT_HTTPS_URL + Connect.BACKOFFICE_PRODUCT_URL + "/" + ppid
        params = {"sourceType": dpid}
        self.__add_api_key(params)
        self.__add_signature(params)
        headers = {'content-type': 'application/json'}
        return requests.delete(url, headers=headers, params=params)

    def postBackofficeUser(self, data):
        url = Connect.DEFAULT_HTTPS_URL + Connect.BACKOFFICE_USER_URL
        params = {}
        self.__add_api_key(params)
        self.__add_signature(params)
        headers = {'content-type': 'application/json'}
        return requests.post(url, data=data, headers=headers, params=params)

    def putBackofficeUser(self, username, data):
        url = Connect.DEFAULT_HTTPS_URL + Connect.BACKOFFICE_USER_URL + "/" + username
        params = {}
        self.__add_api_key(params)
        self.__add_signature(params)
        headers = {'content-type': 'application/json'}
        return requests.put(url, data=data, headers=headers, params=params)

    def getBackofficeUser(self, username, dpid):
        url = Connect.DEFAULT_HTTPS_URL + Connect.BACKOFFICE_USER_URL + "/" + username
        params = {"sourceType": dpid}
        self.__add_api_key(params)
        self.__add_signature(params)
        headers = {'content-type': 'application/json'}
        return requests.get(url, headers=headers, params=params)

    def listBackofficeUser(self):
        url = Connect.DEFAULT_HTTPS_URL + Connect.BACKOFFICE_USER_URL + "s"
        params = {}
        self.__add_api_key(params)
        self.__add_signature(params)
        headers = {'content-type': 'application/json'}
        return requests.get(url, headers=headers, params=params)

    def deleteBackofficeUser(self, username):
        url = Connect.DEFAULT_HTTPS_URL + Connect.BACKOFFICE_USER_URL + "/" + username
        params = {}
        self.__add_api_key(params)
        self.__add_signature(params)
        headers = {'content-type': 'application/json'}
        return requests.delete(url, headers=headers, params=params)

    # private methods
    def __add_signature(self, params):
        m = hashlib.sha256()
        m.update(str.encode(self.__api_key + self.__api_sec + repr(int(time.time()))))
        params['sig'] = m.hexdigest()

    def __add_api_key(self, params):
        params['api_key'] = self.__api_key

