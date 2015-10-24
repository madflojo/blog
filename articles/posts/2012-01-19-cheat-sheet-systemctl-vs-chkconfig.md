
Since I've mostly been using Red Hat or the gui desktop of Ubuntu lately I've neglected to notice the transitions from the sysVinit packages to systemd. Recently I installed Fedora 16 and was a little surprised when chkconfig didn't work anymore. I decided I would write a post that gives the systemctl version of a few common chkconfig commands.

## List processes

**chkconfig**:

    # chkconfig --list

**systemd**:

    # systemctl list-units

## Enable a service

**chkconfig**:

    # chkconfig <servicename> on

**systemd**:

    # systemctl enable <servicename>.service

## Disable a service

**chkconfig**:

    # chkconfig <servicename> off

**systemd**:

    # systemctl disable <servicename>.service

## Start a service

**chkconfig**:

    # service <servicename> start

**systemd**:

    # systemctl start <servicename>.service

## Stop a service

**chkconfig**:

    # service <servicename> stop

**systemd**:

    # systemctl stop <servicename>.service

### Check the status of a service

**chkconfig**:

    # service <servicename> status

**systemd**:

    # systemctl status <servicename>.service
