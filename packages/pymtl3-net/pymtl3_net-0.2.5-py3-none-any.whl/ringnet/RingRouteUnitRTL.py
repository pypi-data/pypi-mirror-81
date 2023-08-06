"""
==========================================================================
RingRouteUnitRTL.py
==========================================================================
A ring route unit with get/give interface.

Author : Yanghui Ou, Cheng Tan
  Date : April 6, 2019
"""
from copy import deepcopy

from pymtl3 import *
from pymtl3.stdlib.ifcs import GetIfcRTL, GiveIfcRTL, SendIfcRTL

from .directions import *


class RingRouteUnitRTL( Component ):

  def construct( s, PacketType, PositionType, num_routers=4 ):

    # Constants
    s.num_outports = 3
    s.num_routers  = num_routers

    DistType  = mk_bits( clog2( num_routers ) )
    s.last_idx = DistType( num_routers-1 )

    # Interface

    s.get  = GetIfcRTL( PacketType )
    s.give = [ GiveIfcRTL (PacketType) for _ in range ( s.num_outports ) ]
    s.pos  = InPort( PositionType )

    # Componets

    s.out_dir  = Wire( mk_bits( clog2( s.num_outports ) ) )
    s.give_ens = Wire( mk_bits( s.num_outports ) )

    s.left_dist  = Wire( DistType )
    s.right_dist = Wire( DistType )
    s.give_msg_wire = Wire( PacketType )

    # Connections

    for i in range( s.num_outports ):
      s.give_ens[i] //= s.give[i].en

    # Routing logic
    @update
    def up_left_right_dist():
      if s.get.ret.dst < s.pos:
        s.left_dist  @= zext(s.pos, DistType) - zext(s.get.ret.dst, DistType)
        s.right_dist @= zext(s.last_idx, DistType) - zext(s.pos, DistType) + zext(s.get.ret.dst, DistType) + 1
      else:
        s.left_dist  @= 1 + zext(s.last_idx, DistType) + zext(s.pos, DistType) - zext(s.get.ret.dst, DistType)
        s.right_dist @= zext(s.get.ret.dst, DistType) - zext(s.pos, DistType)

    @update
    def up_ru_routing():

      s.out_dir @= 0
      s.give_msg_wire @= s.get.ret
      for i in range( s.num_outports ):
        s.give[i].rdy @= 0

      if s.get.rdy:
        if s.pos == s.get.ret.dst:
          s.out_dir @= SELF
        elif s.left_dist < s.right_dist:
          s.out_dir @= LEFT
        else:
          s.out_dir @= RIGHT

        if ( s.pos == s.last_idx ) & ( s.out_dir == RIGHT ):
          s.give_msg_wire.vc_id @= 1
        elif ( s.pos == 0 ) & ( s.out_dir == LEFT ):
          s.give_msg_wire.vc_id @= 1

        s.give[ s.out_dir ].rdy @= 1
        s.give[ s.out_dir ].ret @= s.give_msg_wire

    @update
    def up_ru_get_en():
      s.get.en @= s.give_ens > 0

  # Line trace
  def line_trace( s ):

    out_str = [ "" for _ in range( s.num_outports ) ]
    for i in range (s.num_outports):
      out_str[i] = f"{s.give[i]}"

    return "{}({}){}".format( s.get, s.out_dir, "|".join( out_str ) )
