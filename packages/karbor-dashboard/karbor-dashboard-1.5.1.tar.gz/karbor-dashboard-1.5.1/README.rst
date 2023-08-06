========================
Team and repository tags
========================

.. image:: https://governance.openstack.org/tc/badges/karbor-dashboard.svg
    :target: https://governance.openstack.org/tc/reference/tags/index.html

.. Change things from this point on

================
karbor-dashboard
================

Karbor Dashboard

* Free software: Apache license
* Source: https://opendev.org/openstack/karbor-dashboard/
* Bugs: https://storyboard.openstack.org/#!/project/openstack/karbor-dashboard

Installation instructions
-------------------------

Begin by cloning the Horizon and Karbor Dashboard repositories::

    git clone https://opendev.org/openstack/horizon
    git clone https://opendev.org/openstack/karbor-dashboard

Create a virtual environment and install Horizon dependencies::

    cd horizon
    python tools/install_venv.py

Set up your ``local_settings.py`` file::

    cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py

Open up the copied ``local_settings.py`` file in your preferred text
editor. You will want to customize several settings:

-  ``OPENSTACK_HOST`` should be configured with the hostname of your
   OpenStack server. Verify that the ``OPENSTACK_KEYSTONE_URL`` and
   ``OPENSTACK_KEYSTONE_DEFAULT_ROLE`` settings are correct for your
   environment. (They should be correct unless you modified your
   OpenStack server to change them.)


Install Karbor Dashboard with all dependencies in your virtual environment::

    tools/with_venv.sh pip install -e ../karbor-dashboard/

And enable it in Horizon::

    cp ../karbor-dashboard/karbor_dashboard/enabled/* openstack_dashboard/local/enabled/

To run horizon with the newly enabled Karbor Dashboard plugin run::

    tox -e runserver 0.0.0.0:8080

to have the application start on port 8080 and the horizon dashboard will be
available in your browser at http://localhost:8080/
