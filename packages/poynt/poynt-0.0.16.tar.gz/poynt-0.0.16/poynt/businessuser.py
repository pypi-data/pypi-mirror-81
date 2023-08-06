from poynt import API


class BusinessUser():

    @classmethod
    def get_business_users(cls, business_id):
        """
        Get all users at a business.

        Arguments:
        business_id (str): the business ID
        """

        api = API.shared_instance()
        return api.request(
            url='/businesses/%s/businessUsers' % business_id,
            method='GET'
        )

    @classmethod
    def get_business_user(cls, business_id, business_user_id):
        """
        Get a single user at a business.

        Arguments:
        business_id (str): the business ID
        business_user_id (str): the user ID
        """

        api = API.shared_instance()
        return api.request(
            url='/businesses/%s/businessUsers/%s' % (
                business_id, business_user_id),
            method='GET'
        )
