# M-Pesa SDK for Python

M-Pesa SDK for Python is an unofficial library aiming to help develbusinesses integrating every [M-Pesa](https://developer.mpesa.vm.co.mz) operations to their Python applications.

## Contents

- [Features](#features)
- [Usage](#usage)
   - [Quickstart](#usage/scenario-1)
   - [Receive Money from a Mobile Account](#usage/scenario-1)
   - [Send Money to a Mobile Account](#usage/scenario-2)
   - [Send Money to a Business Account](#usage/scenario-3)
   - [Revert a Transaction](#usage/scenario-4)
   - [Query the Status of a Transaction](#usage/scenario-5)
   - [Examples](#usage/scenario-6)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
   - [Using PIP](#installation/scenario-1)
   - [Installation Scenario 2](#installation/scenario-2)
   - [Installation Scenario 3](#installation/scenario-3)
   - [Installation Scenario 4](#installation/scenario-4)
- [Configuration](#configuration)
   - [Configuration Scenario 1](#configuration/scenario-1)
   - [Configuration Scenario 2](#configuration/scenario-2)
   - [Configuration Scenario 3](#configuration/scenario-3)
   - [Configuration Scenario 4](#configuration/scenario-4)
- [Related Projects](#related-projects)
   - [Dependencies](#related-projects/dependencies)
   - [Friends](#related-projects/friends)
   - [Alternatives](#related-projects/alternatives)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [Authors](#authors)
- [Credits](#credits)
- [License](#license)

## Features <a name="features"></a>

- Receive money from a mobile account to a business account
- Send money from a business account to a mobile account
- Send money from a business account to a another business account
- Revert a transaction
- Query the status of a transaction

## Usage <a name="usage"></a>

### Quickstart <a name="#usage/scenario-1"></a>

### Receive Money from a Mobile Account <a name="#usage/scenario-2"></a>

```python
from paymentsds.mpesa import Client

client = Client(
   api_key='<REPLACE>',              # API Key
   public_key='<REPLACE>',           # Public Key
   service_provider_code='<REPLACE>' # input_ServiceProviderCode
)

try:
   payment_data = {
      'from': '841234567',       # input_CustomerMSISDN
      'reference': '11114',      # input_ThirdPartyReference
      'transaction': 'T12344CC', # input_TransactionReference
      'amount': '10'             # input_Amount
   }

   result = client.receive(payment_data)
except:
   print('Operation failed')

```

### Send Money to a Mobile Account <a name="#usage/scenario-3"></a>

```python
from paymentsds.mpesa import Client

client = Client(
   api_key='<REPLACE>',              # API Key
   public_key='<REPLACE>',           # Public Key
   service_provider_code='<REPLACE>' # input_ServiceProviderCode
)

try:
   payment_data = {
      'to': '841234567',         # input_CustomerMSISDN
      'reference': '11114',      # input_ThirdPartyReference
      'transaction': 'T12344CC', # input_TransactionReference
      'amount': '10'             # input_Amount
   }

   result = client.send(payment_data)
except:
   print('Operation failed')

```

### Send Money to a Business Account <a name="#usage/scenario-4"></a>

```python
from paymentsds.mpesa import Client

client = Client(
   api_key='<REPLACE>',              # API Key
   public_key='<REPLACE>',           # Public Key
   service_provider_code='<REPLACE>' # input_ServiceProviderCode
)

try:
   payment_data = {
      'to': '979797',            # input_ReceiverPartyCode
      'reference': '11114',      # input_ThirdPartyReference
      'transaction': 'T12344CC', # input_TransactionReference
      'amount': '10'             # input_Amount
   }

   result = client.send(payment_data)
except:
   print('Operation failed')

```

### Revert a Transaction <a name="#usage/scenario-5"></a>

```python
from paymentsds.mpesa import Client

client = Client(
   api_key='<REPLACE>',                # API Key
   public_key='<REPLACE>',             # Public Key
   service_provider_code='<REPLACE>',  # input_ServiceProviderCode
   initiatorIdentifier='<REPLACE>',    # input_InitiatorIdentifier,
   securityIdentifier='<REPLACE>'      # input_SecurityCredential
)

try:
   reversion_data = {
      'reference': '11114',      # input_ThirdPartyReference
      'transaction': 'T12344CC', # input_TransactionReference
      'amount': '10'             # input_ReversalAmount
   }

   result = client.revert(reversion_data)
except:
   # Handle success scenario

```

### Query the Status of a Transaction <a name="#usage/scenario-6"></a>

### Examples <a name="usage/scenario-7"></a>

## Prerequisites <a name="prerequisites"></a>

- [Python 3.5+](https://www.python.org)
- [PIP](https://pip.pypa.io)

## Installation <a name="installation"></a>

### Using pip <a name="installation/scenario-1"></a>

```bash
$ pip install paymentsds-mpesa
```

```txt
paymentsds-mpesa
```

```bash
$ pip install -r requirements.txt
```

### Installation Scenario 2 <a name="installation/scenario-2"></a>

### Installation Scenario 3 <a name="installation/scenario-3"></a>

## Configuration <a name="configuration"></a>

### Configuration Scenario 1 <a name="configuration/scenario-1"></a>

### Configuration Scenario 2 <a name="configuration/scenario-2"></a>

### Configuration Scenario 3 <a name="configuration/scenario-3"></a>

## Related Projects <a name="related-projects"></a>

### Dependencies <a name="related-projects/dependencies"></a>

#### Production Dependencies

- [Requests](https://github.com/psf/requests)

#### Development Dependencies

- [Dependency 1](https://github.com/<username>/<project>)
- [Dependency 2](https://github.com/<username>/<project>)
- [Dependency 3](https://github.com/<username>/<project>)
- [Dependency 4](https://github.com/<username>/<project>)

### Friends <a name="related-projects/friends"></a>

- [M-Pesa SDK for Javascript](https://github.com/paymentsds/mpesa-js-sdk)
- [M-Pesa SDK for PHP](https://github.com/paymentsds/mpesa-php-sdk)
- [M-Pesa SDK for Ruby](https://github.com/paymentsds/mpesa-ruby-sdk)

### Alternatives <a name="related-projects/alternatives"></a>

- [Alternative 1](https://github.com/<username>/<project>)
- [Alternative 2](https://github.com/<username>/<project>)
- [Alternative 3](https://github.com/<username>/<project>)
- [Alternative 4](https://github.com/<username>/<project>)


### Inspiration

- [rosariopfernandes/mpesa-node-api](https://github.com/abdulmueid/mpesa-php-api)
- [karson/mpesa-php-sdk](https://github.com/karson/mpesa-php-sdk)
- [codeonweekends/mpesa-php-sdk](https://github.com/codeonweekends/mpesa-php-sdk)
- [abdulmueid/mpesa-php-api](https://github.com/abdulmueid/mpesa-php-api)
- [realdm/mpesasdk](https://github.com/realdm/mpesasdk)


## Contributing <a name="contributing"></a>

## Changelog <a name="changelog"></a>

## Authors <a name="authors"></a>

- [Edson Michaque](https://github.com/edsonmichaque)
- [Nélio Macombo](https://github.com/neliomacombo)

## Credits <a name="credits"></a>

## License <a name="license"></a>

Copyright 2020 Anísio Mandlate, Edson Michaque, Elton Laice and Nélio Macombo

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

