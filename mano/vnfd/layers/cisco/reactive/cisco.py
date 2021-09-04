from charmhelpers.core.hookenv import (
    action_get,
    action_fail,
    action_set,
    status_set,
)
from charms.reactive import (
    clear_flag,
    set_flag,
    when,
    when_not,
)
import charms.sshproxy

@when('sshproxy.configured')
@when_not('cisco.installed')
def install_cisco():
    # Do your setup here.
    #
    # If your charm has other dependencies before it can install,
    # add those as @when() clauses above., or as additional @when()
    # decorated handlers below
    #
    # See the following for information about reactive charms:
    #
    #  * https://jujucharms.com/docs/devel/developer-getting-started
    #  * https://github.com/juju-solutions/layer-basic#overview
    #
    set_flag('cisco.installed')
    status_set('active', 'Ready!')

@when('actions.touch')
def touch():
    """Touch a file."""
    err = ''
    try:
        filename = action_get('filename')
        cmd = ['touch {}'.format(filename)]
        result, err = charms.sshproxy._run(cmd)
    except:
        action_fail('command failed: {}'.format(err))
    else:
        action_set({'output': result})
    finally:
        clear_flag('actions.touch')

@when('actions.upgrade')
def do_upgrade():
    """Update the cisco config and set the new link."""
    err = ''
    try:
        cmd = ['python3 /usr/bin/config.py upgrade']
        result, err = charms.sshproxy._run(cmd)
    except:
        action_fail('command failed: {}'.format(err))
    else:
        action_set({'output': result})
    finally:
        clear_flag('actions.upgrade')

@when('actions.downgrade')
def do_downgrade():
    """Update the cisco config and revert to old link."""
    err = ''
    try:
        cmd = ['python3 /usr/bin/config.py downgrade']
        result, err = charms.sshproxy._run(cmd)
    except:
        action_fail('command failed: {}'.format(err))
    else:
        action_set({'output': result})
    finally:
        clear_flag('actions.downgrade')

@when('actions.test')
def do_test():
    """Test if config was successful."""
    err = ''
    try:
        filename = action_get('host')
        cmd = ['python3 /usr/bin/config.py test']
        result, err = charms.sshproxy._run(cmd)
    except:
        action_fail('command failed: {}'.format(err))
    else:
        action_set({'output': result})
    finally:
        clear_flag('actions.test')
