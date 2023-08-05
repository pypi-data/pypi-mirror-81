import json
from .api_helper import KlaviyoAPI

class Profiles(KlaviyoAPI):
    PERSON = 'person'

    def get_profile(self, profile_id):
        """Get a profile by its ID.

        https://www.klaviyo.com/docs/api/people#person

        Args:
            profile_id (str): Profile id for a profile.

        Returns:
            (dict): Profile properties.
        """
        return self._v1_request('{}/{}'.format(self.PERSON, profile_id), self.HTTP_GET)

    def update_profile(self, profile_id, properties={}):
        """Get a profile by its ID.

        https://www.klaviyo.com/docs/api/people#person

        Args:
            profile_id (str): Profile id for a profile.
            properties (dict): Properties to update on a profile.

        Returns:
            (dict): Profile properties.
        """
        return self._v1_request('{}/{}'.format(self.PERSON, profile_id), self.HTTP_PUT, params=properties)

    def get_profile_metrics_timeline(self, profile_id, since=None, count=100, sort=KlaviyoAPI.SORT_DESC):
        """Gets a timeline of events on a profile.

        https://www.klaviyo.com/docs/api/people#metrics-timeline

        Args:
            profile_id (str): Unique id for profile.
            since (unix timestamp int or uuid str): A timestamp or uuid.
            count (int): The batch of records the response should return.
            sort (str): The order in which results should be returned.

        Returns:
            (dict): Event data related to a profile.
        """
        params = {
            self.COUNT: count,
            self.SORT: sort,
            self.SINCE: since,
        }
        filtered_params = self._filter_params(params)

        return self._v1_request('{}/{}/{}/{}'.format(
                self.PERSON,
                profile_id,
                self.METRICS,
                self.TIMELINE
            ),
            self.HTTP_GET,
            params=filtered_params
        )

    def get_profile_metrics_timeline_by_id(self, profile_id, metric_id, since=None, count=100, sort=KlaviyoAPI.SORT_DESC):
        """Gets a profiles event data for one metric.

        https://www.klaviyo.com/docs/api/people#metric-timeline

        Args:
            profile_id (str): Unique id for profile.
            metric_id (str): Unique id for metric.
            since (unix timestamp int or uuid str): A timestamp or uuid.
            count (int): The batch of records the response should return.
            sort (str): The order in which results should be returned.

        Returns:
            (dict): information about the specified metric id for the profile
        """
        params = {
            self.COUNT: count,
            self.SORT: sort,
            self.SINCE: since,
        }
        filtered_params = self._filter_params(params)

        return self._v1_request('{}/{}/{}/{}/{}'.format(
                self.PERSON,
                profile_id,
                self.METRIC,
                metric_id,
                self.TIMELINE
            ),
            self.HTTP_GET,
            params=filtered_params
        )
