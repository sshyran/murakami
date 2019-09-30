from __future__ import division, print_function
from webthing import (Action, Event, Property, Thing, Value)

import logging
import os
import time
import uuid

class RunWehe(Action):

    def __init__(self, thing, input_):
        Action.__init__(self, uuid.uuid4().hex, thing, 'run', input_=input_)
        print(('input: '),input_)

    def perform_action(self):
        print('perform ')

class WeheClient(Thing):
  """Run Wehe tests."""

    def __init__(self):
        print('init wehe client')
        Thing.__init__(
          self,
          'urn:dev:ops:ndt7-client',
          'Wehe Client',
          ['OnOffSwitch', 'Client'],
          'A client running Wehe tests'
        )

    self.run_test()

    self.add_property(
        Property(self,
            'on',
            Value(True, lambda v: print('On-State is now', v)),
            metadata={
              '@type': 'OnOffProperty',
              'title': 'On/Off',
              'type': 'boolean',
              'description': 'Whether the client is running',
        }))

    self.add_available_action(
        'run',
        {
            'title': 'Run',
            'description': 'Run tests',
            'input': {
                'type': 'object',
                'required': [
                    'download',
                    'upload'
                ],
                'properties': {
                    'download': {
                        'type': 'integer',
                        'minimum': 0,
                        'unit': 'Mbit/s',
                    },
                    'upload': {
                        'type': 'integer',
                        'minimum': 0,
                        'unit': 'Mbit/s',
                    },
                },
            },
        },
      RunWehe)

    self.add_available_event(
        'error',
        {
            'description':
            'There was an error running the tests',
            'type': 'string',
            'unit': 'error',
        })

    def run_test(self):
        os.system('sudo docker build . -t wehe')
        os.system('sudo docker run -v data:/data/RecordReplay --env SUDO_UID=$UID --net=host -it wehe')
