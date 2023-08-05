""" Generic IOS-XE Service Statements """

__author__ = "Myles Dear <pyats-support@cisco.com>"


from unicon.eal.dialogs import Statement
from .patterns import IosXEPatterns, IosXESwitchoverPatterns


def login_handler(spawn, context, session):
    """ handles login prompt
    """
    credential = get_current_credential(context=context, session=session)
    if credential:
        common_cred_username_handler(
            spawn=spawn, context=context, credential=credential)
    else:
        if context.get('tacacs_username'):
            spawn.sendline(context['tacacs_username'])
        elif context.get('username'):
            spawn.sendline(context['username'])
        else:
            raise SubCommandFailure("There is no information available about "
                "username/tacacs_username")
        session['tacacs_login'] = 1

def password_handler(spawn, context, session):
    """ handles password prompt
    """
    credential = get_current_credential(context=context, session=session)
    if credential:
        common_cred_password_handler(
            spawn=spawn, context=context, credential=credential,
            session=session)
    else:
        if session.get('tacacs_login') == 1:
            spawn.sendline(context['tacacs_password'])
            session['tacacs_login'] = 0
        else:
            spawn.sendline(context['enable_password'])


patterns = IosXEPatterns()
switchover_patterns = IosXESwitchoverPatterns()

# loop_continue is set to `True` to ensure the dialog does not end up
# prematurely terminating, which can mess up things like executing the
# "write memory" command.
overwrite_previous = Statement(pattern=patterns.overwrite_previous,
                               action='sendline()',
                               loop_continue=True,
                               continue_timer=False)


delete_filename = Statement(pattern=patterns.delete_filename,
                            action='sendline()',
                            loop_continue=True,
                            continue_timer=False)

# loop_continue is set to `True` to ensure the dialog does not end up
# prematurely terminating, which can mess up things like uniclean
# successive file deletion.
confirm = Statement(pattern=patterns.confirm,
                    action='sendline()',
                    loop_continue=True,
                    continue_timer=False)

are_you_sure = Statement(pattern=patterns.are_you_sure,
                         action='sendline(y)',
                         loop_continue=False,
                         continue_timer=False)

wish_continue = Statement(pattern=patterns.wish_continue,
                          action='sendline(yes)',
                          loop_continue=False,
                          continue_timer=False)

want_continue = Statement(pattern=patterns.want_continue,
                          action='sendline(yes)',
                          loop_continue=False,
                          continue_timer=False)

press_enter = Statement(pattern=patterns.press_enter,
                        action='sendline()',
                        loop_continue=True,
                        continue_timer=False)

switchover_username = Statement(pattern=switchover_patterns.switchover_username,
                                  action=login_handler,
                                  args=None,
                                  loop_continue=False,
                                  continue_timer=False)

switchover_password = Statement(pattern=switchover_patterns.switchover_password,
                                  action=password_handler,
                                  args=None,
                                  loop_continue=False,
                                  continue_timer=False)
