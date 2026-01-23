from typing import Optional, Tuple, Dict, List
import random
from src.board import Board
from src.config import Color, GameState
from src.position import Position
from src.move import Move
from src.move_validator import MoveValidator
from src.observer import GameObserver
from src.ai_player import AiPlayer
from src.ai_player_random import AiPlayerRandom


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

    def __init__(self, ai_player: AiPlayer = AiPlayerRandom(player=Color.BLACK)):

        self.board = Board()
        self.validator = MoveValidator()
        self.state = GameState.PLAYING
        self.current_player = Color.WHITE
        self.selected_position = None
        self.observers = []  # List of observers
        self.ai_player = ai_player

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

    def get_valid_moves_for_selected(self) -> list[Move]:
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

    def make_move(self, selected_origin: Position, selected_dest: Position) -> bool:
        selected_move = next((move for move in self.valid_moves if move.dest_pos == selected_dest), None)
        self.selected_position = None  # if move is successful OR is invalid, anyway clear selected position
        if selected_move:
            # valid move
            self.board.move(selected_move)
            if selected_move.is_capture:
                for captured_piece in selected_move.captured_pieces:
                    self.board.remove_piece(captured_piece)

            if self.current_player == Color.WHITE:
                self.current_player = Color.BLACK
            else:
                self.current_player = Color.WHITE
            return True
        else:  # invalid move OR if selecting the same piece the selection is reset
            return False

    def run(self):
        """Main game loop."""

        # Initial game state for observers
        # TODO

        while self.state == GameState.PLAYING:

            if self.current_player == Color.WHITE:

                move_successful = False
                while not move_successful:
                    # Observers display board
                    for observer in self.observers:
                        observer.on_game_state_changed(self.board, self.current_player, self.state)

                    # Select piece by observers
                    selected_origin = observer.get_selected_origin()
                    self.select_piece(selected_origin)

                    # Display valid moves for the selected piece
                    self.valid_moves = self.get_valid_moves_for_selected()
                    observer.on_piece_selected(self.board, selected_origin, self.valid_moves)

                    # Get and perform movement
                    selected_dest = observer.get_selected_dest()
                    move_successful = self.make_move(selected_origin, selected_dest)
                    observer.on_game_state_changed(self.board, self.current_player, self.state)

            else:  # BLACK turn

                # Select piece by AI player
                selected_origin = self.ai_player.get_selected_origin(self.board)
                self.select_piece(selected_origin)
                self.valid_moves = self.get_valid_moves_for_selected()

                selected_dest = self.ai_player.get_selected_dest(self.board)
                move_successful = self.make_move(selected_origin, selected_dest)
                observer.on_game_state_changed(self.board, self.current_player, self.state)



            # self.clock.tick(self.fps)
            @staticmethod
            def cleanup():
                """Clean up resources."""
                pygame.quit()
                print("Game ended")


if __name__ == '__main__':
    main()
