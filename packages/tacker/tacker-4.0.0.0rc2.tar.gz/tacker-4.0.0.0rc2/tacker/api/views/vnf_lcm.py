# Copyright (C) 2020 NTT DATA
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tacker.api import views as base
from tacker.common import utils
from tacker.objects import fields
from tacker.objects import vnf_instance as _vnf_instance


class ViewBuilder(base.BaseViewBuilder):

    FLATTEN_ATTRIBUTES = _vnf_instance.VnfInstance.FLATTEN_ATTRIBUTES

    def _get_links(self, vnf_instance):
        links = {
            "self": {
                "href": '/vnflcm/v1/vnf_instances/%s' % vnf_instance.id
            }
        }

        if (vnf_instance.instantiation_state ==
                fields.VnfInstanceState.NOT_INSTANTIATED):
            instantiate_link = {
                "instantiate": {
                    "href": '/vnflcm/v1/vnf_instances/%s/instantiate'
                            % vnf_instance.id
                }
            }

            links.update(instantiate_link)

        if (vnf_instance.instantiation_state ==
                fields.VnfInstanceState.INSTANTIATED):
            instantiated_state_links = {
                "terminate": {
                    "href": '/vnflcm/v1/vnf_instances/%s/terminate'
                            % vnf_instance.id
                },
                "heal": {
                    "href": '/vnflcm/v1/vnf_instances/%s/heal'
                            % vnf_instance.id
                }
            }

            links.update(instantiated_state_links)

        return {"_links": links}

    def _get_vnf_instance_info(self,
            vnf_instance, api_version=None):
        vnf_instance_dict = vnf_instance.to_dict()
        if 'vnf_metadata' in vnf_instance_dict:
            metadata_val = vnf_instance_dict.pop('vnf_metadata')
            vnf_instance_dict['metadata'] = metadata_val

        vnf_instance_dict = utils.convert_snakecase_to_camelcase(
            vnf_instance_dict)

        if api_version == "2.6.1":
            del vnf_instance_dict["vnfPkgId"]

        links = self._get_links(vnf_instance)

        vnf_instance_dict.update(links)
        return vnf_instance_dict

    def create(self, vnf_instance):
        return self._get_vnf_instance_info(vnf_instance)

    def show(self, vnf_instance):
        return self._get_vnf_instance_info(vnf_instance)

    def index(self, vnf_instances, api_version=None):
        return [self._get_vnf_instance_info(vnf_instance, api_version)
                for vnf_instance in vnf_instances]
