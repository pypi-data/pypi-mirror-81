# Swimlane Faker

Currently, this repository holds code for generating fake values from a passed in string.  This package is called `swimlane-faker`

`swimlane-faker` relies of `soc-faker` to generate it's values as well as `pendulum` at this time.

## Installation

To install this package simply install using pip:

```bash
pip3 install swimlane-faker
```

## swimlane-faker syntax

The following items can be faked provided the correct inputs:

```python
from swimlanefaker import SwimlaneFaker

sf = SwimlaneFaker()

import pendulum

# Standard Random Data Generator Options
sf.get('True')
sf.get('[[a|b|c|d]]') in ['a','b','c','d']
sf.get('[[a|b|c|d]]') not in ['x','y','z']
sf.get('[[int:0-100]]') in range(0,100)

# Standard Generated Data Options (datetime)

sf.get('[[datetime:now-2d]]')
sf.get('[[datetime:now-2h]]')
sf.get('[[datetime:now-2m]]')
sf.get('[[datetime:now-2s]]')
sf.get('[[datetime:now+2d]]')
sf.get('[[datetime:now+2h]]') 
sf.get('[[datetime:now+2m]]') 
sf.get('[[datetime:now+2s]]')

# Pendulum Generated Data Options
sf.get('<<pendulum.now()>>')
sf.get('<<pendulum.now().add(years=1)>>')
sf.get('<<pendulum.now().add(months=1)>>')
sf.get('<<pendulum.now().add(weeks=1)>>')
sf.get('<<pendulum.now().add(days=1)>>')
sf.get('<<pendulum.now().add(hours=1)>>')
sf.get('<<pendulum.now().add(minutes=1)>>')
sf.get('<<pendulum.now().add(seconds=1)>>')
sf.get('<<pendulum.now().add(years=1,months=1,weeks=1,days=1,hours=1,minutes=1,seconds=1)>>')
sf.get('<<pendulum.now().subtract(years=1)>>')
sf.get('<<pendulum.now().subtract(months=1)>>')
sf.get('<<pendulum.now().subtract(weeks=1)>>')
sf.get('<<pendulum.now().subtract(days=1)>>')
sf.get('<<pendulum.now().subtract(hours=1)>>')
sf.get('<<pendulum.now().subtract(minutes=1)>>')
sf.get('<<pendulum.now().subtract(seconds=1)>>')
sf.get('<<pendulum.now().subtract(years=1,months=1,weeks=1,days=1,hours=1,minutes=1,seconds=1)>>')

# SocFaker Generated Data Options

sf.get('<<socfaker.logs.syslog(count=2)>>')
sf.get('<<socfaker.computer.name>>')
sf.get('<<socfaker.computer.disk>>')
sf.get('<<socfaker.computer.memory>>')
sf.get('<<socfaker.computer.platform>>')
sf.get('<<socfaker.computer.mac_address>>')
sf.get('<<socfaker.computer.os>>')
sf.get('<<socfaker.application.name>>')
sf.get('<<socfaker.application.status>>')
sf.get('<<socfaker.application.account_status>>')
sf.get('<<socfaker.application.logon_timestamp>>')
sf.get('<<socfaker.employee.name>>')
sf.get('<<socfaker.employee.first_name>>')
sf.get('<<socfaker.employee.last_name>>')
sf.get('<<socfaker.employee.username>>')
sf.get('<<socfaker.employee.email>>')
sf.get('<<socfaker.employee.gender>>')
sf.get('<<socfaker.employee.account_status>>')
sf.get('<<socfaker.employee.ssn>>')
sf.get('<<socfaker.employee.dob>>')
sf.get('<<socfaker.employee.photo>>')
sf.get('<<socfaker.employee.user_id>>')
sf.get('<<socfaker.employee.phone_number>>')
sf.get('<<socfaker.employee.logon_timestamp>>')
sf.get('<<socfaker.employee.language>>')
sf.get('<<socfaker.employee.title>>')
sf.get('<<socfaker.employee.department>>')
sf.get('<<socfaker.file.filename>>')
sf.get('<<socfaker.file.size>>')
sf.get('<<socfaker.file.timestamp>>')
sf.get('<<socfaker.file.hashes>>')
sf.get('<<socfaker.file.md5>>')
sf.get('<<socfaker.file.sha1>>')
sf.get('<<socfaker.file.sha256>>')
sf.get('<<socfaker.file.full_path>>')
sf.get("<<socfaker.file.signed>>")
sf.get("<<socfaker.file.signature>>")
sf.get("<<socfaker.file.signature_status>>")
sf.get("<<socfaker.logs.windows.eventlog(count=1)>>")
sf.get("<<socfaker.logs.windows.sysmon(count=2)>>")
sf.get("<<socfaker.network.ipv4>>")
sf.get("<<socfaker.network.ipv6>>")
sf.get("<<socfaker.network.get_cidr_range('192.168.1.0/24')>>")
sf.get("<<socfaker.network.hostname>>")
sf.get("<<socfaker.network.netbios>>")
sf.get("<<socfaker.network.mac>>")
sf.get("<<socfaker.network.protocol>>")
sf.get("<<socfaker.organization.name>>")
sf.get("<<socfaker.organization.division>>")
sf.get("<<socfaker.organization.title>>")
sf.get("<<socfaker.products.azure.vm.details>>")
sf.get("<<socfaker.products.azure.vm.metrics>>")
sf.get("<<socfaker.products.azure.vm.metrics.average>>")
sf.get("<<socfaker.products.azure.vm.metrics.graphs>>")
sf.get("<<socfaker.products.azure.vm.topology>>")
sf.get("<<socfaker.products.elastic.hits(count=1)>>")
sf.get("<<socfaker.products.qualysguard.scan(count=1)>>")
sf.get("<<socfaker.products.servicenow.search()>>")
sf.get("<<socfaker.user_agent>>")
sf.get("<<socfaker.vulnerability().host>>")
sf.get("<<socfaker.vulnerability().scan>>")
sf.get("<<socfaker.vulnerability().data>>")
sf.get("<<socfaker.vulnerability().critical>>")
sf.get("<<socfaker.vulnerability().high>>")
sf.get("<<socfaker.vulnerability().medium>>")
sf.get("<<socfaker.vulnerability().low>>")
sf.get("<<socfaker.vulnerability().informational>>")
```