
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        # pass game master into UI solver
        # game state in the node

        game_master = self.gm
        current_state = self.currentState.state
        children = self.currentState.children
        depth = self.currentState.depth
        visited = self.visited
        # print("aaa")
        # print(self.currentState.depth)
        # When current state equals victory condition

        if current_state == self.victoryCondition:
            # print("Goal")
            return True
        # When current state has children (has movables)
        self.visited[self.currentState] = True
        if game_master.getMovables():
            movable = game_master.getMovables()
            # print('Movables')
            # print(movable)
            for child_num in range(0,len(movable)):
                # print('get movables')
                # print(game_master.getMovables())
                # print(game_master.getMovables()[0])
                # print(game_master.getMovables()[1])
                # print('child_num')
                # print(child_num)
                # movable = game_master.getMovables()[child_num]
                # print('1')
                # print('movable')
                # print(movable)
                # print("Before")
                # print(self.gm.getGameState())
                game_master.makeMove(movable[child_num])
                # print('After')
                # print(self.gm.getGameState())
                children.append(GameState(game_master.getGameState(),depth+1,movable[child_num]))
                children[child_num].parent = self.currentState
                # print('Before reverse')
                # print(self.gm.getGameState())
                game_master.reverseMove(movable[child_num])
                # print('after reverse')
                # print(self.gm.getGameState())
                # print('parent')
                # print(children[child_num].parent.state)
            # print('Children')
            # for i in range(0,len(children)):
            #     print(children[i].state)
            # print('End of Children')
            for child in children:
                # print('children')
                # print(children)
                # print('visited dictionary key')
                if child not in visited.keys():
                #     for key in visited:
                #         print(key.state)
                #     print('2')
                    # print('before')
                    # print(game_master.getGameState())
                    game_master.makeMove(child.requiredMovable)
                    self.currentState = child
                    # print('After')
                    # print(game_master.getGameState())
                    return False
                # print('3')
                # print('Before')
                # print(game_master.getGameState())
                game_master.reverseMove(self.currentState.requiredMovable)
                # print('change currentState to parent')
                self.currentState = self.currentState.parent
                # print('After currentState to parent')
                # print(game_master.getGameState())
                return False
        else:
            # print('4')
            # print('Before')
            # print(game_master.getGameState())
            game_master.reverseMove(self.currentState.state.requiredMovable)
            # print('Before currentState to parent')
            # print(game_master.getGameState())
            self.currentState = self.currentState.parent
            # print('change currentState to parent')
            # print(game_master.getGameState())
            return False





















        # # check victory condition
        # print("current state")
        # print(self.currentState.state)
        # # print("victory condition")
        # if self.currentState.state
        # # print(self.victoryCondition)
        # # generate children of current state
        # # traverse tree to the next node
        # self.currentState


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        return True
