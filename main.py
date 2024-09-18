from src.FleetBattle import FleetBattle

if __name__ == '__main__':
    
    game = FleetBattle()
    game.placeShipsPlayer()
    #game.placeShipsRandomly(True)
    game.placeShipsRandomly(False)
    game.playMainGamePhase()
    
    quit()