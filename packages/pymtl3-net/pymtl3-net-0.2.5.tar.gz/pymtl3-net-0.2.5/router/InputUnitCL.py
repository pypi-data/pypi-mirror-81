"""
==========================================================================
InputUnitCL.py
==========================================================================
Cycle level implementeation of the CL model.

Author : Yanghui Ou
  Date : May 16, 2019
"""
from pymtl3 import *
from pymtl3.stdlib.queues import NormalQueueCL


class InputUnitCL( Component ):

  def construct( s, PacketType, QueueType=NormalQueueCL ):

    # Interface

    s.recv = CalleeIfcCL( Type=PacketType )
    s.give = CalleeIfcCL( Type=PacketType )

    # Component

    s.queue = m = QueueType( num_entries=2 )
    m.enq //= s.recv
    m.deq //= s.give

  def line_trace( s ):
    return f"{s.recv}(){s.give}"
