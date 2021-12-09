'''
Eclipse Point Request/Response Messages
-------------------------------------------
'''
from pymodbus.pdu import ModbusRequest
from pymodbus.pdu import ModbusResponse
from pymodbus.pdu import ModbusExceptions as merror

class EclipsePointRequest(ModbusRequest):
    '''
    This function code is used to pass eclipse point to a remote device.
    '''
    function_code = 100
    _rtu_frame_size = 8

    def __init__(self, R=None, **kwargs):
        ''' Initializes a new instance

        :param R: The computed point on the eclipse curve
        '''
        ModbusRequest.__init__(self, **kwargs)
        self.R = R

    def encode(self):
        ''' Encodes write coil request

        :returns: The byte encoded message
        '''
        assert len(self.R) == 64*2 # 两个椭圆上的点，默认一个点为64个16进制字符
        result = self.R[:64] + ':' + self.R[64:]
        result = result.encode()
        return result

    def decode(self, data):
        ''' Decodes a write coil request

        :param data: The packet data to decode
        '''
        self.R = ''.join(data.decode().split(':'))

    def execute(self, context):
        ''' Run a eclipse point request against a datastore

        :param context: The datastore to request from
        :returns: The populated response or exception message
        '''
        #if self.value not in [ModbusStatus.Off, ModbusStatus.On]:
        #    return self.doException(merror.IllegalValue)

        return EclipsePointResponse(self.R[::-1])

    def get_response_pdu_size(self):
        """
        Func_code (1 byte) + Output Address (2 byte) + Output Value  (2 Bytes)
        :return: 
        """
        return 1 + 128

    def __str__(self):
        ''' Returns a string representation of the instance

        :return: A string representation of the instance
        '''
        return "EclipsePointRequest(%s) => %s" % (self.R, self.R)


class EclipsePointResponse(ModbusResponse):
    '''
    The normal response is an echo of the request, returned the reverse content
    '''
    function_code = 100
    _rtu_frame_size = 8

    def __init__(self, R=None, **kwargs):
        ''' Initializes a new instance

        :param R: The computed point on the eclipse curve
        '''
        ModbusResponse.__init__(self, **kwargs)
        self.R = R

    def encode(self):
        ''' Encodes eclipse point response

        :return: The byte encoded message
        '''
        result = self.R[:64] + ':' + self.R[64:]
        result = result.encode()
        return result

    def decode(self, data):
        ''' Decodes a eclipse point response

        :param data: The packet data to decode
        '''
        self.R = ''.join(data.decode().split(':'))

    def __str__(self):
        ''' Returns a string representation of the instance

        :returns: A string representation of the instance
        '''
        return "EclipsePointResponse(%s) => %s" % (self.R, self.R)
