import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution,PythonExpression
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

from launch_ros.parameter_descriptions import ParameterValue
import xacro


def generate_launch_description():

    # Check if we're told to use sim time
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_ros2_control = LaunchConfiguration('use_ros2_control')

    robot_model = LaunchConfiguration('robot_model')
    

    robot_model_arg = DeclareLaunchArgument(
        'robot_model',
        default_value='robot'
    )

    # robot_model_path = LaunchConfiguration('robot_model_path')
   
    # joy_config = LaunchConfiguration('joy_config')
    # joy_config_dec= DeclareLaunchArgument('joy_config', default_value='ps3')
    # robot_model_dec = DeclareLaunchArgument('robot_model_path', default_value=[LaunchConfiguration('robot_model'), '.urdf.xacro'])

    # Process the URDF file
    
    pkg_path = os.path.join(get_package_share_directory('robot_playground'))

    robot_path = PythonExpression(expression=["'", robot_model, "'", " + '.urdf.xacro'"])

    # xacro_file = os.path.join(pkg_path,'description',robot_path)
    # robot_description_config = Command(['xacro ', robot_path, ' use_ros2_control:=', use_ros2_control, ' sim_mode:=', use_sim_time])
    # robot_description_config = xacro.process_file(xacro_file)
    
    urdf_path = PathJoinSubstitution([pkg_path,'description', robot_path])

    robot_description_content = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    # Create a robot_state_publisher node
    
    params = {'robot_description': robot_description_content, 'use_sim_time': use_sim_time}
    #params = {'robot_description': robot_description_config.toxml(), 'use_sim_time': use_sim_time}
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    # node_joint_state_publisher = Node(
    #     package='joint_state_publisher',
    #     executable='joint_state_publisher',
    # )


    # Launch!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use sim time if true'),
        DeclareLaunchArgument(
            'use_ros2_control',
            default_value='true',
            description='Use ros2_control if true'),
        node_robot_state_publisher,
        robot_model_arg,
        # node_joint_state_publisher
    ])
