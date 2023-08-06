"""
=========================================================================
DORYMeshRouteUnitRTL.py
=========================================================================
A DOR route unit with get/give interface.

Author : Yanghui Ou, Cheng Tan
  Date : Mar 25, 2019
"""
from pymtl3 import *
from pymtl3.stdlib.ifcs import GetIfcRTL, GiveIfcRTL

from .directions import *


class DORYMeshRouteUnitRTL( Component ):

  def construct( s, MsgType, PositionType, num_outports = 5 ):

    # Interface

    s.get  = GetIfcRTL( MsgType )
    s.give = [ GiveIfcRTL (MsgType) for _ in range ( num_outports ) ]
    s.pos  = InPort( PositionType )

    # Componets

    s.give_ens = Wire( mk_bits( num_outports ) )

    # Connections

    for i in range( num_outports ):
      s.get.ret     //= s.give[i].ret
      s.give_ens[i] //= s.give[i].en

    # Routing logic
    @update
    def up_ru_routing():
      s.give[0].rdy @= 0
      s.give[1].rdy @= 0
      s.give[2].rdy @= 0
      s.give[3].rdy @= 0
      s.give[4].rdy @= 0

      if s.get.rdy:
        if (s.pos.pos_x == s.get.ret.dst_x) & (s.pos.pos_y == s.get.ret.dst_y):
          s.give[4].rdy @= 1
        elif s.get.ret.dst_y < s.pos.pos_y:
          s.give[1].rdy @= 1
        elif s.get.ret.dst_y > s.pos.pos_y:
          s.give[0].rdy @= 1
        elif s.get.ret.dst_x < s.pos.pos_x:
          s.give[2].rdy @= 1
        else:
          s.give[3].rdy @= 1

    @update
    def up_ru_get_en():
      s.get.en @= s.give_ens > 0

  # Line trace
  def line_trace( s ):

    out_str = "|".join([ str(x) for x in s.give ])
    return f"{s.get}(){out_str}"
