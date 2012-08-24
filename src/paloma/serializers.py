# -*- coding: utf-8 -*-

from kombu.serialization import registry
from paloma.utils import to_model_signature,from_model_signature

def register_paloma():
    ''' Experimental;Celery Serializer '''

    def encode(task_body):
        ''' Encoder '''
        _encode = registry._encoders['pickle'][2]

        task_body['args'] = tuple(
                        [ to_model_signature(arg) for arg in  task_body['args'] ]
                        )
        task_body['kwargs'] =dict(
                    [(k,to_model_signature(v)) for (k,v) in task_body['kwargs'].items()]
                )
        ret = _encode(task_body) 
        return ret

    def decode(message):
        ''' Decoder '''
        _decode =registry._decoders[ registry._encoders['pickle'][0]  ]
        task_body =  _decode(message)
        
        task_body['args'] = tuple(
                        [ from_model_signature(arg) for arg in  task_body['args'] ]
                        )
        task_body['kwargs'] = dict(
                    [(k,from_model_signature(v)) for (k,v) in task_body['kwargs'].items()]
                )
        return task_body

    #: registration
    registry.register('paloma', 
                    encode, decode,
                    content_type='application/x-python-serialize-paloma',
                    content_encoding='binary')

