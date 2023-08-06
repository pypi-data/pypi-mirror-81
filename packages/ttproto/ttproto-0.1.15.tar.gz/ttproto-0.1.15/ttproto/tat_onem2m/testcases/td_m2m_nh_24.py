from ..common import *


class TD_M2M_NH_24(CoAPTestCase):
    """

TD_M2M_NH_24:
    cfg: M2M_CFG_01
    obj: AE updates information about a subscription via subscription Update Request.
    pre: AE has created an Application Entity resource <AE> on Registrar CSE, 
         AE has created a container resource <container> on Registrar CSE and
         AE has created a subscription resource <subscription> on Registrar CSE.
    ref: 'TS-0001, clause 10.2.11.4 and TS-0004, clause 7.3.7.2'
    seq:
    -   s:
        - 'AE is requested to send a subscription Update Request to update the lifetime of the resource with:'
        -   - Type = 0 (CON)
            - Code = 3 (PUT)
            - Non-empty payload
            - Content-format option
    -   c:
        - 'The request sent by the client contains:'
        -   - Type=0 and Code=3
            - oneM2M-FR option=AE-ID
            - oneM2M-RQI=token-string (CRQI)
            - contentFormat option
            - Non-Empty payload      
    -   v: Check if possible that the <subscription> resource has been updated in registrar CSE. 
    -   c:
        - 'Registrar CSE sends response containing:'
        -   - Type = 0 (CON)
            - Code = 2.04 (UPDATED)
            - Token = CTOK
            - Content-format option
            - non-empty Payload
            - oneM2M-RSC option = 2004
            - oneM2M-RQI=CRQI
    -   v: AE indicates successful operation.
    """

    @classmethod
    @typecheck
    def get_stimulis(cls) -> list_of(Value):
        """
        Get the stimulis of this test case. This has to be be implemented into
        each test cases class.

        :return: The stimulis of this TC
        :rtype: [Value]
        """

        return [CoAP(type='con', code='put')]

    def run(self):
        self.match('client', CoAP(type="con", code="put", pl=Not(b'')), 'fail')
        self.match('client', CoAP(opt=Opt(CoAPOptionContentFormat())), "fail")
        self.match('client', CoAP(opt=Opt(CoAPOptionOneM2MFrom())), 'fail')
        if self.match('client', CoAP(opt=Opt(CoAPOptionOneM2MRequestIdentifier())), 'fail'): 

            OPTS = self.coap['opt']
            RI = OPTS[CoAPOptionOneM2MRequestIdentifier]
            RIVAL = RI[2]

        
            self.next()

            self.match("server", CoAP(code=Any(65, 68), pl=Not(b'')), 'fail')
            self.match('server', CoAP(opt=Opt(CoAPOptionContentFormat())), 'fail')
            self.match('server', CoAP(opt=Opt(CoAPOptionOneM2MResponseStatusCode('2004'))), 'fail')
            self.match('server', CoAP(opt=Opt(CoAPOptionOneM2MRequestIdentifier(RIVAL))), 'fail')
