import datetime
import socket

import threading

from .lgx_response import Response
from random import randrange
from struct import pack, unpack_from
from threading import Timer

"""
The consumer has to send the request to the producer
to register the session and establish the forward
open.

The consumer decides the connection parameters

NOTE: Once the forward open request is sent,
it seems that the first UDP packet is sent
by the consumer.  Need to make that change
"""

class Consumer(object):

    def __init__(self):

        self.ProducerIP = '192.168.1.9'
        self.ConsumerIP = '192.168.1.67'
        self.TagName = 'MyDINT'
        self.Slot = 0
        self.ReturnFunction = None
        self.Route = None
        self.Port = 44818
        self.RPI = 250
        self.OTRPI = 500
        self.Socket = socket.socket()
        self.VendorID = 0x01
        self.OriginatorSerialNumber = 42
        self.SequenceCount = 0
        self._count = 0
        self.DataSize = 88

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Clean up on exit
        """
        return self

    def Start(self):
        """
        Connect to the PLC and exchange data.
        """
        conn = self._connect()
        if not conn[0]:
            return Response(None, None, conn[1])
        self._run = True
        self.Send = Connection(self.OTRPI, self.DataSender)

        self.UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPSocket.bind((self.ConsumerIP, 2222))
        self.data = ''
        while self._run:
            try:
                self.data = self.UDPSocket.recv(1024)
                #value = unpack_from('<I', self.data, 20)[0]
                value = self.data[20:]
                self.ReturnFunction(Response(self.TagName, value, 0))
            except KeyboardInterrupt:
                self.Send.stop()
                self._run = False

    def Stop(self):
        """
        Stop the consumer connection
        """
        self.Send.stop()
        self._run = False

    def _connect(self):
        """
        Register session and establish forward open
        """
        try:
            self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.Socket.settimeout(5.0)
            self.Socket.connect((self.ProducerIP, 44818))
        except socket.error as e:
            #self.SocketConnected = False
            self.SequenceCounter = 1
            self.Socket.close()
            return (False, e)

        self.Socket.send(self._buildRegisterSession())
        ret_data = self.recv_data()

        if ret_data:
            self.SessionHandle = unpack_from('<I', ret_data, 4)[0]
            #self._registered = True
        else:
            #self.SocketConnected = False
            return (False, 'Register session failed')

        self.Socket.send(self._buildForwardOpenPacket())
        #ret_data = self.recv_data()
    
        try:
            ret_data = self.recv_data()
        except socket.timeout as e:
            return (False, e)

        sts = unpack_from('<b', ret_data, 42)[0]
        if not sts:
            self.OTConnectionID = unpack_from('<I', ret_data, 44)[0]
            #self._connected = True
        else:
            #self.SocketConnected = False
            return (False, 'Forward open failed')

        return (True, 'Success')

        # self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.Socket.connect((self.ProducerIP, 44818))
        # r = self._buildRegisterSession()
        # self.Socket.send(r)
        # self.data = self.Socket.recv(1024)
        # self.SessionHandle = struct.unpack_from('<I', self.data, 4)[0]

        # self.Socket.send(self._buildForwardOpenPacket())
        # self.data = self.Socket.recv(1024)
        # self.OTConnectionID = struct.unpack_from('<I', self.data, 44)[0]
        
        # self.Send = Connection(self.OTRPI, self.DataSender)

        # self.UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.UDPSocket.bind((self.ConsumerIP, 2222))
        # self.data = ''

        # self._run = True

        # while self._run:
        #     try:
        #         self.data = self.UDPSocket.recv(1024)
        #         #value = unpack_from('<I', self.data, 20)[0]
        #         value = self.data[20:]
        #         self.ReturnFunction(value)
        #     except KeyboardInterrupt:
        #         self.Send.stop()
        #         self._run = False
        #d.close()

    def recv_data(self):
        """
        When receiving data from the socket, it is possible to receive
        incomplete data.  The initial packet that comes in contains
        the length of the payload.  We can use that to keep calling
        recv() until the entire payload is received.  This only happnens
        when using LargeForwardOpen
        """
        data = b''
        part = self.Socket.recv(4096)
        payload_len = unpack_from('<H', part, 2)[0]
        data += part

        while len(data)-24 < payload_len:
            part = self.Socket.recv(4096)
            data += part

        return data

    def DataSender(self):
        """
        Send keep alive packets to producer
        """
        packet = self._response_packet()
        self.SequenceCount += 1
        self.UDPSocket.sendto(packet, ('192.168.1.9', 2222))

    def _response_packet(self):
        """
        Build the response packet
        """
        item_count = 0x02
        type_id = 0x8002
        length = 0x08
        connection_id = self.OTConnectionID
        sequence_number =  self.SequenceCount
        conn_data = 0x00b1
        data_length = 0x02
        sequence_count = 1

        payload = pack('<HHHIIHHH',
                        item_count,
                        type_id,
                        length,
                        connection_id,
                        sequence_number,
                        conn_data,
                        data_length,
                        sequence_count)

        return payload

    def DataReceiver(self):
        """
        Receive packets from the producer.
        This may not be necessary.
        """
        print("I'm a receiver {}".format(datetime.datetime.now()))

    def _buildRegisterSession(self):
        """
        Register our CIP connection
        """
        EIPCommand = 0x0065
        EIPLength = 0x0004
        EIPSessionHandle = 0x00
        EIPStatus = 0x0000
        EIPContext = 0x00
        EIPOptions = 0x0000

        EIPProtocolVersion = 0x01
        EIPOptionFlag = 0x00

        return pack('<HHIIQIHH',
                    EIPCommand,
                    EIPLength,
                    EIPSessionHandle,
                    EIPStatus,
                    EIPContext,
                    EIPOptions,
                    EIPProtocolVersion,
                    EIPOptionFlag)

    def _buildForwardOpenPacket(self):
        """
        Assemble the forward open packet
        """
        forwardOpen = self._buildCIPForwardOpen()
        rrDataHeader = self._buildEIPSendRRDataHeader(len(forwardOpen))
        return rrDataHeader+forwardOpen

    def _buildEIPSendRRDataHeader(self, frameLen):
        """
        Build the EIP Send RR Data Header
        """
        EIPCommand = 0x6F
        EIPLength = 16+frameLen
        EIPSessionHandle = self.SessionHandle
        EIPStatus = 0x00
        EIPContext = 0x8000004a00000000
        EIPOptions = 0x00

        EIPInterfaceHandle = 0x00
        EIPTimeout = 0x00
        EIPItemCount = 0x02
        EIPItem1Type = 0x00
        EIPItem1Length = 0x00
        EIPItem2Type = 0xB2
        EIPItem2Length = frameLen

        return pack('<HHIIQIIHHHHHH',
                    EIPCommand,
                    EIPLength,
                    EIPSessionHandle,
                    EIPStatus,
                    EIPContext,
                    EIPOptions,
                    EIPInterfaceHandle,
                    EIPTimeout,
                    EIPItemCount,
                    EIPItem1Type,
                    EIPItem1Length,
                    EIPItem2Type,
                    EIPItem2Length)

    def _buildCIPForwardOpen(self):
        """
        Forward Open happens after a connection is made,
        this will sequp the CIP connection parameters
        """
        CIPPathSize = 0x02
        CIPClassType = 0x20

        CIPClass = 0x06
        CIPInstanceType = 0x24

        CIPInstance = 0x01
        CIPPriority = 0x0A
        CIPTimeoutTicks = 0x0e
        CIPOTConnectionID = 0x00
        CIPTOConnectionID = randrange(65000)
        self.SerialNumber = randrange(65000)
        CIPConnectionSerialNumber = self.SerialNumber
        CIPVendorID = self.VendorID
        CIPOriginatorSerialNumber = self.OriginatorSerialNumber
        CIPMultiplier = 0x00
        CIPOTRPI = 500*1000
        CIPConnectionParameters = 0x4802
        CIPTORPI = self.RPI*1000
        CIPTransportTrigger = 0x81

        # decide whether to use the standard ForwardOpen
        # or the large format
        CIPService = 0x54
        #CIPConnectionParameters += 508
        pack_format = '<BBBBBBBBIIHHIIIHIHB'

        CIPOTNetworkConnectionParameters = CIPConnectionParameters
        CIPTONetworkConnectionParameters = 0x4800+self.DataSize

        ForwardOpen = pack(pack_format,
                           CIPService,
                           CIPPathSize,
                           CIPClassType,
                           CIPClass,
                           CIPInstanceType,
                           CIPInstance,
                           CIPPriority,
                           CIPTimeoutTicks,
                           CIPOTConnectionID,
                           CIPTOConnectionID,
                           CIPConnectionSerialNumber,
                           CIPVendorID,
                           CIPOriginatorSerialNumber,
                           CIPMultiplier,
                           CIPOTRPI,
                           CIPOTNetworkConnectionParameters,
                           CIPTORPI,
                           CIPTONetworkConnectionParameters,
                           CIPTransportTrigger)

        # add the connection path

        path_size, path = self._connection_path()
        connection_path = pack('<B', path_size/2)
        connection_path += path
        return ForwardOpen + connection_path

    def _connection_path(self):
        KeySegment = 0x34 #b
        KeyFormat = 0x04 #b
        VendorID = 0x00 #h
        DeviceType = 0x00 #h
        ProductCode = 0x00 #h
        MajorRevision = 0x00 #b
        MinorRevision = 0x00 #b
        # ClassType = 0x20 #b
        # Class = 0x69 #b
        # InstanceType = 0x24 #b
        # Instance = 0x01 #b
        #SymbolType = 0x91 #b

        path = pack('<BBHHHBB',
                    KeySegment,
                    KeyFormat,
                    VendorID,
                    DeviceType,
                    ProductCode,
                    MajorRevision,
                    MinorRevision)

        ANSISymbol = self._buildTagIOI(self.TagName, 160)
        path += ANSISymbol

        return len(path), path

    def _buildTagIOI(self, tagName, data_type):
            """
            The tag IOI is basically the tag name assembled into
            an array of bytes structured in a way that the PLC will
            understand.  It's a little crazy, but we have to consider the
            many variations that a tag can be:

            TagName (DINT)
            TagName.1 (Bit of DINT)
            TagName.Thing (UDT)
            TagName[4].Thing[2].Length (more complex UDT)

            We also might be reading arrays, a bool from arrays (atomic), strings.
                Oh and multi-dim arrays, program scope tags...
            """
            ioi = b""
            tagArray = tagName.split(".")

            # this loop figures out the packet length and builds our packet
            for i in range(len(tagArray)):
                if tagArray[i].endswith("]"):
                    tag, base_tag, index = _parseTagName(tagArray[i], 0)

                    BaseTagLenBytes = len(base_tag)
                    if data_type == 211 and i == len(tagArray)-1:
                        index = int(index/32)

                    # Assemble the packet
                    ioi += pack('<BB', 0x91, BaseTagLenBytes)
                    ioi += base_tag.encode('utf-8')
                    if BaseTagLenBytes % 2:
                        BaseTagLenBytes += 1
                        ioi += pack('<B', 0x00)

                    BaseTagLenWords = BaseTagLenBytes/2
                    if i < len(tagArray):
                        if not isinstance(index, list):
                            if index < 256:
                                ioi += pack('<BB', 0x28, index)
                            if 65536 > index > 255:
                                ioi += pack('<HH', 0x29, index)
                            if index > 65535:
                                ioi += pack('<HI', 0x2A, index)
                        else:
                            for i in range(len(index)):
                                if index[i] < 256:
                                    ioi += pack('<BB', 0x28, index[i])
                                if 65536 > index[i] > 255:
                                    ioi += pack('<HH', 0x29, index[i])
                                if index[i] > 65535:
                                    ioi += pack('<HI', 0x2A, index[i])
                else:
                    """
                    for non-array segment of tag
                    the try might be a stupid way of doing this.  If the portion of the tag
                        can be converted to an integer successfully then we must be just looking
                        for a bit from a word rather than a UDT.  So we then don't want to assemble
                        the read request as a UDT, just read the value of the DINT.  We'll figure out
                        the individual bit in the read function.
                    """
                    try:
                        if int(tagArray[i]) <= 31:
                            pass
                    except Exception:
                        BaseTagLenBytes = int(len(tagArray[i]))
                        ioi += pack('<BB', 0x91, BaseTagLenBytes)
                        ioi += tagArray[i].encode('utf-8')
                        if BaseTagLenBytes % 2:
                            BaseTagLenBytes += 1
                            ioi += pack('<B', 0x00)

            return ioi

def _parseTagName(tag, offset):
    """
    parse the packet to get the base tag name
    the offset is so that we can increment the array pointer if need be
    """
    bt = tag
    ind = 0
    try:
        if tag.endswith(']'):
            pos = (len(tag)-tag.rindex("["))  # find position of [
            bt = tag[:-pos]		    # remove [x]: result=SuperDuper
            temp = tag[-pos:]		    # remove tag: result=[x]
            ind = temp[1:-1]		    # strip the []: result=x
            s = ind.split(',')		    # split so we can check for multi dimensin array
            if len(s) == 1:
                ind = int(ind)
                newTagName = bt+'['+str(ind+offset)+']'
            else:
                # if we have a multi dim array, return the index
                ind = []
                for i in range(len(s)):
                    s[i] = int(s[i])
                    ind.append(s[i])
        else:
            pass
        return tag, bt, ind
    except Exception:
        return tag, bt, 0

class Connection(object):

    def __init__ (self, RPI, function):

        self._timer = None
        self.RPI = RPI *.001
        self.function = function
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.RPI, self._run)
            self._timer.start()
            self.is_running = True
        
    def stop(self):
        self._timer.cancel()
        self.is_running = False

