# Copyright 2020 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
def strip_shacl_prefix(url):
    term = str(url)
    return term[27:]

def strip_url(url):
    term = str(url)
    return term.split("/")[-1]

class ResultRow():
    
    def __init__(self, id, message, property_path, value, severity):
        self.id = id
        self.message = message
        self.property_path = property_path
        self.value = value
        self.severity = severity