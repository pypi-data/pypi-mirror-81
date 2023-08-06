"""
==========================================================================
DORYTorusRouteUnitRTL.py
==========================================================================
A DOR route unit with get/give interface for Torus topology.

Author : Yanghui Ou, Cheng Tan
  Date : June 29, 2019
"""
from copy import deepcopy

from pymtl3 import *
from pymtl3.stdlib.ifcs import GetIfcRTL, GiveIfcRTL

from .directions import *


class DORYTorusRouteUnitRTL( Component ):

  def construct( s, PacketType, PositionType, ncols=2, nrows=2 ):

    # Constants

    num_outports = 5
    s.ncols = ncols
    s.nrows = nrows

    # Here we add 1 to avoid overflow

    posx_type     = mk_bits( clog2( ncols ) )
    posy_type     = mk_bits( clog2( nrows ) )
    ns_dist_type  = mk_bits( clog2( nrows+1 ) )
    we_dist_type  = mk_bits( clog2( ncols+1 ) )

    s.last_row_id = nrows-1
    s.last_col_id = ncols-1

    # Interface

    s.get  = GetIfcRTL( PacketType )
    s.give = [ GiveIfcRTL (PacketType) for _ in range ( num_outports ) ]
    s.pos  = InPort( PositionType )

    # Componets

    s.out_dir       = Wire( Bits3        )
    s.give_ens      = Wire( Bits5        )
    s.turning       = Wire( Bits1        )
    s.north_dist    = Wire( ns_dist_type )
    s.south_dist    = Wire( ns_dist_type )
    s.west_dist     = Wire( we_dist_type )
    s.east_dist     = Wire( we_dist_type )
    s.give_msg_wire = Wire( PacketType   )

    # Connections

    for i in range( num_outports ):
      s.give_ens[i]   //= s.give[i].en
      s.give_msg_wire //= s.give[i].ret

    # Calculate distance

    @update
    def up_ns_dist():
      if s.get.ret.dst_y < s.pos.pos_y:
        s.south_dist @= zext(s.pos.pos_y, ns_dist_type) - zext(s.get.ret.dst_y, ns_dist_type)
        s.north_dist @= s.last_row_id - zext(s.pos.pos_y, ns_dist_type) + 1 + zext(s.get.ret.dst_y, ns_dist_type)
      else:
        s.south_dist @= zext(s.pos.pos_y, ns_dist_type) + 1 + s.last_row_id - zext(s.get.ret.dst_y, ns_dist_type)
        s.north_dist @= zext(s.get.ret.dst_y, ns_dist_type) - zext(s.pos.pos_y, ns_dist_type)

    @update
    def up_we_dist():
      if s.get.ret.dst_x < s.pos.pos_x:
        s.west_dist @= zext(s.pos.pos_x, we_dist_type) - zext(s.get.ret.dst_x,we_dist_type)
        s.east_dist @= s.last_col_id - zext(s.pos.pos_x, we_dist_type) + 1 + zext(s.get.ret.dst_x, we_dist_type)
      else:
        s.west_dist @= zext(s.pos.pos_x, we_dist_type) + 1 + s.last_col_id - zext(s.get.ret.dst_x, we_dist_type)
        s.east_dist @= zext(s.get.ret.dst_x, we_dist_type) - zext(s.pos.pos_x, we_dist_type)

    # Routing logic

    @update
    def up_ru_routing():

      s.give_msg_wire @= s.get.ret
      s.out_dir @= 0
      s.turning @= 0

      for i in range( num_outports ):
        s.give[i].rdy @= 0

      if s.get.rdy:
        if (s.pos.pos_x == s.get.ret.dst_x) & (s.pos.pos_y == s.get.ret.dst_y):
          s.out_dir @= SELF
        elif s.get.ret.dst_y != s.pos.pos_y:
          s.out_dir @= NORTH if s.north_dist < s.south_dist else SOUTH
        else:
          s.out_dir @= WEST if s.west_dist < s.east_dist else EAST

        # Turning logic

        s.turning @= ( s.get.ret.src_x == s.pos.pos_x ) & \
                     ( s.get.ret.src_y != s.pos.pos_y ) & \
                     ( s.out_dir == WEST ) | ( s.out_dir == EAST )

        # Dateline logic

        if s.turning:
          s.give_msg_wire.vc_id @= 0

        if (s.pos.pos_x == 0) & (s.out_dir == WEST):
          s.give_msg_wire.vc_id @= 1
        elif (s.pos.pos_x == s.last_col_id) & (s.out_dir == EAST):
          s.give_msg_wire.vc_id @= 1
        elif (s.pos.pos_y == 0) & (s.out_dir == SOUTH):
          s.give_msg_wire.vc_id @= 1
        elif (s.pos.pos_y == s.last_row_id) & (s.out_dir == NORTH):
          s.give_msg_wire.vc_id @= 1

        s.give[ s.out_dir ].rdy @= 1

    @update
    def up_ru_get_en():
      s.get.en @= s.give_ens > 0

  # Line trace

  def line_trace( s ):
    out_str = "|".join([ str(x) for x in s.give ])
    dir_str = (
      "N" if s.out_dir == NORTH else
      "S" if s.out_dir == SOUTH else
      "W" if s.out_dir == WEST  else
      "E"
    )
    turn_str = "t" if s.turning else " "
    return f"{s.get}({dir_str},{turn_str}){out_str}"
