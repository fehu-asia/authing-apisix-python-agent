# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import Any
from apisix.runner.http.request import Request
from apisix.runner.http.response import Response
from apisix.runner.plugin.core import PluginBase
import json
import requests
import json

def isAllow(request,config):
    return requests.request("POST", 
        config.get("url"), 
        headers={
        'Content-Type': 'application/json'
        }, 
        data=json.dumps({
        "request": request,
        "pluginConfig": config
        })).text



class Rewrite(PluginBase):

    def name(self) -> str:
        """
        The name of the plugin registered in the runner
        :return:
        """
        return "authing_agent"

    def config(self, conf: Any) -> Any:
        """
        Parse plugin configuration
        :param conf:
        :return:
        """
        return conf

    def filter(self, conf: Any, request: Request, response: Response):

        authing_request = {
        "uri": request.get_uri(),
        "method": request.get_method(),
        "args":request.get_args(),
        "headers":request.get_headers(),
        "request_id":request.get_id(),
        "host":request.get_var("host"),
        "remote_addr": request.get_remote_addr(),
        "configs": request.get_configs()
        }
        print(authing_request)
        print(conf)
        result = isAllow(authing_request,eval(conf))
        if result != "ok":
            response.set_body(result)
        else:
            print("response end")
