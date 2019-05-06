#!/usr/bin/python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class KeystoneProvides(RelationBase):
    scope = scopes.GLOBAL

    @hook('{provides:keystone-admin}-relation-joined')
    def joined(self):
        self.set_state('{relation_name}.connected')

    @hook('{provides:keystone-admin}-relation-changed')
    def changed(self):
        self.set_state('{relation_name}.available')

    @hook('{provides:keystone-admin}-relation-{broken,departed}')
    def broken_departed(self):
        self.remove_state('{relation_name}.database.joined')
        self.remove_state('{relation_name}.available')

    @hook('{provides:keystone-admin}-relation-broken')
    def broken(self):
        self.set_state('{relation_name}.removed')

    def publish_info(self,
                     service_hostname,
                     service_port,
                     service_username,
                     service_password,
                     service_tenant_name,
                     service_region,
                     api_version,
                     service_project_domain_name,
                     service_project_name,
                     service_protocol,
                     service_user_domain_name):
        """
        Publish keystone admin credentials

        keystone provides:
            {u'service_password': u'XXXXXXXX',
             u'service_port': u'5000',
             u'private-address': u'10.XX.XX.XXX',
             u'service_hostname': u'10.XX.XX.XXX',
             u'service_username': u'admin',
             u'service_tenant_name': u'Admin',
             u'service_region': u'RegionOne'}
       keystone v3 also provides
            {api_version: "3"
            service_project_domain_name: admin_domain
            service_project_name: admin
            service_protocol: http
            service_user_domain_name: admin_domain}
        """
        convs = self.conversations()
        if len(convs) > 0:
            conv = convs[0]
            conv.set_remote('service_hostname', service_hostname)
            conv.set_remote('service_port', service_port)
            conv.set_remote('service_username', service_username)
            conv.set_remote('service_password', service_password)
            conv.set_remote('service_tenant_name', service_tenant_name)
            conv.set_remote('service_region', service_region)
            if api_version > 2:
                conv.set_remote('api_version', api_version)
                conv.set_remote('service_user_domain_name',
                                service_user_domain_name)
                conv.set_remote('service_project_domain_name',
                                service_project_domain_name)
                conv.set_remote('service_project_name', service_project_name)
                conv.set_remote('service_protocol', service_protocol)
