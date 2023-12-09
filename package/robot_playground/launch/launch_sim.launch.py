import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription,DeclareLaunchArgument,OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution,PythonExpression

from launch_ros.actions import Node

from launch_ros.substitutions import FindPackageShare

def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled

    package_name='robot_playground'

    robot_model = LaunchConfiguration('robot_model')
    world = LaunchConfiguration('world')

    robot_model_arg = DeclareLaunchArgument(
        'robot_model',
        default_value='robot'
    )

    world_arg = DeclareLaunchArgument(
        'world',
        default_value='abu2024'
    )

    pkg_share = FindPackageShare(package=package_name).find(package_name)
    world_path = PythonExpression(expression=["'", world, "'", " + '.sdf'"])
    world_file = PathJoinSubstitution([pkg_share,'worlds', world_path])
    
    # world_file = os.path.join(pkg_share,'worlds',world_v)
    
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true', 'robot_model':robot_model}.items()
    )

    # twist_mux_params = os.path.join(get_package_share_directory(package_name),'config','twist_mux.yaml')
    # twist_mux = Node(
    #         package="twist_mux",
    #         executable="twist_mux",
    #         parameters=[twist_mux_params],
    #         remappings=[('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')]
    #     )
    
    # robot_localization_file_path = os.path.join(pkg_share, 'config/ekf.yaml') 

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'world':world_file}.items() #Change Path to where the file is
             )

    # start_robot_localization_cmd = Node(
    #     package='robot_localization',
    #     executable='ekf_node',
    #     name='ekf_filter_node',
    #     output='screen',
    #     parameters=[robot_localization_file_path, 
    #     {'use_sim_time': True}],
    #     )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')

    # diff_drive_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["diff_cont"],
    # )

    # joint_broad_spawner = Node(
    #     package="controller_manager",
    #     executable="spawner",
    #     arguments=["joint_broad"],
    # )                    



    # Launch them all!
    return LaunchDescription([
        rsp,
        # twist_mux,
        gazebo,
        # start_robot_localization_cmd,
        spawn_entity,
        robot_model_arg,
        world_arg,
        robot_model_arg
        # diff_drive_spawner,
        # joint_broad_spawner
    ])
