from src.fleet_battle import FleetBattle

if __name__ == '__main__':
    
    game = FleetBattle()
    game.place_ships_player()
    #game.placeShipsRandomly(True)
    game.place_ships_randomly(False)
    game.play_main_game_phase()
    
    quit()