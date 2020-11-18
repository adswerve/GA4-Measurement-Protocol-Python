###############################################################################
# Google Analytics 4 Measurement Protocol for Python
# Copyright (c) 2020, Analytics Pros
#
# This project is free software, distributed under the BSD license.
# Analytics Pros offers consulting and integration services if your firm needs
# assistance in strategy, implementation, or auditing existing work.
###############################################################################

import requests
import json

class Ga4mp(object):

    def __init__(self, measurement_id, api_secret, client_id):
        self.measurement_id = measurement_id
        self.api_secret = api_secret
        self.client_id = client_id
        self.event_list = []
        self.base_domain = 'https://www.google-analytics.com/mp/collect'
        self.validation_domain = 'https://www.google-analytics.com/debug/mp/collect'


    def send(self, events, validation_hit=False, postpone=False):

        # check for any missing or invalid parameters among automatically collected and recommended event types
        self.check_params(events)

        if postpone == True:
            # build event list to send later
            for event in events:
                self.event_list.append(event)
        else:
            # batch events into sets of 25 events
            batched_event_list = [events[event:event + 25] for event in range(0, len(events), 25)]
            # send http post request
            self.http_post(batched_event_list, validation_hit=validation_hit)


    def postponed_send(self):

        # batch events into sets of 25 events
        batched_event_list = [self.event_list[event:event + 25] for event in range(0, len(self.event_list), 25)]
        self.http_post(batched_event_list)

        # clear event_list for future use
        self.event_list = []


    def http_post(self, batched_event_list, validation_hit=False):

        # set domain
        domain = self.base_domain
        if validation_hit == True:
            domain = self.validation_domain

        # loop through events in batches of 25
        batch_number = 1
        for batch in batched_event_list:
            url = f'{domain}?measurement_id={self.measurement_id}&api_secret={self.api_secret}'
            request = {'client_id': self.client_id,
                       'events': batch}
            body = json.dumps(request)

            # Send http post request
            result = requests.post(url=url, data=body)
            status_code = result.status_code
            print(f'Batch Number: {batch_number}\nStatus code: {status_code}')
            batch_number += 1


    def check_params(self, events):

        # all automatically collected and recommended event types
        params_dict = {'ad_click': ['ad_event_id'],
                       'ad_exposure': ['firebase_screen', 'firebase_screen_id', 'firebase_screen_class', 'exposure_time'],
                       'ad_impression': ['ad_event_id'],
                       'ad_query': ['ad_event_id'],
                       'ad_reward': ['ad_unit_id', 'reward_type', 'reward_value'],
                       'add_payment_info': ['coupon', 'currency', 'items', 'payment_type', 'value'],
                       'add_shipping_info': ['coupon', 'currency', 'items', 'shipping_tier', 'value'],
                       'add_to_cart': ['currency', 'items', 'value'],
                       'add_to_wishlist': ['currency', 'items', 'value'],
                       'adunit_exposure': ['firebase_screen', 'firebase_screen_id', 'firebase_screen_class', 'exposure_time'],
                       'app_clear_data': [],
                       'app_exception': ['fatal', 'timestamp', 'engagement_time_msec'],
                       'app_remove': [],
                       'app_store_refund': ['product_id', 'value', 'currency', 'quantity'],
                       'app_store_subscription_cancel': ['product_id', 'price', 'value', 'currency', 'cancellation_reason'],
                       'app_store_subscription_convert': ['product_id', 'price', 'value', 'currency', 'quantity'],
                       'app_store_subscription_renew': ['product_id', 'price', 'value', 'currency', 'quantity', 'renewal_count'],
                       'app_update': ['previous_app_version'],
                       'begin_checkout': ['coupon', 'currency', 'items', 'value'],
                       'click': [],
                       'dynamic_link_app_open': ['source', 'medium', 'campaign', 'link_id', 'accept_time'],
                       'dynamic_link_app_update': ['source', 'medium', 'campaign', 'link_id', 'accept_time'],
                       'dynamic_link_first_open': ['source', 'medium', 'campaign', 'link_id', 'accept_time'],
                       'earn_virtual_currency': ['virtual_currency_name', 'value'],
                       'error': ['firebase_error', 'firebase_error_value'],
                       'file_download': ['file_extension', 'file_name', 'link_classes', 'link_domain', 'link_id', 'link_text', 'link_url'],
                       'firebase_campaign': ['source', 'medium', 'campaign', 'term', 'content', 'gclid', 'aclid', 'cp1', 'anid', 'click_timestamp', 'campaign_info_source'],
                       'firebase_in_app_message_action': ['message_name', 'message_device_time', 'message_id'],
                       'firebase_in_app_message_dismiss': ['message_name', 'message_device_time', 'message_id'],
                       'firebase_in_app_message_impression': ['message_name', 'message_device_time', 'message_id'],
                       'first_open': ['previous_gmp_app_id', 'updated_with_analytics', 'previous_first_open_count', 'system_app', 'system_app_update', 'deferred_analytics_collection', 'reset_analytics_cause', 'engagement_time_msec'],
                       'first_visit': [],
                       'generate_lead': ['value', 'currency'],
                       'in_app_purchase': ['product_id', 'price', 'value', 'currency', 'quantity', 'subscription', 'free_trial', 'introductory_price'],
                       'join_group': ['group_id'],
                       'level_end': ['level_name', 'success'],
                       'level_start': ['level_name'],
                       'level_up': ['character', 'level'],
                       'login': ['method'],
                       'notification_dismiss': ['message_name', 'message_time', 'message_device_time', 'message_id', 'topic', 'label', 'message_channel'],
                       'notification_foreground': ['message_name', 'message_time', 'message_device_time', 'message_id', 'topic', 'label', 'message_channel', 'message_type'],
                       'notification_open': ['message_name', 'message_time', 'message_device_time', 'message_id', 'topic', 'label', 'message_channel'],
                       'notification_receive': ['message_name', 'message_time', 'message_device_time', 'message_id', 'topic', 'label', 'message_channel', 'message_type'],
                       'notification_send': ['message_name', 'message_time', 'message_device_time', 'message_id', 'topic', 'label', 'message_channel'],
                       'os_update': ['previous_os_version'],
                       'page_view': ['page_location', 'page_referrer'],
                       'post_score': ['level', 'character', 'score'],
                       'purchase': ['affiliation', 'coupon', 'currency', 'items', 'transaction_id', 'shipping', 'tax', 'value'],
                       'refund': ['transaction_id', 'value', 'currency', 'tax', 'shipping', 'items'],
                       'remove_from_cart': ['currency', 'items', 'value'],
                       'screen_view': ['firebase_screen', 'firebase_screen_class', 'firebase_screen_id', 'firebase_previous_screen', 'firebase_previous_class', 'firebase_previous_id', 'engagement_time_msec'],
                       'scroll': [],
                       'search': ['search_term'],
                       'select_content': ['content_type', 'item_id'],
                       'select_item': ['items', 'item_list_name', 'item_list_id'],
                       'select_promotion': ['items', 'promotion_id', 'promotion_name', 'creative_name', 'creative_slot', 'location_id'],
                       'session_start': [],
                       'share': ['content_type', 'item_id'],
                       'sign_up': ['method'],
                       'view_search_results': ['search_term'],
                       'spend_virtual_currency': ['item_name', 'virtual_currency_name', 'value'],
                       'tutorial_begin': [],
                       'tutorial_complete': [],
                       'unlock_achievement': ['achievement_id'],
                       'user_engagement': ['engagement_time_msec'],
                       'video_start': ['video_current_time', 'video_duration', 'video_percent', 'video_provider', 'video_title', 'video_url', 'visible'],
                       'video_progress': ['video_current_time', 'video_duration', 'video_percent', 'video_provider', 'video_title', 'video_url', 'visible'],
                       'video_complete': ['video_current_time', 'video_duration', 'video_percent', 'video_provider', 'video_title', 'video_url', 'visible'],
                       'view_cart': ['currency', 'items', 'value'],
                       'view_item': ['currency', 'items', 'value'],
                       'view_item_list': ['items', 'item_list_name', 'item_list_id'],
                       'view_promotion': ['items', 'promotion_id', 'promotion_name', 'creative_name', 'creative_slot', 'location_id']}

        # check for any missing or invalid parameters
        for e in events:
            event_name = e['name']
            event_params = e['params']
            if (event_name in params_dict.keys()):
                for parameter in params_dict[event_name]:
                    if parameter not in event_params.keys():
                        print(f"WARNING: Event parameters do not match event type.\nFor {event_name} event type, the correct parameter(s) are {params_dict[event_name]}.\nFor a breakdown of currently supported event types and their parameters go here: https://support.google.com/analytics/answer/9267735\n")
