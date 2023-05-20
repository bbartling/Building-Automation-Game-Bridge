import sc2
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point2
from sc2.player import Bot, Computer
from sc2.ids.buff_id import BuffId


class MyBot(BotAI):

    def __init__(self):
        self.max_workers = 22
        self.initial_wave_done = False
        self.alldone_stalkers = False
        
    async def on_start(self):
        print("Game started")
        print("self.max_workers is ",self.max_workers)

    async def on_step(self, iteration):

        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()
        await self.build_gas()
        await self.build_cyber_core()
        await self.build_four_gates()
        await self.train_stalkers()
        await self.chrono_boost()
        await self.warpgate_research()
        await self.initial_attack()


        
        pass

    async def build_workers(self):
        for nexus in self.townhalls.ready:
            nexus = self.townhalls.ready.random
            if (
                self.can_afford(UnitTypeId.PROBE)
                and nexus.is_idle
                and self.workers.amount < self.townhalls.amount * self.max_workers
            ):
                nexus.train(UnitTypeId.PROBE)
            
            
    async def build_pylons(self):
        for nexus in self.townhalls.ready:
            nexus = self.townhalls.ready.random
            pos = nexus.position.towards(self.enemy_start_locations[0],10)
            if (
                self.supply_left < 3 
                and self.already_pending(UnitTypeId.PYLON) == 0
                and self.can_afford(UnitTypeId.PYLON)
            ):
                await self.build(UnitTypeId.PYLON,near=pos)
            
        
        
    async def build_gas(self):
        if self.structures(UnitTypeId.GATEWAY):
            for nexus in self.townhalls.ready:
                vgs = self.vespene_geyser.closer_than(15,nexus)
                for vg in vgs:
                    if not self.can_afford(UnitTypeId.ASSIMILATOR):
                        break
                    worker = self.select_build_worker(vg.position)
                    if worker is None:
                        break
                    if not self.gas_buildings or not self.gas_buildings.closer_than(1,vg):
                        worker.build(UnitTypeId.ASSIMILATOR,vg)
                        worker.stop(queue=True)
    
    
    async def build_cyber_core(self):
        if self.structures(UnitTypeId.PYLON).ready:
            pylon = self.structures(UnitTypeId.PYLON).ready.random
            if self.structures(UnitTypeId.GATEWAY).ready:
                # if no then build one
                if not self.structures(UnitTypeId.CYBERNETICSCORE):
                    if(
                        self.can_afford(UnitTypeId.CYBERNETICSCORE)
                        and self.already_pending(UnitTypeId.CYBERNETICSCORE) == 0
                    ):
                        await self.build(UnitTypeId.CYBERNETICSCORE,near=pylon)
    
    
    async def train_stalkers(self):
        for gateway in self.structures(UnitTypeId.GATEWAY).ready:
            if (
                self.can_afford(UnitTypeId.STALKER)
                and gateway.is_idle
                and not self.alldone_stalkers
                
            ):
                gateway.train(UnitTypeId.STALKER)
    

    async def build_four_gates(self):
        pylons = self.structures(UnitTypeId.PYLON).ready
        for pylon in pylons:
            if (
                self.can_afford(UnitTypeId.GATEWAY)
                and self.structures(UnitTypeId.WARPGATE).amount + self.structures(UnitTypeId.GATEWAY).amount < 4
            ):
            
                await self.build(UnitTypeId.GATEWAY, near=pylon)


    async def chrono_boost(self):
    
        for nexus in self.townhalls.ready:
            
            # Chrono nexus if cybercore is not ready, else chrono cybercore
            if not self.structures(UnitTypeId.CYBERNETICSCORE).ready:
                if not nexus.has_buff(BuffId.CHRONOBOOSTENERGYCOST) and not nexus.is_idle:
                    if nexus.energy >= 50:
                        if nexus != None:
                            nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, nexus)
            else:
                ccore = self.structures(UnitTypeId.CYBERNETICSCORE).ready.first
                if not ccore.has_buff(BuffId.CHRONOBOOSTENERGYCOST) and not ccore.is_idle:
                    if nexus.energy >= 50:
                        if nexus != None:
                            nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, ccore)
                        
                        
    async def warpgate_research(self):
        if (
            self.structures(UnitTypeId.CYBERNETICSCORE).ready
            and self.can_afford(AbilityId.RESEARCH_WARPGATE)
            and self.already_pending_upgrade(UpgradeId.WARPGATERESEARCH) == 0
        ):
            cybercore = self.structures(UnitTypeId.CYBERNETICSCORE).ready.first
            cybercore.research(UpgradeId.WARPGATERESEARCH)
            
            
            
    async def initial_attack(self):
        print("initial_wave_done is ",self.initial_wave_done)
        print("self.units(UnitTypeId.STALKER).amount ",self.units(UnitTypeId.STALKER).amount)
        if (
            self.units(UnitTypeId.STALKER).amount > 10 
            and self.initial_wave_done
        ):
            for stalker in self.units(UnitTypeId.STALKER).ready.idle:
                targets = (self.enemy_units | self.enemy_structures).filter(lambda unit: unit.can_be_attacked)
                if targets:
                    target = targets.closest_to(stalker)
                    stalker.attack(target)
                else:
                    stalker.attack(self.enemy_start_locations[0])

            
        else:
            if (
                self.units(UnitTypeId.STALKER).amount > 14 
            ):        
                for stalker in self.units(UnitTypeId.STALKER).ready.idle:
                    targets = (self.enemy_units | self.enemy_structures).filter(lambda unit: unit.can_be_attacked)
                    if targets:
                        target = targets.closest_to(stalker)
                        stalker.attack(target)
                    else:
                        stalker.attack(self.enemy_start_locations[0])
                self.initial_wave_done = True


    def on_end(self, result):
        print("Game ended.")
        # Do things here after the game ends


# C:\Program Files (x86)\StarCraft II\Maps

def main():
    sc2.run_game(
        sc2.maps.get("TritonLE"),
        [Bot(sc2.Race.Protoss, MyBot()), 
        Computer(sc2.Race.Protoss, sc2.Difficulty.Medium)],
        realtime=False,
    )



if __name__ == "__main__":
    main()
