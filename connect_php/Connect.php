<?php
/**
 * @author Gerard Montes <gerard.montes@reviewpro.com>
 *
 * Copyright 2014 ReviewRank S.A ( ReviewPro )
 *
 *  Licensed under the Apache License, Version 2.0 (the "License"); you may
 *  not use this file except in compliance with the License. You may obtain
 *  a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 *  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 *  License for the specific language governing permissions and limitations
 *  under the License.
 */

class Connect {
    public $DEFAULT_URL = 'http://connect.reviewpro.com';
    public $REVIEW_SUMMARIES_URL = '/v1/lodging/review/summaries';
    public $CSQ_URL = '/v1/lodging/csq';
    public $REVIEW_AVAILABLE_SRC_URL = '/v1/lodging/sources/available';
    public $PUBLISHED_REVIEWS_SRC_URL = '/v1/lodging/review/published';
    public $PIDS_FOR_ACCOUNT_URL = '/v1/account/lodgings';
    public $DAILY_INDEX_URL = '/v1/lodging/index/daily';
    public $LODGING_DIST_URL = '/v1/lodging/review/rating/distribution';

    private $api_key;
    private $api_sec;

    function Connect($api_key, $api_sec) {
        $this->api_key = $api_key;
        $this->api_sec = $api_sec;
    }

    function __construct($api_key, $api_sec) {
        $this->Connect($api_key, $api_sec);
    }


    function generate_signature() {
        return hash('sha256', $this->api_key.$this->api_sec.time());
    }

    /*
     * Creates the context for http requests
     * @return stream_context with protocol, headers and content to upload
     */
    private function generate_http_context($method, $data="") {
        $context = stream_context_create(
            array(
                "http" => array(
                    "method" => $method,
                    "header" => "Content-Type: application/json",
                    "content" => $data
                )
            )
        );
        return $context;
    }


    /*
     * Makes a request to the desired url with errors control (retries X times the same request)
     * @return string http response with the content requestesd (if GET), reponse code (if POST)
     */
    private function make_api_request($url, $method, $data, $max_error, $endpoint) {
        echo "Request to: ".$url."\n";
        $error_count = 0;
        while ($error_count < $max_error) {
            $context = $this->generate_http_context($method, $data);
            $resp = file_get_contents($url, FALSE, $context);
            if ($resp == TRUE) {
                return $resp;
            } else {
                $error_count++;
                echo sprintf("endpoint \"%s\" responded with error code \"%s\". Retry %d out of %d. Sleeping %d seconds...\n",
                    $endpoint, $http_response_header[0], $error_count, $max_error, pow($error_count, 2));
                sleep(pow($error_count, 2));
            }
        }
        return false;
    }

    /*
     * makes a GET request to retrieve data
     */
    private function make_get_request($url, $max_error, $endpoint) {
        return $this->make_api_request($url, "GET", "", $max_error, $endpoint);
    }

    /*
     * makes a POST request to upload data
     */
    private function make_post_request($url, $data, $max_error, $endpoint) {
        return $this->make_api_request($url, "POST", $data, $max_error, $endpoint);
    }


    /*
     * Generic request method
     * @param string $params string with needed params "fd=2013-01-01&td=2015-01-01&rt=OVERALL"
     * @return string request response
     */
    function fetch_api_data($pid, $params, $endpoint, $max_error=3) {
        $url = "$this->DEFAULT_URL$endpoint?pid=$pid&$params&api_key=$this->api_key";
        return $this->make_get_request($url, $max_error, $endpoint);
    }


    /*
     * THOSE ARE PREDEFINED REQUESTS TO THE API
     */

    // Lodging Rating Indexes
    function fetch_daily_index_for_rating($pid, $fd, $td, $rt, $max_error=3) {
        $endpoint = $this->DAILY_INDEX_URL;
        $url = "$this->DEFAULT_URL$endpoint?pid=$pid&fd=$fd&td=$td&rt=$rt&api_key=$this->api_key";
        return $this->make_get_request($url, $max_error, $endpoint);
    }

    // Lodging Rating Distribution
    function fetch_daily_distribution($pid, $fd, $td, $rt, $max_error=3) {
        $endpoint = $this->LODGING_DIST_URL;
        $url = "$this->DEFAULT_URL$endpoint?pid=$pid&fd=$fd&td=$td&rt=$rt&api_key=$this->api_key";
        return $this->make_get_request($url, $max_error, $endpoint);
    }

    // Sources
    function fetch_available_sources($pid, $fd, $td, $max_error=3) {
        $endpoint = $this->REVIEW_AVAILABLE_SRC_URL;
        $url = "$this->DEFAULT_URL$endpoint?pid=$pid&fd=$fd&td=$td&api_key=$this->api_key";
        return $this->make_get_request($url, $max_error, $endpoint);
    }

    // Reviews
    function fetch_published_reviews($pid, $max_errors=3) {
        $endpoint = $this->PUBLISHED_REVIEWS_SRC_URL;
        $url = "$this->DEFAULT_URL$endpoint?pid=$pid&api_key=$this->api_key";
        return $this->make_get_request($url, $max_errors, $endpoint);
    }

    // Reviews Summary
    function fetch_review_summaries($pid, $fd, $td, $rw=10, $st=0, $max_error=3) {
        $endpoint = $this->REVIEW_SUMMARIES_URL;
        $url = "$this->DEFAULT_URL$endpoint?pid=$pid&fd=$fd&td=$td&rw=$rw&st=$st&api_key=$this->api_key";
        return $this->make_get_request($url, $max_error, $endpoint);
    }

    // Account
    function fetch_pids_for_account($max_errors=3) {
        $endpoint = $this->PIDS_FOR_ACCOUNT_URL;
        $url = "$this->DEFAULT_URL$endpoint?api_key=$this->api_key";
        return $this->make_get_request($url, $max_errors, $endpoint);
    }


    /*
     * Upload a CSQ Review, $data must be a well-formed JSON.
     * @return string json response with response code.
     * */
    function pushCSQ($pid, $data, $max_errors=3) {
        $endpoint = $this->CSQ_URL;
        $sig = $this->generate_signature();
        $url = "$this->DEFAULT_URL$endpoint?pid=$pid&api_key=$this->api_key&sig=$sig";
        return $this->make_post_request($url, $data, $max_errors, $endpoint);
    }

    /*
     * Transforms a JSON object (or string) in a human readable string.
     */
    function pretty_print_json($json) {
        try {
            if (gettype($json) == "string") {
                $json = json_decode($json);
            }
            return json_encode($json, JSON_PRETTY_PRINT);
        } catch (Exception $e) {
            echo "Content not parseable to json.";
        }
    }
}
