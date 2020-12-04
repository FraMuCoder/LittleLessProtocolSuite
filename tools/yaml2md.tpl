{# Little Less Protocol Suite - yaml converter
   Copyright (C) 2020 Frank Mueller

   SPDX-License-Identifier: MIT
#}
# {{ yaml['shortName'].text }} - {{ yaml['longName'].text }}

{% if yaml['minVersion'] == yaml['maxVersion'] %}
Supported Version: {{ yaml['minVersion'].text }}
{% else %}
Supported Versions: {{ yaml['minVersion'].text }} .. {{ yaml['maxVersion'].text }}
{% endif %}

{{ yaml['description'].text | md }}

## Commands
| ID | Short | Long name |
| --:| ----- | --------- |
{% for cmd in yaml['commands'] %}
| [{{ cmd['id'].text }}]({{ cmd | cmd_link }}) | [{{ cmd['shortName'].text }}]({{ cmd | cmd_link }}) | [{{ cmd['longName'].text }}]({{ cmd | cmd_link }}) |
{% endfor %}

{% for cmd in yaml['commands'] %}
---
### {{ cmd | cmd_title }}
{{ cmd['description'].text | md(3) }}

#### Data structure

{{ cmd['structure'].text | md(4) }}
{% endfor %}
