'''
==========================================================================
test_srcs.py
==========================================================================
A collection of test sources.

Author : Yanghui Ou
  Date : Feb 2, 2020
'''
from collections import deque
from pymtl3 import *
from pymtl3.stdlib.ifcs import RecvCL2SendRTL, SendIfcRTL

#-------------------------------------------------------------------------
# MflitPacketSourceCL
#-------------------------------------------------------------------------
# pkts                : a list of MflitPacket objects.
# initial_delay       : number of cycles before sending the very first flit.
# flit_interval_delay : number of cycles between each flit in a packet.
# packet_interval_delay  : number of cycles between each packet.
# TODO: check if inputs packtes are valid

class MflitPacketSourceCL( Component ):

  def construct( s, Format, pkts, initial_delay=0, flit_interval_delay=0, packet_interval_delay=0 ):

    # Interface
    PhitType = mk_bits( Format.nbits )
    s.send = CallerIfcCL( Type=PhitType )

    # Metadata
    s.pkts    = deque( pkts )
    s.cur_pkt = None
    s.count   = initial_delay
    s.f_delay = flit_interval_delay
    s.p_delay = packet_interval_delay

    # Update block
    @update_once
    def up_src_send():
      if s.count > 0:
        s.count -= 1
      elif not s.reset:
        # pop a packet to send
        if not s.cur_pkt and s.pkts:
          s.cur_pkt = s.pkts.popleft()
          assert not s.cur_pkt.empty()

        if s.send.rdy() and s.cur_pkt:
          s.send( s.cur_pkt.pop() )

          if s.cur_pkt.empty():
            s.cur_pkt = None
            s.count   = s.p_delay
          else:
            s.count   = s.f_delay

  def done( s ):
    return not s.pkts and not s.cur_pkt

  def line_trace( s ):
    return f'({s.count}){s.send}'

#-------------------------------------------------------------------------
# MflitPacketSourceRTL
#-------------------------------------------------------------------------

class MflitPacketSourceRTL( Component ):

  def construct( s, Format, pkts, initial_delay=0, flit_interval_delay=0,
                 packet_interval_delay=0, cmp_fn=lambda a, b : a.flits == b.flits ):

    PhitType = mk_bits( Format.nbits )

    s.send    = SendIfcRTL( PhitType )
    s.src_cl  = MflitPacketSourceCL( Format, pkts, initial_delay, flit_interval_delay,
                                         packet_interval_delay )
    s.adapter = RecvCL2SendRTL( PhitType )

    connect( s.src_cl.send,  s.adapter.recv )
    connect( s.adapter.send, s.send         )

  def done( s ):
    return s.src_cl.done()

  def line_trace( s ):
    return f'{s.send}'
