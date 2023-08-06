"""
==========================================================================
OutputUnitCL.py
==========================================================================
Cycle level implementation of output unit.

Author : Yanghui Ou
  Date : July 2, 2019
"""
from pymtl3 import *


class OutputUnitCL( Component ):

  def construct( s, PacketType, QueueType = None ):

    # Interface
    s.get  = CallerIfcCL( Type=PacketType )
    s.send = CallerIfcCL( Type=PacketType )
    s.QueueType = QueueType

    # If queue type is assigned
    if s.QueueType != None:
      # Component
      # TODO: add type for QueueType when pymtl3 has that.
      s.queue = QueueType()

      @update_once
      def up_ou_get_enq():
        if s.get.rdy() and s.queue.enq.rdy():
          s.queue.enq( s.get() )

      @update_once
      def up_ou_deq_send():
        if s.queue.deq.rdy() and s.send.rdy():
          s.send( s.queue.deq() )

    # No ouput queue
    else:
      @update_once
      def up_ou_get_send():
        if s.get.rdy() and s.send.rdy():
          s.send( s.get() )

  def line_trace( s ):
    return "{}(){}".format( s.get, s.send )
