from typing import Optional, Tuple, Dict, List
import random
from src.board import Board
from src.config import Color, GameState
from src.position import Position
from src.move_validator import MoveValidator
from src.observer import GameObserver
#from src.orbit_view import OrbitRenderer


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

    def __init__(self, config: OrbitConfig = None):

        self.board = Board()
        self.validator = MoveValidator()
        self.state = GameState.PLAYING
        self.current_player = Color.WHITE
        self.selected_position = None
        self.observers = []  # List of observers

        '''
        self.config = config or OrbitConfig()
        self.model = GameModel(self.config)
        self.view = OrbitRenderer(self.config)
        self.clock = pygame.time.Clock()
        self.fps = self.config.fps
        self.running = True
        self.paused = self.config.paused
        self.autopilot = RendezvousAutopilot(self.config.mu, self.config.dt, self.config.delta_v)'''

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

    @staticmethod
    def should_execute_autopilot_burn(game_model: 'GameModel', autopilot: RendezvousAutopilot) -> Optional[bool]:
        """
        Get autopilot burn recommendation for GameModel.

        Args:
            game_model: Your existing GameModel instance
            autopilot: RendezvousAutopilot instance

        Returns:
            True for prograde burn, False for retrograde, None for no burn
        """
        if not autopilot.enabled:
            return None

        if game_model.caught_satellite or game_model.collided_with_star:
            return None

        # Extract data from GameModel ships
        ship_state, ship_elements = game_model.extract_orbital_data(game_model.ships[0])
        target_state, target_elements = game_model.extract_orbital_data(game_model.ships[1])

        # Process through autopilot
        analysis = autopilot.process_orbital_data(ship_state, target_state, ship_elements, target_elements)
        burn_command, reasoning = autopilot.compute_burn_command(analysis)
        print(reasoning)

        return burn_command

    def run(self):
        """Main game loop."""
        self.autopilot.enable()

        while self.running:

            # Handle input
            self.handle_events()

            if not self.paused:

                # run autopilot cycle
                if self.autopilot.enabled:
                    # Get autopilot recommendation
                    burn_cmd = self.should_execute_autopilot_burn(self.model, self.autopilot)
                    if burn_cmd is not None:
                        self.model.change_orbit(burn_cmd)

                # Update game logic
                self.model.update()

                # Render
                self.view.render(self.model)

                # exit conditions
                if self.model.collided_with_star:
                    self.running = False
                    print("Collided with star, game over")
                if self.model.caught_satellite:
                    self.running = False
                    print("Caught the satellite, you win")

                self.clock.tick(self.fps)
        self.cleanup()

    @staticmethod
    def cleanup():
        """Clean up resources."""
        pygame.quit()
        print("Game ended")


# if __name__ == '__main__':
    # main()
