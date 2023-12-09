# robot_playground
E12-RBClub simulation for past/future robotic competitions in gazebo 

## How to use
0. Clone this git `git clone https://github.com/E12-CO/robot_playground.git`
1. Paste `worlds_file` under `~/.gazebo/models` or wherever gazebo models file is.
2. Build `robot_playground` in your ros2 workspace with `colcon build --packages-select robot_playground` .
3. Run `ros2 launch robot_playground launch_sim.launch.py robot_model:=<robot_model_name> world:=<world_name>` , replace <robot_model_name> and <world_name> with available robot models and worlds.
4. Control and have fun.

## List of Worlds
- ABU Robocon 2024

## List of Robot Models
- Lorlens by Jame Bond 

## List of control options
- Teleop_twist_keyboard

## TODO
- Add more worlds
- Add more robot models
- Add more control option
- Add joysticks
- More

