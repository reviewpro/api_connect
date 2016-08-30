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


/*****************************************************
 *************       USAGE EXAMPLES       ************
 *****************************************************/
$api_key = "YOUR_API_KEY";
$api_sec = "YOUR_API_SECRET";

$pid = 123456;          //this is a fake product
$fd = '2014-01-01';
$td = '2015-01-01';
$rt = 'OVERALL';

include('../connect_php/Connect.php');
// creates a connect object
$connect = new Connect($api_key, $api_sec);

$resp = $connect->fetch_api_data($pid, "fd=2013-01-01&td=2015-01-01&rt=OVERALL", $connect->DAILY_INDEX_URL); echo $resp."\n\n";
$resp = $connect->fetch_daily_index_for_rating($pid, $fd, $td, $rt); echo $resp."\n\n";
$resp = $connect->fetch_daily_distribution($pid, $fd, $td, $rt); echo $resp."\n\n";
$resp = $connect->fetch_available_sources($pid, $fd, $td); echo $resp."\n\n";
$resp = $connect->fetch_pids_for_account(); echo $resp."\n\n";
$resp = $connect->fetch_published_reviews($pid); echo $resp."\n\n";
$resp = $connect->fetch_management_responses($pid, $fd, $td); echo $resp."\n\n";

$data = json_encode(
    array(
        "id"=>$pid,
        "source"=>"Source Name",
        "reviews" => array(
            array(
                "title"=>"Review Title",
                "text"=>"Review Text",
                "author"=>"Author Name",
                "reservationSource"=>"Reservation",
                "email"=>"some_email@something.com",
                "dateFormat"=>"yyyy-MM-dd",
                "dateOfStay"=>"2015-03-26",
                "language"=>"en",
                "externalId"=>"987654321",
                "ratingValues" => array(
                    array(
                        "ratingType" => "OVERALL",
                        "value" => 8,
                        "outOf" => 10
                    ),
                    array(
                        "ratingType" => "OVERALL",
                        "value" => 9,
                        "outOf" => 10
                    )
                )
            )
        )
    )
);

// echo $data;
$resp = $connect->pushCSQ($pid, $data); echo "\n"; echo $resp."\n\n";

