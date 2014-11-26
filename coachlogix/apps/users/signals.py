def new_user_created(sender, instance, created, **kwargs):
    """
    Handle post-processing of a newly created user.
    """
    if created:
        instance.create_account()
        instance.create_profile()
