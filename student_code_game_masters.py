from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        state_list = []

        for peg_num in range(1,4):
            LOB = self.kb.kb_ask(parse_input("fact: (on ?x peg{})".format(peg_num)))
            temp = []
            if LOB:
                for num_disk in range(0,len(LOB)):
                    disk = str(LOB[num_disk].bindings[0].constant)[-1]
                    # print(disk)
                    temp.append(int(disk))
                temp.sort()
            state_list.append(tuple(temp))
        # print(tuple(state_list))
        return tuple(state_list)



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        # print(type(movable_statement))
        # print(movable_statement)
        #
        # Before = self.getGameState()
        #
        # print("Before")
        # print(Before)

        if self.isMovableLegal(movable_statement):
            # LOB for checking number of disks present in current peg that has the movable disk
            LOB_PegStart = self.kb.kb_ask(parse_input("fact: (on ?x {})".format(movable_statement.terms[1])))
            num_disks_PegStart = len(LOB_PegStart)

            # LOB for checking if there are any disks in target peg
            LOB_PegTarget = self.kb.kb_ask(parse_input("fact: (on ?x {})".format(movable_statement.terms[2])))

            # current peg

            fact_remove_top_current = parse_input("fact: (top {} {})".format(movable_statement.terms[0], movable_statement.terms[1]))
            fact_remove_on_current = parse_input("fact: (on {} {})".format(movable_statement.terms[0], movable_statement.terms[1]))

            #****** add only when current peg has 1 disk that is being moved
            fact_add_empty_current = parse_input("fact: (empty {})".format(movable_statement.terms[1]))

            #****** remove only when current peg has more than one disk
            LOB_above_current = self.kb.kb_ask(parse_input("fact: (above {} ?x)".format(movable_statement.terms[0])))
            if LOB_above_current:
                under_movable = str(LOB_above_current[0].bindings[0].constant)
                fact_remove_above_current = parse_input("fact: (above {} {})".format(movable_statement.terms[0],under_movable))
                # ****** add only when the top disk of current peg, which has more than one disk, is being moved
                fact_add_top_current = parse_input("fact: (top {} {})".format(under_movable, movable_statement.terms[1]))



            # target peg

            fact_add_top_target = parse_input("fact: (top {} {})".format(movable_statement.terms[0], movable_statement.terms[2]))
            fact_add_on_target  = parse_input("fact: (on {} {})".format(movable_statement.terms[0], movable_statement.terms[2]))

            #****** remove only when target peg is not empty
            LOB_top_target = self.kb.kb_ask(parse_input("fact: (top ?x {})".format(movable_statement.terms[2])))
            if LOB_top_target:
                top_target = str(LOB_top_target[0].bindings[0].constant)
                # print("top target")
                # print(top_target)
                fact_remove_top_target = parse_input("fact: (top {} {})".format(top_target, movable_statement.terms[2]))
                fact_add_on_target_new = parse_input("fact: (on {} {})".format(top_target, movable_statement.terms[2]))
                # add only when the target peg contains disks before moving
                fact_add_above_target = parse_input("fact: (above {} {})".format(movable_statement.terms[0], top_target))

            #****** remove only when target peg is empty
            fact_remove_empty_target = parse_input("fact: (empty {})".format(movable_statement.terms[2]))





            # When the current peg, containing movable disk, has more than one disks
            if num_disks_PegStart > 1:
                # print("1")

                # current
                self.kb.kb_retract(fact_remove_top_current)
                self.kb.kb_retract(fact_remove_on_current)

                self.kb.kb_retract(fact_remove_above_current)
                self.kb.kb_assert(fact_add_top_current)
                #target
                self.kb.kb_assert(fact_add_top_target)
                # print(self.getGameState())
                # When target peg has disks
                if LOB_PegTarget:
                    # print("2")

                    # target
                    self.kb.kb_retract(fact_remove_top_target)
                    self.kb.kb_assert(fact_add_on_target_new)
                    self.kb.kb_assert(fact_add_above_target)
                    # print(self.getGameState())

                else:
                    # print("3")

                    # target
                    self.kb.kb_retract(fact_remove_empty_target)
                    # print(self.getGameState())

            # When the current peg, containing movable disk, has only one disk
            else:
                # print("4")

                #curret
                self.kb.kb_retract(fact_remove_top_current)
                self.kb.kb_retract(fact_remove_on_current)

                self.kb.kb_assert(fact_add_empty_current)

                #target
                self.kb.kb_assert(fact_add_top_target)
                # print(self.getGameState())
                # When target peg has disks
                if LOB_PegTarget:
                    # print("5")

                    # target
                    self.kb.kb_retract(fact_remove_top_target)
                    self.kb.kb_assert(fact_add_on_target_new)
                    self.kb.kb_assert(fact_add_above_target)
                    # print(self.getGameState())
                else:
                    # print("6")
                    self.kb.kb_retract(fact_remove_empty_target)
                    # print(self.getGameState())

            After = self.getGameState()
            # print("After")
            # print(After)





    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        state_list = []

        for row_num in range(1,4):
            temp = []
            for col_num in range(1,4):
                # Bindings when there is a tile
                LOB_tiles = self.kb.kb_ask(parse_input("fact: (location ?x pos{} pos{})".format(col_num,row_num)))

                # # Bindings when empty
                # LOB_empty = self.kb.kb_ask(parse_input("fact: (empty ?x ?y)"))
                # # Empty location
                # empty_col_num = int(str(LOB_empty[0].bindings[0].constant)[-1])
                # empty_row_num = int(str(LOB_empty[0].bindings[1].constant)[-1])

                if LOB_tiles:
                    # tile number
                    tile_num = int(str(LOB_tiles[0].bindings[0].constant)[-1])
                    temp.append(tile_num)

                else:
                    temp.append(-1)
            state_list.append(tuple(temp))
        # print(tuple(state_list))
        return tuple(state_list)


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if self.isMovableLegal(movable_statement):
            # print("Before")
            # print(self.getGameState())
            # print("movableeeeer")
            # print(self.getMovables()[0])
            # print(self.getMovables()[1])
            # print(movable_statement)
            # print(movable_statement.terms)

            # Position of the movable tile
            current_tile_col = int(str(movable_statement.terms[1])[-1])
            current_tile_row = int(str(movable_statement.terms[2])[-1])

            empty_col_num = int(str(movable_statement.terms[3])[-1])
            empty_row_num = int(str(movable_statement.terms[4])[-1])


            # # Find position of Empty (same as
            # for row_num in range(0, 3):
            #     for col_num in range(0, 3):
            #         if self.getGameState()[row_num][col_num] == -1:
            #             empty_col_num = col_num + 1
            #             empty_row_num = row_num + 1

            LOB_movable = self.kb.kb_ask(parse_input("fact: (location ?x pos{} pos{})".format(current_tile_col
                                                                                              , current_tile_row)))
            # print("movable tile")
            # print(LOB_movable[0])
            if LOB_movable:
                tile_movable_num = str(LOB_movable[0].bindings[0].constant)[-1]

                # print("retract")
                # remove position of moving tile and empty tile before make move from kb
                remove_current_pos_moving = parse_input("fact: (location tile{} pos{} pos{})".format(tile_movable_num,
                                                                                                     current_tile_col,
                                                                                                     current_tile_row))
                remove_current_pos_empty = parse_input("fact: (empty pos{} pos{})".format(empty_col_num, empty_row_num))

                self.kb.kb_retract(remove_current_pos_moving)
                self.kb.kb_retract(remove_current_pos_empty)
                # print(self.getGameState())

                # print("add")
                # Add switched position of moving tile and empty after make move from kb
                add_new_pos_moving = parse_input("fact: (location tile{} pos{} pos{})".format(tile_movable_num,
                                                                                              empty_col_num,
                                                                                              empty_row_num))
                add_new_pos_empty = parse_input("fact: (empty pos{} pos{})".format(current_tile_col, current_tile_row))

                self.kb.kb_assert(add_new_pos_moving)
                self.kb.kb_assert(add_new_pos_empty)
                # print('after')
                # print(self.getGameState())







    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
