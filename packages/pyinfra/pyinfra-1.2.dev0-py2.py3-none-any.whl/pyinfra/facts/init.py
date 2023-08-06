import re

from pyinfra.api import FactBase


# Valid unit names consist of a "name prefix" and a dot and a suffix specifying the unit type.
# The "unit prefix" must consist of one or more valid characters
# (ASCII letters, digits, ":", "-", "_", ".", and "\").
# The total length of the unit name including the suffix must not exceed 256 characters.
# The type suffix must be one of
# ".service", ".socket", ".device", ".mount", ".automount",
# ".swap", ".target", ".path", ".timer", ".slice", or ".scope".
# Units names can be parameterized by a single argument called the "instance name".
# A template unit must have a single "@" at the end of the name (right before the type suffix).
# The name of the full unit is formed by inserting the instance name
# between "@" and the unit type suffix.
SYSTEMD_UNIT_NAME_REGEX = (
    r'[a-zA-Z0-9\:\-\_\.\\\@]+\.'
    r'(?:service|socket|device|mount|automount|swap|target|path|timer|slice|scope)'
)


class UpstartStatus(FactBase):
    '''
    Returns a dict of name -> status for upstart managed services.
    '''

    command = 'initctl list || true'
    regex = r'^([a-z\-]+) [a-z]+\/([a-z]+)'
    default = dict

    def process(self, output):
        services = {}

        for line in output:
            matches = re.match(self.regex, line)
            if matches:
                services[matches.group(1)] = matches.group(2) == 'running'

        return services


class SystemdStatus(FactBase):
    '''
    Returns a dict of name -> status for systemd managed services.
    '''

    command = 'systemctl -al list-units || true'
    regex = r'^({systemd_unit_name_regex})\s+[a-z\-]+\s+[a-z]+\s+([a-z]+)'.format(
        systemd_unit_name_regex=SYSTEMD_UNIT_NAME_REGEX)
    default = dict

    def process(self, output):
        services = {}

        for line in output:
            line = line.strip()
            matches = re.match(self.regex, line)
            if matches:
                is_active = matches.group(2) == 'running' or matches.group(2) == 'waiting'
                services[matches.group(1)] = is_active

        return services


class SystemdEnabled(FactBase):
    '''
    Returns a dict of name -> whether enabled for systemd managed services.
    '''

    command = '''
        (systemctl --no-legend -al list-unit-files | while read -r UNIT STATUS; do
            if [ "$STATUS" = generated ] &&
                systemctl is-enabled $UNIT >/dev/null 2>&1; then
                STATUS=enabled
            fi
            echo $UNIT $STATUS
        done) || true
    '''

    regex = r'^({systemd_unit_name_regex})\s+([a-z]+)'.format(
        systemd_unit_name_regex=SYSTEMD_UNIT_NAME_REGEX)
    default = dict

    def process(self, output):
        units = {}

        for line in output:
            matches = re.match(self.regex, line)
            if matches:
                units[matches.group(1)] = (
                    matches.group(2) in ('enabled', 'static')
                )

        return units


class InitdStatus(FactBase):
    '''
    Low level check for every /etc/init.d/* script. Unfortunately many of these
    mishehave and return exit status 0 while also displaying the help info/not
    offering status support.

    Returns a dict of name -> status.

    Expected codes found at:
        http://refspecs.linuxbase.org/LSB_3.1.0/LSB-Core-generic/LSB-Core-generic/iniscrptact.html
    '''

    command = '''
        for SERVICE in `ls /etc/init.d/`; do
            _=`cat /etc/init.d/$SERVICE | grep "### BEGIN INIT INFO"`

            if [ "$?" = "0" ]; then
                STATUS=`/etc/init.d/$SERVICE status`
                echo "$SERVICE=$?"
            fi
        done
    '''

    regex = r'([a-zA-Z0-9\-]+)=([0-9]+)'
    default = dict

    def process(self, output):
        services = {}

        for line in output:
            matches = re.match(self.regex, line)
            if matches:
                status = int(matches.group(2))

                # Exit code 0 = OK/running
                if status == 0:
                    status = True

                # Exit codes 1-3 = DOWN/not running
                elif status < 4:
                    status = False

                # Exit codes 4+ = unknown
                else:
                    status = None

                services[matches.group(1)] = status

        return services


class RcdStatus(InitdStatus):
    '''
    Same as ``initd_status`` but for BSD (/etc/rc.d) systems. Unlike Linux/init.d,
    BSD init scripts are well behaved and as such their output can be trusted.
    '''

    command = '''
        for SERVICE in `ls /etc/rc.d/`; do
            _=`cat /etc/rc.d/$SERVICE | grep "daemon="`

            if [ "$?" = "0" ]; then
                STATUS=`/etc/rc.d/$SERVICE check`
                echo "$SERVICE=$?"
            fi
        done
    '''

    default = dict


class LaunchdStatus(FactBase):
    '''
    Returns a dict of name -> status for launchd managed services.
    '''

    command = 'launchctl list || true'
    default = dict

    def process(self, output):
        services = {}

        for line in output:
            bits = line.split()

            if not bits or bits[0] == 'PID':
                continue

            name = bits[2]
            status = False

            try:
                int(bits[0])
                status = True
            except ValueError:
                pass

            services[name] = status

        return services
