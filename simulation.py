import asyncio
from projectairsim import ProjectAirSimClient, World, Drone

async def main():
    client = ProjectAirSimClient()

    try:
        client.connect()
        print("Client connect")
        world = World(client, "scene_basic_drone.jsonb")
        print("World")
        drone = Drone(client, world, "Drone1")
        print("Drone")
        client("Enable API control")
        drone.enable_api_control()
        client("Arm")
        drone.arm()
        await drone.takeoff_async()
        drone.disarm()
        drone.disable_api_control()
    finally:
        print("Disconnect")
        client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())

