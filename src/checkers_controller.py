from typing import Optional, Tuple, Dict, List
import random
from src.board import Board
from src.config import Color, GameState
from src.position import Position
from src.move_validator import MoveValidator
from src.observer import GameObserver


'''
class GameEngine {
        -validator: MoveValidator
        -state: GameState
        +make_move(from_pos, to_pos) bool
        +get_winner() Color
        +get_current_player() Color
        +reset_game()
        -switch_turn()
        -execute_move(move)
        -check_game_over()
'''

class CheckersController:
    """Handles user input and coordinates between model and view."""

    def __init__(self):

        self.board = Board()
        self.validator = MoveValidator()
        self.state = GameState.PLAYING
        self.current_player = Color.WHITE
        self.selected_position = None
        self.observers = []  # List of observers

        '''
        self.clock = pygame.time.Clock()
        self.fps = self.config.fps
        self.running = True'''


    def select_piece(self, position: Position) -> bool:
        """ User selects piece to move, controller returns validity of selection"""
        is_valid_selection = self.validator.is_valid_selection(self.board, position, self.current_player)
        if is_valid_selection:
            self.selected_position = position
        return is_valid_selection

    def get_valid_moves_for_selected(self) -> List[Tuple[Position, Position]]:
        return self.validator.get_all_valid_moves(self.board, self.selected_position)

    def attach_observer(self, observer: GameObserver) -> None:
        self.observers.append(observer)

    def detach_observer(self, observer: GameObserver) -> None:
        self.observers.remove(observer)


    def handle_events(self):
        """Process all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # toggle Pause/unpause
                    self.paused = not self.paused
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_DOWN:
                    self.model.change_orbit(False)
                elif event.key == pygame.K_UP:
                    self.model.change_orbit(True)

    def run(self):
        """Main game loop."""

        # Initial game state for observers
        # TODO

        while self.state == GameState.PLAYING:

            if self.current_player == Color.WHITE:
                # Observers display board
                for observer in self.observers:
                    observer.on_game_state_changed(self.board, self.current_player, self.state)

                # Select piece by observers
                selected_piece = observer.get_selected_piece()
                self.select_piece(selected_piece)
                # Display valid moves for the selected piece
                valid_moves = self.get_valid_moves_for_selected()
                observer.on_piece_selected(self.board, selected_piece, valid_moves)

                # Get and perform movement
                selected_move = observer.get_selected_move()
                if selected_move in valid_moves:
                    pass
                else:  # invalid move
                    self.selected_position = None
                    observer.on_game_state_changed(self.board, self.current_player, self.state)



            # self.clock.tick(self.fps)
            @staticmethod
            def cleanup():
                """Clean up resources."""
                pygame.quit()
                print("Game ended")


if __name__ == '__main__':
    main()
